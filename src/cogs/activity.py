import json
# keep_alive?
import random

import discord
import dta # upm package(dta)
from discord.ext import commands


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Activity cog loaded.")
        with open("src/cogs/datas/activity.json", "r") as f:
            activity = dta.Dict2Attr(json.load(f))
            game = random.choice(activity.game).format(
                len(list(dta.Attr2Dict(activity)))
            )
            if activity.status == "online":
                await self.bot.change_presence(
                    status=discord.Status.online, activity=discord.Game(game)
                )
            elif activity.status == "idle":
                await self.bot.change_presence(
                    status=discord.Status.idle, activity=discord.Game(game)
                )
            elif activity.status == "dnd":
                await self.bot.change_presence(
                    status=discord.Status.dnd, activity=discord.Game(game)
                )
            elif activity.status == "invisible":
                await self.bot.change_presence(
                    status=discord.Status.invisible, activity=discord.Game(game)
                )
            else:
                raise ValueError("Invalid status.")

    @commands.command()
    @commands.has_role("Vynx Devs")
    async def activity(self, ctx, *, activity):
        """
        Set the bot's activity.
        """
        await ctx.message.delete()
        await self.bot.change_presence(activity=discord.Game(name=activity))
        await ctx.send(f"Activity set to {activity}.")


def setup(bot):
    bot.add_cog(Activity(bot))
