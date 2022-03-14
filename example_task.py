import discord
from discord.ext import commands

class a(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def loop_event(self):
        pass
    
    async def setup_hook(self):
        self.loop.create_task(self.loop_event())
        # You can do in on_ready but not recommend

def setup(bot):
    bot.add_cog(a(bot))