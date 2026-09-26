@Repent.command(description=f"Steals another discord users profile. \nUsage: {config_get('prefix')}stealprofile <@user>", help="account")
async def stealprofile(ctx, user: discord.User):
    headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
    response = (await arequesters.get(f"https://discord.com/api/v9/users/{user.id}/profile", headers=headers)).json()
    avatar = response['user']['avatar']
    banner = response['user']['banner']
    if banner != None:
        bannertype = getmediatype(f"https://cdn.discordapp.com/banners/{user.id}/{banner}") 
        banner = f"https://cdn.discordapp.com/banners/{user.id}/{banner}.{bannertype}"

    if avatar != None:
        avatartype = getmediatype(f"https://cdn.discordapp.com/avatars/{user.id}/{avatar}") 
        avatar = f"https://cdn.discordapp.com/avatars/{user.id}/{avatar}.{avatartype}"

    accent_color = response['user']['accent_color']
    global_name = response['user']['global_name']
    avatar_decoration_data = response['user']['avatar_decoration_data']
    banner_color = response['user']['banner_color']
    bio = response['user_profile']['bio']
    pronouns = response['user_profile']['pronouns']
    folder_path = f'Data/Profiles/{user.name.lower()}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    avatar_filename = f'Data/Profiles/{user.name.lower()}/avatar.gif'
    banner_filename = f'Data/Profiles/{user.name.lower()}/banner.gif'

    if avatar:
        avatar_response = (await arequesters.get(avatar))
        with open(avatar_filename, 'wb') as avatar_file:
            avatar_file.write(avatar_response.content)

    if banner:
        banner_response = (await arequesters.get(banner))
        with open(banner_filename, 'wb') as banner_file:
            banner_file.write(banner_response.content)
    profile_data = {
        "accent_colour": accent_color,
        "global_name": global_name,
        "avatar_decoration_data": avatar_decoration_data,
        "banner_color": banner_color,
        "bio": bio,
        "theme_colors": None,
        "profile_effect": None,
        "pronouns": pronouns
    }
    with open(f'Data/Profiles/{user.name}.profile', 'w') as file:
        json.dump(profile_data, file, indent=4)
    heading = "Profile Stolen"
    body = f"User profile '{user.name}' has been successfully stolen."
    cmdname = "stealprofile"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Exports a file containing your entire discord profile. \nUsage: {config_get('prefix')}exportprofile <profile name>", help="account")
async def exportprofile(ctx, *, name: str):  
    headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
    response =  (await arequesters.get("https://discord.com/api/v9/users/@me" , headers=headers))
    response2 = (await arequesters.get(f"https://discord.com/api/v9/users/{ctx.message.author.id}/profile", headers=headers))
    data = response.json()
    data2 = response2.json()
    avatar = ctx.message.author.avatar
    banner_url = f"https://cdn.discordapp.com/banners/{ctx.message.author.id}/{data['banner']}.gif?size=480" if data["banner"] else None
    
    folder_path = f'Data/Profiles/{name.lower()}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    avatar_filename = f'Data/Profiles/{name.lower()}/avatar.gif'
    banner_filename = f'Data/Profiles/{name.lower()}/banner.gif'

    if avatar:
        avatar_response = (await arequesters.get(avatar))
        with open(avatar_filename, 'wb') as avatar_file:
            avatar_file.write(avatar_response.content)

    if banner_url:
        banner_response = (await arequesters.get(banner_url))
        with open(banner_filename, 'wb') as banner_file:
            banner_file.write(banner_response.content)
    
    accent_color = data["accent_color"]
    global_name = data["global_name"]
    avatar_decoration_data = data["avatar_decoration_data"]
    banner_color = data["banner_color"]
    bio = data["bio"]
    pronouns = data2["user_profile"]["pronouns"]
    profile_data = {
        "accent_colour": accent_color,
        "global_name": global_name,
        "avatar_decoration_data": avatar_decoration_data,
        "banner_color": banner_color,
        "bio": bio,
        "pronouns": pronouns}
    if await yougotnitrobro() == "nitro":
      profile_effect = data2["user_profile"]["profile_effect"]
      theme_colors = data2["user_profile"]["theme_colors"]
      profile_data.update({"theme_colors": theme_colors, "profile_effect": profile_effect})

    with open(f'Data/Profiles/{name.lower()}.profile', 'w') as file:
        json.dump(profile_data, file, indent=4)
    heading = "Profile Exported"
    body = f"User profile called '{name}' has been successfully exported."
    cmdname = "exportprofile"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Imports a discord profile saved with exportprofile. \nUsage: {config_get('prefix')}importprofile <profile name>", help="account")
async def importprofile(ctx, *, name: str):
    headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
    decordata_response = (await arequesters.get("https://discord.com/api/v9/users/@me/collectibles-purchases", headers=headers))
    decordata = decordata_response.json()

    def find_id_by_sku_id(sku):
        for collectible in decordata:
            if collectible["sku_id"] == sku:
                return collectible["items"][0]["id"]
        return None

    try:
        with open(f"Data/Profiles/{name.lower()}.profile", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}Profile '{name.lower()}' does not exist")
        await send_webhook("Import Profile Error", f"Profile '{name.lower()}' does not exist.", config_get('error_webhook_url'))
        return
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}An error occurred while reading the profile file: {e}")
        await send_webhook("Import Profile Error", f"An error occurred while reading the profile file: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url'))
        return

    async def picconvert(file_path):
        if file_path and file_path != "null":
            try:
                with open(file_path, 'rb') as file:
                    if await yougotnitrobro() == "nitro":
                        content_type = file.name.split('.')[-1]
                    else:
                        content_type = "png"
                    base64content = base64.b64encode(file.read()).decode('utf-8')
                    converted_data = f'data:image/{content_type};base64,{base64content}'
                    return converted_data
            except FileNotFoundError:
                return None
        return None

    avatar_filename = f'Data/Profiles/{name.lower()}/avatar.gif'
    banner_filename = f'Data/Profiles/{name.lower()}/banner.gif'

    avatar = await picconvert(avatar_filename) if os.path.exists(avatar_filename) else None
    banner = await picconvert(banner_filename) if os.path.exists(banner_filename) else None

    accent_color = data.get("accent_color")
    global_name = data.get("global_name")
    avatar_decoration_data = data.get("avatar_decoration_data")
    sku_id = None
    if avatar_decoration_data:
        sku_id = avatar_decoration_data.get("sku_id")
    asset = find_id_by_sku_id(sku_id)
    if asset == None:
        sku_id = None
    bio = data.get("bio")
    pronouns = data.get("pronouns")
    try:
      profile_effect = data.get("profile_effect")
    except:
        profile_effect = None
    theme_colours = data.get("theme_colors")
    bio_accent_payload = {
        "bio": bio,
        "pronouns": pronouns,
        "theme_colors": theme_colours,
        "accent_colour": accent_color,
        "profile_effect_id": profile_effect
    }
    username_banner_avatar_payload = {
        "global_name": global_name,
        "avatar": avatar,
        "avatar_decoration_id": asset,
        "avatar_decoration_sku_id": sku_id
    }
    if await yougotnitrobro() == "nitro":
        username_banner_avatar_payload["banner"] = banner
    headers = {"Authorization": config_get('token'), "x-super-properties": getxsuper()}
    try:
        e = (await arequesters.patch("https://discord.com/api/v9/users/%40me/profile", headers=headers, json_data=bio_accent_payload))
        e2 = (await arequesters.patch('https://canary.discord.com/api/v9/users/@me', headers=headers, json_data=username_banner_avatar_payload))
        print(e.text)
        print(e2.text)
        heading = "Profile Imported"
        body = f"User profile called '{name}' has been successfully imported."
        cmdname = "importprofile"
        await panelmaker(ctx, heading, body, cmdname)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}An error occurred while updating the user profile: {e}")
        await send_webhook("Profile Update Error", f"An error occurred while updating the user profile: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url'))

@Repent.command(description=f"Lists all saved profiles. \nUsage: {config_get('prefix')}listprofiles", help="account")
async def listprofiles(ctx):
    directory = "Data/Profiles/"
    profile_files = glob.glob(os.path.join(directory, "*.profile"))
    profile_files = [file for file in profile_files if os.path.isfile(file)]
    profile_files = [os.path.basename(file) for file in profile_files]
    all_profiles = '\n'.join(profile_files)
    await ctx.send(f"```Saved Discord Profiles\n\n{all_profiles}```")

@Repent.command(description=f"Deletes a saved profile. \nUsage: {config_get('prefix')}delprofile <name of profile>", help="account")
async def delprofile(ctx, name):
    directory = "Data/Profiles/"
    namee = f"{name}.profile"
    profile_path = os.path.join(directory, namee)
    if os.path.exists(profile_path):
        os.remove(profile_path)
        heading = "Profile Deleted"
        body = f"Profile '{name}' deleted successfully."
        cmdname = "delprofile"
    else:
        heading = "Error"
        body = f"Profile '{name}' does not exist."
        cmdname = "ERROR"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Animates your Discord nickname. \nUsage: {config_get('prefix')}animnick <nickname>\n\nThis is also used as a two way toggle, to turn this off, do the command without any args.", help="account")
async def animnick(ctx, *, text=None):    
    with open('Data/Settings/Configs/Settings.json', 'r') as file:
        settings_data = json.load(file)
    if 'animnick' not in settings_data:
        settings_data['animnick'] = False
        with open('Data/Settings/Configs/Settings.json', 'w') as file:
            json.dump(settings_data, file, indent=4)
    if setting_get('animnick') == True:
        setting_edit('animnick', False)
        heading = "Animated Nickname"
        body = "Your nickname is now no longer animated!"
        cmdname = "animnick"
        await panelmaker(ctx, heading, body, cmdname) 
    elif text == None and setting_get('animnick') == False:
        heading = "Animated Nickname"
        body = "Please provide text for your animated nickname"
        cmdname = "animnick"
        await panelmaker(ctx, heading, body, cmdname) 
    elif text != None and setting_get('animnick') == False:
        setting_edit('animnick', True)
        heading = "Animated Nickname"
        body = "Your nickname is now animated!"
        cmdname = "animnick"
        await panelmaker(ctx, heading, body, cmdname) 
        while setting_get('animnick') == True:
            name = ""
            for letter in text:
                name = name + letter
                await ctx.message.author.edit(nick=name)
                await asyncio.sleep(2.5)

@Repent.command(description=f"Changes status on Discord to playing a game. \nUsage: {config_get('prefix')}playing <message>", help="account")
async def playing(ctx, *, message):    
    game = discord.Game(name=message)
    await Repent.change_presence(activity=game)

@Repent.command(description=f"Changes status on Discord to streaming. \nUsage: {config_get('prefix')}streaming <message>", help="account")
async def streaming(ctx, *, message):    
    stream = discord.Streaming(name=message, url="https://www.twitch.tv/leekbeats",)
    await Repent.change_presence(activity=stream)

@Repent.command(description=f"Changes status on Discord to listening to music. \nUsage: {config_get('prefix')}listening <message>", help="account")
async def listening(ctx, *, message):    
    await Repent.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=message))

@Repent.command(description=f"Changes status on Discord to watching something. \nUsage: {config_get('prefix')}watching <message>", help="account")
async def watching(ctx, *, message):    
    await Repent.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=message))

@Repent.command(description=f"Changes status on Discord to competing in something. \nUsage: {config_get('prefix')}competing <message>", help="account")
async def competing(ctx, *, message):    
    await Repent.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name=message))

@Repent.command(description=f"Sends a random anime pfp. \nUsage: {config_get('prefix')}animepfpgen", help="account")
async def animepfpgen(ctx):    
    r = (await arequesters.get("https://nekos.life/api/v2/img/avatar"))
    res = r.json()
    await ctx.send(res['url'])

@Repent.command(description=f"Changes your hypesquad. \nUsage: {config_get('prefix')}hypesquad [hypesquad]", help="account")
async def hypesquad(ctx, house: str="None"):    
    headers = {
      'Authorization': config_get('token'),
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    if house.lower() == "bravery":
        payload = {'house_id': 1}
    elif house.lower() == "brilliance":
        payload = {'house_id': 2}
    elif house.lower() == "balance":
        payload = {'house_id': 3}
    else:
        houses = [1, 2, 3]
        payload = {'house_id': random.choice(houses)}
    try:
        (await arequesters.post('https://discordapp.com/api/v9/hypesquad/online', headers=headers, json_data=payload))
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}{e}"+Fore.RESET)
        await send_webhook("HypeSquad Change Error", f"Failed to change HypeSquad due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(description=f"Makes your nickname invisible. \nUsage: {config_get('prefix')}invisiblenickname", help="account")
async def invisiblenickname(ctx):    
    try:
        name = "‎‎‎‎‎‎‎‏‏‎឵឵឵‎"
        await ctx.author.edit(nick=name)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
        await send_webhook("Nickname Invisible Error", f"Failed to set invisible nickname due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(description=f"Makes your nickname junk text. \nUsage: {config_get('prefix')}junknickname", help="account")
async def junknickname(ctx):    
    try:
        name = "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"
        await ctx.author.edit(nick=name)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
        await send_webhook("Nickname Junk Error", f"Failed to set junk nickname due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(description=f"Makes your nickname blocks. \nUsage: {config_get('prefix')}blocknickname", help="account")
async def blocknickname(ctx):    
    try:
        name = "█████████████████████████████"
        await ctx.author.edit(nick=name)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
        await send_webhook("Nickname Blocks Error", f"Failed to set block nickname due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(description=f"Changes your nickname to a barcode. \nUsage: {config_get('prefix')}barcodenickname", help="account")
async def barcodenickname(ctx):   
    try:
        name = "█║▌│║▌║▌│█│▌║│█║█║ "
        await ctx.author.edit(nick=name)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
        await send_webhook("Barcode Nickname Error", f"Failed to set barcode nickname due to: {str(e)}.", config_get('error_webhook_url'))

@Repent.command(description=f"Backups all discord servers you are in to a txt file. \nUsage: {config_get('prefix')}backupservers", help="account")
async def backupservers(ctx):    
    token = config_get('token')  
    if os.path.exists('Data/Backups/Servers.txt'):
        os.remove('Data/Backups/Servers.txt')
    
    headers = {"authorization": token}
    payload = {"max_age": "0", "max_uses": "0", "temporary": False}

    for server in Repent.guilds:
        await asyncio.sleep(1)
        default_channel = server.system_channel or server.text_channels[0]
        invite = (await arequesters.post(f"https://discord.com/api/v9/channels/{default_channel.id}/invites", json_data=payload, headers=headers))
        
        if invite.status_code == 403:
            invite_created = False
            for channel in server.text_channels:
                permissions = channel.permissions_for(server.me)
                if not (permissions.read_messages and permissions.create_instant_invite):
                    continue
                
                invite = (await arequesters.post(f"https://discord.com/api/v9/channels/{channel.id}/invites", json_data=payload, headers=headers))
                if invite.status_code == 200:
                    invite_url = f'https://discord.gg/{invite.json()["code"]}'
                    print(f'{Fore.GREEN}Invite SUCCESS! For {server.name}')
                    with open('Servers.txt', "a+", encoding="UTF-8") as f:
                        f.write(f'\n{server.name} || {invite_url}')
                    invite_created = True
                    break
                elif invite.status_code == 429:
                    retry_after = invite.json().get('retry_after', 1)
                    await asyncio.sleep(retry_after)
            
            if not invite_created:
                print(f'{Fore.YELLOW}Invite Creation Failed (Disabled invites) for {server.name}. Skipping...')
        elif invite.status_code == 200:
            invite_url = f'https://discord.gg/{invite.json()["code"]}'
            print(f'{Fore.GREEN}Invite SUCCESS! For {server.name}')
            with open('Data/Backups/Servers.txt', "a+", encoding="UTF-8") as f:
                f.write(f'\n{server.name} || {invite_url}')
        elif invite.status_code == 429:
            retry_after = invite.json().get('retry_after', 1)
            await asyncio.sleep(retry_after)
            invite = (await arequesters.post(f"https://discord.com/api/v9/channels/{default_channel.id}/invites", json_data=payload, headers=headers))
            if invite.status_code == 200:
                invite_url = f'https://discord.gg/{invite.json()["code"]}'
                print(f'{Fore.GREEN}Invite SUCCESS! For {server.name}')
                with open('Data/Backups/Servers.txt', "a+", encoding="UTF-8") as f:
                    f.write(f'\n{server.name} || {invite_url}')
        elif invite.status_code == 400:
            invite_url_response = (await arequesters.get(f"https://discord.com/api/guilds/{server.id}/vanity-url", headers=headers))
            if invite_url_response.status_code == 403:
                print(f'{Fore.YELLOW}Invite Creation Failed (Maximum server invites reached) for {server.name}. Skipping...')
                continue
            invite_url = invite_url_response.json().get('code', 'No Vanity URL')
            with open('Data/Backups/Servers.txt', "a+", encoding="UTF-8") as f:
                f.write(f'\n{server.name} || {invite_url}')
        else:
            print(invite.text)
            print(invite.status_code)
            print("Please report this so it can be fixed or something.")
            return
    
    header = "Servers Backed Up"
    body = "All your servers have been backed up successfully!"
    cmdname = "backupservers"
    print(f"{Fore.LIGHTRED_EX}[Backup Servers]{Fore.WHITE} ~ All servers have been backed up successfully!")
    notif(body)
    await panelmaker(ctx, header, body, cmdname)

@Repent.command(description=f"Joins all the servers in the txt file created by the backupservers cmd. \nUsage: {config_get('prefix')}recoverservers", help="account")
async def recoverservers(ctx):
    token = config_get('token')
    servers = open('Data/Backups/Servers.txt', 'r', encoding='utf-8')
    invites = []
    for line in servers:
        data = line.split(" || ")
        invites.append(data[1].strip("\n"))
    print(invites)
    headers = {'Authorization': f'{token}', 'x-super-properties': getxsuper()}
    for i in range(len(invites)):
        pattern = r'(?:https?://)?discord\.gg/([a-zA-Z0-9]+)'
        match = re.search(pattern, invites[i])
        id = match.group(1)
        url = f"https://discord.com/api/v9/invites/{id}"
        resp = (await arequesters.post(url=url, headers=headers))
        time.sleep(5)

@Repent.command(description=f"Creates a txt with all your Discord friends in it. \nUsage: {config_get('prefix')}backupfriends", help="account")
async def backupfriends(ctx):    
    token = config_get('token')  
    headers = {'authorization': token}
    friends = (await arequesters.get('https://discord.com/api/v9/users/@me/relationships', headers=headers))
    with open('Data/Backups/Discord Friends.txt', 'w', encoding='UTF-8') as f:
        saved_friends = 0
        for friend in friends.json():
            username = 'Username: %s#%s | User ID: %s\n' % (friend['user']['username'], friend['user']['discriminator'], friend['id'])
            username = username.replace('#0', '')
            f.write(username)
            saved_friends += 1
    header = "Backed-Up Friends"
    body = f"{saved_friends} friends have been successfully backed-up!"
    cmdname = "Backup Friends"
    await panelmaker(ctx, header, body, cmdname)

@Repent.command(description=f"Stops commands that run in a loop such as {config_get('prefix')}spam. \nUsage: {config_get('prefix')}stop")
async def stop(ctx):
    global stopper
    stopper = True
    await asyncio.sleep(0.5)
    stopper = False
