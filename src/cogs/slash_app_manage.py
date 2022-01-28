import json

import aiofiles
import discord
from discord.ext import commands

from src.cogs.etc import slash_utils


class SlashAppManage(slash_utils.ApplicationCog):
    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashAppManage cog loaded")

    @slash_utils.slash_command()
    @slash_utils.describe(app_name="Application Name")
    async def make_app(self, ctx, app_name: str):
        """
        Creates an application

        Required Argument:
            The name of the application

        Required Permission:
            Administrator or Role that have permission.
        """
        if app_name == "None":
            await ctx.send("Please enter a name for your application")
            return
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        if no_perm == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red(),
                )
            )

        db[str(ctx.guild.id)]["applications"][app_name] = {
            "closed": False,
            "applications": [],
        }

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
    @slash_utils.describe(
        app_name="Application Name",
        desc="Description of application. (can be multi line)",
    )
    async def set_app_desc(self, ctx, app_name: str, desc: str):
        """
        Sets the description of an application

        Required Argument:
            The name of the application
            Description of the application

        Required Permission:
            Administrator or Role that have permission.
        """

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        if no_perm == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red(),
                )
            )

        db[str(ctx.guild.id)]["applications"][app_name]["description"] = desc

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Application {app_name} description set to {desc}",
                color=discord.Color.green(),
            )
        )

    @slash_utils.slash_command()
    @slash_utils.describe(app="Application Name", question="Question")
    async def make_question(self, ctx, app: str, question: str):
        """
        Adds a question to an application

        Required Argument:
            The name of the application
            Question you want to add

        Required Permission:
            Administrator or Role that have permission.
        """
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

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        if no_perm == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red(),
                )
            )

        if app not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app} not found",
                    color=discord.Color.red(),
                )
            )

        try:
            db[str(ctx.guild.id)]["applications"][app]["questions"].append(question)

        except KeyError:
            db[str(ctx.guild.id)]["applications"][app]["questions"] = [question]

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
    @slash_utils.describe(
        app="Application Name",
        role="A role that will be given to applier that their application is applied",
    )
    async def apply_app_role(self, ctx, app: str, role: discord.Role):
        """
        Sets the role that will be given to the user when they apply for an application

        Required Argument:
            The name of the application
            Role

        Required Permission:
            Administrator or Role that have permission.
        """
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

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        if no_perm == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red(),
                )
            )

        if app not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app} not found",
                    color=discord.Color.red(),
                )
            )

        try:
            db[str(ctx.guild.id)]["applications"][app]["roles"].append(role.id)

        except KeyError:
            db[str(ctx.guild.id)]["applications"][app]["roles"] = [role.id]

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Role {role.name} added to application {app}",
                color=discord.Color.green(),
            )
        )

    @slash_utils.slash_command()
    @slash_utils.describe(
        app="Application Name",
        channel="A text channel that bot can send the application logs",
    )
    async def set_app_log(self, ctx, app: str, channel: discord.TextChannel):
        """
        Sets the channel where application logs will be sent

        Required Argument:
            The name of the application
            Channel

        Required Permission:
            Administrator or Role that have permission.
        """
        if app == "None" or channel == "None":
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter an application name"
                    if app == "None"
                    else "Please enter channel you want to add in application",
                    color=discord.Color.red(),
                )
            )
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        if no_perm == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red(),
                )
            )

        if app not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app} not found",
                    color=discord.Color.red(),
                )
            )

        try:
            db[str(ctx.guild.id)]["applications"][app]["log_channel"] = channel.id

        except KeyError:
            db[str(ctx.guild.id)]["applications"][app]["log_channel"] = channel.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

    @slash_utils.slash_command()
    @slash_utils.describe(
        role="A application moderator role where they can accept and deny the application apply request"
    )
    async def add_app_mod(self, ctx, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("You don't have permissions!")
        if role is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter a role",
                    color=discord.Color.red(),
                )
            )

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        try:
            db[str(ctx.guild.id)]["mod_roles"].append(role.id)
        except KeyError:
            db[str(ctx.guild.id)]["mod_roles"] = [role.id]

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title="Success",
                description=f"Role {role.name} added to mod roles",
                color=discord.Color.green(),
            )
        )

    @slash_utils.slash_command()
    @slash_utils.describe(role="A role where they can configure all applications")
    async def set_setting_role(self, ctx, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("You don't have permissions!")
        if role is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter a role",
                    color=discord.Color.red(),
                )
            )

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        try:
            db[str(ctx.guild.id)]["setting_role"] = role.id
        except KeyError:
            db[str(ctx.guild.id)]["setting_role"] = role.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title="Success",
                description=f"Role {role.name} added to setting role",
                color=discord.Color.green(),
            )
        )


def setup(bot):
    bot.add_cog(SlashAppManage(bot))
