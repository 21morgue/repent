import discord
import asyncio
import os
from discord import app_commands
from discord import Color

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
command = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await command.sync()

@command.command(name="embed")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def test(ctx, heading: str, body: str, cmdname: str, titleurl: str, color: str, image: str, cmdurl: str):
    embed = discord.Embed(title=heading, description=body, url=titleurl)
    embed.set_thumbnail(url=image)
    embed.color = Color(int(color.lstrip('#'), 16))
    embed.set_author(name=cmdname, url=cmdurl)
    await ctx.response.send_message(embed=embed, ephemeral=True)

token = os.environ.get("CHEDDLATRON_USERAPP_TOKEN")
if not token:
    raise RuntimeError("Set CHEDDLATRON_USERAPP_TOKEN before starting the companion bot")

asyncio.run(bot.start(token))
