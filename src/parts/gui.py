window = None
api = None
BOT_READY = False
BOOT_STAGE = "Starting up"
_GUI_READY = threading.Event()
_GUI_READY_TIMEOUT = 20.0

ID_LIST_KEYS = ("music_whitelist", "nitro_blacklist_ids", "giveaway_bot_ids", "giveaway_blacklist_ids")
PROFILE_CACHE_TTL = 60
_profile_cache = {"user_id": None, "at": 0.0, "data": {}}

def fetch_discord_profile(user_id, headers):
    # /users/{id}/profile is heavily rate limited and the dashboard asks for it from several places
    if _profile_cache["user_id"] == user_id and time.time() - _profile_cache["at"] < PROFILE_CACHE_TTL:
        return _profile_cache["data"]
    data = requesters.get(f'https://discord.com/api/v9/users/{user_id}/profile', headers=headers, quiet=True).json()
    if not isinstance(data, dict) or 'user' not in data:
        return _profile_cache["data"] if _profile_cache["user_id"] == user_id else {}
    _profile_cache.update(user_id=user_id, at=time.time(), data=data)
    return data

class API:
    def configedit(self, data, new_value):
        if data in ID_LIST_KEYS:
            # JS can't hold 64-bit snowflakes as numbers, so the UI sends strings
            new_value = [int(v) for v in new_value]
        config_edit(data, new_value)
        if data == "device":
            if window is not None:
                window.destroy()
            API.restart(self)

    def get_user_profile(self):
        try:
            headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
            resp = requesters.get("https://discord.com/api/v9/users/@me", headers=headers).json()
            if not resp or 'id' not in resp:
                print("[WARNING] Failed to fetch user profile (no response from Discord)")
                return None
            user_id = resp['id']

            profile_data = {
                "id": user_id,
                "username": resp.get('username', ''),
                "global_name": resp.get('global_name', ''),
                "avatar": resp.get('avatar', ''),
                "banner": resp.get('banner', ''),
                "banner_color": resp.get('banner_color', ''),
                "accent_color": resp.get('accent_color', 0),
                "bio": resp.get('bio', ''),
                "clan": None,
                "badges": [],
                "email": resp.get('email'),
                "phone": resp.get('phone'),
                "token": config_get('token'),
                "nitro": resp.get('premium_type', 0) > 0,
                "nsfw_allowed": bool(resp.get('nsfw_allowed', False)),
                "mfa_enabled": bool(resp.get('mfa_enabled', False)),
                "locale": (resp.get('locale') or '').replace('_', ' ').title(),
            }

            user_profile = fetch_discord_profile(user_id, headers).get('user') or {}
            if user_profile.get('clan'):
                profile_data['clan'] = user_profile['clan']

            profile_data['badges'] = self.get_badges()

            try:
                friends = requesters.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
                profile_data['friend_count'] = len([r for r in friends if r.get('type') not in (2, 3, 4)])
            except Exception:
                profile_data['friend_count'] = 0
            try:
                guilds = requesters.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
                profile_data['guild_count'] = len(guilds)
            except Exception:
                profile_data['guild_count'] = 0

            try:
                profile_data['bot_uptime_seconds'] = int(time.time() - start_time)
            except Exception:
                profile_data['bot_uptime_seconds'] = None
            try:
                profile_data['bot_latency_ms'] = self.get_bot_stats()['latency_ms']
            except Exception:
                profile_data['bot_latency_ms'] = None
            try:
                profile_data['bot_cmdcount'] = len(Repent.commands)
            except Exception:
                profile_data['bot_cmdcount'] = 0
            profile_data['bot_version'] = ver

            return profile_data
        except Exception as e:
            print(f"Error getting user profile: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_badges(self):
        resp = requesters.get("https://discord.com/api/v9/users/@me", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()}).json()
        if not resp or 'id' not in resp:
            print("[WARNING] Failed to fetch badges (no response from Discord)")
            return []
        id = resp['id']
        badges = []
        try:
            user_flags = resp.get('public_flags', 0)
            
            badge_icons = {
                1 << 0: "https://cdn.discordapp.com/badge-icons/1a499f6d5f548601390c52a0324975e8.png",
                1 << 1: "https://cdn.discordapp.com/badge-icons/3a275c5e7a63ffc936c500fec6fe8fcc.png",
                1 << 2: "https://cdn.discordapp.com/badge-icons/2970454842a5191b8c4770ee26c477d5.png",
                1 << 3: "https://cdn.discordapp.com/badge-icons/07749d139cd217d08908a4048f219fb4.png",
                1 << 6: "https://cdn.discordapp.com/badge-icons/9a878878d904ee68a560893b672e2097.png",
                1 << 7: "https://cdn.discordapp.com/badge-icons/40535a0e1e46f1e85431ba621f163878.png",
                1 << 8: "https://cdn.discordapp.com/badge-icons/a25770292f4627713c294b84c0e86057.png",
                1 << 9: "https://cdn.discordapp.com/badge-icons/6f6a68d704f2ecdf1923207419ee5d9e.png",
                1 << 14: "https://cdn.discordapp.com/badge-icons/848578814d982bff127c33b9e4da43be.png",
                1 << 16: "https://cdn.discordapp.com/badge-icons/548753892235b6900e69e40e63a28198.png",
                1 << 17: "https://cdn.discordapp.com/badge-icons/85d6e77c1c7faa7036660e025e2f2a95.png",
                1 << 18: "https://cdn.discordapp.com/badge-icons/2f8f25f5c8be34a61e5e61e7f86b86c4.png",
                1 << 22: "https://cdn.discordapp.com/badge-icons/6d828ca07a5139389b5a9ff1705f3d52.png",
            }
            
            for flag, icon_url in badge_icons.items():
                if user_flags & flag:
                    badges.append(icon_url)
        except Exception as e:
            print(f"Error fetching public flags badges: {e}")
            
        headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
        try:
            resp_profile = fetch_discord_profile(id, headers)

            if resp_profile.get('user'):
                user_data = resp_profile['user']
                if 'clan' in user_data and user_data['clan'] and 'badge' in user_data['clan']:
                    clan_badge_icon = user_data['clan']['badge']
                    clan_badge_url = f"https://cdn.discordapp.com/badge-icons/{clan_badge_icon}.png"
                    badges.append(clan_badge_url)
            
            if 'badges' in resp_profile:
                for badge in resp_profile.get('badges', []):
                    if 'icon' in badge:
                        icon_url = f"https://cdn.discordapp.com/badge-icons/{badge['icon']}.png"
                        badges.append(icon_url)
            
            if 'guild_badges' in resp_profile:
                for badge in resp_profile.get('guild_badges', []):
                    if 'icon' in badge:
                        icon_url = f"https://cdn.discordapp.com/badge-icons/{badge['icon']}.png"
                        badges.append(icon_url)
        except Exception as e:
            print(f"Error fetching profile badges: {e}")
            import traceback
            traceback.print_exc()
            
        try:
            custom_resp = requesters.get(f'http://localhost:5000/api/v1/badges/{id}', quiet=True).json()
            if custom_resp and custom_resp.get('success'):
                for badge in custom_resp.get('badges', []):
                    if badge.get('icon'):
                        badges.append(badge['icon'])
        except Exception as e:
            pass
            
        try:
            resp_obama = requesters.get(f'https://api.obamabot.me/v2/text/badges?user={id}', quiet=True).json()
            externalbadges = extract_urls(resp_obama)
            badges.extend(list(externalbadges))
        except Exception as e:
            pass

        return badges
    
    def print(self, message):
        console_push("print", str(message))

    def printcenter(self, message):
        console_push("printcenter", str(message))

    def cls(self):
        console_push("cls", "")

    def printmax(self, char):
        console_push("printmax", str(char))

    def printascii(self, ascii):
        console_push("printascii", str(ascii))

    def updatenums(guildnum, friendnum):
        if window is None:
            return
        window.evaluate_js(f'document.getElementById("guildnum").innerText = "{guildnum}"')
        window.evaluate_js(f'document.getElementById("friendnum").innerText = "{friendnum}"')
        window.evaluate_js(f"updateProgressBars({friendnum}, {guildnum});")
    
    def restart(self):
        try:
            os_name = platform.system()
            if os_name == 'Windows':
                os.startfile("Repent.exe")
                os._exit(1)
            elif os_name in ['Darwin', 'Linux']:
                os.system("./Repent.bin")
            else:
                raise NotImplementedError("Unsupported operating system")
            os._exit(1)
        except (FileNotFoundError, NotImplementedError):
            os.system("python Repent.py")
            os._exit(1)
        except Exception as e:
            pass

    def get_file_names(self):
        directory = os.path.join(os.getcwd(), 'Data', 'Themes')
        try:
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except FileNotFoundError:
            return []

    def get_etheme_names(self):
        directory = os.path.join(os.getcwd(), 'Data', 'Settings', 'Configs', 'Ethemes')
        try:
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except FileNotFoundError:
            return []

    def get_etheme_names(self):
        directory = os.path.join(os.getcwd(), 'Data', 'Settings', 'Configs', 'Ethemes')
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            return [os.path.splitext(os.path.basename(file))[0] 
                    for file in files]
        except FileNotFoundError:
            return []

    def getetheme(self, name):
        directory = os.path.join(os.getcwd(), 'Data', 'Settings', 'Configs', 'Ethemes')
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            for file in files:
                if os.path.splitext(os.path.basename(file))[0] == name:
                    with open(os.path.join(directory, file), 'r') as f:
                        return f.read()
        except FileNotFoundError:
            return None
    def loadetheme(self, theme_name):
        theme_path = f"Data/Settings/Configs/Ethemes/{theme_name}.json"
        with open(theme_path, "r") as theme_file:
            return json.load(theme_file)

    def configget(self, data):
        return config_get(data)

    def get_all_settings(self):
        for attempt in range(3):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    settings = json.load(f)
                for key in ID_LIST_KEYS:
                    settings[key] = [str(v) for v in (settings.get(key) or [])]
                return settings
            except json.JSONDecodeError:
                if attempt == 2:
                    raise
                time.sleep(0.05)

    def terminal_ui(self):
        terminalui()

    def initialethemers(self):
        if config_get('etheme') == "":
            config_edit('etheme', 'Default')
        theme_path = f"Data/Settings/Configs/Ethemes/{config_get('etheme')}.json"
        with open(theme_path, "r") as theme_file:
            jsoni = json.load(theme_file)
        return jsoni

    def setethemers(self, etheme):
        theme_path = f"Data/Settings/Configs/Ethemes/{etheme}.json"

        try:
            if not os.path.exists(theme_path):
                print(f"Error: Theme file '{theme_path}' does not exist.")
                return None
            with open(theme_path, "r") as theme_file:
                content = theme_file.read()
            if not content.strip():
                print(f"Error: Theme file '{theme_path}' is empty.")
                return None
            jsoni = json.loads(content)
            required_keys = ['color', 'image', 'title_url', 'cmd_url']
            missing_keys = [key for key in required_keys if key not in jsoni]
            if missing_keys:
                print(f"Error: Missing required keys in theme file: {missing_keys}")
                return None
            return jsoni

        except FileNotFoundError:
            print(f"Error: Theme file '{theme_path}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in theme file: {e}")
        except KeyError as e:
            print(f"Error: Missing required key in theme file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return None

    def saveethemers(self, name, color, image, title_url, cmd_url, author_name="", author_url="", thumbnail="", footer_text="", show_timestamp=False):
        theme_path = f"Data/Settings/Configs/Ethemes/{name}.json"
        data = {
            "color": color,
            "image": image,
            "title_url": title_url,
            "cmd_url": cmd_url,
            "author_name": author_name,
            "author_url": author_url,
            "thumbnail": thumbnail,
            "footer_text": footer_text,
            "show_timestamp": bool(show_timestamp),
        }
        with open(theme_path, "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    def createnewetheme(self, name):
        name = filesafe(name)
        theme_path = f"Data/Settings/Configs/Ethemes/{name}.json"
        data = {
            "color": "#FFFFFF",
            "image": "",
            "title_url": "",
            "cmd_url": "",
            "author_name": "",
            "author_url": "",
            "thumbnail": "",
            "footer_text": "",
            "show_timestamp": False,
        }
        with open(theme_path, "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    def get_guild_list(self):
        try:
            return [{"id": str(g.id), "name": g.name} for g in Repent.guilds]
        except Exception:
            return []

    def get_guild_theme_overrides(self):
        return list_guild_etheme_overrides()

    def set_guild_theme_override(self, guild_id, theme_name):
        set_guild_etheme_name(guild_id, theme_name)

    def clear_guild_theme_override(self, guild_id):
        set_guild_etheme_name(guild_id, None)
    def get_rpc_config(self, name):
        config_path = f"Data/rpc_configs/{name}.json"
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def save_rpc_config(self, name, data_json):
        config_path = f"Data/rpc_configs/{name}.json"
        try:
            data = json.loads(data_json)
            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving RPC config: {e}")

    def get_commands_info(self):
        result = []
        for command in (Repent.commands or []):
            result.append({
                "name": command.name,
                "help": command.help if command.help else "none",
                "description": command.description if command.description else ""
            })
        return result

    def sendnotif(self, message):
        notif(message)

    def apply_rpc(self):
        if not BOT_READY:
            raise RuntimeError("Not connected to Discord yet")
        asyncio.run_coroutine_threadsafe(retardpresence(), Repent.loop).result(timeout=30)
        return True

    def get_bot_stats(self):
        latency = getattr(Repent, 'latency', None)
        latency_ms = round(latency * 1000) if isinstance(latency, float) and latency < float('inf') else None
        return {
            "uptime_seconds": int(time.time() - start_time),
            "latency_ms": latency_ms,
            "cmdcount": len(Repent.commands),
            "version": ver,
            "ready": BOT_READY,
        }

    def get_music_state(self):
        for guild_id, player in list(_music_players.items()):
            queue = player.core.queue
            track = queue.current
            if not track:
                continue
            guild = Repent.get_guild(guild_id)
            voice = guild.voice_client if guild else None
            return {
                "title": track.title,
                "duration": int(track.duration) if track.duration else None,
                "elapsed": int(queue.elapsed() or 0),
                "queued": len(queue.tracks),
                "loop": bool(queue.loop_enabled),
                "guild": guild.name if guild else None,
                "channel": voice.channel.name if voice and voice.channel else None,
            }
        return None

def extract_urls(obj, urls=set()):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                extract_urls(value, urls)
            elif isinstance(value, list):
                for item in value:
                    extract_urls(item, urls)
            elif isinstance(value, str) and value.startswith('http'):
                urls.add(value)
    elif isinstance(obj, list):
        for item in obj:
            extract_urls(item, urls)
    return urls

def commandrecs():
    custom_cmds = []
    non_custom_cmds = []
    
    for command in Repent.commands:
        command_info = {
            'name': command.name,
            'description': command.description,
            'help': command.help
        }
        if command.name == f"{config_get('prefix')}{config_get('prefix')}":
            pass
        elif command.name in ccs:
            custom_cmds.append(command_info)
        else:
            non_custom_cmds.append(command_info)

    return non_custom_cmds, custom_cmds

def update_profile():
    if window is None:
        return
    resp = requesters.get("https://discord.com/api/v9/users/@me", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()}).json()
    id = resp['id']
    globalusername = resp['global_name']
    accname = resp['username']
    biotext = resp['bio']
    biotext = biotext.replace('"', r'\"').replace('\n', '\\n')
    avatar = resp['avatar']
    if resp['avatar'] != None:
        avatartype = getmediatype(f"https://cdn.discordapp.com/avatars/{id}/{avatar}")
        pfpurl = f"https://cdn.discordapp.com/avatars/{id}/{avatar}.{avatartype}"
    else:
        pfpurl = "https://archive.org/download/com.hammerandchisel.discord-i-os-8.1-clutch-2.0.4-v-2.2.4/com.hammerandchisel.discord-iOS8.1-%28Clutch-2.0.4%29%20%28v2.2.4%29.png"
    window.evaluate_js(f'document.getElementById("pfp").src = "{pfpurl}"')
    window.evaluate_js(f'document.getElementById("top-pfp").src = "{pfpurl}"')
    window.evaluate_js(f'document.getElementById("global-username").innerText = "{globalusername}"')
    window.evaluate_js(f'document.getElementById("user-tag").innerText = "{accname}"')
    window.evaluate_js(f'document.querySelector(".top-navbar-center span").innerText = "Welcome back, {globalusername}"')
    window.evaluate_js(f'document.querySelector(".biobox").innerText = "{biotext}"')
    window.evaluate_js(f'fetchBadges()')

def load_profile():
    if window is None:
        return
    wait_for_gui()
    window.evaluate_js("adjustDisplayPosition();")
    window.evaluate_js("fetchBadges();")
    resp = requesters.get("https://discord.com/api/v9/users/@me", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()}).json()
    friends = requesters.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()}).json()
    guilds = requesters.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()}).json()
    friends = [record for record in friends if record["type"] != 4 and record["type"] != 3 and record["type"] != 2]
    friendnum = len(friends)
    guildnum = len(guilds)
    id = resp['id']
    globalusername = resp['global_name']
    accname = resp['username']
    biotext = resp['bio']
    biotext = biotext.replace('"', r'\"').replace('\n', '\\n')
    avatar = resp['avatar']
    cmdcount = len(Repent.commands)
    if resp['avatar'] != None:
        avatartype = getmediatype(f"https://cdn.discordapp.com/avatars/{id}/{avatar}")
        pfpurl = f"https://cdn.discordapp.com/avatars/{id}/{avatar}.{avatartype}"
    else:
        pfpurl = "https://archive.org/download/com.hammerandchisel.discord-i-os-8.1-clutch-2.0.4-v-2.2.4/com.hammerandchisel.discord-iOS8.1-%28Clutch-2.0.4%29%20%28v2.2.4%29.png"
    banner_hash = resp.get('banner', None)
    banner_color = resp.get('banner_color', None)
    if banner_hash:
        bannertype = getmediatype(f"https://cdn.discordapp.com/banners/{id}/{banner_hash}")
        bannerurl = f"https://cdn.discordapp.com/banners/{id}/{banner_hash}.{bannertype}?size=480"
        window.evaluate_js(f'document.getElementById("account-banner").style.background = "none"')
        window.evaluate_js(f'document.getElementById("account-banner").style.backgroundImage = "url({bannerurl})"')
        window.evaluate_js(f'document.getElementById("account-banner").style.backgroundSize = "cover"')
        window.evaluate_js(f'document.getElementById("account-banner").style.backgroundPosition = "center"')
    elif banner_color:
        window.evaluate_js(f'document.getElementById("account-banner").style.backgroundImage = "none"')
        window.evaluate_js(f'document.getElementById("account-banner").style.background = "{banner_color}"')
    created_ms = (int(id) >> 22) + 1420070400000
    created_date = datetime.fromtimestamp(created_ms / 1000, tz=timezone.utc).strftime("%b %d, %Y")
    window.evaluate_js(f'document.getElementById("pfp").src = "{pfpurl}"')
    window.evaluate_js(f'document.getElementById("top-pfp").src = "{pfpurl}"')
    window.evaluate_js(f'document.getElementById("global-username").innerText = "{globalusername}"')
    window.evaluate_js(f'document.getElementById("user-tag").innerText = "{accname}"')
    window.evaluate_js(f'document.getElementById("welcome-username").innerText = "{globalusername}"')
    window.evaluate_js(f'document.getElementById("welcome-avatar").src = "{pfpurl}"')
    window.evaluate_js(f'document.querySelector(".top-navbar-center span").innerText = "Welcome back, {globalusername}"')
    window.evaluate_js(f'document.querySelector(".biobox").innerText = "{biotext}"')
    window.evaluate_js(f'document.getElementById("friendnum").innerText = "{friendnum}"')
    window.evaluate_js(f'document.getElementById("guildnum").innerText = "{guildnum}"')
    window.evaluate_js(f'document.getElementById("created-date").innerText = "{created_date}"')
    window.evaluate_js(f'document.getElementById("cmdcount").innerText = "{cmdcount}"')
    window.evaluate_js(f'document.getElementById("ver").innerText = "{ver}"')
    token = config_get('token')
    user_id = resp.get('id', 'N/A')
    user_email = resp.get('email', 'N/A') or 'N/A'
    user_phone = resp.get('phone', 'N/A') or 'Not linked'
    user_nitro = 'Yes' if resp.get('premium_type', 0) > 0 else 'No'
    user_nsfw = 'Yes' if resp.get('nsfw_allowed', False) else 'No'
    user_mfa = 'Enabled' if resp.get('mfa_enabled', False) else 'Disabled'
    user_lang = resp.get('locale', 'N/A').replace('_', ' ').title()
    user_verified = 'Yes' if resp.get('verified', False) else 'No'
    window.evaluate_js(f'document.getElementById("user-id").innerText = "{user_id}"')
    window.evaluate_js(f'document.getElementById("user-email").innerText = "{user_email}"')
    window.evaluate_js(f'document.getElementById("user-phone").innerText = "{user_phone}"')
    window.evaluate_js(f'document.getElementById("user-token").innerText = "{token}"')
    window.evaluate_js(f'document.getElementById("user-nitro").innerText = "{user_nitro}"')
    window.evaluate_js(f'document.getElementById("user-nsfw").innerText = "{user_nsfw}"')
    window.evaluate_js(f'document.getElementById("user-mfa").innerText = "{user_mfa}"')
    window.evaluate_js(f'document.getElementById("user-lang").innerText = "{user_lang}"')
    try:
        start_time = getattr(Repent, 'start_time', None)
        if start_time:
            uptime_seconds = int((datetime.now(timezone.utc) - start_time).total_seconds())
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                uptime_str = f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                uptime_str = f"{hours}h {minutes}m {seconds}s"
            else:
                uptime_str = f"{minutes}m {seconds}s"
        else:
            uptime_str = 'N/A'
    except:
        uptime_str = 'N/A'
    
    try:
        latency = round(Repent.latency * 1000) if hasattr(Repent, 'latency') and Repent.latency else 'N/A'
        if latency != 'N/A':
            latency = f"{latency}ms"
    except:
        latency = 'N/A'
    
    window.evaluate_js(f'document.getElementById("bot-uptime").innerText = "{uptime_str}"')
    window.evaluate_js(f'document.getElementById("bot-cmdcount").innerText = "{cmdcount}"')
    window.evaluate_js(f'document.getElementById("bot-latency").innerText = "{latency}"')
    window.evaluate_js(f'document.getElementById("bot-version").innerText = "{ver}"')
    prefix = config_get('prefix')
    deltimer = config_get('delete_timer')
    afkmode = config_get('afkmode')
    afkmsg = config_get('afkmsg')
    devicee = config_get('device')
    embedmode = config_get('embed_mode')
    nitrosniper = config_get('nitro_sniper')
    giveawaysniper = config_get('giveaway_sniper')
    nitrotoken = config_get('nitro_sniper_redeemer')
    givedelay = config_get('giveaway_delay')
    pinglog = config_get('pinglogger')
    dmlog = config_get('dmlogger')
    sessionlog = config_get('sessionlogger')
    nitrohook = config_get('nitro_webhook_url')
    givehook = config_get('giveaway_webhook_url')
    pinghook = config_get('pinglogger_webhook_url')
    dmhook = config_get('dmlogger_webhook_url')
    webhooknotif = config_get('webhooknotifs')
    ctheme = config_get('theme') if config_get('theme') != "" else ""
    etheme = config_get('etheme')
    window.evaluate_js(f'document.getElementById("token").querySelector(".character-count-container textarea").value = {json.dumps(token)}')
    window.evaluate_js(f'document.getElementById("prefix").querySelector(".character-count-container textarea").value = {json.dumps(prefix)}')
    window.evaluate_js(f'document.getElementById("delete_timer").querySelector(".character-count-container textarea").value = {json.dumps(deltimer)}')
    window.evaluate_js(f'settoggle(document.getElementById("afkmode").querySelector(".toggle-switch input"), {json.dumps(bool(afkmode))});')
    window.evaluate_js(f'document.getElementById("afkmsg").querySelector(".character-count-container textarea").value = {json.dumps(afkmsg)}')
    window.evaluate_js(f'document.getElementById("DeviceDropdown").value = {json.dumps(devicee)}')
    window.evaluate_js(f'document.getElementById("EmbedDropdown").value = {json.dumps(embedmode)}')
    window.evaluate_js(f'document.getElementById("CThemeDropdown").value = {json.dumps(ctheme)}')
    window.evaluate_js(f'document.getElementById("EThemeDropdown").value = {json.dumps(etheme)}')
    window.evaluate_js(f'settoggle(document.getElementById("nitro_sniper").querySelector(".toggle-switch input"), {json.dumps(bool(nitrosniper))});')
    window.evaluate_js(f'settoggle(document.getElementById("giveaway_sniper").querySelector(".toggle-switch input"), {json.dumps(bool(giveawaysniper))});')
    window.evaluate_js(f'document.getElementById("nitro_sniper_redeemer").querySelector(".character-count-container textarea").value = {json.dumps(nitrotoken)}')
    window.evaluate_js(f'document.getElementById("giveaway_delay").querySelector(".character-count-container textarea").value = {json.dumps(givedelay)}')
    window.evaluate_js(f'settoggle(document.getElementById("pinglogger").querySelector(".toggle-switch input"), {json.dumps(bool(pinglog))});')
    window.evaluate_js(f'settoggle(document.getElementById("dmlogger").querySelector(".toggle-switch input"), {json.dumps(bool(dmlog))});')
    window.evaluate_js(f'settoggle(document.getElementById("sessionlogger").querySelector(".toggle-switch input"), {json.dumps(bool(sessionlog))});')
    window.evaluate_js(f'document.getElementById("nitro_webhook_url").querySelector(".character-count-container textarea").value = {json.dumps(nitrohook)}')
    window.evaluate_js(f'document.getElementById("giveaway_webhook_url").querySelector(".character-count-container textarea").value = {json.dumps(givehook)}')
    window.evaluate_js(f'document.getElementById("pinglogger_webhook_url").querySelector(".character-count-container textarea").value = {json.dumps(pinghook)}')
    window.evaluate_js(f'document.getElementById("dmlogger_webhook_url").querySelector(".character-count-container textarea").value = {json.dumps(dmhook)}')
    window.evaluate_js(f'settoggle(document.getElementById("webhooknotifs").querySelector(".toggle-switch input"), {json.dumps(bool(webhooknotif))});')
    window.evaluate_js("document.body.classList.add('loaded')")
    

def run_web_gui_server():
    from flask import Flask, jsonify, send_from_directory, request, cli as flask_cli
    global api
    ui_dir = Path(GUI_FILE).parent
    assets_dir = ui_dir / "assets"
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    flask_cli.show_server_banner = lambda *args, **kwargs: None

    app = Flask(__name__)
    port = 8080
    print(f"[INFO] assets exists: {assets_dir.exists()}")
    api = API()

    @app.route('/')
    def index():
        try:
            with open(GUI_FILE, 'r') as f:
                return f.read()
        except:
            return "GUI file not found", 404

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        assets_path = assets_dir / filename
        if assets_path.exists() and assets_path.is_file():
            resp = send_from_directory(str(assets_dir), filename)
            resp.headers['Cache-Control'] = 'no-store'
            return resp
        print(f"[ERROR] Asset not found: {filename} (looked in {assets_dir})")
        return f"Asset not found: {filename}", 404

    @app.route('/api/console')
    def api_console():
        since = request.args.get('since', 0, type=int)
        with CONSOLE_LOG_LOCK:
            entries = [e for e in CONSOLE_LOG if e["id"] > since]
            latest = CONSOLE_LOG[-1]["id"] if CONSOLE_LOG else since
        return jsonify({"entries": entries, "latest": latest})

    @app.route('/api/profile')
    def api_profile():
        try:
            return jsonify(api.get_user_profile())
        except Exception as e:
            print(f"[ERROR] Error getting profile: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/status')
    def api_status():
        return jsonify({"ready": BOT_READY, "stage": BOOT_STAGE})

    @app.route('/api/rpc', methods=['POST'])
    def api_rpc():
        data = request.get_json(force=True, silent=True) or {}
        method_name = data.get('method', '')
        args = data.get('args', [])
        method = getattr(api, method_name, None) if not method_name.startswith('_') else None
        if not callable(method):
            return jsonify({"error": f"Unknown method: {method_name}"}), 404
        try:
            return jsonify({"result": method(*args)})
        except Exception as e:
            print(f"[ERROR] RPC {method_name} failed: {e}")
            return jsonify({"error": str(e)}), 500

    print(f"[INFO] starting server on http://localhost:{port}")
    time.sleep(1)
    webbrowser.open(f"http://localhost:{port}")
    app.run(host='localhost', port=port, debug=False, use_reloader=False, threaded=True)

def runbot():
    global BOOT_STAGE
    BOOT_STAGE = "Logging into Discord"
    asyncio.run(Repent.start(config_get("token")))

def start_gui():
    os_name = platform.system()

    if os_name == "Windows":
        os.system("cls")
        os.system("mode con: cols=90 lines=20")
    else:
        os.system("clear")

    print(f"[INFO] starting repent | os: ({os_name})")

    discord_thread = threading.Thread(target=runbot, daemon=True)
    discord_thread.start()

    run_web_gui_server()

start_gui()

