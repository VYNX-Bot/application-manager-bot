import difflib
import sys
import traceback

import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            nearest = difflib.get_close_matches(e.command, ctx.bot.commands, cutoff=0.7)
            if len(nearest) >= 2:
                newline = "\n"
                await ctx.send(
                    f"Did you mean any of these command?\n{newline.join(nearest)}"
                )
            elif len(nearest) == 1:
                await ctx.send(f"Did you mean this command?\n{nearest[0]}")
            else:
                await ctx.send(f"I don't know this command.")
        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument.")

        elif isinstance(e, commands.MissingPermissions):
            await ctx.send(f"You don't have permission to use this command.")

        else:
            single_quote = "'"
            await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Exception Name {type(e).strip(f'<class{single_quote}{single_quote}>')}\nFull Error\n```\n{e}\n```",
                    color=discord.Color.red(),
                )
            )
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
