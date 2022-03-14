import os

import discord
from discord.ext import commands


def check():
    def inner(ctx):
        for role in ctx.author.roles:
            if role.id == 932721712485769292:
                return True
        if ctx.author.id == 890913140278181909:
            return True
        return False

    return commands.check(inner)


class CogsManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("CogsManagement is loaded.")

    @commands.command(hidden=True)
    @check()
    async def load(self, ctx, *, cog: str):
        """
        Loads a cog.
        """
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.command(hidden=True)
    @check()
    async def unload(self, ctx, *, cog: str):
        """
        Unloads a cog.
        """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.command(hidden=True)
    @check()
    async def reload(self, ctx, *, cog: str):
        """
        Reloads a cog.
        """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send(f"**`SUCCESS`**")

    @commands.command(hidden=True)
    @check()
    async def reloadall(self, ctx):
        """
        Reloads all cogs.
        """
        for cog in os.listdir("./src/cogs"):
            if cog == "cogs_management.py":
                continue
            if not cog.endswith(".py"):
                continue
            try:
                self.bot.unload_extension("src.cogs." + cog[:-3])
                self.bot.load_extension("src.cogs." + cog[:-3])
            except Exception as e:
                await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
            else:
                await ctx.send(f"**`SUCCESS`**")


async def setup(bot):
    await bot.add_cog(CogsManagement(bot))
