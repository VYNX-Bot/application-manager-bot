import discord
from src.cogs.datas.slash_utils import ApplicationCog
import json
import aiofiles
import random
import string
import time
from datetime import datetime
import asyncio
import src.cogs.datas.slash_utils as slash

class SlashApplicationManager(ApplicationCog):
	
	def __init__(self,bot):
		print("SlashApplicationManager is loaded.")
		super().__init__(bot)
		self.bot = bot
		self.admin = 911930082673696798
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
				"blah",
				"blah2"
			],
			"staff":[
				"a",
				"b",
				"c"
			]
		}
		self.roles = {
			"support":[
				927257982931173417,
				927257821379174420,
				911930501613359124
			],
			"staff":[
				928281498925297724,
				911930501613359124
			]
		}
	@slash.slash_command()
	@slash.describe(apply_="Application name")
	async def apply(self,ctx:slash.Context,apply_:str):
		"""
		This command for apply the application.
		"""
		if apply_ not in list(self.applicable):
			a = '\n'.join(list(self.applicable))
			return await ctx.send(embed=discord.Embed(title="Application not found",description=f"You cannnot supply empty application name.\nAvailable applications:\n\n{a}", color=0x00e5ff))
		await self.applicable[apply_](ctx)

	async def staff(self,ctx:slash.Context):
		await ctx.author.send(embed=discord.Embed(title="Staff applying process.",description="I have started this application process.", color=0x00ffd2))
		questions = self.question["staff"]
		await ctx.send("Check your direct messages!👀")
		await ctx.author.send("You will have to answer some questions to apply for the staff position. Please Note: that you have **2 minutes** for each question.")
		responses = {}
		for question in questions:
			await ctx.author.send(f"Question: {question}")
			response = await self.bot.wait_for('message',check=lambda m: m.author == ctx.author and m.guild is None)
			if response in [""," ",None]:
				return await ctx.send("You can't return an empty answer! Start over!")
			responses[question] = response.content
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
			embed.set_footer(text=f"You can accept this application by do `a!accept {id}`")
			
			db = json.loads(await fp.read())
			for channel in ctx.guild.channels:
				if channel.id == 926647677033259058:
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
	
	@slash.slash_command()
	@slash.describe(app_id="Application ID",reason="Reason why you accept this application.")
	async def accept(self,ctx:slash.Context,app_id:str,*,reason:str="No reason provided"):
		"""
		This command for accepting the application.
		"""
		roles = []
		for role in ctx.author.roles:
			roles.append(role.id)
		if self.admin not in roles:
			return await ctx.send("You don't have permission to do this!")
		if app_id == "":
			return await ctx.send("No application ID supplied")
		for role in ctx.author.roles:
			if role.id == 911930082673696798:
				async with aiofiles.open("src/cogs/datas/applications.json") as fp:
					db = json.loads(await fp.read())
		
				if app_id not in list(db):
					return await ctx.send("There's no guy with that ID? What do you mean?")
		
				await self.acceptance[db[app_id]["type"]](ctx,db,app_id,reason)
				await ctx.send("Successfully applied application and done the process.")
		
	async def staff_accept(self,ctx:slash.Context,db,app_id,reason):
		user = ctx.guild.get_member(int(db[app_id]["name"].strip("<@>")))
		for role in ctx.guild.roles:
			for role_id in self.roles["staff"]:
				if role_id == role.id:
					print(f"Adding {role.name} which is {role.id}")
					await user.add_roles(role)
		await user.send(embed=discord.Embed(title=f"Congratulations! Your staff application is accepted! in {ctx.guild.name} by {ctx.author.mention}",description=f"Congratulations! Your staff application is accepted! in {ctx.guild.name} by {ctx.author.mention}\nReason:\n{reason}"))
		del db[app_id]
		async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
			await fp.write(json.dumps(db,indent=4))
		await ctx.send("Successfully applied application and deleted from application database.")

	async def support(self,ctx:slash.Context):
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
		await ctx.author.send("Thanks for taking some times for questions! Your application will be applyed shortly!")
		now = time.time()
		async with aiofiles.open("src/cogs/datas/applications.json") as fp:
			id = ''.join(random.sample(string.ascii_letters + string.digits, 10))
			embed = discord.Embed(title="New Application!")
			embed.add_field(name="Name",value=ctx.author.mention)
			for question,answer in responses.items():
				embed.add_field(name="Q: "+question,value="A: " + answer)
			embed.add_field(name="Applied when",value=str(datetime.fromtimestamp(now)).replace("-","/"))
			embed.add_field(name="Type:",value="Support")
			embed.set_footer(text=f"You can accept this application by do `a!accept {id}`")
			db = json.loads(await fp.read())
			for channel in ctx.guild.channels:
				if channel.id == 926647677033259058:
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
	
	async def support_accept(self,ctx:slash.Context,db,app_id,reason):
		user = ctx.guild.get_member(int(db[app_id]["name"].strip("<@>")))
		for role in ctx.guild.roles:
			for role_id in self.roles["support"]:
				if role_id == role.id:
					print(f"Adding {role.name} which is {role.id}")
					await user.add_roles(role)
		await user.send(embed=discord.Embed(title=f"Congratulations! Your support application is accepted! in {ctx.guild.name} by {ctx.author.mention}",description=f"Congratulations! Your support application is accepted! in {ctx.guild.name} by {ctx.author.mention}\nReason:\n{reason}"))
		del db[app_id]
		async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
			await fp.write(json.dumps(db,indent=4))
		await ctx.author.send("Successfully applied application and deleted from application database.")
	@slash.slash_command()
	async def applications(self,ctx:slash.Context):
		"""
		This command for listing application.
		"""
		a = '\n'.join(list(self.applicable))
		await ctx.send(embed=discord.Embed(title='Available Applications',description=f"{a}"))
					   
	@slash.slash_command()
	async def lists(self,ctx:slash.Context):
		"""
		This command for list all pending application.
		"""
		roles = []
		for role in ctx.author.roles:
			roles.append(role.id)
		if self.admin not in roles:
			return await ctx.send("You don't have permission to do this!")
		for role in ctx.author.roles:
			if role.id == 911930082673696798:
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
				for embed in embeds:
					await ctx.send(embed=embed)
					await asyncio.sleep(0.3)
					
	@slash.slash_command()
	@slash.describe(app_id="Application ID",reason="A reason why you decline this application.")
	async def decline(self,ctx:slash.Context,app_id:str,*,reason:str="No reason provided"):
		"""
		This command for declining application.
		"""
		roles = []
		for role in ctx.author.roles:
			roles.append(role.id)
		if self.admin not in roles:
			return await ctx.send("You don't have permission to do this!")
		if app_id == "":
			return await ctx.send("No application ID supplied")
		async with aiofiles.open("src/cogs/datas/applications.json") as fp:
			db = json.loads(await fp.read())
		if app_id not in list(db):
			return await ctx.send("What application you trying to decline? 🤔")
		name = db[app_id]['aname']
		user = await self.bot.fetch_user(int(db[app_id]["name"].strip("<@>")))
		a = await ctx.send(embed=discord.Embed(title=f"Cancelling {db[app_id]['aname']}'s Application."))
		type = db[app_id]['type']
		del db[app_id]
		async with aiofiles.open("src/cogs/datas/applications.json","w") as fp:
			await fp.write(json.dumps(db,indent=4))
		await user.send(embed=discord.Embed(title=f"Your {type} application is declined!",description=f"Reason:\n{reason}"))
		await ctx.send(embed=discord.Embed(title=f"Cancelled {name}'s Application'"))
	
			
def setup(bot):
	bot.add_cog(SlashApplicationManager(bot))