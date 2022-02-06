import os

import discord
from discord.ext import commands


class CogsManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("CogsManagement is loaded.")

    @commands.command(hidden=True)
    @commands.has_role("Vynx Devs")
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
    @commands.has_role("Vynx Devs")
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
    @commands.has_role("Vynx Devs")
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
    @commands.has_role("Vynx Devs")
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


def setup(bot):
    bot.add_cog(CogsManagement(bot))
