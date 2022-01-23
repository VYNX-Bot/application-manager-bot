import json

import discord
from discord.ext import command
from discord.utils import get as finder

from src.cogs.etc import slash_utils


class Application_Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Application Manager cog loaded")

    @slash_utils.slash_command()
    async def list_applications(self, ctx):
        db = json.load(open("src/cogs/db/db.json"))
        applications = db[str(ctx.guild.id)]["applications"]
        embed = discord.Embed(title="Applications", color=discord.Color.green())
        for app in applications:
            embed.add_field(
                name=app, value=applications[app]["description"], inline=False
            )
        await ctx.send(embed=embed)

    @slash_utils.slash_command()
    async def apply(self, ctx, app_name: str):
        if app_name == "None":
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="Please enter an application name",
                    color=discord.Color.red(),
                )
            )
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        try:
            if str(ctx.author.id) in list(
                db[str(ctx.guild.id)]["applications"][app_name]["applications"]
            ):
                return await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description="You have already applied to this application",
                        color=discord.Color.red(),
                    )
                )
            for app in db[str(ctx.guild.id)]["applications"]:
                if str(ctx.author.id) in list(
                    db[str(ctx.guild.id)]["applications"][app]["applications"]
                ):
                    return await ctx.send(
                        embed=discord.Embed(
                            title="Error",
                            description="You can't have multiple applications pending at the same time!",
                            color=discord.Color.red(),
                        )
                    )
        except KeyError:
            pass
        if app_name not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Application {app_name} not found",
                    color=discord.Color.red(),
                )
            )
        if db[str(ctx.guild.id)]["applications"][app_name]["closed"] == True:
            return await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"Sadly... Application {app_name} is closed",
                    color=discord.Color.red(),
                )
            )

        await self.process(ctx, app_name, db)

    @slash_utils.slash_command()
    async def close(self, ctx, app_name: str):
        a = await ctx.send(
            embed=discord.Embed(
                title="Question",
                description="Are you sure you want to close your application submission?",
                color=discord.Color.yellow(),
            )
        )
        await a.add_reaction("✅")
        await a.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
        except asyncio.TimeoutError:
            return await a.delete()

        if str(reaction.emoji) == "✅":
            async with aiofiles.open("src/cogs/db/db.json") as fp:
                db = json.loads(await fp.read())
            del db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                str(ctx.author.id)
            ]
            await a.edit(
                embed=discord.Embed(
                    title="Success",
                    description=f"Your application for {app_name} closed",
                    color=discord.Color.green(),
                )
            )
            async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
                await fp.write(json.dumps(db))
        else:
            await a.delete()

    async def process(self, ctx, app_name, db):
        def dm_check(m):
            return m.author == ctx.author and m.channel == ctx.author.dm_channel

        logger = finder(
            ctx.guild.channels,
            id=db[str(ctx.guild.id)]["applications"][app_name]["log_channel"],
        )
        if logger == None:
            return await ctx, author.send(
                embed=discord.Embed(
                    title="Error",
                    description=f"The log channel for {app_name} does not exist. Please tell this to your server admin",
                    color=discord.Color.red(),
                )
            )
        applier = ctx.author
        embed = discord.Embed(
            title=f"{applier.name} has applied for {app_name}",
            color=discord.Color.green(),
            description=f"{applier.mention} trying to apply for {app_name} application.",
        )
        msg = await logger.send(embed=embed)
        app_info = db[str(ctx.guild.id)]["applications"][app_name]
        questions = app_info["questions"]
        answers = {}
        counter = 0
        await applier.send(
            f"Hello {applier.mention}, you are applying for {app_name} for {ctx.guild.name}\nRemember! You have 1 minute for each question!"
        )
        for question in questions:
            counter += 1
            await applier.send(counter + "." + question)
            try:
                answer = await self.bot.wait_for("message", check=dm_check, timeout=60)
                answers[question] = answer.content
                embed.add_field(
                    name=counter + "." + question, value=answer.content, inline=True
                )
                await msg.edit(embed=embed)
            except asyncio.TimeoutError:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Error",
                        description="You took too long to answer the questions",
                        color=discord.Color.red(),
                    )
                )
        db[str(ctx.guild.id)]["applications"][app_name]["applications"][
            str(applier.id)
        ] = answers
        await applier.send(
            "Thank you for applying, please wait for the application to be processed"
        )
        async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
            await fp.write(json.dumps(db, indent=4))


def setup(bot):
    bot.add_cog(Application_Manager(bot))
