#--------------------------JoyBot - Python Branch-------------------------#

import os,random,discord,pickle,json,io,contextlib,itertools
from discord.ext.tasks import asyncio
from discord.ext import commands
from discord.utils import find
from datetime import datetime
from decimal import Decimal
from shutil import copyfile
from heapq import nlargest
from pathlib import Path

#--------------------------Options-------------------------#

prefix="."
client = commands.Bot(command_prefix = prefix)
tabGoal = 25

cross = "❌"

yes = "👍"
no = "👎"

one = "1️⃣"
two = "2️⃣"
three = "3️⃣"
four = "4️⃣"
five = "5️⃣"
six = "6️⃣"
seven = "7️⃣"
eight = "8️⃣"
nine = "9️⃣"
ten = "🔟"

admins_ids = [
246862123328733186,
202513952406503425,
253059354331316224
]

errorcharacter = "\u001b[31m"
resetcharacter = "\u001b[0m"

#--------------------------Variables-------------------------#

facesList={}
facesAmount={}
pollDict={}
scoreDict={}

allGifs = ["hugs","kisses","marry"]
gifsList={}
gifsAmount={}


ynpoll = [yes,no,cross]
numpoll = {

	1: one,
	2: two,
	3: three,
	4: four,
	5: five,
	6: six,
	7: seven,
	8: eight,
	9: nine,
	10: ten
}

with open('./data/token.txt', 'r') as file:
	botToken = file.read().replace('\n', '')

#--------------------------Functions-------------------------#

def inch_cm(convert):
	#CM
	try:
		if convert.isnumeric():
			inches = int(convert) / 2.54
			feet = 0
			while inches >= 13:
				feet += 1
				inches -= 12
			return str(feet)+"'"+str(round(inches))

		#Inches
		else:
			if "'" in convert:
				split = convert.split("'")
				if split[0].isnumeric():
					if split[1].isnumeric():
						inches = int(split[0]) * 12
						inches += int(split[1])
						cm = inches * 2.54
						return str(round(cm))+"cm"
					else:
						return False
				else:
					return False
			#Meters
			elif "." in convert:
				split = convert.split(".")
				if split[0].isnumeric():
					if split[1].isnumeric():
						return str(round(Decimal(convert)*100))+"cm"
					else:
						return False
				else:
					return False

			else:
				return False

	#CM again but the provided argument was a number
	except AttributeError:
		inches = int(convert) / 2.54
		feet = 0
		while inches >= 13:
			feet += 1
			inches -= 12
		return str(feet)+"'"+str(round(inches))

def stringPOP(string, pop):
	popped = ""
	for i in range(len(string)): 
		if i != pop: 
			popped = popped + string[i]
	return popped

#This spacifies
def spacifyFunction(text):
	endString=""
	for x in range(0,len(text)):
		endString=(endString+text[x]+" ")
	return endString

#Edit the poll dict
def pollDictMod(type, author, message):
	if type == "add":
		try:
			oldDict = pollDict[author]
		except KeyError:
			oldDict = []

		oldDict.append(message)
		pollDict[author] = oldDict

	elif type == "remove":
		try:
			oldDict = pollDict[author]
		except KeyError:
			return

		if message in oldDict:
			oldDict.remove(message)
			return True
	elif type == "list":
		return pollDict
		
	else:
		raise Exception(f"Invalid type of '{type}'!")

def scoreDictMod(type, author, amount=0):
	try:
		global scoreDict
		if type == "add":
			try:
				oldDict = scoreDict[author]
			except KeyError:
				oldDict = 0

			oldDict += amount
			scoreDict[author] = oldDict

		elif type == "minus":
			try:
				oldDict = scoreDict[author]
			except KeyError:
				return

			oldDict -= amount
			if oldDict <= 0:
				scoreDict.pop(author)

			else:
				scoreDict[author] = oldDict
		elif type == "one":
			try:
				oldDict = scoreDict[author]
			except KeyError:
				return 0
			return oldDict

		elif type == "list":
			return scoreDict

		else:
			raise Exception(f"Invalid type of '{type}'!")
	finally:
		with open("./data/bumpscores.pkl", "wb") as fp:
			pickle.dump(scoreDict, fp)

#Import all the faces from folder
def updateFaces(whichFolder=None):
	global facesAmount,facesList
	totalFaces=[]

	if whichFolder == None: 
		print("Updating all faces...")

		facesList={}
		facesAmount={}

		for folder in os.listdir("./faces"):
			for filename in sorted(os.listdir("./faces/"+folder)):
				if filename.endswith(".png"):
					if filename[:-4].isdigit():
						totalFaces.append(filename)
					else:
						print(f"{errorcharacter}The file '{filename}' in folder '{folder}' was not named correctly!{resetcharacter}")
				else:
					print(f"{errorcharacter}The file '{filename}' in folder '{folder}' was not named correctly!{resetcharacter}")

			if len(totalFaces) != 0:
				facesList[folder] = totalFaces
				facesAmount[folder] = len(totalFaces)
				totalFaces=[]
			else:
				print(f"{errorcharacter}The folder {folder} did not have any valid pictures!{resetcharacter}")

		if facesAmount == {}:
			print(f"{errorcharacter}No faces loaded!{resetcharacter}\n")

	else:
		if os.path.exists(f"./faces/{whichFolder}"):
			print(f"Updating the '{whichFolder}' folder...")
			for filename in sorted(os.listdir("./faces/"+whichFolder)):
				if filename.endswith(".png"):
					if filename[:-4].isdigit():
						totalFaces.append(filename)
					else:
						print(f"{errorcharacter}The file '{filename}' in folder '{whichFolder}' was not named correctly!{resetcharacter}")
				else:
					print(f"{errorcharacter}The file '{filename}' in folder '{whichFolder}' was not named correctly!{resetcharacter}")

			if len(totalFaces) != 0:
				facesList[whichFolder] = totalFaces
				facesAmount[whichFolder] = len(totalFaces)
				totalFaces=[]
			else:
				print(f"{errorcharacter}The folder '{whichFolder}' did not have any valid pictures!{resetcharacter}")

		else:
			raise Exception(f"Tried to access the folder './faces/{whichFolder}, but it does not exist!'")

def updateGifs(whichGifs=None):
	global gifsList,gifsAmount
	totalGifs=[]

	if whichGifs == None:
		for gifType in allGifs:
			for filename in os.listdir(f"./gifs/{gifType}"):
				if filename.endswith(".gif"):
					if filename[:-4].isdigit():
						totalGifs.append(filename)
					else:
						print(f"{errorcharacter}The gif '{filename}' in folder '{gifType}' was not named correctly!{resetcharacter}")
				else:
					print(f"{errorcharacter}The gif '{filename}' in folder '{gifType}' was not named correctly!{resetcharacter}")
			
			if len(totalGifs) != 0:
				gifsList[gifType] = totalGifs
				gifsAmount[gifType] = len(totalGifs)
				totalGifs=[]
			else:
				print(f"{errorcharacter}The folder '{gifType}' did not have any valid gifs!{resetcharacter}")

	elif whichGifs in allGifs:
		for filename in os.listdir(f"./gifs/{whichGifs}"):
			if filename.endswith(".gif"):
				if filename[:-4].isdigit():
					totalGifs.append(filename)
				else:
					print(f"{errorcharacter}The gif '{filename}' in folder '{whichGifs}' was not named correctly!{resetcharacter}")
			else:
				print(f"{errorcharacter}The gif '{filename}' in folder '{whichGifs}' was not named correctly!{resetcharacter}")

		if len(totalGifs) != 0:
			gifsList[whichGifs] = totalGifs
			gifsAmount[whichGifs] = len(totalGifs)
			totalGifs=[]

		else:
			print(f"{errorcharacter}The folder '{whichGifs}' did not have any valid gifs!{resetcharacter}")
	else:
		raise Exception(f"The type '{whichGifs}' can't be used in this function! (updateGifs)")

def randomGif(whichGifs):
	if whichGifs in allGifs:
		return random.choice(gifsList[whichGifs])
	else:
		return False

#Prints a person and their total pictures nicely.
def printPerson(person,endnum):
	if len(person) > tabGoal-1:
		person="Folder name too long"

	while len(person) != tabGoal:
		person = person+" "

	print(person+endnum)

#--------------------------Events-------------------------#

#Triggers when bot starts
#Updates the presence and prints to console we've connected
@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game("Just JoyBot things :)"))
	print(f"Logged in as the bot ({client.user})!")

@client.event
async def on_message(message):
	if message.content == "<@!504030703264989194>":
		if message.author.id != 504030703264989194:
			await message.channel.send("My prefix is `.` and `^`!\nType `.help` and `^help`!")
	await client.process_commands(message)
	if message.author.id == 302050872383242240:
		for embed in message.embeds:
			if "Bump done" in embed.description:
				bumpID = embed.description
				bumpID = stringPOP(bumpID,0)
				bumpID = stringPOP(bumpID,0)
				bumpID, _ = bumpID.split(">")
				scoreDictMod("add",int(bumpID),1)
				top = str(getTopDict(scoreDict, 1))
				top = stringPOP(top, 0)
				top = stringPOP(top, 0)
				top, _ = top.split(",")

				header = f"<@{bumpID}>, your bump score has been increased by one!\nType `.bumpscore` to view your current bump score!"
				if int(top) == int(bumpID):
					role = discord.utils.find(lambda r: r.id == 760719803844788235, message.guild.roles)
					member = message.guild.get_member(int(bumpID))

					if not role in member.roles:
						await message.channel.send(f"{header}\nYou also managed to get the top spot! Nice!")
						await member.add_roles(role)

						with open("./data/roletop.txt", "r") as fp:
							oldID = int(fp.read().replace('\n', ''))

						with open("./data/roletop.txt", "w") as fp:
							fp.write(str(bumpID))

						oldMember = message.guild.get_member(int(oldID))
						await oldMember.remove_roles(role)
						await message.channel.send(f"{oldMember.mention}, you've lost your top spot!")
					else:
						await message.channel.send(header)
				else:
					await message.channel.send(header)

	#testing
	if "do testbump now" == message.content:
		bumpID = message.author.id
		scoreDictMod("add",int(bumpID),0)
		top = str(getTopDict(scoreDict, 1))
		top = stringPOP(top, 0)
		top = stringPOP(top, 0)
		top, _ = top.split(",")
		header = f"<@{bumpID}>, your bump score has been increased by none (test bump!)!\nType `.bumpscore` to view your current bump score!"
		if int(top) == int(bumpID):
			role = discord.utils.find(lambda r: r.id == 760719803844788235, message.guild.roles)
			member = message.guild.get_member(bumpID)
			
			print(member, member.roles)
			print(type(bumpID), bumpID)

			if not role in member.roles:
				await message.channel.send(f"{header}\nYou also managed to get the top spot! Nice!")
				await member.add_roles(role)

				with open("./data/roletop.txt", "r") as fp:
					oldID = int(fp.read().replace('\n', ''))

				with open("./data/roletop.txt", "w") as fp:
					fp.write(str(bumpID))

				oldMember = message.guild.get_member(oldID)
				await oldMember.remove_roles(role)
				await message.channel.send(f"{oldMember.mention}, you've lost your top spot!")
			else:
				await message.channel.send(header)
		else:
			await message.channel.send(header)



#Triggers on any command
#Stops the error from appearing if it's any command not found error
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.CommandNotFound):
		return
	raise error

#-------------------------Backwords-----------------------#

def function_backwords(passthrough):
	endString=""
	for x in passthrough:
		endString = x + endString
	return endString

@client.command(name="backwords",description="returns the string backwords!")
async def backwords(ctx, *, text):
	
	convert = function_backwords(text)
	if convert != "":
		await ctx.send(f"{ctx.author.mention}, here is your backwords string: {convert}")
	else:
		await ctx.send(f"{ctx.author.mention}, please provide something to return backwords!")

#-------------------------Reversecaps----------------------------#

@client.command(name="reversecaps",description="reverses the caps in the provided argument!")
async def reversecaps(ctx, *, text=None):
	if text == None:
		await ctx.send(f"{ctx.author.mention}, please suppy an argument to reversecaps!")
		return

	await ctx.send(f"{ctx.author.mention}, here is your reversecaps:\n{text.swapcase()}")

#---------------------------Evaluate-------------------------------#

@client.command(name="evaluate",description="evaluates some provided python code!",aliases=["e","eval"])
async def evaluate(ctx, *, code=None):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, you can't use this command!")
		return
	if code == None:
		await ctx.send(f"Please supply some code!")
		return

	str_obj = io.StringIO() #Retrieves a stream of data
	try:
		with contextlib.redirect_stdout(str_obj):
			exec(code)
	except Exception as e:
		return await ctx.send(f"{ctx.author.mention}, An exception occured!\n```{e.__class__.__name__}: {e}```")
	if str_obj.getvalue() == "":
		await ctx.send(f'{ctx.author.mention}, the run completed succesfully with no output!')
	else:
		try:
			await ctx.send(f'{ctx.author.mention}, the run completed succesfully, heres the output:\n```{str_obj.getvalue()}```')
		except discord.errors.HTTPException:
			await ctx.send(f"{ctx.author.mention}, the run completed succesfully but the output was too long to send!")


#--------------------------Bumpscore--------------------------#

@client.command(name="bumpscore", description="gets the bumpscore of you or someone else")
async def bumpscore(ctx, person : discord.Member = None):
	if person == None:
		curScore = scoreDictMod("one",ctx.author.id,0)

		if curScore == 0:
			await ctx.send("You haven't bumped disboard yet!")
		else:
			await ctx.send(f"Your current bump score is `{curScore}`")

	else:
		curScore = scoreDictMod("one",person.id)

		if curScore == 0:
			await ctx.send(f"{person} hasn't bumped disboard yet!")
		else:
			await ctx.send(f"{person}'s current bump score is `{curScore}`")

@bumpscore.error
async def bumpscore_error(ctx, error):
	if isinstance(error, commands.errors.BadArgument):
		await ctx.send("That's not a valid member!")

#-------------------------Top bumpscore----------------------------#

def getTopDict(dictionary, num=10000000000000000):
	topx = nlargest(num, dictionary, key=dictionary.get)
	returnList = []
	for key in topx:
		returnList.append((key, dictionary[key]))
	return returnList

@client.command(name="topbumpscore", description="gets the top bumpers")
async def topbumpscore(ctx):
	topbumps = getTopDict(scoreDict, 10)
	printstring=""

	message = await ctx.send("Getting the top 10 bumpers...")

	for num, x in enumerate(topbumps):
		user = await client.fetch_user(x[0])
		username = f"{user.name}#{user.discriminator}"



		if int(x[1]) == 69:
			if num >= 9:
				printstring += f"{num+1})   {username} — {x[1]} — Nice.\n"
			else:
				printstring += f"{num+1})    {username} — {x[1]} — Nice.\n"

		elif int(x[1]) == 420:
			if num >= 9:
				printstring += f"{num+1})   {username} — {x[1]} — Blaze it!.\n"
			else:
				printstring += f"{num+1})    {username} — {x[1]} — Blaze it!.\n"
		else:
			if num >= 9:
				printstring += f"{num+1})   {username} — {x[1]}\n"
			else:
				printstring += f"{num+1})    {username} — {x[1]}\n"
			

	if printstring == "":
		await message.edit(content = f"{ctx.author.mention}, looks like nobody has bumped disboard!\n(this is strange, contact Joyte#0001 maybe?)")
		return

	await message.edit(content = f"{ctx.author.mention}, here are the top 10 bumpers:\n```{printstring}```")

#-----------------------Bumpscore json--------------------#

@client.command(name="dictjson", description="returns a dict in json format")
async def dictjson(ctx, whichDict=None):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, you can't use this command!")
		return

	#i'm genuinely sorry for this code
	beforetext = "Hey, just warning you there's no use for this command as it's not stored in json anymore, it's pickled.\n"

	if whichDict == "facesList":
		message = await ctx.send(f"{beforetext}Loading dict...")
		jsonText = json.dumps(facesList, indent=4)
		await message.edit(content = f"{beforetext}Faces list dict:```json\n{jsonText}```")

	elif whichDict == "facesAmount":
		message = await ctx.send(f"{beforetext}Loading dict...")
		jsonText = json.dumps(facesAmount, indent=4)
		await message.edit(content = f"{beforetext}Faces amount dict:```json\n{jsonText}```")

	elif whichDict == "pollDict":
		message = await ctx.send(f"{beforetext}Loading dict...")
		jsonText = json.dumps(pollDict, indent=4)
		await message.edit(content = f"{beforetext}Poll owner list dict:```json\n{jsonText}```")

	elif whichDict == "scoreDict":
		message = await ctx.send(f"{beforetext}Loading dict...")
		jsonText = json.dumps(scoreDict, indent=4)
		await message.edit(content = f"{beforetext}Bump score dict:```json\n{jsonText}```")

	else:
		await ctx.send("That's not a valid dict, please choose one of these:\n`facesList`\n`facesAmount`\n`pollDict`\n`scoreDict`")

#-----------------------Bumpscore pkl--------------------#

@client.command(name="dictpkl", description="returns a dict in pkl format")
async def dictpkl(ctx, whichDict=None):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, you can't use this command!")
		return

	beforetext = ""
	try:
		if whichDict == "facesList":
			message = await ctx.send(f"{beforetext}Loading dict...")
			pklText = pickle.dumps(facesList)
			dictName = "Faces list dict"
			await message.edit(content = f"{beforetext}{dictName}:```json\n{pklText}```")

		elif whichDict == "facesAmount":
			message = await ctx.send(f"{beforetext}Loading dict...")
			pklText = pickle.dumps(facesAmount)
			dictName = "Faces amount dict"
			await message.edit(content = f"{beforetext}{dictName}:```json\n{pklText}```")

		elif whichDict == "pollDict":
			message = await ctx.send(f"{beforetext}Loading dict...")
			pklText = pickle.dumps(pollDict)
			dictName = "Poll owner list dict"
			await message.edit(content = f"{beforetext}{dictName}:```json\n{pklText}```")

		elif whichDict == "scoreDict":
			message = await ctx.send(f"{beforetext}Loading dict...")
			pklText = pickle.dumps(scoreDict)
			dictName = "Bump score dict"
			await message.edit(content = f"{beforetext}{dictName}:```json\n{pklText}```")
			
		else:
			await ctx.send("That's not a valid dict, please choose one of these:\n`facesList`\n`facesAmount`\n`pollDict`\n`scoreDict`")
	except discord.errors.HTTPException:
		await message.delete()
		split_1, split_2 = pklText[:len(pklText)//2], pklText[len(pklText)//2:]
		try:
			await ctx.send(f"{beforetext}{dictName}:```\n{split_1}```")
			await ctx.send(f"```{split_2}```")
		except discord.errors.HTTPException:
			try:
				split_again1, split_again2 = split_1[:len(split_1)//2], split_1[len(split_1)//2:]
				split_again3, split_again4 = split_2[:len(split_2)//2], split_2[len(split_2)//2:]
				await ctx.send(f"{beforetext}{dictName}:```\n{split_again1}```")
				await ctx.send(f"```{split_again2}```")
				await ctx.send(f"```{split_again3}```")
				await ctx.send(f"```{split_again4}```")
			except discord.errors.HTTPException:
				await ctx.send("Sorry, but the data is too long to send!")

#-----------------------Add/Remove bumpscore--------------------#

@client.command(name="changebumpscore", description="changes the bumpscore of a user")
async def changebumpscore(ctx, amount = None, person : discord.Member = None):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, you can't use this command!")
		return
		
	if amount == None:
		await ctx.send(f"{ctx.author.mention}, Please supply an amount to change by!")
		return

	if person == None:
		if str(amount)[0] == "-":
			amount = stringPOP(amount,0)
			if amount.isnumeric():
				scoreDictMod("minus",ctx.author.id,int(amount))
				await ctx.send(f"Changed your bump score by -{amount}")
			else:
				await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")
		else:
			if amount.isnumeric():
				scoreDictMod("add",ctx.author.id,int(amount))
				await ctx.send(f"Changed your bump score by {amount}")
			else:
				await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")
	else:
		if str(amount)[0] == "-":
			amount = stringPOP(amount,0)
			if amount.isnumeric():
				scoreDictMod("minus",person.id,int(amount))
				await ctx.send(f"Changed {person}'s bump score by -{amount}")
			else:
				await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")
		else:
			if amount.isnumeric():
				scoreDictMod("add",person.id,int(amount))
				await ctx.send(f"Changed {person}'s bump score by {amount}")
			else:
				await ctx.send(f"{ctx.author.mention}, Please give a valid amount!")

@changebumpscore.error
async def changebumpscore_error(ctx, error):
	if isinstance(error, commands.errors.BadArgument):
		await ctx.send("That's not a valid member!")

#--------------------------Convert-------------------------#

#Number poll
@client.command(name="convert",description="Converts height!")
async def convert(ctx, text=None):
	if text == None:
		await ctx.send("Please convert either:\nFeet'inches to CM\nCM to Feet'inches\nMetres to CM")
		return

	convert = inch_cm(text)
	if convert != False:
		await ctx.send(f"{ctx.author.mention}, here is your conversion: {convert}")
	else:
		await ctx.send(f"{ctx.author.mention}, that's not a valid conversion!")

#--------------------------Random Face-------------------------#

#Get a random face and print it to discord.
@client.command(name="randomface",description="Gets a random face!")
async def randomface(ctx, person=None):
	try:
		if person == None: #Nobody specified
			printFaces = ""
			for person in facesList.keys():
				printFaces = (printFaces+"`"+person+"` **—** `"+str(facesAmount[person])+"`\n")
			await ctx.send(f"{ctx.author.mention}, Please specify a valid person!\nList:\n"+printFaces)
			return

		else: 
			if person in facesList: #we got him bois!
				fileName = (str(random.choice(range(1,facesAmount[person]+1)))+".png")
				validPicture = (os.getcwd()+"/faces/"+person+"/"+fileName)

				if fileName == "69.png":
					nice = " | Nice."
				else:
					nice = ""

				with open(validPicture, 'rb') as fp:
					await ctx.send(f"{ctx.author.mention}, Here's your picture! `{fileName}`{nice}",file=discord.File(fp, fileName))

			else: #Invalid person
				printFaces = ""
				for person in facesList:
					printFaces = (printFaces+"`"+person+"` **—** `"+str(facesAmount[person])+"`\n")

				await ctx.send(f"{ctx.author.mention}, Please specify a valid person!\nList:\n"+printFaces)
				return

	except FileNotFoundError:
		message = await ctx.send(f"{ctx.author.mention}, An error occured!")
		updateFaces(person)

		if os.path.exists(f"./faces/{person}/{fileName}"):
			await message.edit(content = f"{ctx.author.mention}, An error occured, but i've managed to fix it!")
			return

		if int(fileName[:-4]) > facesAmount[person]:
			await message.edit(content = f"{ctx.author.mention}, An error occured, but i've managed to fix it!")
			return

#--------------------------Addpic-------------------------#

#Adds a picture to either the faces command or the gifs.
@client.command(name="addpic",description="Adds a picture!")
async def addpic(ctx, type=None, person=None):
	if not int(ctx.author.id) in admins_ids:
		await ctx.send(f"{ctx.author.mention}, hey you can't use this command!")
		return

	if ctx.message.attachments == []:
		await ctx.send(f"{ctx.author.mention}, please use this command with an attached file!")
		return

	if type == None:
		await ctx.send(f"{ctx.author.mention}, please give a type!\n**List:**\n`gifs`\n`faces`")
		return

	if person == None:
		if type == "faces":
			await ctx.send(f"{ctx.author.mention}, please give a person to add the face to!")
		elif type == "gifs":
			await ctx.send(f"{ctx.author.mention}, please specify which type of gif this is!\n**List:**\n`marry`\n`kisses`\n`hugs`")
		else:
			await ctx.send(f"{ctx.author.mention}, please specify argument two!")
		return

	if not person.isalpha():
		await ctx.send(f"{ctx.author.mention}, please limit your person name to alphabetical characters only!")
		return

	if type == "faces":
		for file in ctx.message.attachments:
			try:
				await file.save(f"./faces/{person}/{facesAmount[person]+1}.png")
				await ctx.send(f"{ctx.author.mention}, Added the picture to the `{person}` folder!")
			except KeyError:
				try:
					os.mkdir(f"./faces/{person}")
					await file.save(f"./faces/{person}/1.png")
					await ctx.send(f"{ctx.author.mention}, Made the `{person}` folder, and added the picture to it!")
				except FileExistsError:
					await file.save(f"./faces/{person}/1.png")
					await ctx.send(f"{ctx.author.mention}, The `{person}` folder already existed without any pictures, so i just added the picture to it!")
		updateFaces(person)
	elif type == "gifs":
		if person in allGifs:
			for file in ctx.message.attachments:
				await file.save(f"./gifs/{person}/{gifsAmount[person]+1}.png")
				await ctx.send(f"{ctx.author.mention}, Added the gif to the `{person}` folder!")

		else:
			await ctx.send(f"{ctx.author.mention}, please specify a valid gif type!\n**List:**\n`marry`\n`kisses`\n`hugs`")
	else:
		await ctx.send(f"{ctx.author.mention}, that's not a valid type!\n**List:**\n`gifs`\n`faces`")

#------------------------Addpic history------------------#

#TODO:	This command, make it scan the last {amount} messages and
#		add them all to the {person} folder. there should be an
#		optional {replace} argument, where a backup of the {person}
#		folder is made, (with the timestamp and person as the name)
#		and everything is deleted and replaced with the attachments
#		provided using addpic-history.
#		format: .addpic-history <amount> <person> [replace]
#		or maybe add arguments onto the addpic command, with the format
#		.addpic <person> [<history> <amount> <replace>]
#		which would be better, as it is only one command
#		will decide later

#@client.command(name=".addpic_history",description="Adds the picture history to a person or face")
#async def addpic_history(ctx, person=None, amount=100, replace=None):
#	messagehistory = await ctx.channel.history(limit=amount,).flatten()

#--------------------------History------------------------#

@client.command()
async def history(ctx, limit: int = 100):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, hey you can't use this command!")
		return

	editmsg = await ctx.send(f"{ctx.author.mention}, getting the message history...")
	messages = await ctx.channel.history(limit=limit).flatten()

	try:
		with open(f"history-{ctx.channel.id}.txt", "a") as f:
			print(f"Requested {limit} lines by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})\n\n", file=f)
			for message in messages:
				print(f"#{message.channel.name} ({message.channel.id}): @{message.author.name}#{message.author.discriminator} ({message.author.id}): {message.content}", file=f)
	except ssl.SSLError:
		pass

	with open(f"history-{ctx.channel.id}.txt", "rb") as fp:
		await editmsg.edit(content = f"{ctx.author.mention}, here's the history of the channel, up to {limit}:")
		await ctx.send(file = discord.File(fp, f"history-{ctx.channel.id}.txt"))

	os.remove(f"history-{ctx.channel.id}.txt")

#---------------------Delface------------------------------#

#TODO: Convert to delpic

@client.command(name="delface",description="deletes a face")
async def delface(ctx, num, person=None):

	if not int(ctx.author.id) in admins_ids:
		await ctx.send(f"{ctx.author.mention}, hey you can't use this command!")
		return

	if person == None:
		await ctx.send(f"{ctx.author.mention}, please give a person to delete the face of!")
		return

	if not person.isalpha():
		await ctx.send(f"{ctx.author.mention}, please limit your person name to alphabetical characters only!")
		return

	if not num.isnumeric():
		await ctx.send(f"{ctx.author.mention}, please make the first argument a number!")
		return
	else:
		num = int(num)

	if num == 0:
		await ctx.send(f"{ctx.author.mention}, okay, i deleted no faces for you :)")
		return

	try:
		if num > facesAmount[person]:
			if facesAmount[person] == 1:
				await ctx.send(f"{ctx.author.mention}, {person} only has one face!")
				return
			else:
				await ctx.send(f"{ctx.author.mention}, {person} only has {facesAmount[person]} faces!")
			return

		if not os.path.exists(f"./faces/{person}/{num}.png"):
			if num == facesAmount[person]:
				await ctx.send(f"{ctx.author.mention}, this file has already been deleted, contact <@246862123328733186> to help!\ndebug info:\nperson: {person}\nnum: {num}")
				print(f"{errorcharacter}file already deleted, debug info:\nperson: {person}\nnum: {num}\nfaces list:{facesList[person]}{resetcharacter}")
				return

			await ctx.send(f"{ctx.author.mention}, this file has already been deleted, but i'll try to fix the corruption!")
			if os.path.exists(f"./faces/{person}/{facesAmount[person]}.png"):
				if num == facesAmount[person]:
					updateFaces(person)
					await ctx.send("Okay, i've fixed it!")
					return

				copyfile(f"./faces/{person}/{facesAmount[person]}.png",f"./faces/{person}/{num}.png")
				os.remove(f"./faces/{person}/{facesAmount[person]}.png")
				await ctx.send(f"Hopefully i've fixed it!")
				updateFaces(person)
				return

			else:
				await ctx.send(f"I couldn't fix it, but contact <@246862123328733186> to help!\ndebug info:\nperson: {person}\nnum: {num}")
				print(f"{errorcharacter}file already deleted, debug info:\nperson: {person}\nnum: {num}\nfaces list:{facesList[person]}{resetcharacter}")
				return

		if facesAmount[person] == 1:
			os.remove(f"./faces/{person}/{num}.png")
			os.rmdir(f"./faces/{person}")
			await ctx.send(f"{ctx.author.mention}, deleted `{person}`'s folder!")
			updateFaces(person)
			return

		if num == facesAmount[person]:
			os.remove(f"./faces/{person}/{num}.png")
			await ctx.send(f"{ctx.author.mention}, deleted `{person}`'s `{num}.png`!")
			updateFaces(person)
			return

		os.remove(f"./faces/{person}/{num}.png")
		copyfile(f"./faces/{person}/{facesAmount[person]}.png",f"./faces/{person}/{num}.png")
		os.remove(f"./faces/{person}/{facesAmount[person]}.png")

		await ctx.send(f"{ctx.author.mention}, deleted `{person}`'s `{num}.png`!")
		updateFaces(person)
		return

	except KeyError:
		await ctx.send(f"{ctx.author.mention}, that's not a valid person!")
		return
#--------------------------update all-------------------------#

@client.command(name="updateall",description="Updates all the faces")
async def updateallfaces(ctx):
	if not int(ctx.author.id) in admins_ids:
		await ctx.send(f"{ctx.author.mention}, hey you can't use this command!")
		return

	message = await ctx.send(f"{ctx.author.mention}, updating all the faces and gifs...")
	updateFaces()
	updateGifs()
	await message.edit(content = "Faces updated!")

#--------------------------Marry command-------------------------#

#TODO: finish this

"""
@client.command(name="marry", description="give someone a marry (what's a english)")
async def marry(ctx, person : discord.Member = None):
	await ctx.send("nothing :)")

@kiss.error
async def marry_error(ctx, error):
	if isinstance(error, commands.errors.BadArgument):
		await ctx.send("That's not a valid member!")
"""

#--------------------------Kiss command-------------------------#

@client.command(name="kiss", description="give someone a kiss")
async def kiss(ctx, person : discord.Member = None):
	if person == None:
		await ctx.send("I need to know who you are kissing!")
		return
	if person.id == ctx.author.id:
		await ctx.send("You can't kiss yourself!")
		return
	random_gif = randomGif("kisses")
	fileName = f"./gifs/kisses/{random_gif}"
	with open(fileName, 'rb') as fp:
		await ctx.send(f"{ctx.author.mention} has kissed {person.mention}",file=discord.File(fp, fileName))

@kiss.error
async def kiss_error(ctx, error):
	if isinstance(error, commands.errors.BadArgument):
		await ctx.send("That's not a valid member!")

#--------------------------Hug command-------------------------#

@client.command(name="hug", description="give someone a hug")
async def hug(ctx, person : discord.Member = None):
	if person == None:
		await ctx.send("I need to know who you are hugging!")
		return
	if person.id == ctx.author.id:
		await ctx.send("You can't hug yourself!")
		return
	random_gif = randomGif("hugs")
	fileName = f"./gifs/hugs/{random_gif}"
	with open(fileName, 'rb') as fp:
		await ctx.send(f"{ctx.author.mention} has hugged {person.mention}",file=discord.File(fp, fileName))

@hug.error
async def hug_error(ctx, error):
	if isinstance(error, commands.errors.BadArgument):
		await ctx.send("That's not a valid member!")

#--------------------------Polls-------------------------#

#Yes/No poll
@client.command(name="yesnopoll",description="Makes a yes no poll!",aliases=["yesnovote"])
async def yesnopoll(ctx, *, question=None):
	await ctx.message.delete()
	if question == None:
		error = await ctx.send(f"{ctx.author.mention}, Please supply arguments!\nExample:\t`.numberpoll This is the question`")
		await error.add_reaction(cross)
		pollDictMod("add",ctx.author.id,error.id)
		return

	poll = await ctx.send(f"{ctx.author.mention} wants to know:\n**Yes/No** `{question}`")
	for reaction in ynpoll:
		await poll.add_reaction(reaction)
	pollDictMod("add",ctx.author.id,poll.id)

#Spacify
@client.command(name="spacify",description="Spacifies")
async def spacify(ctx, *, text):
	spacedText = spacifyFunction(text)
	await ctx.send(f"{ctx.author.mention}, here is your message:\n{spacedText}")

#Number poll
@client.command(name="numberpoll",description="Makes a number poll!",aliases=["numbervote"])
async def numberpoll(ctx, *, text=None):
	await ctx.message.delete()
	if text == None:
		error = await ctx.send(f"{ctx.author.mention}, Please supply arguments!\nExample:\t`.numberpoll This is the question, This is answer one, This is answer two, etc`")
		await error.add_reaction(cross)
		pollDictMod("add",ctx.author.id,error.id)
		return

	split = text.split(",")

	if len(split) == 1:
		error = await ctx.send(f"{ctx.author.mention}, Please supply some answers, not just the question!\n`{text}`")
		await error.add_reaction(cross)
		pollDictMod("add",ctx.author.id,error.id)
		return

	if len(split) > 11:
		error = await ctx.send(f"{ctx.author.mention}, Please limit your poll to 10 options or less!\n`{text}`")
		await error.add_reaction(cross)
		pollDictMod("add",ctx.author.id,error.id)
		return

	popsplit = []
	for string in split:
		beforepop = string
		while string[0] == " ":
			string = stringPOP(string,0)

		while string[len(string)-1] == " ":
			string = stringPOP(string,len(string)-1)
		
		popsplit.append(string)

	header = popsplit[0]
	popsplit.pop(0)

	sendmessage = f"{ctx.author.mention} asks `{header}`:\n"
	curnum = 1
	for string in popsplit:
		if curnum == len(popsplit)+1:
			break
		sendmessage = sendmessage + f"{numpoll[curnum]} — {string}\n"
		curnum += 1

	poll = await ctx.send(sendmessage)

	curnum = 1
	for string in popsplit:
		if curnum == len(popsplit)+1:
			break
		await poll.add_reaction(numpoll[curnum])
		curnum += 1

	await poll.add_reaction(cross)

	pollDictMod("add",ctx.author.id,poll.id)

#Remove if x
@client.event
async def on_reaction_add(reaction, user):
	if str(reaction.emoji) == cross:
		state = pollDictMod("remove",user.id,reaction.message.id)
		if state == True:
			await reaction.message.delete()

#--------------------------------------Say----------------------------------#

@client.command(name="say", description="says something from the bot's perspective")

async def say(ctx, *, saying):
	if not ctx.author.id in admins_ids:
		await ctx.send(f"{ctx.author.mention}, Nice try Buddy.")
		return
	await ctx.message.delete()
	await ctx.send(saying)
#------------------------------Final bootstrap------------------------------------#

print(f"{resetcharacter}Booting up...")

#Update the faces
updateFaces()
if facesAmount != {}:
	print("\nLoaded faces:\n")
	for person in facesList:
		printPerson(person,str(facesAmount[person]))
	print("\n")

#Updating gifs
print("Updating gifs...")
updateGifs()
if gifsAmount != {}:
	print("\nLoaded gifs:\n")
	for gif in gifsList:
		printPerson(gif,str(gifsAmount[gif]))
	print("\n")


#Load the bumpscores
if os.path.exists("./data/bumpscores.pkl"):
	#try:
	print("Loading pickle bump scores...")
	try:
		with open('./data/bumpscores.pkl', 'rb') as fp:
			scoreDict = pickle.load(fp)
	except (EOFError, pickle.UnpicklingError):
		print(f"{errorcharacter}Pickle decoder error, the pkl file has been reset, and a backup has been made.{resetcharacter}")
		copyfile("./data/bumpscores.pkl", f"./data/bumpscores.pkl.{datetime.utcnow()}")
		os.remove("./data/bumpscores.pkl")


#------------------------------------Log into discord-------------------------------------#
print("Logging into discord...")
client.run(botToken)