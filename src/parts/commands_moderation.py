@Repent.command(description=f"Unlocks a channel so people can talk in it after it being locked. \nUsage: {config_get('prefix')}unlock", help="moderation") 
async def unlock(ctx):    
    roles = list(ctx.guild.roles)
    overwrites = discord.PermissionOverwrite(send_messages=True)
    for role in roles:
        await ctx.channel.set_permissions(role, overwrite=overwrites)
    heading = "Unlocked!"
    body = "Channel Successfully Unlocked!"
    cmdname = "unlock"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Locks a channel so nobody can talk in it. \nUsage: {config_get('prefix')}lock", help="moderation") 
async def lock(ctx):    
    roles = list(ctx.guild.roles)
    overwrites = discord.PermissionOverwrite(send_messages=False)

    for role in roles:
        await ctx.channel.set_permissions(role, overwrite=overwrites)
    heading = "Locked!"
    body = "Channel Successfully Locked!"
    cmdname = "lock"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Locks all channels so nobody can send any messages anywhere. \nUsage: {config_get('prefix')}lockdown", help="moderation") 
async def lockdown(ctx):   
    roles = list(ctx.guild.roles)
    overwrites = discord.PermissionOverwrite(send_messages=False)   
    for channel in ctx.guild.text_channels:
        for role in roles:
            await channel.set_permissions(role, overwrite=overwrites)
    heading = "Locked Down!"
    body = "Whole Server Successfully Locked Down!"
    cmdname = "lockdown"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Allows people to talk in the server after a server lockdown. \nUsage: {config_get('prefix')}unlockdown", help="moderation") 
async def unlockdown(ctx):    
    roles = list(ctx.guild.roles)
    overwrites = discord.PermissionOverwrite(send_messages=True)    
    for channel in ctx.guild.text_channels:
        for role in roles:
            await channel.set_permissions(role, overwrite=overwrites)
    heading = "UnLocked Down!"
    body = "Whole Server Successfully UnLocked Down!"
    cmdname = "unlockdown"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Imports the bans from another server and bans everyone from the server the command was executed in. \nUsage: {config_get('prefix')}importbans <server id>", help="moderation")
async def importbans(ctx, server_id: int):    
    server = ctx.bot.get_guild(server_id)
    if server is None:
        heading = "ERROR"
        body = f"Server with ID {server_id} not found."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    try:
        banned_users = await server.bans()
    except discord.Forbidden:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}You don't have the necessary permissions to access bans in that server.")
        return
    for banned_entry in banned_users:
        user_id = banned_entry.user.id
        try:
            await ctx.guild.ban(discord.Object(id=user_id))
        except discord.NotFound:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}User with ID {user_id} not found.")
        except discord.Forbidden:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}You don't have the necessary permissions to unban user with ID {user_id}.")
        except discord.HTTPException:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}An error occurred while trying to unban user with ID {user_id}.")
    heading = "Import Bans"
    body = f"Bans successfully imported from {Repent.get_guild(server_id).name}"
    cmdname = "importbans"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Imports all emojis from given server into the new server where the command was used and stops when hitting the limit \nUsage: {config_get('prefix')}importemojis <server id>", help="moderation")  
async def importemojis(ctx, source_server_id: int):    
    source_server = ctx.bot.get_guild(source_server_id)
    destination_server = ctx.guild  
    if source_server is None:
        heading = "ERROR"
        body = f"Source server with ID {source_server_id} could not be found."
        cmdname = "importemojis"
        await panelmaker(ctx, heading, body, cmdname)
        return
    try:
        emojis = source_server.emojis
    except discord.Forbidden:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}You don't have the necessary permissions to access emojis in the source server.")
        return
    emoji_limit = destination_server.emoji_limit
    for emoji in emojis:
        if len(destination_server.emojis) >= emoji_limit:
            heading = "Import Emojis"
            body = "Emoji limit reached. Stopping import."
            cmdname = "importemojis"
            await panelmaker(ctx, heading, body, cmdname)
            break
        try:
            await destination_server.create_custom_emoji(name=emoji.name, image=await emoji.url.read())
        except discord.Forbidden:
            print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}You don't have the necessary permissions to create emojis in the destination server.")
            break
        except discord.HTTPException:
            print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}An error occurred while trying to create the emoji {emoji.name}.")
    if len(destination_server.emojis) >= emoji_limit:
        pass
    else:
        heading = "Import Emojis"
        body = "Emoji Successfully Imported!"
        cmdname = "importemojis"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Deletes all emojis in a server. \nUsage: {config_get('prefix')}delemojis", help="moderation") 
async def delemojis(ctx):    
    if not ctx.guild.me.guild_permissions.manage_emojis:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}You don't have the necessary permissions to manage emojis.")
        return
    emojis = ctx.guild.emojis
    if not emojis:
        print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}There are no emojis to delete.")
        return
    for emoji in emojis:
        try:
            await emoji.delete()
        except discord.Forbidden:
            print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}Unable to delete emoji {emoji.name}. You don't have the necessary permissions.")
            break
        except discord.HTTPException:
            print(f"{Fore.LIGHTRED_EX}[ERROR] {Fore.WHITE}An error occurred while trying to delete emoji {emoji.name}.")
    heading = "Delete Emojis"
    body = "All emojis have been deleted!"
    cmdname = "delemoji"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Exports all bans from a server and stores them in a txt. \nUsage: {config_get('prefix')}exportbans", help="moderation")
async def exportbans(ctx):    
    ban_info = ""
    bans = await ctx.guild.bans()
    for entry in bans:
        ban_info += f"{entry.user} - {entry.reason}\n"
    if ban_info:
        with open(f"Data//Dumps//Ban Lists//{ctx.guild.name}'s ban list.txt", "w", encoding="utf-8") as file:
            file.write(ban_info)
        heading = "Export Bans"
        body = f"Ban information saved to '{ctx.guild.name}'s ban list.txt"
        cmdname = "exportbans"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "Export Bans"
        body = f"No Bans Were Found."
        cmdname = "exportbans"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Sends a list of all bans in chat. \nUsage: {config_get('prefix')}listbans", help="moderation")
async def listbans(ctx):
    ban_info = ""
    bans = await ctx.guild.bans()

    for entry in bans:
        ban_info += f"User: {entry.user.name} Reason: {entry.reason}\n"

        if len(ban_info) >= 1800 and config_get('embed_mode') == "indent":
            heading = f"{ctx.guild.name}'s Ban List "
            body = ban_info
            cmdname = "listbans"
            await panelmaker(ctx, heading, body, cmdname)
            ban_info = ""

        elif config_get('embed_mode') == "web" and len(ban_info) >= 150:
            heading = f"{ctx.guild.name}'s Ban List "
            body = ban_info
            cmdname = "listbans"
            await panelmaker(ctx, heading, body, cmdname)
            ban_info = ""

    ban_info = ban_info.rstrip('\n')

    if ban_info:
        heading = f"{ctx.guild.name}'s Ban List "
        body = ban_info
        cmdname = "listbans"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "List Bans"
        body = "No Bans Were Found"
        cmdname = "listbans"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Bans a user from a server with their Discord ID. \nUsage: {config_get('prefix')}idban <user id> [reason]", help="moderation")
async def idban(ctx, member_id: int, *, reason=None):
    if reason is None:
        reason = "Repent"
    await ctx.guild.ban(discord.Object(id=member_id), reason=reason)
    heading = "ID Ban"
    body = f"{member_id} was banned for {reason}."
    cmdname = "idban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Bans and then unbans a user from a server with their Discord ID. \nUsage: {config_get('prefix')}softidban <user id> [reason]", help="moderation")
async def softidban(ctx, member_id: int, *, reason=None):
    if reason is None:
        reason = "Repent"
    await ctx.guild.ban(discord.Object(id=member_id), reason=reason)
    await ctx.guild.unban(discord.Object(id=member_id), reason=reason)
    heading = "Soft ID Ban"
    body = f"{member_id} was softbanned for {reason}."
    cmdname = "softidban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Bans and then unbans a user from a server. \nUsage: {config_get('prefix')}softban <@user> [reason]", help="moderation")
async def softban(ctx, user: discord.Member, *, reason=None):
    if reason is None:
        reason = "Repent"
    await user.ban(reason=reason)
    await user.unban(reason=reason)
    heading = "Soft Ban"
    body = f"{user} was softbanned for {reason}."
    cmdname = "softban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Removes a role from a user. \nUsage: {config_get('prefix')}removerole <@user> <role name>", help="moderation")
async def removerole(ctx, member: discord.Member, *, name):
    role = get(ctx.guild.roles, name=name)
    await member.remove_roles(role)
    heading = "Role Removal"
    body = f"{member} was removed from the role {name}."
    cmdname = "removerole"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a stage channel. \nUsage: {config_get('prefix')}makechannel <channel name>", help="moderation") 
async def makestage(ctx, *, name):    
    await ctx.guild.create_stage_channel(name)

@Repent.command(description=f"Bans a user from a server. \nUsage: {config_get('prefix')}ban <@user> [reason]", help="moderation")
async def ban(ctx, user: discord.Member, *, reason=None):
    if reason is None:
        reason = "Repent"
    await user.ban(reason=reason)
    heading = "Ban"
    body = f"{user} was banned for {reason}."
    cmdname = "ban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Creates a role. \nUsage: {config_get('prefix')}makerole <name>", help="moderation")
async def makerole(ctx, *, role):
    await ctx.guild.create_role(name=role)
    heading = "Role Creation"
    body = f"{role} was created."
    cmdname = "makerole"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Gives a specific user a role. \nUsage: {config_get('prefix')}giverole <@user> <role name>", help="moderation")
async def giverole(ctx, member: discord.Member, *, name):
    role = get(ctx.guild.roles, name=name)
    await member.add_roles(role)
    heading = "Role Assignment"
    body = f"{member} was given the role {name}."
    cmdname = "giverole"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Gives all members in a server a role. \nUsage: {config_get('prefix')}roleall <role name>", help="moderation")
async def roleall(ctx, *, name):
    role = get(ctx.guild.roles, name=name)
    for member in list(ctx.guild.members):
        try:
            await member.add_roles(role)
        except:
            print(Exception)
    heading = "Role Assignment to All"
    body = f"All members were given the role: {name}."
    cmdname = "roleall"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Removes a role from all members in a server. \nUsage: {config_get('prefix')}unroleall <role name>", help="moderation")
async def unroleall(ctx, *, name):
    role = get(ctx.guild.roles, name=name)
    for member in list(ctx.guild.members):
        try:
            await member.remove_roles(role)
        except:
            print(Exception)
    heading = "Role Removal from All"
    body = f"{name} role was taken from all members."
    cmdname = "unroleall"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Changes a user's nickname. \nUsage: {config_get('prefix')}nick <@user> <nickname>", help="moderation")
async def nick(ctx, member: discord.Member, *, nick):   
    await member.edit(nick=nick)

@Repent.command(description=f"Gets rid of a user's nickname. \nUsage: {config_get('prefix')}clearnick <@user>", help="moderation")
async def clearnick(ctx, user: discord.Member):    
    await user.edit(nick=None)

@Repent.command(description=f"Kicks a user from a server. \nUsage: {config_get('prefix')}kick <@user>", help="moderation")
async def kick(ctx, user: discord.Member):   
    await user.kick(reason="Repent")
    heading = "Kick"
    body = f"{user} was kicked."
    cmdname = "kick"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Mutes a user in a server. \nUsage: {config_get('prefix')}mute <@user>", help="moderation")
async def mute(ctx, user: discord.Member):    
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
    await user.add_roles(role)
    heading = "Mute"
    body = f"{user} was muted."
    cmdname = "mute"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Unmutes a user in a server. \nUsage: {config_get('prefix')}unmute <@user>", help="moderation")
async def unmute(ctx, user: discord.Member):    
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.remove_roles(role)
    heading = "Unmute"
    body = f"{user} was unmuted."
    cmdname = "unmute"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Makes a channel in a server. \nUsage: {config_get('prefix')}makechannel <channel name>", help="moderation")
async def makechannel(ctx, *, name):    
    await ctx.guild.create_text_channel(name)

@Repent.command(description=f"Makes a voice channel in a server. \nUsage: {config_get('prefix')}makevc <channel name>", help="moderation")
async def makevc(ctx, *, name):    
    await ctx.guild.create_voice_channel(name)

@Repent.command(description=f"Makes a category in a server. \nUsage: {config_get('prefix')}makecategory <category name>", help="moderation")
async def makecategory(ctx, *, name):    
    await ctx.guild.create_category_channel(name)

@Repent.command(description=f"Deletes a category. \nUsage: {config_get('prefix')}delcategory <#category-tag>", help="moderation")
async def delcategory(ctx, channel: discord.CategoryChannel):    
    await channel.delete()

@Repent.command(description=f"Renames a category. \nUsage: {config_get('prefix')}renamecategory <#category-tag> <channel name>", help="moderation")
async def renamecategory(ctx, channel: discord.CategoryChannel, *, name):    
    await channel.edit(name=name)

@Repent.command(description=f"Deletes a channel in a server. \nUsage: {config_get('prefix')}delchannel <#channel-tag>", help="moderation")
async def delchannel(ctx, channel: discord.TextChannel):    
    await channel.delete()

@Repent.command(description=f"Deletes a voice channel. \nUsage: {config_get('prefix')}delvc <#vc-tag>", help="moderation")
async def delvc(ctx, channel: discord.VoiceChannel):    
    await channel.delete()

@Repent.command(description=f"Renames a voice channel. \nUsage: {config_get('prefix')}renamevc <#vc-tag> <channel name>", help="moderation")
async def renamevc(ctx, channel: discord.VoiceChannel, *, name):    
    await channel.edit(name=name)

@Repent.command(description=f"Renames a channel in a server. \nUsage: {config_get('prefix')}renamechannel <#channel-tag> <channel name>", help="moderation")
async def renamechannel(ctx, channel: discord.TextChannel, *, name):    
    await channel.edit(name=name)

@Repent.command(description=f"Puts slowmode on in a server. \nUsage: {config_get('prefix')}slowmode [slowmode length (seconds)]", help="moderation")
async def slowmode(ctx, time=60):    
    await ctx.channel.edit(slowmode_delay=time)

@Repent.command(description=f"Turns off slowmode in a server. \nUsage: {config_get('prefix')}removeslowmode", help="moderation")
async def removeslowmode(ctx):    
    await ctx.channel.edit(slowmode_delay=0)

@Repent.command(description=f"Untimes out users in a server in mass. \nUsage: {config_get('prefix')}masstimeout", help="moderation") 
async def massuntimeout(ctx): 
    users = scrape(ctx.guild.id, ctx.guild.member_count)  
    for user in users:
        headers = {'authorization': config_get('token'), 'x-super-properties': getxsuper(), "Content-Type": "application/json"}   
        date = (datetime.utcnow().strftime('%Y-%m-%d'))
        data = f'{{"communication_disabled_until":"{date}T00:00:00.000Z"}}'
        response = requested.patch(f'https://discordapp.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers=headers, data=data)    
        if response.status_code == 403:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Failed To Untimeout {user.name} In {ctx.guild.name}")
            await send_webhook("Mass Untimeout Error", f"Failed to untimetime out {user.name} In {ctx.guild.name}.", config_get('error_webhook_url'))
        elif response.status_code == 200:
            pass
    heading = "Mass Untimeout"
    body = "Successfully untimed out everyone."
    cmdname = "massuntimeout"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Times out a user. \nUsage: {config_get('prefix')}timeout <@use> [timeout time (mins)]", help="moderation") 
async def timeout(ctx, user: discord.Member, time_minutes: int=60):    
    if time_minutes > 10080:
        heading = "Error"
        body = "You cannot set a timeout longer than 7 days."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    hours = time_minutes // 60
    minutes = time_minutes % 60
    timeout_datetime = datetime.utcnow() + timedelta(hours=hours, minutes=minutes)
    timeout_str = timeout_datetime.strftime('%Y-%m-%dT%H:%M:%S.999Z')
    headers = {'authorization': config_get('token'), 'x-super-properties': getxsuper(), "Content-Type": "application/json"}   
    data = f'{{"communication_disabled_until":"{timeout_str}"}}'
    response = requested.patch(f'https://discordapp.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers=headers, data=data)   
    if response.status_code == 403:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Failed To Timeout {user.name} In {ctx.guild.name}")
        await send_webhook("Timeout Error", f"Failed to timeout {user.name} In {ctx.guild.name}.", config_get('error_webhook_url'))
    elif response.status_code == 200:
        heading = "Timeout"
        body = f"{user} was timed out for {hours} hours and {minutes} minutes."
        cmdname = "timeout"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Untimes out a user in a server. \nUsage: {config_get('prefix')}untimeout <@user>", help="moderation") 
async def untimeout(ctx, user: discord.Member):   
    headers = {'x-super-properties': getxsuper(), 'authorization': config_get('token'), "Content-Type": "application/json"}   
    date = (datetime.utcnow().strftime('%Y-%m-%d'))
    data = f'{{"communication_disabled_until":"{date}T00:00:00.000Z"}}'
    response = requested.patch(f'https://discordapp.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers=headers, data=data)    
    if response.status_code == 403:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Failed To Untimeout {user.name} In {ctx.guild.name}")
        await send_webhook("Untimeout Error", f"Failed to untimetime out {user.name} In {ctx.guild.name}.", config_get('error_webhook_url'))
    elif response.status_code == 200:
        heading = "Untimeout"
        body = f"{user} was untimed out."
        cmdname = "untimeout"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Unbans a user from a server using their ID. \nUsage: {config_get('prefix')}idunban <user id> [reason]", help="moderation") 
async def idunban(ctx, member_id: int, *, reason=None):   
    if reason == None:
        reason = "Repent"
    await ctx.guild.unban(discord.Object(id=member_id), reason=reason)
    heading = "ID Unban"
    body = f"{member_id} was unbanned."
    cmdname = "idunban"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Deletes and remakes a channel to wipe it of its contents. \nUsage: {config_get('prefix')}nukechannel", help="moderation")
async def nukechannel(ctx):
    channel = ctx.channel
    perms = ctx.channel.overwrites
    position = channel.position
    await channel.delete()
    await ctx.guild.create_text_channel(name=str(channel), help=channel.category, overwrites=perms, position=position)

@Repent.command(description=f"Disconnects from the current voice channel. \nUsage: {config_get('prefix')}vcleave", help="moderation")
async def vcleave(ctx):
    if not currentvc or not currentvcguild:
        heading, body, cmdname = "Error", "Not currently in a voice channel.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    ws = get_websocket()
    await ws.send_as_json({"op": 4, "d": {"guild_id": str(currentvcguild), "channel_id": None, "self_mute": False, "self_deaf": False}})
    heading, body, cmdname = "VC Leave", "Left the current voice channel.", "vcleave"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles self-mute in the current voice channel. \nUsage: {config_get('prefix')}vcmute", help="moderation")
async def vcmute(ctx, state: bool = True):
    if not currentvc or not currentvcguild:
        heading, body, cmdname = "Error", "Not currently in a voice channel.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    ws = get_websocket()
    await ws.send_as_json({"op": 4, "d": {"guild_id": str(currentvcguild), "channel_id": str(currentvc), "self_mute": state, "self_deaf": False}})
    heading, body, cmdname = "VC Mute", f"Self-mute {'enabled' if state else 'disabled'}.", "vcmute"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Toggles self-deafen in the current voice channel. \nUsage: {config_get('prefix')}vcdeafen", help="moderation")
async def vcdeafen(ctx, state: bool = True):
    if not currentvc or not currentvcguild:
        heading, body, cmdname = "Error", "Not currently in a voice channel.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    ws = get_websocket()
    await ws.send_as_json({"op": 4, "d": {"guild_id": str(currentvcguild), "channel_id": str(currentvc), "self_mute": state, "self_deaf": state}})
    heading, body, cmdname = "VC Deafen", f"Self-deafen {'enabled' if state else 'disabled'}.", "vcdeafen"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Protects a server's vanity invite, reclaiming it automatically if it gets sniped. \nUsage: {config_get('prefix')}vanityprotect <server id> <code>", help="moderation")
async def vanityprotect(ctx, server_id: int, code: str):
    guild = Repent.get_guild(server_id)
    if guild is None:
        heading, body, cmdname = "Error", f"Server with ID {server_id} not found.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    data = load_vanity_protect()
    data[str(server_id)] = code
    save_vanity_protect(data)
    heading = "Vanity Protector"
    body = f"Now watching **{guild.name}**'s vanity `/{code}` - it'll be automatically reclaimed if lost."
    cmdname = "vanityprotect"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Stops protecting a server's vanity invite. \nUsage: {config_get('prefix')}vanityunprotect <server id>", help="moderation")
async def vanityunprotect(ctx, server_id: int):
    data = load_vanity_protect()
    if str(server_id) in data:
        del data[str(server_id)]
        save_vanity_protect(data)
        heading, body, cmdname = "Vanity Protector", f"Stopped protecting the vanity for server {server_id}.", "vanityunprotect"
    else:
        heading, body, cmdname = "Vanity Protector", f"Server {server_id} wasn't being protected.", "vanityunprotect"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Lists all servers with vanity protection enabled. \nUsage: {config_get('prefix')}vanitylist", help="moderation")
async def vanitylist(ctx):
    data = load_vanity_protect()
    if not data:
        heading, body, cmdname = "Vanity Protector", "No servers are currently protected.", "vanitylist"
    else:
        lines = []
        for gid, code in data.items():
            guild = Repent.get_guild(int(gid))
            lines.append(f"{guild.name if guild else gid}: `/{code}`")
        heading, body, cmdname = "Vanity Protector", "\n".join(lines), "vanitylist"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Backs up a server's roles and channel structure. \nUsage: {config_get('prefix')}backupserver [server id]", help="moderation")
async def backupserver(ctx, server_id: int = None):
    server_id = server_id or ctx.guild.id
    path = save_backup(server_id)
    if path is None:
        heading, body, cmdname = "Error", f"Server with ID {server_id} not found.", "ERROR"
    else:
        heading, body, cmdname = "Server Backup", f"Backed up roles and channels to `{path.name}`.", "backupserver"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Lists available backups for a server. \nUsage: {config_get('prefix')}listbackups [server id]", help="moderation")
async def listbackups(ctx, server_id: int = None):
    server_id = server_id or ctx.guild.id
    backups = list_backups(server_id)
    if not backups:
        heading, body, cmdname = "Server Backups", "No backups found for that server.", "listbackups"
    else:
        heading, body, cmdname = "Server Backups", "\n".join(backups), "listbackups"
    await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Restores missing roles/channels from a backup (never deletes anything). \nUsage: {config_get('prefix')}restoreserver <filename> [server id]", help="moderation")
async def restoreserver(ctx, filename: str, server_id: int = None):
    server_id = server_id or ctx.guild.id
    path = BACKUPS_DIR / str(server_id) / filename
    if not path.exists():
        heading, body, cmdname = "Error", f"Backup `{filename}` not found for that server.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    guild = Repent.get_guild(server_id)
    if guild is None:
        heading, body, cmdname = "Error", f"Server with ID {server_id} not found.", "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return
    with open(path, "r") as f:
        data = json.load(f)
    created_roles, created_channels = await restore_backup(guild, data)
    heading = "Server Restore"
    body = f"Restored {created_roles} role(s) and {created_channels} channel(s) from `{filename}`."
    cmdname = "restoreserver"
    await panelmaker(ctx, heading, body, cmdname)
