from src.cogs.utils import json

import aiofiles
from discord.ext import commands


class Guild_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Guild_Handler cog loaded")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        db[str(guild.id)] = {
            "applications": {},
        }

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))


def setup(bot):
    bot.add_cog(Guild_Handler(bot))
