import discord
from discord.ext import commands
import json
import random
import string
import datetime
class ApplicationManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Application manager cog loaded.')
    
    @commands.command()
    async def apply(self, ctx, appid:int):
        a = await ctx.send(f"Finding the application with Application ID {appid}...")

        async with ctx.typing():
            with open(f"src/data/applications.json") as f:
                applications = json.load(f)
                try:
                    application = applications[appid]
                    assert application['status'] == 'open' and application['guildID'] == ctx.guild.id
                except KeyError:
                    await a.edit(content=f"Application ID {appid} not found.",delete_after=5)
                    return
                except AssertionError:
                    await a.edit(content=f"Application ID {appid} is not open or you're in wrong guild.",delete_after=5)
                    return
                await a.edit(content=f"Application ID {appid} found.\n\n{application['description']}\nPlease check your DM and proceed the application in there!",delete_after=5)
                await dm_application_process(ctx,appid)
    
    async def dm_application_process(self, ctx, appid):
        with open(f"src/data/applications.json") as f:
            applications = json.load(f)
            application = applications[appid]
        await ctx.author.send(f"{ctx.author.mention} You have 1 minutes for each questions!")
        responses = {}
        for question in application["question"]:
            await ctx.author.send(f"Question: {question['question']}\nAnswer:")
            response = self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            if response is None or response == "":
                await ctx.author.send(f"You have not answered in time!\nYou have to start over.")
                return
            responses[question] = response.content
            text = ""
        for question,answer in response.items():
            text += f"Question: {question}\nAnswer: {answer}\n\n"
        await ctx.send("Try to check the question again.\nIf you are satisfied, type 'yes' to submit your application. Otherwise, type 'no' to start over.")
        response = self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
        if response is None or response == "":
            await ctx.author.send(f"You have not answered in time!\nYou have to start over.")
            return
        if response.content.lower() == "yes":
            await ctx.send(f"Your application has been submitted.\nHere's the question and answer.\n{text}")
            applyid = ''.join(random.sample(string.ascii_letters + string.digits, k=10))
            application['users'] = {str(ctx.author.id):responses,"applyid":applyid,time:time.time()}
            with open(f"src/data/applications.json", "w") as f:
                json.dump(applications, f, indent=4)
            await self.notify(ctx, appid, applyid)
        else:
            await ctx.author.send(f"Your application has been cancelled.")
    
    async def notify(self, ctx, appid, applyid):
        with open(f"src/data/applications.json") as f:
            applications = json.load(f)
        guild = self.bot.get_guild(int(applications[appid]['guildID']))
        channel = guild.get_channel(int(applications[appid]['channelID']))
        await channel.send(f"New application from {ctx.author.mention}!\nApplication ID: {applyid}")
        embed = discord.Embed(title=f"Response from {ctx.author.mention}", description=f"Application ID: {applyid}", color=0x00ff00)
        for question,responses in app['users'][str(ctx.author.id)].items():
            embed.add_field(name=question, value=responses)
        embed.set_footer(text=f"Application ID: {applyid}. Type 'a!accept {applyid}' to accept the application. Type 'a!reject {applyid}' to reject the application.\nSend when {str(datetime.datetime.fromtimestamp(app['users'][str(ctx.author.id)]['time'])).replace('-' ,'/')}")
        await channel.send(embed=embed)
    
    @commands.command()
    async def create_application(self, ctx, *, description=None):
        if description is None:
            description="When impostor is sus. 🥶🥶🥶🥶🥶🥶💀💀🤔"
        guild = ctx.guild
        channel = ctx.channel
        with open(f"src/cogs/datas/applications.json") as f:
            applications = json.load(f)
        applicationid = ''.join(random.sample(string.ascii_letters + string.digits, k=10))
        applications[applicationid] = {
            "guildID":guild.id,
            "channelID":channel.id,
            "description":description,
            "question":[],
            "status":"open"
        }
        with open(f"src/cogs/datas/applications.json", "w") as f:
            json.dump(applications, f, indent=4)
        await ctx.send(f"Application created.\nApplication ID: {len(applications)}\nType 'a!apply {len(applications)}' to apply.")
        await ctx.send("Now let's setup questions")
        questions = []
        while True:
            await ctx.send("Send any message to be the question. Type 'done' when you're done. Remember you have 2 minutes for each question.")
            response = self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=120)
            if response is None or response == "":
                await ctx.send("You didn't send question in time. I think that would be done.")
                return
            if response.content.lower() == "done":
                break
            questions.append(response.content)
        await ctx.send("Done!")
        with open(f"src/data/applications.json") as f:
            applications = json.load(f)
        applications[applicationid]["question"] = questions
        with open(f"src/data/applications.json", "w") as f:
            json.dump(applications, f, indent=4)
        
        

def setup(bot):
    bot.add_cog(ApplicationManager(bot))
