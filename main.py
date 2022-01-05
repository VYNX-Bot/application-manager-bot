import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
bot = commands.Bot(command_prefix='a!')

a = {}
for line in open(".env").readlines():
    a[line.split("=")[0]] = line.split("=")[1].strip()
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

for cog in os.listdir('./src/cogs'):
    if cog.endswith('.py'):
        cog = f'src.cogs.{cog[:-3]}'
        bot.load_extension(cog)

bot.run(a["TOKEN"])