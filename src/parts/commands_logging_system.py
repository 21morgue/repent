async def establish_websocket(accesstoken):
    uri = "wss://sydney.bing.com/sydney/ChatHub?sec_access_token=" + urllib.parse.quote(accesstoken)
    ws = await connect(uri)
    await ws.send('{"protocol":"json","version":1}\x1e')
    return ws

async def send_query(ws, query, conversationId, clientId):
    now = datetime.now().astimezone(timezone(timedelta(hours=1)))
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    timestamp = timestamp[:-2] + ':' + timestamp[-2:]
    j2 = {"arguments":[{"source":"cib","optionsSets":["nlu_direct_response_filter","deepleo","disable_emoji_spoken_text","responsible_ai_policy_235","enablemm","dv3sugg","iyxapbing","iycapbing","h3precise","clgalileo","gencontentv3","storagev2fork","papynoapi","gndlogcf","gptvnoex"],"allowedMessageTypes":["ActionRequest","Chat","ConfirmationCard","Context","InternalSearchQuery","InternalSearchResult","Disengaged","InternalLoaderMessage","Progress","RenderCardRequest","RenderContentRequest","AdsQuery","SemanticSerp","GenerateContentQuery","SearchQuery","GeneratedCode"],"sliceIds":["bgstreamcf","designer2cf","suppsm240hm","srchqryfix","suppsm240-t","cmcpupsalltf","sydtransctrl","proupsallcf","0209bicv3","130memrev","116langwbs0","927storev2fk","0208papynoa","sapsgrds0","1119backoss0","enter4nl"],"verbosity":"verbose","scenario":"SERP","plugins":[],"conversationHistoryOptionsSets":["autosave","savemem","uprofupd","uprofgen"],"isStartOfSession":True,"message":{"locale":"en-GB","timestamp":timestamp,"author":"user","inputMethod":"Keyboard","text":query,"messageType":"Chat"},"tone":"Precise","spokenTextMode":"None","conversationId":conversationId,"participant":{"id":clientId}}],"invocationId":"0","target":"chat","type":4}
    await ws.send(json.dumps(j2) + "\x1e")

async def queryCopilot(query, ws, conversationId, clientId):
    try:
        await send_query(ws, query, conversationId, clientId)
        
        while True:
            message = await ws.recv()
            data = message.split("\x1e")

            for cleandata in data:
                if cleandata == "":
                    continue

                j = json.loads(cleandata)

                if cleandata == "{}":
                    await ws.send('{"type":6}\x1e')
                    await send_query(ws, query, conversationId, clientId)
                    continue

                if j["type"] == 2:
                    return j["item"]["result"]["message"]
    finally:
        await ws.close()

@Repent.command(aliases=['gpt4'], description=f"Talks to the GPT-4 AI. \nUsage: {config_get('prefix')}gpt <text>", help="fun")
async def gpt(ctx, *, query):
    session = requested.Session()

    headers = {
        'authority': 'copilot.microsoft.com',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://copilot.microsoft.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"120.0.6099.199"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.199"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-ms-client-request-id': '5e2ba668-a315-422e-8bc1-2b699da1b29f',
        'x-ms-useragent': 'azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.12.3 OS/Windows',
        }
    params = {
        'bundleVersion': '1.1573.4',
    }

    response = session.get('https://copilot.microsoft.com/turing/conversation/create', params=params, headers=headers)
    response.raise_for_status()
    j = response.json()
    accesstoken = response.headers["X-Sydney-Encryptedconversationsignature"]
    conversationId = j["conversationId"]
    clientId = j["clientId"]
    
    ws = await establish_websocket(accesstoken)

    try:
        result = await queryCopilot(query, ws, conversationId, clientId)
        heading = "GPT-4 Response"
        body = result
        cmdname = "gpt"
        await panelmaker(ctx, heading, body, cmdname)
    finally:
        session.close()

message_history = {
    "deleted": defaultdict(list),
    "edited": defaultdict(list)
}

@Repent.event
async def on_message_delete(message):
    try:
        if message is None or message.author is None:
            logging.info("The message or message.author was None.")
            return
        
        if message.author == Repent.user:
            logging.info("Ignoring bot's own messages.")
            return
        
        channel_messages = message_history["deleted"][message.channel.id]
        channel_messages.append(message)
        if len(channel_messages) > 5:
            channel_messages.pop(0)

        logging.info(f"Stored deleted message from {message.author.name}: {message.content}")
    except Exception as e:
        logging.error(f"Error in on_message_delete: {e}")

@Repent.event
async def on_message_edit(before, after):
    try:
        if before.author == Repent.user or before.content == after.content:
            return
        
        message_history["edited"][before.channel.id].append({
            "before": before,
            "after": after
        })

        channel_messages = message_history["edited"][before.channel.id]
        if len(channel_messages) > 5:
            channel_messages.pop(0)
        logging.info(f"Stored edited message from {before.author.name}: '{before.content}' -> '{after.content}'")
    except Exception as e:
        logging.error(f"Error in on_message_edit: {e}")

@Repent.command(aliases=['sn', 'snipe'], description=f"Snipes a deleted message, Allows number of messages to be specified. \nUsage: {config_get('prefix')}snipemsg [Amount]", help="utility")
async def snipemsg(ctx, amount = 1):
    count = 0
    if amount > 5:
        amount = 5
    try:
        if ctx.channel.id in message_history["deleted"]:
            messages = message_history["deleted"][ctx.channel.id]
            if not messages:
                no_snipe_heading = "SnipeMsg"
                no_snipe_body = "There's nothing to snipe!"
                no_snipe_cmdname = "snipemsg"
                await panelmaker(ctx, no_snipe_heading, no_snipe_body, no_snipe_cmdname)
                return
            
            body = ""
            for message in reversed(messages):
                content = message.content[:1024]
                author = message.author.display_name
                body += f"\n{author}: {content}"
                count +=1
                if count == amount:
                    break
            
            heading = "Sniped Messages"
            cmdname = "SnipeMsg"
            await panelmaker(ctx, heading, body, cmdname)
        else:
            no_snipe_heading = "SnipeMsg"
            no_snipe_body = "There's nothing to snipe!"
            no_snipe_cmdname = "snipemsg"
            await panelmaker(ctx, no_snipe_heading, no_snipe_body, no_snipe_cmdname)
    except Exception as e:
        logging.error(f"Error in snipe command: {e}")

@Repent.command(aliases=['es', 'esnipe'], description=f"Snipes an edited message, Allows number of messages to be specified. \nUsage: {config_get('prefix')}editsnipe [Amount]", help="utility")
async def editsnipe(ctx, amount = 1):
    count = 0
    if amount > 5:
        amount = 5
    try:
        if ctx.channel.id in message_history["edited"]:
            edits = message_history["edited"][ctx.channel.id]
            if not edits:
                no_edit_snipe_heading = "EditSnipe"
                no_edit_snipe_body = "There's nothing to snipe!"
                no_edit_snipe_cmdname = "editsnipe"
                await panelmaker(ctx, no_edit_snipe_heading, no_edit_snipe_body, no_edit_snipe_cmdname)
                return
            
            body = ""
            for edit_info in reversed(edits):
                before_content = edit_info["before"].content[:1024]
                after_content = edit_info["after"].content[:1024]
                author = edit_info["before"].author.display_name
                body += f"\n{author}:\nBefore: {before_content}\nAfter: {after_content}"
                count +=1
                if count == amount:
                    break
            
            heading = "EditSniped Messages"
            cmdname = "EditSnipe"
            await panelmaker(ctx, heading, body, cmdname)
        else:
            no_edit_snipe_heading = "EditSnipe"
            no_edit_snipe_body = "There's nothing to snipe!"
            no_edit_snipe_cmdname = "editsnipe"
            await panelmaker(ctx, no_edit_snipe_heading, no_edit_snipe_body, no_edit_snipe_cmdname)
    except Exception as e:
        logging.error(f"Error in editsnipe command: {e}")

@Repent.command(description=f"Sets the amount of pings you have in a channel. \nUsage: {config_get('prefix')}setpings [amount of pings]", help="fun")
async def setpings(ctx, amount: int=9999):
    channel_id = ctx.channel.id
    thing = json.loads((await arequesters.get(f'https://canary.discord.com/api/v9/channels/{channel_id}/messages?limit=1', headers={'authorization': config_get('token')})).text)[0]
    j = (await arequesters.post(f'https://canary.discord.com/api/v9/channels/{channel_id}/messages/{thing["id"]}/ack', headers={'authorization': config_get('token')}, json_data={"manual":True,"mention_count":amount}))

soundlist = [
    {'id': '1', 'emoid': None, 'gid': None, 'emoname': '🦆'},
    {'id': '2', 'emoid': None, 'gid': None, 'emoname': '🔊'},
    {'id': '3', 'emoid': None, 'gid': None, 'emoname': '🦗'},
    {'id': '4', 'emoid': None, 'gid': None, 'emoname': '👏'},
    {'id': '5', 'emoid': None, 'gid': None, 'emoname': '🎺'},
    {'id': '6', 'emoid': None, 'gid': None, 'emoname': '🥁'},
]

def soundspammer():
    global soundspambool
    global stopper
    while True:
        if stopper == True:
            return
        if soundspambool:
            if currentvc:
                sound = random.choice(soundlist)
                soundid = sound['id']
                soundgid = sound['gid']
                soundemo = sound['emoid']
                soundemoname = sound['emoname']
                payload = {"sound_id":soundid,"emoji_id":soundemo}
                if soundemoname:
                    payload['emoji_name'] = soundemoname
                if soundgid:
                    payload['source_guild_id'] = soundgid
                url = f'https://discord.com/api/v9/channels/{currentvc}/send-soundboard-sound'
                requesters.post(url, headers={'authorization': config_get('token')}, json_data=payload)
        else: return
soundspambool = False

@Repent.command(description=f"Spams all possible soundboard sounds. \nUsage: {config_get('prefix')}soundspam", help="fun")
async def soundspam(ctx):
    heading = "Soundboard Spam"
    cmdname = "soundspam"
    if not currentvc:
            heading = "Error"
            body = "Please mute then unmute or rejoin vc then run the command again.\nOr join a vc if you're not in one."
            cmdname = "ERROR"
            await panelmaker(ctx, heading, body, cmdname)
            return
    global soundspambool
    if not soundspambool: 
        soundspambool = True
        body = "Starting soundspam"
        await panelmaker(ctx, heading, body, cmdname)
    else: 
        soundspambool = False
        body = 'Stopping soundspam'
        await panelmaker(ctx, heading, body, cmdname)
        return
    if len(soundlist) == 0: return
    for i in range(0, 10):
        threading.Thread(target=soundspammer).start()

@Repent.command(description=f"Bans any user who pings you in the server they pinged you from. \nUsage: {config_get('prefix')}userpingban", help="utility")
async def userpingban(ctx, user: discord.User):
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'userpingban' not in settings_data:
        settings_data['userpingban'] = []
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)

    if user.id in settings_data['userpingban']:
        settings_data['userpingban'].remove(user.id)  
        with open('Data/Settings/Configs/Settings.json', 'w') as file: 
            json.dump(settings_data, file, indent=4)
        heading = f"User Ping Ban"
        body = f"{user.name} removed from ping ban from all possible servers."
        cmdname = "userpingban"
    else:
        settings_data['userpingban'].append(user.id)
        with open('Data/Settings/Configs/Settings.json', 'w') as file:  
            json.dump(settings_data, file, indent=4)
        heading = f"User Ping Ban"
        body = f"{user.name} added to ping ban for all possible servers."
        cmdname = "userpingban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Bans a user who pings you in the server this commands was used in. \nUsage: {config_get('prefix')}serverpingban", help="utility")
async def serverpingban(ctx):
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'serverpingban' not in settings_data:
        settings_data['serverpingban'] = []
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)
    if ctx.guild.me.guild_permissions.ban_members:
        if ctx.guild.id in settings_data['serverpingban']:
            settings_data['serverpingban'].remove(ctx.guild.id)  
            with open('Data/Settings/Configs/Settings.json', 'w') as file: 
                json.dump(settings_data, file, indent=4)
            heading = f"Server Ping Ban"
            body = f"{ctx.guild.name} removed from ping ban list."
            cmdname = "serverpingban"
        else:
            settings_data['serverpingban'].append(ctx.guild.id)
            with open('Data/Settings/Configs/Settings.json', 'w') as file:  
                json.dump(settings_data, file, indent=4)
            heading = f"Server Ping Ban"
            body = f"{ctx.guild.name} added to ping ban list."
            cmdname = "serverpingban"
    else:
        heading = "Error"
        body = "You do not have ban permissions in this server."
        cmdname = "ERROR"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Kicks any user who pings you in the server this commands was used in. \nUsage: {config_get('prefix')}serverpingkick", help="utility")
async def serverpingkick(ctx):
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'serverpingkick' not in settings_data:
        settings_data['serverpingkick'] = []
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)
    if ctx.guild.me.guild_permissions.ban_members:
        if ctx.guild.id in settings_data['serverpingkick']:
            settings_data['serverpingkick'].remove(ctx.guild.id)  
            with open('Data/Settings/Configs/Settings.json', 'w') as file: 
                json.dump(settings_data, file, indent=4)
            heading = f"Server Ping Kick"
            body = f"{ctx.guild.name} removed from ping kick list."
            cmdname = "serverpingkick"
        else:
            settings_data['serverpingkick'].append(ctx.guild.id)
            with open('Data/Settings/Configs/Settings.json', 'w') as file:  
                json.dump(settings_data, file, indent=4)
            heading = f"Server Ping Kick"
            body = f"{ctx.guild.name} added to ping kick list."
            cmdname = "serverpingkick"
    else:
        heading = "Error"
        body = "You do not have kick permissions in this server."
        cmdname = "ERROR"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Kicks a user who pings you in the server they pinged you from. \nUsage: {config_get('prefix')}userpingkick", help="utility")
async def userpingkick(ctx, user: discord.User):
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'userpingkick' not in settings_data:
        settings_data['userpingkick'] = []
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)

    if user.id in settings_data['userpingkick']:
        settings_data['userpingkick'].remove(user.id)  
        with open('Data/Settings/Configs/Settings.json', 'w') as file: 
            json.dump(settings_data, file, indent=4)
        heading = f"User Ping Kick"
        body = f"{user.name} removed from ping kick from all possible servers."
        cmdname = "userpingkick"
    else:
        settings_data['userpingkick'].append(user.id)
        with open('Data/Settings/Configs/Settings.json', 'w') as file:  
            json.dump(settings_data, file, indent=4)
        heading = f"User Ping Kick"
        body = f"{user.name} added to ping kick for all possible servers."
        cmdname = "userpingkick"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Adds a channel to the message logging list. \nUsage: {config_get('prefix')}logchannel [channel id]", help="utility")
async def logchannel(ctx, id=None):
    if not isinstance(ctx.channel, discord.TextChannel) or not isinstance(ctx.channel, discord.VoiceChannel):
            heading = "Error"
            body = "Please either enter a channel id or use this command in a guild channel."
            cmdname = "ERROR"
            await panelmaker(ctx, heading, body, cmdname)
            return
    channel_id = int(id) if id else ctx.channel.id
    channel = Repent.get_channel(channel_id)   
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'msglogids' not in settings_data:
        settings_data['msglogids'] = []
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)

    if channel_id in settings_data['msglogids']:
        settings_data['msglogids'].remove(channel_id)  
        with open('Data/Settings/Configs/Settings.json', 'w') as file: 
            json.dump(settings_data, file, indent=4)
        heading = f"Channel Log"
        body = f"Stopped logging {channel.name}"
        cmdname = "logchannel"
    else:
        settings_data['msglogids'].append(channel_id)
        with open('Data/Settings/Configs/Settings.json', 'w') as file:  
            json.dump(settings_data, file, indent=4)
        heading = f"Channel Log"
        body = f"Now logging {channel.name}"
        cmdname = "logchannel"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Fetches and displays the first message sent in a channel or DM. \nUsage: {config_get('prefix')}firstmsg", panel="fun")
async def firstmsg(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.send(f"https://discord.com/channels/@me/{ctx.channel.id}/{message.id}")
            heading = "First DM Message"
            body = f"Author: {message.author.name}\nContent: {message.content}"
            cmdname = "firstmsg"
            await panelmaker(ctx, heading, body, cmdname)
    else:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.send(f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}")
            heading = "First Server Message"
            body = f"Author: {message.author.name}\nContent: {message.content}"
            cmdname = "firstmsg"
            await panelmaker(ctx, heading, body, cmdname)

def make_circle(img):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)

    out = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    out.putalpha(mask)
    return out

@Repent.command(description=f"Creates a gigachad image with a users profile picture. \nUsage: {config_get('prefix')}gigachad [@user]", help="fun")
async def gigachad(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    response = (await arequesters.get("https://assets.idlesys.xyz/assets/cf1803c7768ffbf8ed35493d3b5b2f36f309225b78e77f0f042b3f1e253925bd.png"))
    imge = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar = str(user.avatar.replace(format='png'))
    response = (await arequesters.get(avatar))
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    circular_img = make_circle(img)
    pfp = circular_img.resize((207, 194))
    imge.paste(pfp, (135, 40), pfp)
    final_image_bytes = io.BytesIO()
    imge.save(final_image_bytes, format="PNG")
    final_image_bytes.seek(0)
    await ctx.send(file=discord.File(final_image_bytes, "gigachad.png"))

@Repent.command(description=f"Creates a George Floyd image with 2 users profile pictures. \nUsage: {config_get('prefix')}derek <@user> <@user>", help="fun")
async def derek(ctx, user1: discord.User, user2: discord.User):
    response = (await arequesters.get("https://assets.idlesys.xyz/assets/25bc3b56c6a047658ed33c85e8ed6fc529adf1c84fbafe1ecb2e6dde5cc2238c.png"))
    imge = Image.open(BytesIO(response.content)).convert("RGBA")
    for user in [user1, user2]:
        avatar = str(user.avatar.replace(format='png'))
        response = (await arequesters.get(avatar))
        pfp = Image.open(BytesIO(response.content)).convert("RGBA")
        circular_pfp = make_circle(pfp)
        circular_pfp = circular_pfp.resize((80, 80))
        if user == user1:
            imge.paste(circular_pfp, (50, 0), circular_pfp)
        else:
            imge.paste(circular_pfp, (110, 290), circular_pfp)
    with BytesIO() as image_binary:
        imge.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='derek.png'))

@Repent.command(description=f"Creates an image of a profile picture on a nokia phone. \nUsage: {config_get('prefix')}nokia [@user]", help="fun")
async def nokia(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    response = (await arequesters.get("https://assets.idlesys.xyz/assets/a7bc85956bbb4baede7884904c77801d20e3faeeace28c9d4d8a62714b31d4c9.png"))
    img = Image.open(BytesIO(response.content))
    avatar = str(user.avatar.replace(format='png'))
    response = (await arequesters.get(avatar))
    pfp = Image.open(BytesIO(response.content)).convert("RGBA")
    pfp = pfp.resize((233, 171))
    img.paste(pfp, (65, 159))
    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='Nokia.png'))

@Repent.command(description=f"Creates a ps4 game cover using a profile picute. \nUsage: {config_get('prefix')}ps4cover [@user]", help="fun")
async def ps4cover(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    response = (await arequesters.get("https://assets.idlesys.xyz/assets/e2c248a2410c14b6bcf9ec19380eced69ff4e889939e4c7aa88aa88116b87d7a.png"))
    img = Image.open(BytesIO(response.content))
    avatar = str(user.avatar.replace(format='png'))
    response = (await arequesters.get(avatar))
    pfp = Image.open(BytesIO(response.content)).convert("RGBA")
    pfp = pfp.resize((1073, 1190))
    img.paste(pfp, (2, 180))
    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='PS4Cover.png'))

@Repent.command(description=f"Speechbubbles an image and sends it as a gif. \nUsage: {config_get('prefix')}sbubble <url/attachment>", help="fun")
async def sbubble(ctx, url: str = None):
    if url:
        response = (await arequesters.get(url))
    else:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            response = (await arequesters.get(attachment.url))
        else:
            heading = "Error"
            body = "Please provide an image URL or attach an image."
            cmdname = "ERROR"
            await panelmaker(ctx, heading, body, cmdname)
            return
    response.raise_for_status()
    image_bytes = io.BytesIO(response.content)
    image = Image.open(image_bytes).convert("RGBA")
    bubble_response = (await arequesters.get("https://assets.idlesys.xyz/assets/9f0442096eedc65e06031fd1aa454667f00768f48a490f3cdebf018aed2a6d2d.png"))
    bubble_response.raise_for_status()
    bubble_image_bytes = io.BytesIO(bubble_response.content)
    bubble_image = Image.open(bubble_image_bytes).convert("RGBA")
    bubble_width = image.width
    bubble_height = int((bubble_image.height / bubble_image.width) * bubble_width)
    bubble_height = min(bubble_height, image.height // 8)
    bubble_image = bubble_image.resize((bubble_width, bubble_height), Image.Resampling.LANCZOS)
    x = (image.width - bubble_image.width) // 2
    y = 0
    image.paste(bubble_image, (x, y), bubble_image)
    output_bytes = io.BytesIO()
    image.save(output_bytes, format='PNG')
    output_bytes.seek(0)
    await ctx.send(file=discord.File(output_bytes, filename='SBubble.gif'))

@Repent.command(description=f"Creates an image of a pfp doing a roman salute. \nUsage: {config_get('prefix')}salute [@user]", help="fun")
async def salute(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author
    avatar = str(user.avatar.replace(format='png'))
    response = (await arequesters.get("https://assets.idlesys.xyz/assets/6ea7cf38eedd664e57481c8a7388d7acf1ec3a280a6efa92ccf7f0f34d967a66.png"))
    base_image_bytes = io.BytesIO(response.content)
    imge = Image.open(base_image_bytes)
    avatar_response = (await arequesters.get(str(avatar)))
    avatar_image = Image.open(BytesIO(avatar_response.content)).convert("RGBA")
    avatar_size = (80, 80)
    avatar_image = avatar_image.resize(avatar_size)
    mask = Image.new("L", avatar_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=255)
    avatar_image.putalpha(mask)
    imge.paste(avatar_image, (144, 12), avatar_image)
    output_bytes = io.BytesIO()
    imge.save(output_bytes, format='PNG')
    output_bytes.seek(0)
    await ctx.send(file=discord.File(output_bytes, filename='salute.png'))

@Repent.command(description=f"Generates a unique username using discords username generation system. \nUsage: {config_get('prefix')}username", help="fun")
async def username(ctx):
    headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
    resp = (await arequesters.get("https://discord.com/api/v9/unique-username/username-suggestions-unauthed", headers=headers)).json()
    heading = "Unique Username"
    body = resp['username']
    cmdname = "username"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows your pc specs. \nUsage: {config_get('prefix')}specs", help="fun")
async def specs(ctx):
        platform_system = platform.system()
        platform_version = platform.version()
        cpu_info = cpuinfo.get_cpu_info()['brand_raw']
        cpu_MHz = cpuinfo.get_cpu_info()['hz_advertised_friendly']
        cpu_arc = cpuinfo.get_cpu_info()['arch']
        total_cores = psutil.cpu_count(logical=True)
        svmem = psutil.virtual_memory()
        total_memory = f"{svmem.total / (1024.0 **3):.2f} GB"
        gpus = GPUtil.getGPUs()
        sorted_gpus = sorted(gpus, key=lambda gpu: gpu.load, reverse=True)
        gpu = sorted_gpus[0]
        heading = "PC Specs"
        body = f"System: {platform_system}\nSystem Version: {platform_version}\nGPU: {gpu.name}\nGPU Vram: {gpu.memoryTotal} MB\nCPU: {cpu_info}\nCPU Cores: {total_cores}\nCPU MHz: {cpu_MHz}\nCPU Architecture: {cpu_arc}\nTotal RAM: {total_memory}"
        cmdname = "specs"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a CSS codeblock. \nUsage: {config_get('prefix')}css <text>", help="codeblock")
async def css(ctx, *, msg):    
    await ctx.send(f"```css\n{msg}\n```")

@Repent.command(description=f"Creates a BrainFuck codeblock. \nUsage: {config_get('prefix')}brainfuck <text>", help="codeblock")
async def brainfuck(ctx, *, msg):    
    await ctx.send(f"```brainfuck\n{msg}\n```")

@Repent.command(description=f"Creates a MD codeblock. \nUsage: {config_get('prefix')}md <text>", help="codeblock")
async def md(ctx, *, msg):    
    await ctx.send(f"```md\n{msg}\n```")

@Repent.command(description=f"Creates a Fix codeblock. \nUsage: {config_get('prefix')}fix <text>", help="codeblock")
async def fix(ctx, *, msg):    
    await ctx.send(f"```fix\n{msg}\n```")

@Repent.command(description=f"Creates a GLSL codeblock. \nUsage: {config_get('prefix')}glsl <text>", help="codeblock")
async def glsl(ctx, *, msg):    
    await ctx.send(f"```glsl\n{msg}\n```")

@Repent.command(description=f"Creates a Diff codeblock. \nUsage: {config_get('prefix')}diff <text>", help="codeblock")
async def diff(ctx, *, msg):    
    await ctx.send(f"```diff\n{msg}\n```")

@Repent.command(description=f"Creates a Bash codeblock. \nUsage: {config_get('prefix')}bash <text>", help="codeblock")
async def bash(ctx, *, msg):    
    await ctx.send(f"```bash\n{msg}\n```")

@Repent.command(description=f"Creates a C# codeblock. \nUsage: {config_get('prefix')}cs <text>", help="codeblock")
async def cs(ctx, *, msg):    
    await ctx.send(f"```cs\n{msg}\n```")

@Repent.command(description=f"Creates a C++ codeblock. \nUsage: {config_get('prefix')}cpp <text>", help="codeblock")
async def cpp(ctx, *, msg):    
    await ctx.send(f"```cpp\n{msg}\n```")

@Repent.command(description=f"Creates a Ini codeblock. \nUsage: {config_get('prefix')}ini <text>", help="codeblock")
async def ini(ctx, *, msg):    
    await ctx.send(f"```ini\n{msg}\n```")

@Repent.command(description=f"Creates an AsciiDoc codeblock. \nUsage: {config_get('prefix')}asciidoc <text>", help="codeblock")
async def asciidoc(ctx, *, msg):   
    await ctx.send(f"```asciidoc\n{msg}\n```")

@Repent.command(description=f"Creates an AutoHotKey codeblock. \nUsage: {config_get('prefix')}ahk <text>", help="codeblock")
async def ahk(ctx, *, msg):    
    await ctx.send(f"```autohotkey\n{msg}\n```")

@Repent.command(description=f"Creates a Python codeblock. \nUsage: {config_get('prefix')}python <text>", help="codeblock")
async def python(ctx, *, msg):    
    await ctx.send(f"```python\n{msg}\n```")

@Repent.command(description=f"Creates a Lua codeblock. \nUsage: {config_get('prefix')}lua <text>", help="codeblock")
async def lua(ctx, *, msg):    
    await ctx.send(f"```lua\n{msg}\n```")

@Repent.command(description=f"Creates a PHP codeblock. \nUsage: {config_get('prefix')}php <text>", help="codeblock")
async def php(ctx, *, msg):    
    await ctx.send(f"```php\n{msg}\n```")

@Repent.command(description=f"Creates a Rust codeblock. \nUsage: {config_get('prefix')}rust <text>", help="codeblock")
async def rust(ctx, *, msg):    
    await ctx.send(f"```rust\n{msg}\n```")

@Repent.command(description=f"Creates a Java codeblock. \nUsage: {config_get('prefix')}java <text>", help="codeblock")
async def java(ctx, *, msg):    
    await ctx.send(f"```java\n{msg}\n```")

@Repent.command(description=f"Creates a Kotlin codeblock. \nUsage: {config_get('prefix')}kotlin <text>", help="codeblock")
async def kotlin(ctx, *, msg):    
    await ctx.send(f"```kotlin\n{msg}\n```")

@Repent.command(description=f"Creates a JavaScript codeblock. \nUsage: {config_get('prefix')}js <text>", help="codeblock")
async def js(ctx, *, msg):    
    await ctx.send(f"```javascript\n{msg}\n```")

@Repent.command(description=f"Creates a MySql codeblock. \nUsage: {config_get('prefix')}mysql <text>", help="codeblock")
async def mysql(ctx, *, msg):   
    await ctx.send(f"```MySQL\n{msg}\n```")

@Repent.command(description=f"Creates a MarkDown codeblock. \nUsage: {config_get('prefix')}markdown <text>", help="codeblock")
async def markdown(ctx, *, msg):    
    await ctx.send(f"```markdown\n{msg}\n```")

@Repent.command(description=f"Creates a Ansi codeblock. \nUsage: {config_get('prefix')}ansi <text>", help="codeblock")
async def ansi(ctx, *, msg):    
    await ctx.send(f"```ansi\n{msg}\n```")

@Repent.command(description=f"Creates a CoffeeScript codeblock. \nUsage: {config_get('prefix')}coffeescript <text>", help="codeblock")
async def coffeescript(ctx, *, msg):    
    await ctx.send(f"```coffeescript\n{msg}\n```")

@Repent.command(description=f"Creates a HTML codeblock. \nUsage: {config_get('prefix')}html <text>", help="codeblock")
async def html(ctx, *, msg):    
    await ctx.send(f"```html\n{msg}\n```")

@Repent.command(description=f"Creates a Ruby codeblock. \nUsage: {config_get('prefix')}ruby <text>", help="codeblock")
async def ruby(ctx, *, msg):    
    await ctx.send(f"```ruby\n{msg}\n```")

@Repent.command(description=f"Creates a Go-lang codeblock. \nUsage: {config_get('prefix')}go <text>", help="codeblock")
async def go(ctx, *, msg):    
    await ctx.send(f"```go\n{msg}\n```")

@Repent.command(description=f"Creates a YAML codeblock. \nUsage: {config_get('prefix')}yaml <text>", help="codeblock")
async def yaml(ctx, *, msg):    
    await ctx.send(f"```yaml\n{msg}\n```")

@Repent.command(description=f"Creates a TypeScript codeblock. \nUsage: {config_get('prefix')}typescript <text>", help="codeblock")
async def typescript(ctx, *, msg):    
    await ctx.send(f"```typescript\n{msg}\n```")
