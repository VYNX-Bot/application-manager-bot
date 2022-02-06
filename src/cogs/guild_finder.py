import discord
from discord.ext import commands, tasks
import asyncio
import json
import aiofiles
class Guild_Finder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_finder_task.start()
    
    @tasks.loop(seconds=5)
    async def guild_finder_task(self):
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

def setup(bot):
    bot.add_cog(Guild_Finder(bot))