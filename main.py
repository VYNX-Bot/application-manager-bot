import discord
from discord.ext import commands
import os
import keep_alive

bot = commands.Bot(command_prefix='a!',intents=discord.Intents().all())

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

keep_alive.keep_alive()
bot.run(os.environ["TOKEN"])