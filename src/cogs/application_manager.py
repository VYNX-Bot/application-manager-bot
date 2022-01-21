import discord
import json
import aiofiles
import random
import string
import time
from datetime import datetime
import asyncio
from discord.ext import commands
class ApplicationManager(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        self.applicable = {
            "staff":self.staff,
            "support":self.support
        }
        self.acceptance = {
            "staff":self.staff_accept,
            "support":self.support_accept
        }
        self.question = {
            "support":[
                "What is your discord username and descriminator?\ne.g.Blency#7291",
                "What is your discord ID\n\nIf you would like to get your id, Go to Account settings>Advanced>And enable Developer options",
				"**:warning: | HUMAN VERIFICATION IN PROCESS PLEASE TYPE `staff` TO PROVE THAT YOU ARE A HUMAN | :warning:**",
				"How long have you been in the server? (If you don't know just guess)",
				"The next 5 questions are personal questions and are not required to answer. We will not share this information and only the owners/admins of the server is able to read the application. If you feel uncomfortable or you do not want to answer you may answer",
				"What is your age, If you wish not to answer proceed with *skip*.",
				"What is your timezone? ex: America/Chicago\n\nIf you do not know use this, https://kevinnovak.github.io/Time-Zone-Picker/",
				"How many hours do you spend daily on Discord? (If you do not know just guess)",
				"Do you have past experience as a support member in another server? (If yes, please describe the member count, your staff position etc.)",
				"How would you describe yourself?",
				"In what way would you be able to help the server?",
				"What? You made it this far? Great job!\n\nThis section of the application is the **Scenario Questions**\nI will list of some scenarios that might happen when you are a support\nTry to do your best and describe what you would do in this scenario",
            ],
            "staff":[
                "What is your discord username and descriminator?\ne.g.Blency#7291",
                "What is your discord ID\n\nIf you would like to get your id, Go to Account settings>Advanced>And enable Developer options",
                "**:warning: | HUMAN VERIFICATION IN PROCESS PLEASE TYPE `staff` TO PROOVE THAT YOU ARE A HUMAN | :warning:**",
				"Tell us about yourself.",
				"What is the main job of a moderator?",
				"How long have you been in the server? (If you don't know just guess)",
				"What is your age, If you wish not to answer proceed with *skip*.",
				"What is your timezone? ex: America/Chicago\n\nIf you do not know use this, https://kevinnovak.github.io/Time-Zone-Picker/",
				"How many hours do you spend daily on Discord? (If you do not know just guess)",
				"Do you have past experience as a staff member in another server? (If yes, please describe the member count, your staff position etc.)",
				"How would you describe yourself?",
				"In what way would you be able to help the server?",
				"What? You made it this far? Great job!\n\nThis section of the application is the **Scenario Questions**\nI will list of some scenarios that might happen when you are a moderator\nTry to do your best and describe what you would do in this scenario.",
				"Someone is mildly spamming in chat for the first time. What will you do?",
				"Someone posted NSFW content in the server. What will you do?",
				"Someone is mass pinging. What will you do?",
				"Someone used racial/homophobic slurs or language in chat. What will you do?",
				"An argument has started in the server. What will you do?",
				"A user is trolling users on the server, what will you do?",
				"A user is using channels for the wrong purpose. What will you do? (Example : Bot commands in general chat.)",
				"A user is constantly promoting in chat. What will you do?\n\nex: Hey guys!! Join my server!!",
				"A user has dm advertised to another user and the user report via a ticket or in your private dms. What will you do?",
				"A user is harassing other people what would you do?",
				"A user scammed within the Trading Plaza. What would you do?"
            ]
        }
        self.roles = {
            "support": [932721712460607525,932721712460607521,932721712460607518],
            "staff": [932721712460607525,932721712460607522],
        }
    @commands.Cog.listener()
    async def on_ready(self):
        print("ApplicationManager cog is loaded.")
    @commands.command()
    async def apply(self,ctx,apply_:str):
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            db = json.loads(await fp.read())
        ids = []
        for application, info in db.items():
            ids.append(int(info["name"].strip("<@!>")))
        if ctx.author.id in ids:
            return await ctx.send("You already applied an application! Wait until your application is reviewed")
        if apply_ is None:
            a = '\n'.join(list(self.applicable))
            return await ctx.send(embed=discord.Embed(title="Application not found",description=f"You cannnot supply empty application name.\nAvailable applications:\n\n{a}", color=0x00e5ff))
        if apply_ not in list(self.applicable):
            return await ctx.send("Your application seem doesn't exist *yet*.")
        await self.applicable[apply_](ctx)

    async def staff(self,ctx):
        await ctx.author.send(embed=discord.Embed(title="Staff applying process.",description="I have started this application process.", color=0x00ffd2))
        questions = self.question["staff"]
        await ctx.send("Check your direct messages!👀")
        await ctx.author.send("You will have to answer some questions to apply for the staff position. Please Note: that you have **2 minutes** for each question and you have 256 characters to send us an answer (due to discord restriction).")
        responses = {}
        count = 1
        for question in questions:
            print("Question",count,"is",len(question),"long")
            await ctx.author.send(embed=discord.Embed(title=f"Question #{count}",description=question))
            response = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.guild is None)
            if response in [""," ",None]:
                return await ctx.send("You can't return an empty answer! Start over!")
            responses[question] = response.content
            count += 1
        await ctx.author.send("Thanks for taking some times for questions! Your application will be applyed shortly!")
        now = time.time()
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            id = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            embed = discord.Embed(title="New Application!")
            embed.add_field(name="Name",value=ctx.author.mention)
            for question,answer in responses.items():
                embed.add_field(name="Q: "+question,value="A: " + answer)
            embed.add_field(name="Applied when",value=str(datetime.fromtimestamp(now)).replace("-","/"))
            embed.add_field(name="Type",value="staff")
            embed.set_footer(text=f"You can accept this application by do `a!accept {id}` or to decline it, do `a!decline {id}`")
            
            db = json.loads(await fp.read())
            for channel in ctx.guild.channels:
                if channel.id == 932721714008301606:
                    break
            a = await channel.send(embed=embed)
            a = a.id
            db[id] = {
                "name":ctx.author.mention,
                "response":responses,
                "when":now,
                "type":"staff",
                "id":a,
                "aname":ctx.author.name
            }
        async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
            await fp.write(json.dumps(db,indent=4))
    
    @commands.command()
    @commands.has_role("Server Admins")
    async def accept(self,ctx,app_id:str):
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            db = json.loads(await fp.read())

        if app_id not in list(db):
            return await ctx.send("There's no guy with that ID? What do you mean?")

        await self.acceptance[db[app_id]["type"]](ctx,db,app_id)
        await ctx.send(f"{ctx.author.mention}'s application is accepted")

    async def staff_accept(self,ctx,db,app_id):
        user = ctx.guild.get_member(int(db[app_id]["name"].strip("<@!>")))
        for role in ctx.guild.roles:
            for role_id in self.roles["staff"]:
                if role_id == role.id:
                    print(f"Adding {role.name} which is {role.id}")
                    await user.add_roles(role)
        await user.send(f"Congratulations! Your staff application is accepted! in {ctx.guild.name} by {ctx.author.mention}")
        del db[app_id]
        async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
            await fp.write(json.dumps(db,indent=4))

    async def support(self,ctx):
        await ctx.author.send(embed=discord.Embed(title="Support applying process.",description="what ever sentence u want"))
        questions = self.question["support"]
        await ctx.send("Check your direct messages!👀")
        await ctx.author.send("You will have to have to answer some questions to apply for the support position. Please Note: that you have **2 minutes** for each question.")
        responses = {}
        for question in questions:
            await ctx.author.send(f"Question: {question}")
            response = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.guild is None)
            if response in [""," ",None]:
                return await ctx.author.send("You can't return an empty answer! Start over!")
            responses[question] = response.content
        await ctx.send("Thanks for taking some times for questions! Your application will be applyed shortly!")
        now = time.time()
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            id = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            embed = discord.Embed(title="New Application!")
            embed.add_field(name="Name",value=ctx.author.mention)
            for question,answer in responses.items():
                embed.add_field(name="Q: "+question,value="A: " + answer)
            embed.add_field(name="Applied when",value=str(datetime.fromtimestamp(now)).replace("-","/"))
            embed.add_field(name="Type:",value="Support")
            embed.set_footer(text=f"You can accept this application by do `a!accept {id}` or deny it using `a!decline {id}`")
            db = json.loads(await fp.read())
            for channel in ctx.guild.channels:
                if channel.id == 932721714008301606:
                    break
            a = await channel.send(embed=embed)
            a = a.id
            db[id] = {
                "name":ctx.author.mention,
                "response":responses,
                "when":now,
                "type":"support",
                "id":a,
                "aname":ctx.author.name
            }
        async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
            await fp.write(json.dumps(db,indent=4))
    
    async def support_accept(self,ctx,db,app_id):
        user = ctx.guild.get_member(int(db[app_id]["name"].strip("<@!>")))
        for role in ctx.guild.roles:
            for role_id in self.roles["support"]:
                if role_id == role.id:
                    print(f"Adding {role.name} which is {role.id}")
                    await user.add_roles(role)
        await user.send(f"Congratulations! Your support application is accepted! in {ctx.guild.name} by {ctx.author.mention}")
        del db[app_id]
        async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
            await fp.write(json.dumps(db,indent=4))
    @commands.command(aliases=["apps"])
    async def applications(self,ctx):
        a = '\n'.join(list(self.applicable))
        await ctx.send(embed=discord.Embed(title='Available Applications',description=f"{a}"))
                       
    @commands.command(aliases=["l"])
    @commands.has_role("Vynx Devs")
    async def lists(self,ctx):
        embeds = []
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            db = json.loads(await fp.read())
        for id in list(db):
            embed = discord.Embed(title=f"{db[id]['aname']}'s Application")
            embed.add_field(name="Name",value=ctx.author.mention)
            for question,answer in db[id]["response"].items():
                embed.add_field(name="Q: "+question,value="A: " + answer)
            embed.add_field(name="Applied when",value=str(datetime.fromtimestamp(db[id]["when"])).replace("-","/"))
            embed.add_field(name="Type",value="staff")
            embed.set_footer(text=f"You can accept this application by do `a!accept {id}`")
            embeds.append(embed)
        if embeds == []:
            return await ctx.send("No application pending")
        for embed in embeds:
            await ctx.send(embed=embed)
            await asyncio.sleep(0.3)
    @commands.command()
    async def decline(self,ctx,app_id:str,*,reason:str="No reason provided"):
        async with aiofiles.open("src/cogs/datas/applications.json") as fp:
            db = json.loads(await fp.read())
        if app_id not in list(db):
            return await ctx.send("What application you trying to decline? 🤔")
        name = db[app_id]['aname']
        user = await self.bot.fetch_user(int(db[app_id]["name"].strip("<@!>")))
        a = await ctx.send(embed=discord.Embed(title=f"Cancelling {db[app_id]['aname']}'s Application."))
        type = db[app_id]['type']
        del db[app_id]
        async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
            await fp.write(json.dumps(db,indent=4))
        await user.send(embed=discord.Embed(title=f"Your {type} application is declined!",description=f"Reason:\n{reason}"))
        await a.edit(embed=discord.Embed(title=f"Cancelled {name}'s Application'"))
    
            
def setup(bot):
    bot.add_cog(ApplicationManager(bot))