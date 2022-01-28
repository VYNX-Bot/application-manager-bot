import json

import aiofiles
import discord
from discord.ext import commands

from src.cogs.etc import slash_utils


class SlashSettings(slash_utils.ApplicationCog):
    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings cog loaded")

    @slash_utils.slash_command()
    @slash_utils.describe(app_name="The name of the application that you want to make.")
    async def make_app(self, ctx, app_name: str):
        """
        Create Application
        """
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("You don't have permissions!")
        if app_name == "None":
            await ctx.send("Please enter a name for your application")
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        db[str(ctx.guild.id)]["applications"].append(app_name)

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Application {app_name} created",
                color=discord.Color.green(),
            )
        )

    @slash_utils.slash_command()
    async def make_question(self, ctx, app: str, question: str):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("You don't have permissions!")
        if app == "None" or question == "None":
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter an application name"
                    if app == "None"
                    else "Please enter question you want to add in application",
                    color=discord.Color.red(),
                )
            )
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if app not in db[str(ctx.guild.id)]["applications"]:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app} not found",
                    color=discord.Color.red(),
                )
            )

        try:
            db[str(ctx.guild.id)]["applications"]["questions"].append(question)

        except KeyError:
            db[str(ctx.guild.id)]["applications"]["questions"] = [question]

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Question {question} added to application {app}",
                color=discord.Color.green(),
            )
        )

    @slash_utils.slash_command()
    async def apply_app_role(self, ctx, app: str, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("You don't have permissions!")
        if app == "None" or role == "None":
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter an application name"
                    if app == "None"
                    else "Please enter role you want to add in application",
                    color=discord.Color.red(),
                )
            )
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if app not in db[str(ctx.guild.id)]["applications"]:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app} not found",
                    color=discord.Color.red(),
                )
            )

        try:
            db[str(ctx.guild.id)]["applications"]["roles"].append(role.id)

        except KeyError:
            db[str(ctx.guild.id)]["applications"]["roles"] = [role.id]

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Role {role.name} added to application {app}",
                color=discord.Color.green(),
            )
        )


def setup(bot):
    bot.add_cog(SlashSettings(bot))
