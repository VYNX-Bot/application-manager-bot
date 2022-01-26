from dotenv import load_dotenv
load_dotenv()
import os

import discord
import requests
import keep_alive
import src.cogs.datas.slash_utils as slash

bot = slash.Bot(command_prefix="a!", intents=discord.Intents().all())


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


for cog in os.listdir("./src/cogs"):
    if cog.endswith(".py"):
        bot.load_extension("src.cogs." + cog[:-3])

try:
    r = requests.head(url="https://discord.com/api/v1")
except Exception:
    print(f"Rate limit {round(int(r.headers['Retry-After']) / 60, 2)} minutes left")

keep_alive.keep_alive()
bot.run(os.environ["TOKEN"])
