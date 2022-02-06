import json

import aiofiles
import discord
from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Settings cog loaded")

    @commands.command()
    async def make_app(self, ctx, app_name: str = None):
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
        else:
            no_perm = False

        print(no_perm)
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
                title="Success",
                description=f"Application {app_name} created",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def set_app_desc(self, ctx, app_name: str = None,* , desc: str = None):
        """
        Sets the description of an application

        Required Argument:
            The name of the application
            Description of the application

        Required Permission:
            Administrator or Role that have permission.
        """
        if app_name == None or desc == None:
            await ctx.send("Please enter a name for your application and a description")
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if app_name not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error!",
                    description="Application Not Found",
                    color=discord.Color.red(),
                )
            )

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        else:
            no_perm = False
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
                title="Success",
                description=f"Application {app_name} description set to {desc}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def make_question(self, ctx, app: str = None, *, question: str = None):
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
        else:
            no_perm = False
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
                title="Success",
                description=f"Question {question} added to application {app}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def apply_app_role(self, ctx, app: str = None, role: discord.Role = None):
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
        else:
            no_perm = False
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
                title="Success",
                description=f"Role {role.name} added to application {app}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def set_app_log(
        self, ctx, app: str = None, channel: discord.TextChannel = None
    ):
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

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
        else:
            no_perm = False
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

        await ctx.send(
            embed=discord.Embed(
                title="Success",
                description=f"Added {channel} to logging for {app}",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_app_mod(self, ctx, role: discord.Role = None):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_setting_role(self, ctx, role: discord.Role = None):
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
    bot.add_cog(Settings(bot))
