@Repent.command(description=f"Flips a coin and returns heads or tails. \nUsage: {config_get('prefix')}coinflip", help="fun")
async def coinflip(ctx):    
    coin = randint(1, 2)
    heading = "Coin Flip"
    cmdname = "coinflip"
    if coin == 1:
        body = "Heads"
    elif coin == 2:
        body = "Tails"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a wave of text. \nUsage: {config_get('prefix')}wave <text>", help="fun")
async def wave(ctx, *, sentence):
    spaces = 0
    string = ''
    max_length = 1500
    for _ in range(9):  
        for _ in range(5):
            string += f'{" " * spaces}{sentence}\n'
            spaces += 1
            if len(string) >= max_length:
                await ctx.send(string)
                string = ''
        for _ in range(5):
            spaces -= 1
            if spaces >= 0:
                string += f'{" " * spaces}{sentence}\n'
                if len(string) >= max_length:
                    await ctx.send(string)
                    string = ''
    if string:
        await ctx.send(string)

@Repent.command(description=f"Sends a random Netflix movie/series with details. \nUsage: {config_get('prefix')}randomnetflix", help="fun")
async def randomnetflix(ctx):    
    r = (await arequesters.get(f'https://api.reelgood.com/v3.0/content/random?availability=onAnySource&content_kind=both&nocache=true&region=de&sources=netflix'))
    jss = json.loads(r.text)
    title = jss['title']
    overview = jss['overview']
    releasedate = jss['released_on']
    releasedate = releasedate.split('T')[0]
    releasedate = releasedate.split('-')
    year = releasedate[0]
    month = releasedate[1]
    day = releasedate[2]
    tagline = jss['tagline']
    yozaid = jss['id']
    if tagline == '':
        tagline = 'No tagline for this movie ):'
    else:
        pass
    heading = "Random Netflix"
    body = f"Title: {title}\nTagline: {tagline}\nDescription: {overview}\nRelease Date: {day}\\{month}\\{year}"
    cmdname = "randommovie"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(aliases=['atv'], description=f"Converts audio into a voice message. \nUsage: {config_get('prefix')}audiotovoice <link/attached audio>", help="fun")             
async def audiotovoice(ctx, *, filepath_url = None):
    async def convtoopus(file):
        json_data = {
            'targetformat': 'opus',
            'audiobitratetype': '0',
            'customaudiobitrate': '',
            'audiosamplingtype': '0',
            'customaudiosampling': '',
            'code': '82000',
            'oAuthToken': '',
            'legal': 'Our PHP programs can only be used in aconvert.com. We DO NOT allow using our PHP programs in any third-party websites, software or apps. We will report abuse to your cloud provider, Google Play and App store if illegal usage found!'
        }

        files=[
        ('file',('4883.MP4',file,'application/octet-stream'))
        ]

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://www.aconvert.com',
            'Referer': 'https://www.aconvert.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        e = requested.post("https://s31.aconvert.com/convert/convert9.php", data=json_data, headers=headers, files=files).json()
        server = e['server']
        filename = e['filename']
        opus = requested.get(f"https://s{server}.aconvert.com/convert/p3r68-cdx67/{filename}")
        return opus.content

    try:
        file_url = None
        filepath = None
        if not filepath_url:
            if ctx.message.attachments:
                file_url = ctx.message.attachments[0].url
            else:
                header = "Error"
                body = "No attachment or URL provided."
                cmdname = "ERROR"
                await panelmaker(ctx, heading=header, body=body, cmdname=cmdname)
                return
        elif filepath_url.startswith('https://'):
            file_url = filepath_url
        else:
            filepath = filepath_url
        
        file_content = None
        if file_url:
            response = (await arequesters.get(file_url))
            if response.status_code == 200:
                file_content = response.content
            else:
                header = "Error"
                body = "Failed to fetch the file from the URL.\nTry uploading file normally and using the link."
                cmdname = "ERROR"
                await panelmaker(ctx, heading=header, body=body, cmdname=cmdname)
                return
        elif filepath:
            with open(filepath, 'rb') as file:
                file_content = file.read()
        
        voicefile = await convtoopus(file_content)
        filesize = len(voicefile)
        
        headers = {
            "Content-Length": str(filesize),
            "User-Agent": "Discord/42954 CFNetwork/1390 Darwin/22.0.0",
            "Authorization": config_get('token'),
            "x-debug-options": "bugReporterEnabled",
            "Accept-Language": "en-NZ",
            "x-discord-locale": "en-US",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "x-super-properties": getxsuper()
        }

        rbody = {
            "files": [{"file_size": filesize, "filename": "voice-message.ogg", "id": "69"}]
        }
        firstreq = requested.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/attachments', headers=headers, json=rbody)
        firstreq_data = firstreq.json()
        
        uploadname = firstreq_data['attachments'][0]["upload_filename"]
        uploadurl = firstreq_data['attachments'][0]["upload_url"]
        print(uploadurl)
        
        upload_headers = {
            "Host": "discord-attachments-uploads-prd.storage.googleapis.com",
            "Accept-Language": "en-NZ,en-AU;q=0.9,en;q=0.8",
            "User-Agent": "Discord/42954 CFNetwork/1390 Darwin/22.0.0",
            "Content-Type": "audio/ogg",
            "Connection": "keep-alive",
            "Content-Length": str(filesize)
        }
        
        upload_response = requested.put(uploadurl, data=voicefile, headers=upload_headers)
        
        msgdata = {
            "channel_id": ctx.channel.id,
            "flags": 8192,
            "content": "",
            "nonce": "",
            "type": 0,
            "attachments": [{
                "id": "0",
                "filename": "voice-message.ogg",
                "uploaded_filename": uploadname,
                "duration_secs": 0,
                "waveform": ""
            }]
        }
        final_response = requested.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages', headers=headers, json=msgdata)
    except Exception as e:
        print(e)
        

@Repent.command(description=f"Creates an among us emergency meeting screen. \nUsage: {config_get('prefix')}emergencymeeting <text>", help="fun")
async def emergencymeeting(ctx, *, text):    
    await apiimg(ctx,(urlify(f"https://vacefron.nl/api/emergencymeeting?text={text}")))

@Repent.command(description=f"Creates an among us ejected screen. \nUsage: {config_get('prefix')}ejected <name>", help="fun")
async def ejected(ctx, *, name):    
    a = ["true", "false"]
    b = ["black", "blue", "brown", "cyan", "darkgreen", "lime", "orange", "pink", "purple", "red", "white", "yellow"]
    imposter = random.choice(a)
    colour = random.choice(b)
    if colour == "red":
        imposter = "true"
    url = f'https://vacefron.nl/api/ejected?name={name}&impostor={imposter}&crewmate={colour}'
    await apiimg(ctx, url)

@Repent.command(description=f"Widens a user's pfp. \nUsage: {config_get('prefix')}wide <@user>", help="fun")
async def wide(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author
    av = user.avatar.replace(format="png", size=1024)
    url = f"https://vacefron.nl/api/wide?image={av}"
    await apiimg(ctx, url)

@Repent.command(description=f"Creates a wanted poster. \nUsage: {config_get('prefix')}wanted <@user>", help="fun")
async def wanted(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author
    av = user.avatar.replace(format="png", size=1024)
    url = f'https://api.popcat.xyz/wanted?image={av}'
    await apiimg(ctx, url)

@Repent.command(description=f"Makes a user's pfp hold the chat at gun-point. \nUsage: {config_get('prefix')}gunpoint <@user>", help="fun")
async def gunpoint(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author
    av = user.avatar.replace(format="png", size=1024)
    url = f'https://api.popcat.xyz/gun?image={av}'
    await apiimg(ctx, url)

@Repent.command(description=f"Makes a fake iPhone emergency alert notification. \nUsage: {config_get('prefix')}iphonealert <text>", help="fun")
async def iphonealert(ctx, *, msg):    
    url = f'https://api.popcat.xyz/alert?text={msg}'
    await apiimg(ctx, url)

@Repent.command(description=f"Makes someone's pfp drippy. \nUsage: {config_get('prefix')}drippy <@user>", help="fun")
async def drippy(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author
    av = user.avatar.replace(format="png", size=1024)
    url = f'https://api.popcat.xyz/drip?image={av}'
    await apiimg(ctx, url)

@Repent.command(description=f"Makes a who would win table. \nUsage: {config_get('prefix')}whowouldwin <@user1> <@user2>", help="fun")
async def whowouldwin(ctx, user1: discord.User, user2: discord.User):   
    av1 = user1.avatar.replace(format="png", size=1024)
    av2 = user2.avatar.replace(format="png", size=1024)
    url = f'https://api.popcat.xyz/whowouldwin?image2={av2}&image1={av1}'
    await apiimg(ctx, url)

@Repent.command(description=f"Determines how gay someone is. \nUsage: {config_get('prefix')}gayrate <@user>", help="fun")
async def gayrate(ctx, member: discord.User=None):    
    if member is None:
        member = ctx.message.author
    percent = randint(1,100)
    await ctx.send(f"```{member} is {percent}% gay```")

@Repent.command(description=f"Determines if someone is lying or not. \nUsage: {config_get('prefix')}liedetector <@user>", help="fun")
async def liedetector(ctx, member: discord.User=None):    
    if member is None:
        member = ctx.message.author
    choice = ["is", "is not"]
    choi = random.choice(choice)
    await ctx.send(f"```{member} {choi} lying```")

@Repent.command(description=f"Sends a random and useless fact. \nUsage: {config_get('prefix')}uselessfact", help="fun")
async def uselessfact(ctx):    
    r = (await arequesters.get('https://uselessfacts.jsph.pl/random.json?language=en'))
    r = r.json()
    fact = r['text']
    heading = "Useless Fact"
    body = fact
    cmdname = "uselessfact"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Shows information on a pokemon. \nUsage: {config_get('prefix')}pokedex <pokemon>", help="fun")
async def pokedex(ctx, pokemon):    
    poke = urllib.parse.quote(pokemon)
    r = (await arequesters.get(f'https://pokeapi.co/api/v2/pokemon/{poke.lower()}'))
    r = r.json()
    poke = r['name']
    dex = r['id']
    type = r['types'][0]["type"]["name"]
    hp = r["stats"][0]["base_stat"]
    att = r["stats"][1]["base_stat"]
    deff = r["stats"][2]["base_stat"]
    spatk = r["stats"][3]["base_stat"]
    spdef = r["stats"][4]["base_stat"]
    spd = r["stats"][5]["base_stat"]
    heading = f"Pokedex Entry of {poke}"
    body = f"ID: {dex}\nType: {type}\nHealth: {hp}\nAttack: {att}\nDefense: {deff}\nSpAttack: {spatk}\nSpDefnse: {spdef}\nSpeed: {spd}"
    cmdname = "pokedex"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Overlays the gay flag on someone's pfp. \nUsage: {config_get('prefix')}gayoverlay <@user>", help="fun")
async def gayoverlay(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    url = f'https://some-random-api.com/canvas/gay?avatar={user.avatar.replace(format="png")}'
    await apiimg(ctx, url)

@Repent.command(description=f"Creates a horny license. \nUsage: {config_get('prefix')}hornycard <@user>", help="fun")
async def hornycard(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author          
    url = f'https://some-random-api.com/canvas/horny?avatar={user.avatar.replace(format="png")}'
    await apiimg(ctx, url)

@Repent.command(description=f"Creates a simp card. \nUsage: {config_get('prefix')}simpcard <@user>", help="fun")
async def simpcard(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author    
    url = f'https://some-random-api.com/canvas/simpcard?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Says a random insult to a user. \nUsage: {config_get('prefix')}insult <@user>", help="fun")
async def insult(ctx, user: discord.User=None):
    if user == None:
        user = ctx.message.author   
    insult = (await arequesters.get("https://insult.mattbas.org/api/insult")).text
    await ctx.send(f"<@{user.id}>, {insult}")

@Repent.command(description=f"Sends a custom Minecraft achievement. \nUsage: {config_get('prefix')}mcachievement <title> <text>", help="fun") 
async def mcachievement(ctx, title: str, text: str):   
    url = urlify(f"https://skinmc.net/achievement/1/{title}/{text}")
    await apiimg(ctx, url)

@Repent.command(description=f"Sends a random quote from Kanye West. \nUsage: {config_get('prefix')}kanyequote", help="fun")
async def kanyequote(ctx):    
    r = (await arequesters.get('https://api.kanye.rest/'))
    r = r.json()
    quote = r['quote']
    heading = "Kanye Quote"
    body = quote
    cmdname = "kanyequote"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Flips text upside down. \nUsage:{config_get('prefix')}flip <text>", help="fun")
async def flip(ctx, *, message):    
    char_list = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}"
    alt_char_list = "{|}zʎxʍʌnʇsɹbdouɯlʞɾᴉɥƃɟǝpɔqɐ,‾^[\\]Z⅄XMΛ∩┴SɹQԀONW˥ʞſIHפℲƎpƆq∀@¿<=>;:68ㄥ9ϛㄣƐᄅƖ0/˙-'+*(),⅋%$#¡"[::-1]
    text_flip = dict(zip(char_list + alt_char_list, alt_char_list + char_list))
    result = "".join(text_flip.get(char, char) for char in message[::-1])
    await ctx.send(result)

@Repent.command(description=f"Impersonates someone using webhooks. \nUsage:{config_get('prefix')}impersonate <@user> <text>", help="fun")
async def impersonate(ctx, member: discord.Member, *, message):
    avatar = member.avatar.replace(format='png', size=256)
    pfp = (await arequesters.get(avatar)).content
    hook = await ctx.channel.create_webhook(name=member.display_name, avatar=pfp)
    await hook.send(message)
    await hook.delete()

@Repent.command(description=f"Displays a random number of a dice (numbers 1-6). \nUsage: {config_get('prefix')}dice", help="fun")
async def dice(ctx):    
    heading = "Dice Roll"
    body = f"You rolled a {random.randrange(1, 6)}!"
    cmdname = "dice"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a stickbug meme from someone's pfp. \nUsage: {config_get('prefix')}stickbug <@user>", help="fun")
async def stickbug(ctx, user: discord.User = None):    
    user = user or ctx.author
    url = (await arequesters.get(f"https://nekobot.xyz/api/imagegen?type=stickbug&url={str(user.avatar).replace('', 'png')}")).json()['message']
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_data = io.BytesIO(await response.read())
            await ctx.send(file=discord.File(image_data, f'Repent_Stickbug.mp4'))

@Repent.command(description=f"Displays a user's dick size. \nUsage: {config_get('prefix')}dick <@user>", help="fun")
async def dick(ctx, *, user: discord.User = None): 
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    heading = f"{user.name}'s Dick Size"
    body = f"8{dong}D"
    cmdname = "dick"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays a cum animation. \nUsage: {config_get('prefix')}cum", help="fun")
async def cum(ctx):   
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:=D
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D
             :trumpet:      :eggplant:
             ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant:
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    
@Repent.command(description=f"Displays a 9/11 animation. \nUsage: {config_get('prefix')}nineeleven", help="fun")
async def nineeleven(ctx):   
    nineleven = await ctx.send(":airplane:** ** ** ** ** ** ** **:office::office:")
    await asyncio.sleep(1)
    await nineleven.edit(content=":airplane:** ** ** ** ** **:office::office:")
    await asyncio.sleep(1)
    await nineleven.edit(content=":airplane:** ** ** **:office::office:")
    await asyncio.sleep(1)
    await nineleven.edit(content=":airplane:** **:office::office:")
    await asyncio.sleep(1)
    await nineleven.edit(content=":airplane::office::office:")
    await asyncio.sleep(1)
    await nineleven.edit(content=":fire::fire::fire:")

@Repent.command(name='8ball', description=f"Answers a question like a magic 8ball. \nUsage: {config_get('prefix')}8ball <question>", help="fun")
async def _ball(ctx, *, question):    
    responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'That is a definite yes!',
        'Maybe',
        'There is a good chance',
        'Yes.'
    ]
    answer = random.choice(responses)
    heading = "Magic 8 Ball"
    body = f"Question: {question}\nAnswer: {answer}"
    cmdname = "8ball"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays a tweet as if you were another discord user. \nUsage: {config_get('prefix')}tweet @user (text)", help="fun")
async def tweet(ctx, username: str, *, message: str):     
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}"
    await apiimg(ctx, url)

@Repent.command(description=f"Combines 2 words. \nUsage: {config_get('prefix')}combine <word1> <word2>", help="fun")
async def combine(ctx, name1, name2):     
    name1letters = name1[:round(len(name1) / 2)]
    name2letters = name2[round(len(name2) / 2):]
    ship = "".join([name1letters, name2letters])   
    heading = "Combine"
    body = f"{name1}+{name2}\n\n{ship}"
    cmdname = "combine"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a lenny face. \nUsage: {config_get('prefix')}lenny", help="fun")
async def lenny(ctx):    
    lenny = '( ͡° ͜ʖ ͡°)'
    await ctx.send(lenny)

@Repent.command(aliases=['wouldyourather'], description=f"Displays a would you rather question. \nUsage: {config_get('prefix')}wyr", help="fun")
async def wyr(ctx):    
    r = (await arequesters.get('https://www.conversationstarters.com/wyrqlist.php')).text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qor = soup.find(id='qor').text
    qb = soup.find(id='qb').text
    heading = "Would You Rather"
    body = f"{qa}\n{qor}\n{qb}"
    cmdname = "wyr"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"sends a random topic. \nUsage: {config_get('prefix')}topic", help="fun")
async def topic(ctx):     
    r = (await arequesters.get('https://www.conversationstarters.com/generator.php')).content
    soup = bs4(r, 'html.parser')
    topic = soup.find(id="random").text
    heading = "Random Topic"
    body = topic
    cmdname = "topic"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a random dad joke. \nUsage: {config_get('prefix')}joke", help="fun")
async def joke(ctx):     
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession()as session:
        async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
            r = await req.json()
    heading = "Dad Joke"
    body = r['joke']
    cmdname = "joke"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a random dark joke. \nUsage: {config_get('prefix')}darkjoke", help="fun")
async def darkjoke(ctx):      
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Dark", headers=headers) as req:
            r = await req.json()
    if 'setup' in r:
        heading = "Dark Joke"
        body = f"{r['setup']}\n{r['delivery']}"
        cmdname = "darkjoke"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "Dark Joke"
        body = f"{r['joke']}"
        cmdname = "darkjoke"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Displays a virus animation. \nUsage: {config_get('prefix')}virus", help="fun")
async def virus(ctx):    
    virus = await ctx.send("``[▓▓▓                    ] / Ched-virus.exe Packing files.``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓                ] - Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \\ Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \\ Ched-virus.exe Packing files..``")
    await asyncio.sleep(1)
    await virus.edit(content="``Successfully downloaded Ched-virus.exe``")
    await asyncio.sleep(1)
    await virus.edit(content="``Injecting virus.   |``")
    await asyncio.sleep(1)
    await virus.edit(content="``Injecting virus..  /``")
    await asyncio.sleep(1)
    await virus.edit(content="``Injecting virus... -``")
    await asyncio.sleep(1)
    await virus.edit(content=f"``Successfully Injected Ched-virus.exe into {Repent.user.name}``")
    await asyncio.sleep(1)
    await virus.edit(content=f"``Goodbye {Repent.user.name}``")
    await asyncio.sleep(1)
    subprocess.run(["taskkill", "/f", "/im", "Discord.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

@Repent.command(description=f"Makes a user's pfp funky. \nUsage: {config_get('prefix')}magik <@user>", help="fun")
async def magik(ctx, user: discord.User = None):    
    endpoint = "https://nekobot.xyz/api/imagegen?type=magik&intensity=3&image="
    if user is None:
        user = ctx.message.author
    avatar = str(user.avatar.replace(format="png"))
    endpoint += avatar
    r = (await arequesters.get(endpoint))
    res = r.json()
    await apiimg(ctx, res["message"])

@Repent.command(description=f"Makes a user's pfp deepfried. \nUsage: {config_get('prefix')}fry <@user>", help="fun")
async def fry(ctx, user: discord.User = None):    
    endpoint = "https://nekobot.xyz/api/imagegen?type=deepfry&image="
    if user is None:
        user = ctx.message.author
    avatar = str(user.avatar.replace(format="png"))
    endpoint += avatar
    r = (await arequesters.get(endpoint))
    res = r.json()
    await apiimg(ctx, res["message"])

@Repent.command(description=f"Changes the colors of a user's pfp. \nUsage: {config_get('prefix')}blurpify <@user>", help="fun")
async def blurpify(ctx, user: discord.User = None):    
    endpoint = "https://nekobot.xyz/api/imagegen?type=blurpify&image="
    if user is None:
        user = ctx.message.author
    avatar = str(user.avatar.replace(format="png"))
    endpoint += avatar
    r = (await arequesters.get(endpoint))
    res = r.json()
    await apiimg(ctx, res["message"])

@Repent.command(description=f"Creates a custom hub comment. \nUsage: {config_get('prefix')}phc [@user] <text>", help="fun")
async def phc(ctx, user: discord.User=None, *, args=None):    
    if user == None:
        user = ctx.message.author
    elif args == None:
        args = "You forgot to put a comment dummy"
    args = urlify(args)
    pfp = user.avatar.replace(format="png", size=1024)
    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={args}&username={user.name}&image={pfp}"
    r = (await arequesters.get(endpoint))
    res = r.json()
    await apiimg(ctx, res["message"])

@Repent.command(description=f"Sends a photo of a dog. \nUsage: {config_get('prefix')}dog", help="fun")
async def dog(ctx):    
    r = (await arequesters.get("https://dog.ceo/api/breeds/image/random")).json()
    link = str(r['message'])
    await apiimg(ctx, link)

@Repent.command(description=f"Sends a photo of a cat. \nUsage: {config_get('prefix')}cat", help="fun")
async def cat(ctx):    
    r = (await arequesters.get("https://api.thecatapi.com/v1/images/search")).json()
    link = str(r[0]["url"])
    await apiimg(ctx, link)

@Repent.command(description=f"Sends a game of minesweeper. \nUsage: {config_get('prefix')}minesweeper [number of mines] [gridsize]", help="fun")
async def minesweeper(ctx, mines_number: int = 10, size: int = 5):    
    MINE = ':boom:'
    NUMBERS = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:']
    SPOILER = '||'
    response = ''
    if size <= 0 or size > 12:
        response = "Please Pick a number between 1 and 12"
    else:
        grid = [None] * (size * size)
        for mine in range(mines_number):
            grid[random.randrange(0, len(grid))] = MINE
        for case in range(len(grid)):
            if grid[case] != MINE:
                number = sum(
                    grid[cursor] == MINE
                    for cursor in [
                        case - size - 1, case - size, case - size + 1,
                        case - 1, case + 1,
                        case + size - 1, case + size, case + size + 1
                    ]
                    if 0 <= cursor < len(grid)
                )
                grid[case] = NUMBERS[number]
        for line in range(size):
            line_value = ''.join(f'{SPOILER}{grid[line * size + case]}{SPOILER}' for case in range(size))
            response += f"{line_value}\n"
    await ctx.send(response)

@Repent.command(description=f"Reverses text. \nUsage: {config_get('prefix')}reverse <text>", help="fun")
async def reverse(ctx, *, message):    
    message = message[::-1]
    await ctx.send(message)

@Repent.command(description=f"Sends a fuck you emoji. \nUsage: {config_get('prefix')}fuckyou", help="fun")
async def fuckyou(ctx):        
        await ctx.send("╭∩╮(･◡･)╭∩╮")

@Repent.command(description=f"Encrypts a message. \nUsage: {config_get('prefix')}encrypt <text>", help="fun")
async def encrypt(ctx, *, text):        
        to_morse = {
        ' ': 'ᛝᧀಣಱಣಱᛥಉᛝᥪಣಱಣಱᧀᔑ',
        'a': 'ᥪಣಱᧀ',
        'b': 'ᣠಣಱᢩಣಱ',
        'c': 'ᛥᛝ',
        'd': 'ಉಣಱ',
        'e': 'ᚰಣಱᚸಣಱᚹ',
        'f': 'ᒴᒰ',
        'g': 'ϖ',
        'h': 'ლಣಱქ',
        'i': 'ᔑΩᔑ',
        'j': 'ΩᔑΩ',
        'k': 'ၸၴ',
        'l': 'ၡ',
        'm': 'ႁၡ',
        'n': 'ႰႤ',
        'o': 'ჰწჯ',
        'p': 'ᛠᛩ',
        'q': 'ᛠߐᢂᢂᢂᢂ',
        'r': 'ᛤᛟᛮ',
        's': 'ᖸᗱ',
        't': '⏇⏅⏆',
        'u': 'ϧ⏁⏇',
        'v': '⏂⏁',
        'w': '₶⊡',
        'x': 'ᾣ‿',
        'y': 'ᢆᢂ',
        'z': 'ᣆᣂ',
        '1': '⏂',
        '2': 'ᣆ',
        '3': 'ᢂᢂᢂᢂᢂᢂ',
        '4': '⏅ᢂᢂᢂᢂᢂ',
        '5': 'ᗱᗱEᗱ',
        '6': 'ᢆᗱ⏅',
        '7': 'ϧ⏅ლᗱ',
        '8': '⊡⊡⊡⊡⏅⏅ლ',
        '9': '⏇⏇ߐ',
        '0': 'ႁoႁ',
        ',': 'ϖ⊡',
        '!': 'ၸၴ⊡',
        '.': 'ჯწ',
        '?': 'წ⏇',
        '-': '⏇ϧ⏅',
        '#': '⊡⏅ლ',
        '@': 'ᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂ',
        '*': '42',
        '"': '⏅ლၸၴ⊡ᢂᢂ',
        "'": "ၸၴᢂᢂᢂ"
        }
        output = ""
        text = list(text.lower())
        for letter in text:
            if letter in to_morse:
                output = output + to_morse[letter] + " "
            else:
                output = output + letter
        await ctx.send(output)

@Repent.command(description=f"Decrypts a message that was encrypted by another Repent user. \nUsage: {config_get('prefix')}decrypt <encrypted text>", help="fun")
async def decrypt(ctx, *, text):    
    to_morse = {
        ' ': 'ᛝᧀಣಱಣಱᛥಉᛝᥪಣಱಣಱᧀᔑ',
        'a': 'ᥪಣಱᧀ',
        'b': 'ᣠಣಱᢩಣಱ',
        'c': 'ᛥᛝ',
        'd': 'ಉಣಱ',
        'e': 'ᚰಣಱᚸಣಱᚹ',
        'f': 'ᒴᒰ',
        'g': 'ϖ',
        'h': 'ლಣಱქ',
        'i': 'ᔑΩᔑ',
        'j': 'ΩᔑΩ',
        'k': 'ၸၴ',
        'l': 'ၡ',
        'm': 'ႁၡ',
        'n': 'ႰႤ',
        'o': 'ჰწჯ',
        'p': 'ᛠᛩ',
        'q': 'ᛠߐᢂᢂᢂᢂ',
        'r': 'ᛤᛟᛮ',
        's': 'ᖸᗱ',
        't': '⏇⏅⏆',
        'u': 'ϧ⏁⏇',
        'v': '⏂⏁',
        'w': '₶⊡',
        'x': 'ᾣ‿',
        'y': 'ᢆᢂ',
        'z': 'ᣆᣂ',
        '1': '⏂',
        '2': 'ᣆ',
        '3': 'ᢂᢂᢂᢂᢂᢂ',
        '4': '⏅ᢂᢂᢂᢂᢂ',
        '5': 'ᗱᗱEᗱ',
        '6': 'ᢆᗱ⏅',
        '7': 'ϧ⏅ლᗱ',
        '8': '⊡⊡⊡⊡⏅⏅ლ',
        '9': '⏇⏇ߐ',
        '0': 'ႁoႁ',
        ',': 'ϖ⊡',
        '!': 'ၸၴ⊡',
        '.': 'ჯწ',
        '?': 'წ⏇',
        '-': '⏇ϧ⏅',
        '#': '⊡⏅ლ',
        '@': 'ᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂᢂ',
        '*': '42',
        '"': '⏅ლၸၴ⊡ᢂᢂ',
        "'": "ၸၴᢂᢂᢂ"
        }
    text += ' '
    decipher = ''
    cipher = ''
    for letter in text:
        if letter != ' ':
            i = 0
            cipher += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(to_morse.keys())[list(to_morse.values()).index(cipher)]
                cipher = ''
    await ctx.send(f"{decipher}")

@Repent.command(description=f"Animates text. \nUsage: {config_get('prefix')}animate <text>", help="fun")
async def animate(ctx, *, text):        
        output = ""
        text = list(text)
        msg = await ctx.send(text[0])
        for letter in text:
            output = output + letter + ""
            await msg.edit(content=output)
            await asyncio.sleep(0.5)

@Repent.command(description=f"Animates text. \nUsage: {config_get('prefix')}animate <text>", help="fun")
async def emojify(ctx, *, text):        
        text = text.lower()
        regional_indicators = {
        'a': '<:regional_indicator_a:803940414524620800>',
        'b': '<:regional_indicator_b:803940414524620800>',
        'c': '<:regional_indicator_c:803940414524620800>',
        'd': '<:regional_indicator_d:803940414524620800>',
        'e': '<:regional_indicator_e:803940414524620800>',
        'f': '<:regional_indicator_f:803940414524620800>',
        'g': '<:regional_indicator_g:803940414524620800>',
        'h': '<:regional_indicator_h:803940414524620800>',
        'i': '<:regional_indicator_i:803940414524620800>',
        'j': '<:regional_indicator_j:803940414524620800>',
        'k': '<:regional_indicator_k:803940414524620800>',
        'l': '<:regional_indicator_l:803940414524620800>',
        'm': '<:regional_indicator_m:803940414524620800>',
        'n': '<:regional_indicator_n:803940414524620800>',
        'o': '<:regional_indicator_o:803940414524620800>',
        'p': '<:regional_indicator_p:803940414524620800>',
        'q': '<:regional_indicator_q:803940414524620800>',
        'r': '<:regional_indicator_r:803940414524620800>',
        's': '<:regional_indicator_s:803940414524620800>',
        't': '<:regional_indicator_t:803940414524620800>',
        'u': '<:regional_indicator_u:803940414524620800>',
        'v': '<:regional_indicator_v:803940414524620800>',
        'w': '<:regional_indicator_w:803940414524620800>',
        'x': '<:regional_indicator_x:803940414524620800>',
        'y': '<:regional_indicator_y:803940414524620800>',
        'z': '<:regional_indicator_z:803940414524620800>'
        }
        output = ""
        text = list(text)
        for letter in text:
            if letter in regional_indicators:
                output = output + regional_indicators[letter] + " "
            else:
                output = output + letter
        await ctx.send(output)

@Repent.command(description=f"Turns text into zalgo. \nUsage: {config_get('prefix')}zalgo <text>", help="fun")
async def zalgo(ctx, *, text):       
        text = text.lower()
        regional_indicators = {
        'a': 'ą̸͖͈̟̗͉̪̠̎̀̓͘',
        'b': 'b̵̨̩͍͇̻̪̖̟̭͒͊',
        'c': 'ç̴̧̻̩͎̳̮̼̪̥̠̬̀̎́',
        'd': 'ḑ̸̛̱̥̯͔̻̮̘͎̱̻͙͇͕̉̈͂̐͑͗̓̉̄͌̑̉͂',
        'e': 'ë̵̩͇̪̪̣́̒',
        'f': 'f̴̥̗̲̻̭̩̲̬̦̖͖̏͂̆͋̾̕͠',
        'g': 'g̶͂̍̈̒̍̔͌͛̅͠ͅ',
        'h': 'h̵̤͊̌̇̉̈́̎̔͑̈͘',
        'i': 'i̶̧̢̼̭̱̼̪̪͈͔͙͓͈̰͔̋̏',
        'j': 'j̸̛̫̠̞̦̳̬̼̲͐̄̓͂̈́̐̆͊̑̕̚͜ͅ',
        'k': 'k̶̢̧͎͖̗͙̳̞͎̣͖̬͚̀̈́̍̌̓̿̈́̍͆͗',
        'l': 'l̴̛̫͎͊̿̌͜',
        'm': 'ḿ̴̩͉̫̫̉̏̏̉',
        'n': 'n̵̗̖̳̝̳̯̳͋̐̄̆͌̓̀̇̿̌͌̒̕̕͠',
        'o': 'o̵̡̢̦̘̜͍͛',
        'p': 'p̴̹̺͔͎̖̥͊̂̈́̉',
        'q': 'q̶̢͚͕̥̱̹̙̿̎̉̓̊',
        'r': 'r̶̺̥̀̃',
        's': 's̶͖̀́̆',
        't': 't̵̖̪͔̠̃͑̉',
        'u': 'u̴͔̟͌̈́̈́̈́̚͠',
        'v': 'v̵͉̂̚',
        'w': 'ẃ̷̛͚̭͍̺̖̈́',
        'x': 'x̸͍͌̌͜͜',
        'y': 'y̶̨͓͈̔̎̋',
        'z': 'z̸̨̹̜̅̿̌̈͘͜͜'
        }
        output = ""
        text = list(text)
        for letter in text:
            if letter in regional_indicators:
                output = output + regional_indicators[letter] + " "
            else:
                output = output + letter
        await ctx.send(output)

@Repent.command(description=f"Searches for a gif. \nUsage: {config_get('prefix')}gif <query>", help="fun")
async def gif(ctx, query=None):   
    if query is None:
        r = (await arequesters.get("https://api.giphy.com/v1/gifs/random?api_key=ldQeNHnpL3WcCxJE1uO8HTk17ICn8i34&tag=&rating=R"))
        res = r.json()
        await ctx.send(res['data']['url'])
    else:
        r = (await arequesters.get(f"https://api.giphy.com/v1/gifs/search?api_key=ldQeNHnpL3WcCxJE1uO8HTk17ICn8i34&tag=&rating=R&q={query}"))
        res = r.json()
        gif_data = res['data'][0]
        await ctx.send(gif_data['url'])

@Repent.command(description=f"Counts up to a specified number. \nUsage: {config_get('prefix')}countto [number]", help="fun")
async def countto(ctx, number: int=10):    
    for count in range(number):
        await ctx.send(count)
        time.sleep(2)

@Repent.command(description=f"Sends horseplinko. \nUsage: {config_get('prefix')}horseplinko", help="fun")
async def horseplinko(ctx):    
    await ctx.send("https://Repent.eintim.me/content/cdn/EbCsJrPLDBdV.gif")
    await ctx.send("https://Repent.eintim.me/content/cdn/vUYtfSGaVkIY.gif")
    await ctx.send("https://Repent.eintim.me/content/cdn/hOrCbSsqYVAJ.gif")

@Repent.command(description=f"Puts wasted screen of a user's pfp. \nUsage: {config_get('prefix')}wasted <@user>", help="fun")
async def wasted(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/wasted?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Puts jail bars over a user's pfp. \nUsage: {config_get('prefix')}jail <@user>", help="fun")
async def jail(ctx, user: discord.User=None):   
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/overlay/jail?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Turns a user's pfp into a triggered gif. \nUsage: {config_get('prefix')}triggered <@user>", help="fun")
async def triggered(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/triggered?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Puts USSR flag on a user's pfp. \nUsage: {config_get('prefix')}ussr <@user>", help="fun")
async def ussr(ctx, user: discord.User=None):   
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/comrade?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Overlays missionpassed meme on someone's pfp. \nUsage: {config_get('prefix')}missionpassed <@user>", help="fun")
async def missionpassed(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/passed?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Pixelates a user's pfp. \nUsage: {config_get('prefix')}pixelate <@user>", help="fun")
async def pixelate(ctx, user: discord.User=None):   
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/pixelate?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Blurs a person's pfp. \nUsage: {config_get('prefix')}blur <@user>", help="fun")
async def blur(ctx, user: discord.User=None):    
    if user is None:
        user = ctx.message.author 
    url = f'https://some-random-api.com/canvas/blur?avatar={user.avatar.replace(format="png", size=1024)}'
    await apiimg(ctx, url)

@Repent.command(description=f"Sends a custom YT comment. \nUsage: {config_get('prefix')}ytcomment <@use>r <text>", help="fun")
async def ytcomment(ctx, avatar: discord.Member, *, comment: str):    
    url = f'https://some-random-api.com/canvas/youtube-comment?avatar={avatar.avatar.replace(format="png", size=1024)}&comment={comment}&username={avatar}'
    await apiimg(ctx, url)

@Repent.command(description=f"Sends a tickle gif. \nUsage: {config_get('prefix')}tickle <@user>", help="fun")
async def tickle(ctx, user: discord.Member):   
    r = (await arequesters.get("https://nekos.life/api/v2/img/tickle"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Sends a slapping gif. \nUsage: {config_get('prefix')}slap <@user>", help="fun")
async def slap(ctx, user: discord.Member): 
    r = (await arequesters.get("https://nekos.life/api/v2/img/slap"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Sends a hugging gif. \nUsage: {config_get('prefix')}hug <@user>", help="fun")
async def hug(ctx, user: discord.Member):    
    r = (await arequesters.get("https://nekos.life/api/v2/img/hug"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Sends a smug gif. \nUsage: {config_get('prefix')}smug <@user>", help="fun")
async def smug(ctx, user: discord.Member):     
    r = (await arequesters.get("https://nekos.life/api/v2/img/smug"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Sends a pat gif. \nUsage: {config_get('prefix')}pat <@user>", help="fun")
async def pat(ctx, user: discord.Member):    
    r = (await arequesters.get("https://nekos.life/api/v2/img/pat"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Sends a kissing gif. \nUsage: {config_get('prefix')}kiss <@user>", help="fun")
async def kiss(ctx, user: discord.Member):    
    r = (await arequesters.get("https://nekos.life/api/v2/img/kiss"))
    res = r.json()
    await ctx.send(user.mention + f" {res['url']}")

@Repent.command(description=f"Displays someone's Rainbow Six Siege stats. \nUsage: {config_get('prefix')}r6stats <r6 username>", help="fun")
async def r6stats(ctx, user):    
    r = (await arequesters.get('https://r6.tracker.network/profile/pc/' + user))
    if r.status_code == 404:
        stats = r.text
        index1 = stats.find('PVPWLRatio')
        index1 += 13
        index2 = stats.find('<', index1) - 1
        winLoss = stats[index1:index2]
        index1 = stats.find('PVPKDRatio')
        index1 += 13
        index2 = stats.find('<', index1) - 1
        killDeath = stats[index1:index2]
        index1 = stats.find('PVPKills')
        index1 += 11
        index2 = stats.find('<', index1) - 1
        kills = stats[index1:index2]
        index1 = stats.find('PVPMatchesWon')
        index1 += 16
        index2 = stats.find('<', index1) - 1
        wins = stats[index1:index2]
        index1 = stats.find('PVPMatchesLost')
        index1 += 17
        index2 = stats.find('<', index1) - 1
        loss = stats[index1:index2]
        index1 = stats.find('PVPAccuracy')
        index1 += 14
        index2 = stats.find('<', index1) - 1
        headShotPercent = stats[index1:index2]
        index1 = stats.find('PVPTimePlayed')
        index1 += 16
        index2 = stats.find('<', index1) - 1
        playtime = stats[index1:index2]
        index1 = stats.find('PVPMatchesPlayed')
        index1 += 19
        index2 = stats.find('<', index1) - 1
        playedmatch = stats[index1:index2]
        index1 = stats.find('PVPHeadshots')
        index1 += 15
        index2 = stats.find('<', index1) - 1
        heads = stats[index1:index2]
        heading = f"{user}'s R6 Stats"
        body = f"Win/Loss Ratio: {winLoss}\nKill/Death Ratio: {killDeath}\nHeadshots: {heads}\nHeadshot Accuracy: {headShotPercent}\nKills: {kills}\nWins: {wins}\nLosses: {loss}\nMatches Played: {playedmatch}\nPlayTime: {playtime}"
        cmdname = "r6stats"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "R6 Stats"
        body = f"Could not find {user}'s R6 Stats"
        cmdname = "r6stats"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Converts given text into a Text To Speech message. \nUsage: {config_get('prefix')}tts <text>", help="fun")
async def tts(ctx, *, message):
    async def convtoopus(file):
        json_data = {
            'targetformat': 'opus',
            'audiobitratetype': '0',
            'customaudiobitrate': '',
            'audiosamplingtype': '0',
            'customaudiosampling': '',
            'code': '82000',
            'oAuthToken': '',
            'legal': 'Our PHP programs can only be used in aconvert.com. We DO NOT allow using our PHP programs in any third-party websites, software or apps. We will report abuse to your cloud provider, Google Play and App store if illegal usage found!'
        }

        files=[
        ('file',('4883.MP4',file,'application/octet-stream'))
        ]

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://www.aconvert.com',
            'Referer': 'https://www.aconvert.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        e = requested.post("https://s31.aconvert.com/convert/convert9.php", data=json_data, headers=headers, files=files).json()
        server = e['server']
        filename = e['filename']
        opus = requested.get(f"https://s{server}.aconvert.com/convert/p3r68-cdx67/{filename}")
        return opus.content
    
    async def do_tts(message):
        f = io.BytesIO()
        tts = gTTS(text=message.lower(), lang="en")
        tts.write_to_fp(f)
        f.seek(0)
        return f.getvalue()

    voicefile = await do_tts(message)
    voicefile = await convtoopus(voicefile)

    headers = {
        'Authorization': config_get('token'),
        'X-Super-Properties': getxsuper(),
    }

    payload  = {"files":[{"filename":"voice-message.ogg","file_size":1,"id":"69","is_clip":False}]}

    upload = (await arequesters.post(f"https://discord.com/api/v9/channels/{ctx.channel.id}/attachments", headers=headers, json_data=payload)).json()
    uploadname = upload['attachments'][0]["upload_filename"]
    uploadurl = upload['attachments'][0]["upload_url"]

    upload_headers = {
            "Host": "discord-attachments-uploads-prd.storage.googleapis.com",
            "Accept-Language": "en-NZ,en-AU;q=0.9,en;q=0.8",
            "User-Agent": "Discord/42954 CFNetwork/1390 Darwin/22.0.0",
            "Content-Type": "audio/ogg",
            "Connection": "keep-alive",
            "Content-Length": str(1)
    }
        
    upload_response = requested.put(uploadurl, data=voicefile, headers=upload_headers)

    payload = {"channel_id": str(ctx.channel.id), "flags": 8192, "content": "", "nonce": "", "type": 0, "attachments": [{"id": "69", "filename": "voice-message.ogg", "duration_secs": 0, "uploaded_filename": uploadname, "waveform": ""}]}
    requested.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/messages', headers=headers, json=payload)

@Repent.command(description=f"Sends a petpet meme of someone's pfp. \nUsage: {config_get('prefix')}petpet <@user>", help="fun")
async def petpet(ctx, image: discord.user.User):    
    type(image) == discord.user.User
    image = await image.avatar.replace(format='png').read()
    source = BytesIO(image)
    dest = BytesIO()
    petpetgif.make(source, dest)
    dest.seek(0)
    await ctx.send(file=discord.File(dest, filename=f"{image[0]}_Repent_petpet.gif"))

@Repent.command(description=f"Makes someone's pfp ripple. \nUsage: {config_get('prefix')}ripplepfp <@user>", help="fun")
async def ripplepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="radiate", file_extension="gif")

@Repent.command(description=f"Flips a user's pfp. \nUsage: {config_get('prefix')}flippingpfp <@user>", help="fun")
async def flippingpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="shear", file_extension="gif")

@Repent.command(description=f"Makes a user into an Elmo burn meme. \nUsage: {config_get('prefix')}elmoburn <@user>", help="fun")
async def elmoburn(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="burn", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp have a shock. \nUsage: {config_get('prefix')}shockpfp <@user>", help="fun")
async def shockpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="shock", file_extension="gif")

@Repent.command(description=f"Bonks a user's pfp. \nUsage: {config_get('prefix')}bonkpfp <@user>", help="fun")
async def bonkpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="bonks", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp explicit. \nUsage: {config_get('prefix')}explicitpfp <@user>", help="fun")
async def explicitpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="explicit", file_extension="gif")

@Repent.command(description=f"Flickers a user's pfp. \nUsage: {config_get('prefix')}flickerpfp <@user>", help="fun")
async def flickerpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="lamp", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp rainy. \nUsage: {config_get('prefix')}rainypfp <@user>", help="fun")
async def rainypfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="rain", file_extension="gif")

@Repent.command(description=f"Shoots a user's pfp. \nUsage: {config_get('prefix')}shootpfp <@user>", help="fun")
async def shootpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="shoot", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp on TV. \nUsage: {config_get('prefix')}tvpfp <@user>", help="fun")
async def tvpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="tv", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp through a printer. \nUsage: {config_get('prefix')}printerpfp <@user>", help="fun")
async def printerpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="print", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp into the matrix. \nUsage: {config_get('prefix')}matrixpfp <@user>", help="fun")
async def matrixpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="matrix", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp into a sensitive warning. \nUsage: {config_get('prefix')}sensitivepfp <@user>", help="fun")
async def sensitivepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="sensitive", file_extension="gif")

@Repent.command(description=f"Dilates a user's pfp. \nUsage: {config_get('prefix')}dilatepfp <@user>", help="fun")
async def dilatepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="dilate", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp into a logging off meme. \nUsage: {config_get('prefix')}loggingoff <@user>", help="fun")
async def loggingoff(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="logoff", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp into an endless picture. \nUsage: {config_get('prefix')}endlesspfp <@user>", help="fun")
async def endlesspfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="endless", file_extension="gif")

@Repent.command(description=f"Puts a user's pfp into a washing machine. \nUsage: {config_get('prefix')}washingmachine <@user>", help="fun")
async def washingmachine(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="laundry", file_extension="gif")

@Repent.command(description=f"Rips a user's pfp. \nUsage: {config_get('prefix')}rippedpfp <@user>", help="fun")
async def rippedpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="ripped", file_extension="gif")

@Repent.command(description=f"Rufies a user's pfp. \nUsage: {config_get('prefix')}rufiepfp <@user>", help="fun")
async def rufiepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="stretch", file_extension="gif")

@Repent.command(description=f"Shreds a user's pfp. \nUsage: {config_get('prefix')}shredpfp <@user>", help="fun")
async def shredpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="shred", file_extension="gif")

@Repent.command(description=f"Liquefies a user's pfp. \nUsage: {config_get('prefix')}liquifypfp <@user>", help="fun")
async def liquifypfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="liquefy", file_extension="gif")

@Repent.command(description=f"Spins a user's pfp. \nUsage: {config_get('prefix')}spinpfp <@user>", help="fun")
async def spinpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="spin", file_extension="gif")

@Repent.command(description=f"Turns a user's pfp into plates. \nUsage: {config_get('prefix')}platepfp <@user>", help="fun")
async def platepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="plate", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp multicolored. \nUsage: {config_get('prefix')}rgbpfp <@user>", help="fun")
async def rgbpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="lsd", file_extension="gif")

@Repent.command(description=f"Paparazzi's a user's pfp. \nUsage: {config_get('prefix')}paparazzipfp <@user>", help="fun")
async def paparazzipfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="paparazzi", file_extension="gif")

@Repent.command(description=f"Big brains a user's pfp. \nUsage: {config_get('prefix')}bigbrainpfp <@user>", help="fun")
async def bigbrainpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="equations", file_extension="gif")

@Repent.command(description=f"Turns a user's pfp into an advert. \nUsage: {config_get('prefix')}adpfp <@user>", help="fun")
async def adpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="ads", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp infinite. \nUsage: {config_get('prefix')}infinitepfp <@user>", help="fun")
async def infinitepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="infinity", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp flappy. \nUsage: {config_get('prefix')}flappypfp <@user>", help="fun")
async def flappypfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="ripple", file_extension="gif")

@Repent.command(description=f"Makes a user's pfp into a brick wall. \nUsage: {config_get('prefix')}brickpfp <@user>", help="fun")
async def brickpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="wall", file_extension="gif")

@Repent.command(description=f"Paints a user's pfp. \nUsage: {config_get('prefix')}paintpfp <@user>", help="fun")
async def paintpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="paint", file_extension="gif")

@Repent.command(aliases=['toilet'], description=f"Puts a user's pfp into a toilet. \nUsage: {config_get('prefix')}toiletpfp <@user>", help="fun")
async def toiletpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="flush", file_extension="gif")

@Repent.command(description=f"Makes someone's pfp canny. \nUsage: {config_get('prefix')}cannypfp <@user>", help="fun")
async def cannypfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="canny", file_extension="gif")

@Repent.command(description=f"Makes someone's pfp shakey. \nUsage: {config_get('prefix')}shakeypfp <@user>", help="fun")
async def shakeypfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="earthquake", file_extension="gif")

@Repent.command(description=f"Makes someone's pfp wiggly. \nUsage: {config_get('prefix')}wigglepfp <@user>", help="fun")
async def wigglepfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="boil", file_extension="gif")

@Repent.command(description=f"Glitches out someone's pfp. \nUsage: {config_get('prefix')}glitchpfp <@user>", help="fun")
async def glitchpfp(ctx, user: discord.User=None):
    if user is None:
        user = ctx.message.author
    await jeyyapi(ctx, user=user, endpointer="glitch", file_extension="gif")
