Repent = commands.Bot(
    command_prefix=config_get("prefix"),
    case_insensitive=True,
    help_command=None,
    chunk_guilds_at_startup=False,
    self_bot=True,
)

def _install_gateway_parser_fixes():
    state = Repent._connection
    original_oauth_revoke = state.parsers.get("OAUTH2_TOKEN_REVOKE")
    if original_oauth_revoke is None:
        return

    def parse_oauth2_token_revoke(data):
        if not isinstance(data, dict):
            return
        if "access_token" not in data or "application_id" not in data:
            return
        original_oauth_revoke(data)

    state.parsers["OAUTH2_TOKEN_REVOKE"] = parse_oauth2_token_revoke

_install_gateway_parser_fixes()

@Repent.check
async def _global_self_throttle_check(ctx):
    try:
        if not config_get('selfthrottle'):
            return True
        if is_throttled():
            remaining = int(THROTTLE_UNTIL - time.time())
            try:
                await ctx.send(f"Self-throttle active - please wait {remaining}s (avoiding Discord's automod).", delete_after=5)
            except Exception:
                pass
            return False
        return True
    except Exception as e:
        print(f"[Self-Throttle] Check error (allowing command through): {e}")
        return True

_ANSI_ESCAPE_RE = re.compile(r'\x1b\[[0-9;]*m')

def _visible_len(s):
    return len(_ANSI_ESCAPE_RE.sub('', s))

_neofetch_cpu_brand = None

def _neofetch_info_lines():
    global _neofetch_cpu_brand
    try:
        user_str = str(Repent.user) if Repent.user else "Unknown"
    except Exception:
        user_str = "Unknown"
    try:
        guild_count = len(Repent.guilds)
    except Exception:
        guild_count = 0
    try:
        uptime_str = str(timedelta(seconds=int(round(time.time() - start_time))))
    except Exception:
        uptime_str = "Unknown"
    try:
        os_str = f"{platform.system()} {platform.release()}"
    except Exception:
        os_str = "Unknown"
    try:
        if _neofetch_cpu_brand is None:
            _neofetch_cpu_brand = cpuinfo.get_cpu_info().get('brand_raw', 'Unknown')
        cpu_str = _neofetch_cpu_brand
    except Exception:
        cpu_str = "Unknown"
    try:
        svmem = psutil.virtual_memory()
        ram_str = f"{svmem.used / (1024.0 ** 3):.1f}GB / {svmem.total / (1024.0 ** 3):.1f}GB"
    except Exception:
        ram_str = "Unknown"
    try:
        du = psutil.disk_usage(os.getcwd())
        disk_str = f"{du.used / (1024.0 ** 3):.1f}GB / {du.total / (1024.0 ** 3):.1f}GB"
    except Exception:
        disk_str = "Unknown"
    try:
        gpus = GPUtil.getGPUs()
        gpu_str = gpus[0].name if gpus else "None"
    except Exception:
        gpu_str = "Unknown"
    try:
        python_str = platform.python_version()
    except Exception:
        python_str = "Unknown"
    try:
        lat = Repent.latency
        latency_str = "Unknown" if lat != lat else f"{round(lat * 1000)}ms"
    except Exception:
        latency_str = "Unknown"
    try:
        commands_str = str(len(Repent.commands))
    except Exception:
        commands_str = "Unknown"

    L = f"{Fore.LIGHTBLUE_EX}"
    V = f"{Fore.LIGHTWHITE_EX}"
    R = f"{Style.RESET_ALL}"
    fields = [
        ("User", user_str),
        ("Guilds", str(guild_count)),
        ("Prefix", config_get('prefix')),
        ("Latency", latency_str),
        ("Uptime", uptime_str),
        ("Commands", commands_str),
        ("OS", os_str),
        ("Python", python_str),
        ("CPU", cpu_str),
        ("GPU", gpu_str),
        ("RAM", ram_str),
        ("Disk", disk_str),
    ]
    label_w = max(len(name) for name, _ in fields)
    return [f"{L}{name.ljust(label_w)}{R}  {V}{value}" for name, value in fields]

_neofetch_art_raw = [
    "⣇⣿⠘⣿⣿⣿⡿⡿⣟⣟⢟⢟⢝⠵⡝⣿⡿⢂⣼⣿⣷⣌⠩⡫⡻⣝⠹⢿⣿⣷",
    "⡆⣿⣆⠱⣝⡵⣝⢅⠙⣿⢕⢕⢕⢕⢝⣥⢒⠅⣿⣿⣿⡿⣳⣌⠪⡪⣡⢑⢝⣇",
    "⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕⢽",
    "⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕⢕",
    "⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱⢕",
    "⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀⢕",
    "⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗⢄",
    "⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕⢕",
    "⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵⣿",
    "⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟",
    "⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁⣠",
    "⡝⡵⡈⢟⢕⢕⢕⢕⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠿⠋⣀⣈⠙",
    "⡝⡵⡕⡀⠑⠳⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⡠⡲⡫⡪⡪⡣",
]

def terminalui():
 api.cls()
 if config_get("theme") == "":
    B = f"{Fore.LIGHTBLUE_EX}"
    R = f"{Style.RESET_ALL}"

    art_lines = [f"{B}{line}{R}" for line in _neofetch_art_raw]
    info_lines = _neofetch_info_lines()

    art_w = max(_visible_len(l) for l in art_lines)
    info_w = max((_visible_len(l) for l in info_lines), default=0)
    rows = max(len(art_lines), len(info_lines))

    body_rows = []
    for i in range(rows):
        art = art_lines[i] if i < len(art_lines) else ""
        info = info_lines[i] if i < len(info_lines) else ""
        art_pad = ' ' * (art_w - _visible_len(art))
        info_pad = ' ' * (info_w - _visible_len(info))
        body_rows.append(f"{art}{art_pad} {B}│{R} {info}{info_pad}")

    inner_w = art_w + 3 + info_w

    header_text = "REPENT.WTF"
    header_gap = max(inner_w - len(header_text), 0)
    header_left = header_gap // 2
    header_right = header_gap - header_left
    header_row = f"{' ' * header_left}{Fore.LIGHTWHITE_EX}{header_text}{R}{' ' * header_right}"
    sep_row = f"{B}{'─' * inner_w}{R}"

    lines_out = [f"{B}┌{'─' * (inner_w + 2)}┐{R}"]
    lines_out.append(f"{B}│{R} {header_row} {B}│{R}")
    lines_out.append(f"{B}│{R} {sep_row} {B}│{R}")
    for row in body_rows:
        pad = ' ' * max(inner_w - _visible_len(row), 0)
        lines_out.append(f"{B}│{R} {row}{pad} {B}│{R}")
    lines_out.append(f"{B}└{'─' * (inner_w + 2)}┘{R}")

    title = "\n" + "\n".join(lines_out)

    try:
        builtins.print(title)
    except UnicodeEncodeError:
        builtins.print(title.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    console_push("print", title)
 else:
    read_theme(config_get("theme"))
@Repent.command(name=f'{config_get("prefix")}{config_get("prefix")}') 
async def DONOTREMOVETHIS(ctx):
    pass
async def retardpresence():
    ws = get_websocket()
    if config_get('rpc') == "":
        req = (await arequesters.get("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
        settings = base64.b64decode(req['settings']).decode('utf-8', errors='ignore')
        if "invisible" in settings:
            Status = "invisible"
        elif "online" in settings:
            Status = "online"
        elif "idle" in settings:
            Status = "idle"
        else:
            Status = "dnd"
        jasondata = {"op": 3, "d":{"status": Status, "since": 0, "activities": [], "afk": True}}
        try:
            await ws.send_as_json(jasondata)
            logging.info("WebSocket message sent")
        except Exception as e:
            logging.error(f"WebSocket send failed: {e}")
            return 0

    async def RetardPresenceLinkChecker(link):
        regex = r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/|twitch\.tv\/)((?:[^\/\s]+\/)*[^\/\s]+)$'
        if re.search(regex, link):
            return True
        return False

    async def RetardPresenceSearcher(item_name):
        item_name = item_name + ".json"
        for dirpath, dirnames, filenames in os.walk('Data/rpc_configs'):
            if item_name in dirnames:
                return os.path.join(dirpath, item_name), "folder"
            if item_name in filenames:
                return os.path.join(dirpath, item_name), "file"
        return None, None

    async def RetardPresenceType(RetardPresenceData):
        if "SongLength" in RetardPresenceData:
            RetardPresenceType = "spotify"
        elif "Platform" in RetardPresenceData:
            RetardPresenceType = "console"
        else:
            RetardPresenceType = "normal"
        return RetardPresenceType

    async def RetardPresenceButtonBuilder(RetardPresenceData):
        labels = []
        urls = []
        buttons = RetardPresenceData.get("Buttons")
        for button in buttons:
            labels.append(button["label"])
            urls.append(button["url"])
        return labels, urls

    async def RetardPresenceBuilder():

        RetardPresenceDir, fileorfolder = await RetardPresenceSearcher(str(config_get('rpc')))
        if fileorfolder == "file":
            with open(RetardPresenceDir, "r") as RetardPresenceFile:
                RetardPresenceConfig = json.load(RetardPresenceFile)
            RetardPresenceTyping = await RetardPresenceType(RetardPresenceConfig)

            if RetardPresenceTyping == "normal":
                Title = RetardPresenceConfig.get("Title")
                if Title == "" or Title == " ":
                    Title = "‎"

                Description = RetardPresenceConfig.get("Description")
                if Description == "" or Description == " ":
                    Description = "‎"

                Sub_Text = RetardPresenceConfig.get("SubText")
                if Sub_Text == "" or Sub_Text == " ":
                    Sub_Text = None

                Large_Image = RetardPresenceConfig.get("Large_Image")
                if Large_Image == "" or Large_Image == " " or (await arequesters.get(Large_Image)).status_code != 200:
                    Large_Image = "https://assets.idlesys.xyz/assets/04a622be86cf465de35207feecffcb0e27fc34ed5c2590e7366d20bf0a28859b.png"
                Large_Image = getExternalToken(Large_Image)

                Small_Image = RetardPresenceConfig.get("Small_Image")
                if Small_Image == "" or Small_Image == " " or (await arequesters.get(Small_Image)).status_code != 200:
                    Small_Image = None
                if Small_Image:
                    Small_Image = getExternalToken(Small_Image)

                Large_Image_Text = RetardPresenceConfig.get("Large_Image_Text")
                if Large_Image_Text == "" or Large_Image_Text == " ":
                    Large_Image_Text = None

                Small_Image_Text = RetardPresenceConfig.get("Small_Image_Text")
                if Small_Image_Text == "" or Small_Image_Text == " ":
                    Small_Image_Text = None

                Status = RetardPresenceConfig.get("Status")
                if Status.lower() !=  "dnd" or Status.lower() != "online" or Status.lower() != "idle":
                    req = (await arequesters.get("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
                    settings = base64.b64decode(req['settings']).decode('utf-8', errors='ignore')
                    if "invisible" in settings:
                        Status = "dnd"
                    elif "online" in settings:
                        Status = "online"
                    elif "idle" in settings:
                        Status = "idle"
                    else:
                        Status = "dnd"
 
                State = RetardPresenceConfig.get("State")
                if State.lower() == "playing":
                    State = 0
                elif State.lower() == "streaming":
                    State = 1
                elif State.lower() == "listening":
                    State = 2
                elif State.lower() == "watching":
                    State = 3
                elif State.lower() == "competing":
                    State = 5
                else:
                    State = 0

                Timer = RetardPresenceConfig.get("Timer")
                if Timer == True:
                    Timer = start_time*1000
                else:
                    Timer = None

                RetardPresenceLabels, RetardPresenceUrls = await RetardPresenceButtonBuilder(RetardPresenceConfig)
                if RetardPresenceLabels == [] or RetardPresenceUrls == []:
                    RetardPresenceUrls = None
                    RetardPresenceLabels = None
                try:
                    if len(RetardPresenceLabels) > 2 or len(RetardPresenceUrls) > 2:
                        RetardPresenceUrls = RetardPresenceUrls[:2]
                        RetardPresenceLabels = RetardPresenceLabels[:2]
                except:
                    pass

                RetardPresenceWebsocketJson = {
                    "op": 3,
                    "d":{
                        "status": Status,
                        "since": 0,
                        "activities": [
                            {
                                "state": Sub_Text,
                                "details": Description,
                                "timestamps": {
                                    "start": Timer
                                },
                                "assets": {
                                    "large_image": Large_Image,
                                    "large_text": Large_Image_Text,
                                    "small_image": Small_Image,
                                    "small_text": Small_Image_Text
                                },
                                "buttons": RetardPresenceLabels,
                                "name": Title,
                                "application_id": "1298647912456257557",
                                "flags": 1,
                                "type": State,
                                "metadata": {
                                    "button_urls": RetardPresenceUrls,
                                },

                            }
                        ],
                        "afk": True
                    }
                }

                if State == 1: 
                    if await RetardPresenceLinkChecker(RetardPresenceConfig.get('Watch_Url')):
                        Watch_Url = RetardPresenceConfig.get('Watch_Url')
                        RetardPresenceWebsocketJson["d"]["activities"][0]["url"] = Watch_Url

                return RetardPresenceWebsocketJson

            elif RetardPresenceTyping == "spotify":
                Title = RetardPresenceConfig.get("SongTitle")
                if Title == "" or Title == " ":
                    Title = "‎"
                
                ArtistName = RetardPresenceConfig.get("ArtistName")
                if ArtistName == "" or ArtistName == " ":
                    ArtistName = "‎"
                
                AlbumName = RetardPresenceConfig.get("AlbumName")
                if AlbumName == "" or AlbumName == " ":
                    AlbumName = "‎"

                Image = RetardPresenceConfig.get("Image")
                if Image == "" or Image == " " or (await arequesters.get(Image)).status_code != 200:
                    Image = "https://assets.idlesys.xyz/assets/04a622be86cf465de35207feecffcb0e27fc34ed5c2590e7366d20bf0a28859b.png"
                Image = getExternalToken(Image)

                SongLength = RetardPresenceConfig.get("SongLength")
                try:
                    SongLength = int(SongLength)
                except:
                    SongLength = 120

                Status = RetardPresenceConfig.get("Status")
                if Status.lower() !=  "dnd" or Status.lower() != "online" or Status.lower() != "idle":
                    req = (await arequesters.get("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
                    settings = base64.b64decode(req['settings']).decode('utf-8', errors='ignore')
                    if "invisible" in settings:
                        Status = "dnd"
                    elif "online" in settings:
                        Status = "online"
                    elif "idle" in settings:
                        Status = "idle"
                    else:
                        Status = "dnd"

                Buttons = RetardPresenceConfig.get('Buttons')
                if Buttons == True or Buttons == False:
                    pass
                else:
                    Buttons == True
                if Buttons:
                    flags = 48
                    id = "spotify1"
                else:
                    flags = None
                    id = None

                albumid = RetardPresenceConfig.get("AlbumID")
                if albumid == "" or albumid == " ":
                    albumid = "7pFKs0bdrEm8qTsQczwvr4"

                RetardPresenceWebsocketJson = {
                    "op": 3,
                    "d": {
                        "status": Status,
                        "since": 0,
                        "activities": [{
                            "type": 2,
                            "name": "Spotify",
                            "assets": {
                                "large_image": Image,
                                "large_text": AlbumName
                            },
                            "details": Title,
                            "state": ArtistName,
                            "timestamps": {
                                "start": start_time*1000,
                                "end": ((start_time*1000) + SongLength * 1000)
                            },
                            "party": {
                                "id": f"spotify:{Repent.user.id}"
                            },
                            "id": id,
                            "flags": flags,
                            "metadata": {
                                "album_id": albumid
                            },
                            "instance": True
                        }],
                        "afk": True
                    }
                } 
                
                return RetardPresenceWebsocketJson
            
            elif RetardPresenceTyping == "console":
                Title = RetardPresenceConfig.get("Title")
                if Title == "" or Title == " ":
                    Title = "‎"

                Description = RetardPresenceConfig.get("Description")
                if Description == "" or Description == " ":
                    Description = "‎"

                Sub_Text = RetardPresenceConfig.get("SubText")
                if Sub_Text == "" or Sub_Text == " ":
                    Sub_Text = None

                Large_Image = RetardPresenceConfig.get("Large_Image")
                if Large_Image == "" or Large_Image == " " or (await arequesters.get(Large_Image)).status_code != 200:
                    Large_Image = "https://assets.idlesys.xyz/assets/04a622be86cf465de35207feecffcb0e27fc34ed5c2590e7366d20bf0a28859b.png"
                Large_Image = getExternalToken(Large_Image)

                Small_Image = RetardPresenceConfig.get("Small_Image")
                if Small_Image == "" or Small_Image == " " or (await arequesters.get(Small_Image)).status_code != 200:
                    Small_Image = None
                if Small_Image:
                    Small_Image = getExternalToken(Small_Image)

                Large_Image_Text = RetardPresenceConfig.get("Large_Image_Text")
                if Large_Image_Text == "" or Large_Image_Text == " ":
                    Large_Image_Text = None

                Small_Image_Text = RetardPresenceConfig.get("Small_Image_Text")
                if Small_Image_Text == "" or Small_Image_Text == " ":
                    Small_Image_Text = None

                Status = RetardPresenceConfig.get("Status")
                if Status.lower() !=  "dnd" or Status.lower() != "online" or Status.lower() != "idle":
                    req = (await arequesters.get("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
                    settings = base64.b64decode(req['settings']).decode('utf-8', errors='ignore')
                    if "invisible" in settings:
                        Status = "dnd"
                    elif "online" in settings:
                        Status = "online"
                    elif "idle" in settings:
                        Status = "idle"
                    else:
                        Status = "dnd"
                
                Timer = RetardPresenceConfig.get("Timer")
                if Timer == True:
                    Timer = start_time*1000
                else:
                    Timer = None

                console = RetardPresenceConfig.get("Platform")
                if console == "" or console == " " or console[0].lower() == "p":
                    console = "ps5"
                elif console[0].lower() == "x":
                    console = "xbox"
                else:
                    console = "ps5"

                RetardPresenceWebsocketJson = {
                    "op": 3,
                    "d":{
                        "status": Status,
                        "since": 0,
                        "activities": [
                            {
                                "state": Sub_Text,
                                "details": Description,
                                "timestamps": {
                                    "start": Timer
                                },

                                "assets": {
                                    "large_image": Large_Image,
                                    "large_text": Large_Image_Text,
                                    "small_image": Small_Image,
                                    "small_text": Small_Image_Text
                                },
                                "platform": console,
                                "name": Title,
                                "application_id": "1298647912456257557",
                                "flags": 1,
                                "type": 0,
                            }
                        ],
                        "afk": True
                    }
                }
                return RetardPresenceWebsocketJson

    presence = await RetardPresenceBuilder()
    try:
        await ws.send_as_json(presence)
    except Exception as e:
        pass

start_time = time.time()

async def update_gui_bot_status():
    global window
    while True:
        try:
            now = datetime.now(timezone.utc)
            start_dt = datetime.fromtimestamp(start_time, timezone.utc)
            uptime_seconds = int((now - start_dt).total_seconds())
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if days > 0:
                uptime_str = f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                uptime_str = f"{hours}h {minutes}m {seconds}s"
            else:
                uptime_str = f"{minutes}m {seconds}s"
                
            try:
                latency = round(Repent.latency * 1000) if hasattr(Repent, 'latency') and Repent.latency else 'N/A'
                if latency != 'N/A':
                    latency = f"{latency}ms"
            except:
                latency = 'N/A'
                
            cmd_count = len(Repent.commands)
            
            if 'window' in globals():
                try:
                    window.evaluate_js(f'document.getElementById("bot-uptime").innerText = "{uptime_str}"')
                    window.evaluate_js(f'document.getElementById("bot-cmdcount").innerText = "{cmd_count}"')
                    window.evaluate_js(f'document.getElementById("bot-latency").innerText = "{latency}"')
                except:
                    pass
                    
        except Exception as e:
            print(f"Error updating GUI bot status: {e}")
            import traceback
            traceback.print_exc()
            
        await asyncio.sleep(5)

async def auto_backup_loop():
    while True:
        try:
            if config_get('autobackup'):
                for guild in list(Repent.guilds):
                    if guild.me and (guild.me.guild_permissions.manage_guild or guild.owner_id == Repent.user.id):
                        try:
                            save_backup(guild.id)
                        except Exception as e:
                            print(f"[Auto Backup] Failed for {guild.name}: {e}")
                print(f"{Fore.LIGHTGREEN_EX}[Auto Backup] Completed scheduled backup pass.{Fore.WHITE}")
        except Exception as e:
            print(f"[Auto Backup] Error: {e}")
        await asyncio.sleep(86400)

async def subscringeguilds(ws):
    large_guilds = [g for g in Repent.guilds if g.member_count > 100000]
    for guild in large_guilds:
        try:
            await ws.send_as_json({"op": 37, "d": {"subscriptions": {f"{guild.id}": {"typing": True,"threads": True,"activities": False,"members": [],"member_updates": False,"channels": {},"thread_member_lists": []}}}})
        except Exception as e:
            pass

async def subscringedms(ws):
    r = json.loads((await arequesters.get('https://discord.com/api/v9/users/@me/channels', headers={'authorization': config_get('token'), 'x-super-properties': getxsuper()})).text)
    for channel in r:
        if channel['type'] == 1:
            try:
                await ws.send_as_json({"op": 13, "d": {"channel_id": f"{channel['id']}"}})
                await asyncio.sleep(0.5)
            except Exception as e:
                pass
        else:
            pass

@Repent.event
async def on_connect():
    global BOOT_STAGE
    BOOT_STAGE = "Connected to Discord, syncing account data"
    try:
        ws = get_websocket()
        await retardpresence()
        asyncio.create_task(subscringeguilds(ws))
        asyncio.create_task(subscringedms(ws))
        asyncio.create_task(update_gui_bot_status())
        asyncio.create_task(auto_backup_loop())
        headers = {"Authorization": config_get('token'), 'X-Super-Properties': getxsuper()}
        (await arequesters.post("https://discord.com/api/v9/oauth2/authorize?client_id=1298647912456257557&scope=applications.commands", headers=headers, json_data={"permissions":"0","authorize":True,"integration_type":1}))
        BOOT_STAGE = "Building terminal and loading commands"
        terminalui()
        customcmds()
        windowname(0)
        load_custom_aliases()
        notif("Repent Has Loaded!")
        BOOT_STAGE = "Ready"
        global BOT_READY
        BOT_READY = True
        non_custom_cmds, custom_cmds = commandrecs()
        commands_data = json.dumps({
            'customCmds': custom_cmds,
            'nonCustomCmds': non_custom_cmds
        })
    except Exception as e:
        print(e)
fetchedactivity = ""
lastsesh = ""
@Repent.listen('on_socket_raw_receive')
async def activitycollector(data):
    global lastsesh
    global soundspambool
    global seshid
    global seshidhash
    global soundlist
    event_type = data.get('t') if isinstance(data, dict) else None
    event_data = data.get('d', {}) if isinstance(data, dict) else {}
    if event_type == "READY":
        seshid = event_data.get('session_id')
        seshidhash = event_data.get('auth_session_id_hash')
        soundlist[:] = [sound for sound in soundlist if sound.get('gid') is None]
        for guild in event_data.get('guilds', []):
            for sound in guild.get('soundboard_sounds', []):
                soundlist.append({
                    'id': sound.get('sound_id'),
                    'emoid': sound.get('emoji_id'),
                    'gid': sound.get('guild_id') or guild.get('id'),
                    'emoname': sound.get('emoji_name'),
                })
    if event_type == "USER_UPDATE":
        update_profile()
    if event_type == "USER_APPLICATION_REMOVE":
        if event_data.get('application_id') == '1298647912456257557':
            headers = {"Authorization": config_get('token'), 'X-Super-Properties': getxsuper()}
            (await arequesters.post("https://discord.com/api/v9/oauth2/authorize?client_id=1298647912456257557&scope=applications.commands", headers=headers, json_data={"permissions":"0","authorize":True,"integration_type":1}))
    if event_type == "VOICE_STATE_UPDATE" and soundspambool is True and event_data.get('member', {}).get('user', {}).get('id') == str(Repent.user.id):
        if event_data.get('channel_id') is None:
            print(event_data)
            soundspambool = False
    if event_type == "GUILD_MEMBERS_CHUNK":
        global fetchedactivity
        async def extract_raw_activities(chunk):
            raw_activities_list = []
            presences = chunk.get('d', {}).get('presences', [])
            for presence in presences:
                activities = presence.get('activities', [])
                user_id = presence.get('user', {}).get('id')
                for activity in activities:
                    session_id = activity.get('session_id')
                    application_id = activity.get('application_id')
                    if user_id is not None and session_id is not None and application_id is not None:
                        buttonmeta = (await arequesters.get(f"https://discord.com/api/v9/users/{user_id}/sessions/{session_id}/activities/{application_id}/metadata", headers={"Authorization": config_get('token'), "X-Super-Properties": getxsuper()}))
                        activity['metadata'] = buttonmeta.json()
                    raw_activities_list.append(activity)
            return raw_activities_list

        parsed = await extract_raw_activities(data)
        activities_json = json.dumps(parsed, indent=4)
        fetchedactivity = activities_json

    elif event_type == "SESSIONS_REPLACE":
        if config_get('sessionlogger') is True:
            resp = (await arequesters.get("https://discord.com/api/v9/auth/sessions", headers={"Authorization": config_get('token'), "X-Super-Properties": getxsuper()})).json()
            def parse_time(session):
                return datetime.fromisoformat(session["approx_last_used_time"].replace('Z', '+00:00'))
            def get_latest_session(sessions):
                latest_session = max(sessions, key=parse_time)
                return latest_session
            sessions = resp["user_sessions"]
            latest = get_latest_session(sessions)
            latestsesh = latest['id_hash']
            if latestsesh == lastsesh or latestsesh == seshidhash:
                return
            else:
                lastsesh=latestsesh
            timee = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            info = f"ID Hash: {latest['id_hash']}\nDate: {timee}\nOS: {latest['client_info']['os']}\nPlatform: {latest['client_info']['platform']}\nLocation: {latest['client_info']['location']}"
            print(f"{Fore.LIGHTRED_EX}[New Session Detected]{Fore.WHITE}\n{info}")
            notification = Notify()
            notification.application_name = "Repent Selfbot"
            notification.title = f"New Session Detected"
            notification.message = "Check console for more info!"
            notification.icon = str(ICON_FILE)
            notification.send()

    elif event_type == "GUILD_CREATE":
        ws = get_websocket()
        guild = Repent.get_guild(int(event_data['id']))
        if guild is not None and guild.member_count > 100000:
            try:
                await ws.send_as_json({"op": 37, "d": {"subscriptions": {f"{guild.id}": {"typing": True,"threads": True,"activities": True,"members": [],"member_updates": True,"channels": {},"thread_member_lists": []}}}})
            except Exception as e:
                pass

    elif event_type in {"GUILD_DELETE", "GUILD_CREATE", "RELATIONSHIP_REMOVE", "RELATIONSHIP_ADD"}:
        if event_type in ("RELATIONSHIP_ADD", "RELATIONSHIP_REMOVE") and config_get('relationshiplogger'):
            asyncio.create_task(log_relationship_change(event_type, event_data))
        friends = (await arequesters.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
        guilds = (await arequesters.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
        guildnum = len(guilds)
        guilds = (await arequesters.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
        friends = [record for record in friends if record["type"] != 4 and record["type"] != 3 and record["type"] != 2]
        friendnum = len(friends)
        API.updatenums(guildnum, friendnum)

    elif event_type == "GUILD_UPDATE":
        protected = load_vanity_protect()
        desired_code = protected.get(str(event_data.get('id')))
        if desired_code and event_data.get('vanity_url_code') != desired_code:
            asyncio.create_task(handle_vanity_lost(event_data.get('id'), desired_code))

    elif event_type == 'VOICE_STATE_UPDATE':
        if int(event_data['user_id']) == Repent.user.id:
            global currentvc, currentvcguild
            currentvc = event_data.get('channel_id')
            currentvcguild = event_data.get('guild_id')
        if config_get('autovcleave') and currentvc and currentvcguild and event_data.get('guild_id') == currentvcguild:
            asyncio.create_task(leave_voice_if_alone())

RELATIONSHIP_TYPE_LABELS = {1: "Friend", 2: "Blocked", 3: "Incoming Friend Request", 4: "Outgoing Friend Request"}

async def log_relationship_change(event_type, event_data):
    try:
        headers = {"Authorization": config_get('token'), "X-Super-Properties": getxsuper()}
        user = event_data.get('user') or {}
        user_id = event_data.get('id') or user.get('id')
        if not user.get('username') and user_id:
            resp = (await arequesters.get(f"https://discord.com/api/v9/users/{user_id}", headers=headers, quiet=True))
            if resp.status_code == 200:
                user = resp.json()
        username = user.get('username', f"Unknown ({user_id})")
        rel_type = RELATIONSHIP_TYPE_LABELS.get(event_data.get('type'), "Relationship")
        action = "Added" if event_type == "RELATIONSHIP_ADD" else "Removed"
        title = f"__{rel_type} {action}!__"
        description = f"**User:** {username} (`{user_id}`)"
        print(f"{Fore.LIGHTRED_EX}[Relationship Logger] ~ {rel_type} {action}: {Fore.WHITE}{username} ({user_id})")
        if config_get('webhooknotifs') and config_get('relationship_webhook_url'):
            await send_webhook(title, description, config_get('relationship_webhook_url'))
    except Exception as e:
        print(f"[Relationship Logger] Error: {e}")

async def handle_vanity_lost(guild_id, desired_code):
    try:
        success = await reclaim_vanity(guild_id, desired_code)
        guild = Repent.get_guild(int(guild_id))
        guild_name = guild.name if guild else guild_id
        if success:
            print(f"{Fore.LIGHTGREEN_EX}[Vanity Protector] Reclaimed vanity '/{desired_code}' for {guild_name}.{Fore.WHITE}")
            if config_get('webhooknotifs') and config_get('error_webhook_url'):
                await send_webhook("__Vanity Reclaimed!__", f"Re-set `/{desired_code}` on **{guild_name}** before it could be sniped.", config_get('error_webhook_url'))
        else:
            print(f"{Fore.LIGHTRED_EX}[Vanity Protector] Failed to reclaim '/{desired_code}' for {guild_name} - it may already be taken.{Fore.WHITE}")
            if config_get('webhooknotifs') and config_get('error_webhook_url'):
                await send_webhook("__Vanity Reclaim Failed!__", f"Could not re-set `/{desired_code}` on **{guild_name}** - it may already be taken.", config_get('error_webhook_url'))
    except Exception as e:
        print(f"[Vanity Protector] Error: {e}")

async def leave_voice_if_alone():
    try:
        if not currentvc or not currentvcguild:
            return
        guild = Repent.get_guild(int(currentvcguild))
        if guild is None:
            return
        channel = guild.get_channel(int(currentvc))
        if channel is None:
            return
        human_members = [m for m in channel.members if not m.bot and m.id != Repent.user.id]
        if human_members:
            return
        ws = get_websocket()
        await ws.send_as_json({"op": 4, "d": {"guild_id": str(currentvcguild), "channel_id": None, "self_mute": False, "self_deaf": False}})
        print(f"{Fore.LIGHTYELLOW_EX}[Auto VC-Leave] Left '{channel.name}' - no one else was in the channel.{Fore.WHITE}")
    except Exception as e:
        print(f"[Auto VC-Leave] Error: {e}")

def getExternalToken(url):
    parsed_url = urlparse(url)
    file_path, ext = os.path.splitext(parsed_url.path)
    if parsed_url.netloc in ["cdn.discordapp.com", "media.discordapp.net"] and ext == ".webp":
        response = requested.get(url)
        image = Image.open(BytesIO(response.content))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        headers = {"Authorization": "Client-ID 546c25a59c58ad7"}
        files = {"image": ("Repent.png", buffer, "image/png")}
        req = requested.post("https://api.imgur.com/3/upload", headers=headers, files=files).json()
        url = req['data']['link']
    elif parsed_url.netloc in ["cdn.discordapp.com", "media.discordapp.net"]:
        payload = {
            "image": url,
            "type": "url",
            "name": f"Repent{ext}"
        }
        headers = {"Authorization": "Client-ID 546c25a59c58ad7"}
        req = requested.post("https://api.imgur.com/3/upload", headers=headers, json=payload).json()
        url = req['data']['link']
    r = requested.post("https://discord.com/api/v9/applications/356876176465199104/external-assets", headers={"authorization": config_get('token')}, json={
        "urls": [
            url
        ]
    })
    return "mp:" + r.json()[0]["external_asset_path"]

@Repent.before_invoke
async def before_command(ctx):
    if ctx.command.name != ">>":
        if ctx.author.id == Repent.user.id:
            await ctx.message.delete()
        Repent.command_prefix = config_get('prefix')
        if not hasattr(before_command, "commandsdone"):
            before_command.commandsdone = 0
        print(f"{Fore.LIGHTRED_EX}[{get_time()}] Command Used {Fore.LIGHTWHITE_EX}~ {ctx.command.name}" + Fore.RESET)
        before_command.commandsdone += 1
        windowname(before_command.commandsdone)
    else:
        pass

@Repent.event
async def on_command_error(ctx, error):
    try:
        try:
            await ctx.message.delete()
        except:
            pass
        heading = "Error"
        cmdname = "ERROR"
        error_str = str(error)
        Repent.command_prefix = config_get('prefix')
        if isinstance(error, commands.CommandNotFound):
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}The command entered does not exist." + Fore.RESET)
            body = "Command Not Found!"
            await panelmaker(ctx, heading, body, cmdname)
        elif isinstance(error, commands.CheckFailure):
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}You're missing the permissions to execute this command." + Fore.RESET)
            body = "You're missing the permissions to execute this command."
            await panelmaker(ctx,heading,body,cmdname)
        elif isinstance(error, commands.MissingRequiredArgument):
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}You're missing the required argument(s) ({error.param.name}) to execute this command." + Fore.RESET)
            body = f"You're missing the required argument(s) ({error.param.name}) to execute this command."
            await panelmaker(ctx,heading,body,cmdname)
        elif isinstance(error, discord.Forbidden):
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{error}" + Fore.RESET)
            body = error
            await panelmaker(ctx,heading,body,cmdname)
        elif "Cannot send an empty message" in error_str:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Could not send an empty message." + Fore.RESET)
            body = "Could not send an empty message."
            await panelmaker(ctx,heading,body,cmdname)
        elif "ssl" in error_str.lower():
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {error}" + Fore.RESET)
            body = "An SSL issue occured, please try again."
            await panelmaker(ctx,heading,body,cmdname)
            return
        else:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{error_str}" + Fore.RESET)
            body = error_str
            await panelmaker(ctx,heading,body,cmdname)
            return
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}An unknown error occurred: {e}" + Fore.RESET)
        body = "An unknown error occurred. Try again later."
        await panelmaker(ctx,heading,body,cmdname)
        asyncio.run(await send_webhook("Bot Command Error", f"An unknown error occurred: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url')))

@Repent.event
async def on_spotify_session_replace(userid, session_id, state, syncid):
    global seshid
    seshid = session_id

async def run_whitelisted_music_command(message):
    # self_bot=True makes process_commands ignore other users, so whitelisted music commands are invoked directly
    if not message.content.startswith(config_get('prefix') or ''):
        return
    ctx = await Repent.get_context(message)
    if ctx.command is None or ctx.command.help != "music":
        return
    try:
        await Repent.invoke(ctx)
    except Exception:
        import traceback
        traceback.print_exc()

@Repent.event
async def on_message(message):
        # print(f"[DEBUG] on_message fired: author_id={message.author.id} me={Repent.user.id if Repent.user else None} content={message.content!r} prefix={config_get('prefix')!r}")
        if message.author.id == Repent.user.id:
            if message.content.startswith(config_get('prefix') or ''):
                record_self_message()
            try:
                await Repent.process_commands(message)
            except Exception as e:
               # print(f"[DEBUG] process_commands raised: {e!r}")
                import traceback
                traceback.print_exc()
        elif message.author.id in (config_get('music_whitelist') or []):
            await run_whitelisted_music_command(message)
        sniper = config_get('nitro_sniper')
        token = config_get('token')
        time = datetime.now().strftime('%H:%M:%S %p')
        dmlogid = setting_get('dmlogid')
        blacklist = config_get('nitro_blacklist_ids')
        serverpingbanlist = setting_get('serverpingban')
        userpingbanlist = setting_get('userpingban')
        serverpingkicklist = setting_get('serverpingkick')
        userpingkicklist = setting_get('userpingkick')
        if blacklist == None:
            blacklist = []
        channel_info = (
            f"{message.channel.name}"
            if isinstance(message.channel, discord.TextChannel)
            else (
                f"Private channel with {message.author.name}"
                if isinstance(message.channel, discord.DMChannel)
                else (
                    f"{message.channel.name}"
                    if isinstance(message.channel, discord.Thread)
                    else ("Unknown Name")
                )
            )
        )

        if sniper:
                if message.guild and int(message.guild.id) in blacklist:
                    pass
                else:
                    start = datetime.now()
                    code_match = re.search(r"(?:https://)?discord\.gift/([a-zA-Z0-9]+)", message.content)
                    if code_match:
                        code = code_match.group(1)
                        req = await redeem_code(code, token)
                        delay = datetime.now() - start
                        delay = str(delay.microseconds)[:3]
                        if 'subscription_plan' in req:
                            status = "Real"
                        elif 'Unknown Gift Code' in req:
                            status = "Invalid"
                        elif 'This gift has been redeemed already.' in req:
                            status = "Already Claimed"
                        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
                            jumpurl = f"discord://-/channels/@me/{message.channel.id}/{message.id}"
                        else:
                            jumpurl = f"discord://-/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                        print(f"{Fore.LIGHTRED_EX}[NITRO SNIPER] ~ {time}{Fore.WHITE}\nCode: discord.gift/{code}\nDelay: {delay}ms\nServer: {message.guild}\nChannel: [{channel_info}]({jumpurl})\nSent By: {message.author.name}\nStatus: {status}")
                        if config_get('webhooknotifs') and config_get('nitro_webhook_url') != "": 
                            if status == "Real":
                                title = "__SNIPED NITRO__"
                                description = f"\n\n**Delay:** {delay}ms\n**Time Sniped:** {time}\n**Server:** {message.guild}\n**Sent By:** {message.author.mention}\n**Code:** discord.gift/{code}\n**Channel:** {channel_info}\n**Message:** [**{channel_info}**]({message.jump_url})\n**Status:** {status}\n\n<@{Repent.user.id}>"
                            else:
                                title ="__NITRO SNIPER LOG__"
                                description = f"\n\n**Delay:** {delay}ms\n**Time Sniped:** {time}\n**Server:** {message.guild}\n**Sent By:** {message.author.mention}\n**Code:** discord.gift/{code}\n**Channel:** {channel_info}\n**Message:** [**{channel_info}**]({message.jump_url})\n**Status:** {status}"
                            await send_webhook(title,description,config_get('nitro_webhook_url'))

        if message.reference:
            try:
                resolved_user = message.reference.resolved.author
            except:
                resolved_user = ""
        if message.reference and message.reference.resolved and resolved_user == Repent.user or Repent.user.mention in message.content and message.author.id != Repent.user.id:
            try:
                if message.author.id in userpingbanlist:
                    if message.guild.me.guild_permissions.ban_members:
                        await message.author.ban(reason="Repent Ping-Ban")
                    else:
                        pass
                if message.guild.id in serverpingbanlist:
                    if message.guild.me.guild_permissions.ban_members:
                        await message.author.ban(reason="Repent Ping-Ban")
                    else:
                        pass
                if message.guild.id in serverpingkicklist:
                    if message.guild.me.guild_permissions.kick_members:
                        await message.author.kick(reason="Repent Ping-Kick")
                    else:
                        pass
                if message.author.id in userpingkicklist:
                    if message.guild.me.guild_permissions.kick_members:
                        await message.author.kick(reason="Repent Ping-Kick")
                    else:
                        pass
            except:
                pass
            if "Chedmind" in message.content:
                return
            if config_get('pinglogger') == True:
                if message.author == Repent.user:
                    return
                if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
                    jumpurl = f"discord://-/channels/@me/{message.channel.id}/{message.id}"
                else:
                    jumpurl = f"discord://-/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                title = "__Ping Logged!__"
                description = f"**Author:** {message.author.mention}\n**Message:** {message.content}\n**Server:** {message.guild}\n**Channel:** [**{channel_info}**]({message.jump_url})"
                if config_get('pinglogger_webhook_url') != "" and config_get('webhooknotifs'):
                    await send_webhook(title,description,config_get('pinglogger_webhook_url'))
                    url = message.jump_url.split('/')
                print(f"{Fore.LIGHTRED_EX}[PingLogger] ~ {time}{Fore.WHITE}\nAuthor: {message.author.name}\nMessage: {message.content}\nServer: {message.guild}\nChannel: [{channel_info}]({jumpurl})")
            
            if config_get('afkmode') == True:
                afk_msg_length = len(config_get('afkmsg'))
                typing_duration = afk_msg_length * 0.2
                async with message.channel.typing():
                    await asyncio.sleep(typing_duration)
                    await message.reply(config_get('afkmsg'))
                url = f"https://canary.discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}/ack"
                headers = {'authorization': token }
                json_data = {"manual": True, "mention_count": 1}
                (await arequesters.post(url, headers=headers, json_data=json_data))

        if dmlogid is not None and isinstance(message.channel, discord.GroupChannel) == False:
            if isinstance(message.channel, discord.DMChannel):
                try:
                    if message.author.id in dmlogid or message.author.id == Repent.user.id and message.channel.recipient.id in dmlogid:
                        if message.author.id != Repent.user.id:
                            if config_get('dmlogger_webhook_url') != "" and config_get('webhooknotifs'):
                                title = "__Direct Message Logged!__"
                                description = f"**Author:** {message.author.mention}\n**Message:** {message.content}\n"
                                description += f"**Channel:** [**Direct Message With {message.author.name}**]({message.jump_url})"
                                await send_webhook(title, description, config_get('dmlogger_webhook_url'))

                            print(f"{Fore.LIGHTRED_EX}[DM Logger] ~ {time}{Fore.WHITE}\nAuthor: {message.author.name}\nMessage: {message.content}\n", end="")
                            print(f"Channel: Direct Message With {message.author.name}\n", end="")

                        chat_style = """
                        <style>
                        .embed {
                            padding: 10px;
                            background-color: #2B2D31;
                            border-radius: 8px;
                            display: flex;
                            border-left-width: 5px;
                            max-width: 500px
                        }

                        .embed-image-container {
                            display: inline-block;
                            padding: 5px;
                            background-color: #2B2D31;
                            border-radius: 8px;
                            max-width: 500px
                        }

                        .embed-content {
                            flex: 1;
                        }

                        .embed-title a {
                            text-decoration: none;
                            color: inherit;
                        }

                        .embed-description {
                            font-size: 0.9em;
                            margin-bottom: 10px;
                        }

                        .embed-media {
                            margin-top: 10px;
                        }

                        .image {
                            max-width: 25%;
                            height: auto;
                        }

                        .videoo {
                            max-width: 25%;
                            height: auto;
                        }

                        .embed-image {
                            max-width: calc(100% - 10px);
                            height: auto;
                            border-radius: 8px;
                        }

                        .embed-video {
                            max-width: calc(100% - 10px);
                            height: auto;
                        }

                        body {
                            background-color: #313338;
                            color: #ffffff;
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 10px;
                        }

                        .timestamp {
                            color: #888888;
                            font-size: 0.8em;
                            margin-left: 5px;
                            margin-right: 5px;
                        }

                        .chat-wrapper {
                            position: relative;
                            overflow-y: auto;
                            padding: 10px;
                        }

                        .chat-container {
                            display: flex;
                            flex-direction: column; 
                        }

                        .message {
                            display: flex;
                            align-items: flex-start;
                            padding-bottom: 10px;
                        }

                        .profile-image {
                            width: 32px;
                            height: 32px;
                            border-radius: 50%;
                            margin-right: 5px;
                        }

                        .message-content {
                            display: flex;
                            flex-direction: column;
                            word-wrap: break-word; 
                        }

                        .message-header {
                            display: flex;
                            align-items: center;
                            width: 100%;
                        }

                        .author {
                            color: #7289da;
                            font-weight: bold;
                        }

                        .audio {
                            width: 100%;
                        }
                        </style>
                        """
                        content = await process_messagee(message)
                        file_path = f'Data/Logs/{message.channel.recipient.name}.html'
                        async with aiofiles.open(file_path, 'a', encoding='utf-8') as file:
                            if os.path.getsize(file_path) == 0:
                                await file.write("<html>")
                                await file.write(chat_style)
                                await file.write("<body>")
                                await file.write('<div class="chat-wrapper">')
                                await file.write('<div class="chat-container">')
                            await file.flush()
                            await file.write(content)
                except:
                    pass

        if setting_get('msglogids') is None:
            pass
        else:
            if message.channel.id in setting_get('msglogids'):
                chat_style = """
                <style>
                .embed {
                    padding: 10px;
                    background-color: #2B2D31;
                    border-radius: 8px;
                    display: flex;
                    border-left-width: 5px;
                    max-width: 500px
                }

                .embed-image-container {
                    display: inline-block;
                    padding: 5px;
                    background-color: #2B2D31;
                    border-radius: 8px;
                    max-width: 500px
                }

                .embed-content {
                    flex: 1;
                }

                .embed-title a {
                    text-decoration: none;
                    color: inherit;
                }

                .embed-description {
                    font-size: 0.9em;
                    margin-bottom: 10px;
                }

                .embed-media {
                    margin-top: 10px;
                }

                .image {
                    max-width: 25%;
                    height: auto;
                }

                .videoo {
                    max-width: 25%;
                    height: auto;
                }

                .embed-image {
                    max-width: calc(100% - 10px);
                    height: auto;
                    border-radius: 8px;
                }

                .embed-video {
                    max-width: calc(100% - 10px);
                    height: auto;
                }

                body {
                    background-color: #313338;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 10px;
                }

                .timestamp {
                    color: #888888;
                    font-size: 0.8em;
                    margin-left: 5px;
                    margin-right: 5px;
                }

                .chat-wrapper {
                    position: relative;
                    overflow-y: auto;
                    padding: 10px;
                }

                .chat-container {
                    display: flex;
                    flex-direction: column; 
                }

                .message {
                    display: flex;
                    align-items: flex-start;
                    padding-bottom: 10px;
                }

                .profile-image {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    margin-right: 5px;
                }

                .message-content {
                    display: flex;
                    flex-direction: column;
                    word-wrap: break-word; 
                }

                .message-header {
                    display: flex;
                    align-items: center;
                    width: 100%;
                }

                .author {
                    color: #7289da;
                    font-weight: bold;
                }

                .audio {
                    width: 100%;
                }
                </style>
                """
                if not os.path.exists(f'Data/Logs/{message.guild.name}~Message_Logs'):
                    os.mkdir(f'Data/Logs/{message.guild.name}~Message_Logs')
                content = await process_messagee(message)
                file_path = f'Data/Logs/{message.guild.name}~Message_Logs/{message.channel.name}.html'
                async with aiofiles.open(file_path, 'a', encoding='utf-8') as file:
                    if os.path.getsize(file_path) == 0:
                        await file.write("<html>")
                        await file.write(chat_style)
                        await file.write("<body>")
                        await file.write('<div class="chat-wrapper">')
                        await file.write('<div class="chat-container">')
                    await file.flush()
                    await file.write(content)

joinedgwlist = []
@Repent.listen('on_socket_raw_receive')
async def universalgiveawaybot(data):
    giveawaybotlist = config_get('giveaway_bot_ids')
    blacklist = config_get('giveaway_blacklist_ids')
    if blacklist == None:
        blacklist = []
    time = datetime.now().strftime('%H:%M:%S %p')
    try:
        if data['t'] == 'MESSAGE_CREATE':
                if int(data['d']['author']['id']) in giveawaybotlist or int(data['d']['author']['id']) == 294882584201003009 and config_get('giveaway_sniper') == True:
                    if data['d']['id'] in joinedgwlist:
                        return
                    if int(data['d']['guild_id']) in blacklist:
                        return
                    nonce = ''
                    for i in range(0,19): nonce += str(random.randint(1,9))
                    if len(data['d']['embeds']) > 0:
                        if len(data['d']['components']) > 0:            
                            my13threasonwhy = {'type': 3,
                                'nonce': nonce,
                                'guild_id': data['d']['guild_id'],
                                'channel_id': data['d']['channel_id'],
                                'message_flags': 0,
                                'message_id': data['d']['id'],
                                'application_id': data['d']['author']['id'],
                                'session_id': 'whyhavesessionidwhendonothingwith',
                                'data': {'component_type': data['d']['components'][0]['components'][0]['type'],'custom_id': data['d']['components'][0]['components'][0]['custom_id']}
                                }
                            await asyncio.sleep(int(config_get('giveaway_delay'))) 
                            r = (await arequesters.post('https://canary.discord.com/api/v9/interactions', headers={'authorization': config_get('token')}, json_data=my13threasonwhy))
                            if r.status_code == 204:
                                joinedgwlist.append(data['d']['id'])
                                print(f"{Fore.LIGHTRED_EX}[Entered giveaway]{Fore.RESET} ~ {time}")
                                print(f"Guild ID: {data['d']['guild_id']}")
                                print(f"Message: discord://-/channels/{data['d']['guild_id']}/{data['d']['channel_id']}/{data['d']['id']}")
                                if config_get('webhooknotifs') == True:
                                    server_name = data['d']['guild_id']  
                                    if 'guilds' in data:
                                        for guild in data['guilds']:
                                            if guild['id'] == data['d']['guild_id']:
                                                server_name = guild['name']
                                                break
                                    url = f"https://canary.discord.com/channels/{data['d']['guild_id']}/{data['d']['channel_id']}/{data['d']['id']}"
                                    title = "Giveaway Sniper"
                                    description = f"Link to giveaway: [**Giveaway**]({url})\nJoined at: {time}"
                                    await send_webhook(title,description,config_get('giveaway_webhook_url'))
    except Exception as e:
        pass

_cached_xsuper = None

def getxsuper():
            global _cached_xsuper
            if _cached_xsuper:
                return _cached_xsuper
            os = platform.system()
            browser = "Discord Client"
            osarch = platform.architecture()[0]
            if osarch == '64bit':
                osarch = 'x64'
            elif osarch == '32bit':
                osarch = 'x32'
            current_locale = locale.getdefaultlocale()[0]
            syslocale = current_locale.replace("_", "-")
            osver = platform.version()
            resp = requesters.get("https://discord.sale/api/builds")
            data = resp.json()
            cbuild = data.get("build_number")
            x = {"os":os,"build_number":cbuild, "os_version":osver, "system_locale":syslocale,"browser":browser}
            json_str = json.dumps(x)
            xsuper = base64.b64encode(json_str.encode()).decode()
            _cached_xsuper = xsuper
            return xsuper

def get_command_categories():
    categories = set()  
    for command in Repent.commands:
        if command.help:
            categories.add(command.help.lower())
    return sorted(categories)

def get_commands(category, num=None):
    commands = set()
    category = category
    sorted_commands = sorted(Repent.commands, key=lambda x: x.name)
    filtered_commands = [command for command in sorted_commands if command and command.help == category]
    max_panels = len(filtered_commands) // 11 + (1 if len(filtered_commands) % 11 != 0 else 0)
    try:
        if num is None:
            num = 1
        else:
            num = int(num)
    except ValueError:
        num = 1 
    start_index = (num - 1) * 11
    end_index = start_index + 11
    commands_to_return = filtered_commands[start_index:end_index]
    for command in commands_to_return:
        commands.add(f"{command.name}")
    return sorted(commands), max_panels

def format_commands(commands):
    return '\n'.join([f"{config_get('prefix')}{cmd}" for cmd in commands])

def format_catagories(catagories):
    return '\n'.join([f"{config_get('prefix')}help {catagory}" for catagory in catagories])

def is_cmd(cmd):
    cmd = cmd.lower()
    for command in Repent.commands:
        if command.name == cmd or cmd in [alias.lower() for alias in command.aliases]:
            if command.description is None:
                description = "None"
            else:
                description = command.description
            return True, description
    return False, None
