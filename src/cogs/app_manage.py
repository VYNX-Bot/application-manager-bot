import asyncio
import json
import time
from datetime import datetime

import aiofiles
import discord
from discord.ext import commands
from discord.utils import get as finder


class App_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("App_manager cog loaded")

    @commands.command()
    async def accept_app(self, ctx, app_name: str, app_: str, bypass: str = "false"):
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())
        if bypass == "true":
            embed = discord.Embed(
                title="Are you sure you want to accept this application?",
                description="This action cannot be undone",
            )
            embed.add_field(name="Application Name", value=app_name)
            embed.add_field(name="Application ID", value=app_)
            embed.add_field(
                name="Applier",
                value=str(
                    ctx.guild.get_member(
                        db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                            app_
                        ]["applier"]
                    )
                ),
            )
            for question, answer in db[str(ctx.guild.id)]["applications"][app_name][
                "answers"
            ].items():
                embed.add_field(name=question, value=answer)
            embed.add_field(
                name="Applied when",
                value=str(
                    datetime.fromtimestamp(
                        db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                            app_
                        ]["timestamp"]
                    )
                ),
            )
            await ctx.send(embed=embed)
            await ctx.send("Please type `yes` to accept this application")
            msg = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            if msg.content == "yes":
                member = ctx.guild.get_member(
                    db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                        app_
                    ]["applier"]
                )
                for role in ctx.guild.get_role(
                    db[str(ctx.guild.id)]["applications"][app_name]["role"]
                ):
                    role = ctx.guild.get_role(role)
                    await member.add_roles(role)
                del db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                    app_
                ]
                await ctx.send("Application accepted")
                async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
                    await fp.write(json.dumps(db, indent=4))
                await member.send(
                    "Your application name {} has been accepted".format(app_name)
                )
            else:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Cancelled",
                        description="Application not accepted",
                        color=discord.Color.red(),
                    )
                )

    @commands.command()
    async def decline_app(self, ctx, app_name: str, app_: str, bypass: str = "false"):
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())
        if bypass == "true":
            embed = discord.Embed(
                title="Are you sure you want to decline this application?",
                description="This action cannot be undone",
            )
            embed.add_field(name="Application Name", value=app_name)
            embed.add_field(name="Application ID", value=app_)
            embed.add_field(
                name="Applier",
                value=str(
                    ctx.guild.get_member(
                        db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                            app_
                        ]["applier"]
                    )
                ),
            )
            for question, answer in db[str(ctx.guild.id)]["applications"][app_name][
                "answers"
            ].items():
                embed.add_field(name=question, value=answer)
            embed.add_field(
                name="Applied when",
                value=str(
                    datetime.fromtimestamp(
                        db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                            app_
                        ]["timestamp"]
                    )
                ),
            )
            await ctx.send(embed=embed)
            await ctx.send("Please type `yes` to decline this application")
            msg = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            if msg.content == "yes":
                del db[str(ctx.guild.id)]["applications"][app_name]["applications"][
                    app_
                ]
                await ctx.send("Application declined")
                async with aiofiles.open("src/cogs/db/db.json", "w") as fp:
                    await fp.write(json.dumps(db, indent=4))
            else:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Cancelled",
                        description="Application not declined",
                        color=discord.Color.red(),
                    )
                )

    @commands.command(aliases=["lab"])
    async def list_applications_submission(self, ctx, app_name: str = None):
        async with aiofiles.open("src/cogs/db/db.json") as fp:
            db = json.loads(await fp.read())

        if app_name is None:
            return await ctx.send("You need to input application name")
        elif app_name not in list(db[str(ctx.guild.id)]["applications"]):
            return await ctx.send("Your application isn't exist")

        embeds = []

        for userID, info in db[str(ctx.guild.id)]["applications"]["app_name"][
            "applications"
        ].items():
            member = ctx.guild.get_member(int(userID))
            embed = discord.Embed(title=f"{member.name}'s application")
            embed.add_field(
                name="Informations",
                value=f"""
Name: {member.name}
Applied when: {str(datetime.fromtimestamp(info["timestamp"])).replace('-', '/')}
Application ID: {info["id"]}
            """,
            )
            question_answer_thing = ""
            count = 1
            for question, answer in info["answers"].items():
                question_answer_thing += f"{count}. {question}\nAnswer: {answer}"
            embed.add_field(name="Questions and Answers", value=question_answer_thing)
            embeds.append(embed)
        for embed in embeds:
            await ctx.send(embed=embed)
            await asyncio.sleep(0.3)


def setup(bot):
    bot.add_cog(App_manager(bot))
