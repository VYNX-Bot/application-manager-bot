import json

import aiofiles
import discord
from discord.ext import commands
from discord.utils import get as finder


class App_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("App_manager cog loaded")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def accept_app(self, app_name, app_):
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        db[str(ctx.guild.id)]["applications"][app_name]["applications"]
