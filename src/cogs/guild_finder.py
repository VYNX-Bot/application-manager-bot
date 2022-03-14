import discord
from discord.ext import commands, tasks
import asyncio
import json
import aiofiles
class Guild_Finder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def guild_finder_task(self):
        while True:
            await self.bot.wait_until_ready()
            guilds = self.bot.guilds
            async with aiofiles.open("src/cogs/db/db.json") as fp:
                data = await fp.read()
                data = json.loads(data)
            
            for guild in guilds:
                if str(guild.id) not in data:
                    data[str(guild.id)] = {
                        "applications": {},
                    }
            
            async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
                await fp.write(json.dumps(data))

        await asyncio.sleep(5)

    async def setup_hook(self):
        self.loop.create_task(self.guild_finder_task())

def setup(bot):
    bot.add_cog(Guild_Finder(bot))
