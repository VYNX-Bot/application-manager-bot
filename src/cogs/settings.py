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
    @commands.has_permissions(administrator=True)
    async def make_app(self, app_name: str = None):
        """
        Creates an application

        Required Argument:
            The name of the application
        
        Required Permission:
            Administrator
        """
        if app_name == "None":
            await ctx.send("Please enter a name for your application")
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        db[str(ctx.guild.id)]["applications"][app] = {"closed": False,"applications": []}

        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db))

        await ctx.send(
            embed=discord.Embed(
                title=f"Success",
                description=f"Application {app_name} created",
                color=discord.Color.green(),
            )
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_app_desc(self, ctx, app_name: str = None, desc: str = None):
        """
        Sets the description of an application

        Required Argument:
            The name of the application
            Description of the application
        
        Required Permission:
            Administrator
        """
        if app_name == "None" or desc == "None":
            await ctx.send("Please enter a name for your application and a description")
            return

        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def make_question(self, app: str = None, question: str = None):
        """
        Adds a question to an application

        Required Argument:
            The name of the application
            Question you want to add
        
        Required Permission:
            Administrator
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def apply_app_role(self, app: str = None, role: discord.Role = None):
        """
        Sets the role that will be given to the user when they apply for an application

        Required Argument:
            The name of the application
            Role

        Required Permission:
            Administrator
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
    
    @commands.command()
    async def set_app_log(self, app: str = None, channel: discord.TextChannel = None):
        """
        Sets the channel where application logs will be sent

        Required Argument:
            The name of the application
            Channel
        
        Required Permission:
            Administrator
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


def setup(bot):
    bot.add_cog(Settings(bot))
