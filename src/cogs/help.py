import random

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, command: str = None):
        """
        Get help for a command.
        """
        if command is None:
            embed = discord.Embed(
                title="Help", description="", color=discord.Color.blue()
            )
            for command in self.bot.commands:
                if command.hidden:
                    continue
                if command.aliases:
                    aliases = " | ".join(command.aliases)
                    embed.add_field(
                        name=f"{command.name} | {aliases}",
                        value=command.help,
                        inline=True,
                    )
                else:
                    embed.add_field(name=command.name, value=command.help, inline=True)
            await ctx.send(embed=embed)

        else:
            command = self.bot.get_command(command)
            if command is None:
                await ctx.send("That command does not exist.")
                return
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Usage", value=command.usage)
            embed.add_field(
                name="Aliases",
                value=", ".join(command.aliases) if command.aliases else "None",
            )
            await ctx.send(embed=embed)

        @commands.command()
        async def tips(self, ctx):
            tips_ = [
                "You can create application with space in it but you need to wrap it in double quotes and everytime you need to configure the application you need to wrap it in double quote.",
                "Help is most helpful command in the world",
                "Found error? Come at Vynx Development support server for help!",
                "Get stuck? Come at Vynx Development support server for help!",
                "This bot written entire in python. (and the fact that only one dev make entire bot and fixing bugs :joy:)",
                "Want to host your own of application bot? Simply follow instruction on https://github.com/vynx-bot/application-manager-bot",
                "Want a nicer bot? You can send us a PR!",
                "Slash command is the most underrated feature in discord.",
            ]
            await ctx.send(
                embed=discord.Embed(
                    title="Tips for using this bot", description=random.choice(tips_)
                )
            )


def setup(bot):
    bot.add_cog(Help(bot))
