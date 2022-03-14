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
                await ctx.send("I don't know this command.")
        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument.")

        elif isinstance(e, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)
            error = ''.join(traceback.TracebackException.from_exception(exception).format())
            await ctx.send(embed=discord.Embed(title="Command errors out!, please contact Unpredictable!",description="```\n"+error+"\n```"))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
