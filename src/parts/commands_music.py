try:
    from ytqueue import MusicPlayer, Resolver, ResolverConfig
    from ytqueue.discord import DiscordPlayer
    from ytqueue.cookie_sync import CookieSyncServer
    YTQUEUE_AVAILABLE = True
except ImportError as e:
    YTQUEUE_AVAILABLE = False
    print(f"[WARNING] ytqueue is not installed - music commands are disabled. Run: pip install ytqueue ({e})")

MUSIC_COOKIES_FILE = str(DATA_DIR / "cookies.txt")
_music_cookie_server = None
_music_resolver = None
_music_players = {}
_music_last_channel = {}

if YTQUEUE_AVAILABLE:
    try:
        _music_cookie_server = CookieSyncServer(cookies_file=MUSIC_COOKIES_FILE)
        _music_cookie_server.start()
    except Exception as e:
        print(f"[WARNING] Could not start the music cookie-sync server: {e}")
        _music_cookie_server = None

    _music_resolver = Resolver(ResolverConfig(
        cookies_file=MUSIC_COOKIES_FILE,
        on_cookie_error=_music_cookie_server.request_refresh_and_wait if _music_cookie_server else None,
    ))

def _format_duration(seconds):
    if not seconds:
        return "Unknown"
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{mins}:{secs:02d}"

def get_music_player(guild_id):
    player = _music_players.get(guild_id)
    if player is None:
        player = DiscordPlayer(core=MusicPlayer(resolver=_music_resolver))

        async def _on_track_started(track):
            channel = _music_last_channel.get(guild_id)
            if channel is None:
                return
            body = f"{track.title}\nDuration: {_format_duration(track.duration)}"
            await panelmaker(channel, "Now Playing", body, "mplay")

        async def _on_track_skipped(track):
            channel = _music_last_channel.get(guild_id)
            if channel is None:
                return
            await panelmaker(channel, "Track Skipped", f"Couldn't load '{track.title}', skipping.", "mplay")

        player.core.on_track_started = _on_track_started
        player.core.on_track_skipped_load_failure = _on_track_skipped
        _music_players[guild_id] = player
    return player

async def ensure_music_voice(ctx):
    if ctx.guild is None:
        return None, "This command only works inside a server."
    if not ctx.author.voice or not ctx.author.voice.channel:
        return None, "You need to be in a voice channel first."
    vc = ctx.guild.voice_client
    try:
        if vc is None:
            vc = await ctx.author.voice.channel.connect()
        elif vc.channel.id != ctx.author.voice.channel.id:
            await vc.move_to(ctx.author.voice.channel)
    except Exception as e:
        return None, f"Couldn't connect to voice: {e}"
    return vc, None

@Repent.command(aliases=['mp'], description=f"Plays a song from YouTube (URL or search query) in your voice channel. \nUsage: {config_get('prefix')}mplay <query/url>", help="music")
async def mplay(ctx, *, query: str):
    if not YTQUEUE_AVAILABLE:
        await panelmaker(ctx, "Error", "ytqueue isn't installed. Run `pip install ytqueue` and restart.", "ERROR")
        return
    vc, error = await ensure_music_voice(ctx)
    if error:
        await panelmaker(ctx, "Error", error, "ERROR")
        return
    _music_last_channel[ctx.guild.id] = ctx.channel
    player = get_music_player(ctx.guild.id)
    tracks = await player.enqueue_url_or_query(query)
    if not tracks:
        await panelmaker(ctx, "Error", f"Couldn't find anything for '{query}'.", "ERROR")
        return
    was_idle = not (vc.is_playing() or vc.is_paused())
    await player.play_next(ctx, vc)
    if not was_idle:
        names = "\n".join(f"- {t.title}" for t in tracks[:5])
        await panelmaker(ctx, "Added to Queue", names, "mplay")

@Repent.command(description=f"Skips the currently playing song. \nUsage: {config_get('prefix')}mskip", help="music")
async def mskip(ctx):
    vc = ctx.guild.voice_client if ctx.guild else None
    if vc is None or not (vc.is_playing() or vc.is_paused()):
        await panelmaker(ctx, "Error", "Nothing is playing.", "ERROR")
        return
    vc.stop()
    await panelmaker(ctx, "Skipped", "Skipped to the next track.", "mskip")

@Repent.command(aliases=['mleave', 'mdc'], description=f"Stops playback, clears the queue, and leaves the voice channel. \nUsage: {config_get('prefix')}mstop", help="music")
async def mstop(ctx):
    vc = ctx.guild.voice_client if ctx.guild else None
    if vc is None:
        await panelmaker(ctx, "Error", "Not connected to a voice channel.", "ERROR")
        return
    player = _music_players.get(ctx.guild.id)
    if player:
        player.core.queue.clear()
        player.core.queue.loop_enabled = False
    if vc.is_playing() or vc.is_paused():
        vc.stop()
    await vc.disconnect()
    await panelmaker(ctx, "Stopped", "Stopped playback and left the voice channel.", "mstop")

@Repent.command(description=f"Shows the current music queue. \nUsage: {config_get('prefix')}mqueue", help="music")
async def mqueue(ctx):
    player = _music_players.get(ctx.guild.id) if ctx.guild else None
    if player is None or (not player.core.queue.current and not player.core.queue.tracks):
        await panelmaker(ctx, "Queue", "Nothing is queued.", "mqueue")
        return
    body = ""
    if player.core.queue.current:
        body += f"Now Playing: {player.core.queue.current.title}\n\n"
    if player.core.queue.tracks:
        upcoming = "\n".join(f"{i+1}. {t.title}" for i, t in enumerate(list(player.core.queue.tracks)[:10]))
        body += f"Up Next:\n{upcoming}"
    else:
        body += "Nothing else queued."
    await panelmaker(ctx, "Queue", body, "mqueue")

@Repent.command(aliases=['mnp'], description=f"Shows the currently playing song. \nUsage: {config_get('prefix')}mnowplaying", help="music")
async def mnowplaying(ctx):
    player = _music_players.get(ctx.guild.id) if ctx.guild else None
    if player is None or not player.core.queue.current:
        await panelmaker(ctx, "Now Playing", "Nothing is playing.", "mnowplaying")
        return
    track = player.core.queue.current
    elapsed = int(player.core.queue.elapsed() or 0)
    body = f"{track.title}\nElapsed: {_format_duration(elapsed)} / {_format_duration(track.duration)}"
    await panelmaker(ctx, "Now Playing", body, "mnowplaying")

@Repent.command(description=f"Toggles looping the current track. \nUsage: {config_get('prefix')}mloop [true/false]", help="music")
async def mloop(ctx, state: bool = None):
    if ctx.guild is None:
        await panelmaker(ctx, "Error", "This command only works inside a server.", "ERROR")
        return
    player = get_music_player(ctx.guild.id)
    if state is None:
        state = not player.core.queue.loop_enabled
    player.core.queue.loop_enabled = state
    await panelmaker(ctx, "Loop", f"Loop {'enabled' if state else 'disabled'}.", "mloop")

@Repent.command(description=f"Toggles autoplay (queues similar songs once the queue runs out). \nUsage: {config_get('prefix')}mautoplay [true/false]", help="music")
async def mautoplay(ctx, state: bool = None):
    if ctx.guild is None:
        await panelmaker(ctx, "Error", "This command only works inside a server.", "ERROR")
        return
    player = get_music_player(ctx.guild.id)
    if state is None:
        state = not player.core.queue.autoplay_enabled
    player.core.queue.autoplay_enabled = state
    await panelmaker(ctx, "Autoplay", f"Autoplay {'enabled' if state else 'disabled'}.", "mautoplay")

@Repent.command(description=f"Sets the music playback volume (0-200). \nUsage: {config_get('prefix')}mvolume <0-200>", help="music")
async def mvolume(ctx, percent: int):
    if ctx.guild is None:
        await panelmaker(ctx, "Error", "This command only works inside a server.", "ERROR")
        return
    percent = max(0, min(200, percent))
    player = get_music_player(ctx.guild.id)
    player.volume = percent / 100
    vc = ctx.guild.voice_client
    if vc is not None and vc.source is not None:
        vc.source.volume = percent / 100
    await panelmaker(ctx, "Volume", f"Volume set to {percent}%.", "mvolume")
