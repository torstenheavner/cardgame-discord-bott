import asyncio as a
import random as r
import json
import sys
import os
from discord.ext import commands
from datetime import datetime
from time import *


def clear(): return os.system("cls")


sys.path.append("T:/all")
# client = discord.Client()
bot = commands.Bot(command_prefix = "c.")
suits = ["diamonds", "clubs", "hearts", "spades"]
types = "ace two three four five six seven eight nine ten jack queen king".split(" ")
deck = []
data = {
	"inplay": [],
	"hands": {}
}
for suit in suits:
	for type in types:
		deck.append("%s of %s" % (type, suit))


@bot.event
async def on_ready():
	clear()
	print("\n\ncard time\n\n")


# @bot.command()
# async def commands(ctx):
# 	global deck, data
# 	await ctx.send("""\
# **c.help** - this
# **c.showdeck** - Show the top ten cards in the deck/draw pile.
# **c.showinplay** - Show the top ten cards that have been played previously.
# **c.showhand** - Show your hand.
# **c.shuffle** - Shuffle the deck/draw pile.
# **c.draw <amount>** - Draw some amount of cards from the deck/draw pile. Amount is 1 by default.
# **c.play [card]** - Play some card from your hand.
# """)


@bot.command()
async def showdeck(ctx):
	global deck, data
	outputarray = []
	for num in range(10):
		outputarray.append(deck[num])
	await ctx.send("**Top Ten Cards of the Deck:**\n%s" % "\n".join(outputarray))


@bot.command()
async def showinplay(ctx):
	global deck, data
	outputarray = []
	for num in range(10):
		try:
			outputarray.append(data["inplay"][num])
		except:
			break
	await ctx.send("**Top Ten Cards In Play:**\n%s" % "\n".join(outputarray))


@bot.command()
async def showhand(ctx):
	global deck, data
	try:
		await ctx.send("**%s's Hand:**\n%s" % (ctx.author.name, "\n".join(data["hands"][ctx.author.id])))
	except:
		await ctx.send("You have to draw some cards first!")


@bot.command()
async def shuffle(ctx):
	global deck, data
	r.shuffle(deck)
	await ctx.send("Deck shuffled!")


@bot.command()
async def draw(ctx, arg="1"):
	global deck, data
	arg = int(arg)
	try:
		data["hands"][ctx.author.id].append("")
		data["hands"][ctx.author.id] = data["hands"][ctx.author.id][:-1]
	except:
		data["hands"][ctx.author.id] = []
	i = 0
	for num in range(arg+1):
		i = num
		try:
			data["hands"][ctx.author.id].append(deck[num])
		except:
			break
	deck = deck[i:]
	await ctx.send("**%s** drew **%s** card(s). The deck now has %s card(s) left." % (ctx.author.name, i, len(deck)))


@bot.command()
async def play(ctx, *, arg=""):
	global deck, data
	if arg == "":
		await ctx.send("You must specify what card you want to play!")
	else:
		try:
			if arg in data["hands"][ctx.author.id]:
				data["inplay"].insert(0, arg)
				data["hands"][ctx.author.id].remove(arg)
				await ctx.send("**%s** played a **%s**!" % (ctx.author.name, arg))
				await ctx.message.delete()
			else:
				await ctx.send("You dont have that card!")
		except:
			await ctx.send("You have to draw some cards first!")



with open("T:/all/cardtoken.txt", "r") as token:
    bot.run(token.read())
