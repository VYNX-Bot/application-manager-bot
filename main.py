from dotenv import load_dotenv

load_dotenv()
import asyncio
import os

import discord
import requests
from discord.ext import commands

import keep_alive

bot = commands.Bot(command_prefix="a!", intents=discord.Intents().all())


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


try:
    r = requests.head(url="https://discord.com/api/v1")
except Exception:
    print(f"Rate limit {round(int(r.headers['Retry-After']) / 60, 2)} minutes left")
    exit(1)


async def main():
    async with bot:
        for cog in os.listdir("./src/cogs"):
            if cog.endswith(".py"):
                await bot.load_extension("src.cogs." + cog[:-3])
        keep_alive.keep_alive()
        await bot.start(os.getenv("APP_BOT_TOKEN"))


asyncio.run(main())
