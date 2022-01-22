import discord
from discord.ext import commands
import aiofiles
import json
from discord.utils import get as finder

class App_manager(commands.Cog):
    def