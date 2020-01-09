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
	"players": [],
	"hands": {}
}
for suit in suits:
	for type in types:
		deck.append("%s of %s" % (type, suit))


@bot.event
async def on_ready():
	clear()
	print("\n\ncard time\n\n")


@bot.command(brief="Show top 10 cards in the deck")
async def showdeck(ctx):
	global deck, data
	outputarray = []
	for num in range(10):
		outputarray.append(deck[num])
	await ctx.send("**Top Ten Cards of the Deck:**\n%s" % "\n".join(outputarray))


@bot.command(brief="Show last 10 cards that were played")
async def showinplay(ctx):
	global deck, data
	outputarray = []
	for num in range(10):
		try:
			outputarray.append(data["inplay"][num])
		except:
			break
	await ctx.send("**Top Ten Cards In Play:**\n%s" % "\n".join(outputarray))


@bot.command(brief="Show your hand (works in DMs)")
async def showhand(ctx):
	global deck, data
	try:
		await ctx.send("**%s's Hand:**\n%s" % (ctx.author.name, "\n".join(data["hands"][ctx.author.id])))
	except:
		await ctx.send("You have to draw some cards first!")


@bot.command(brief="Shuffle the deck")
async def shuffle(ctx):
	global deck, data
	r.shuffle(deck)
	await ctx.send("Deck shuffled!")
	await ctx.message.delete()


@bot.command(brief="Draw some amount of cards", usage="<amount>")
async def draw(ctx, arg="1"):
	global deck, data
	arg = int(arg)
	try:
		data["hands"][ctx.author.id].append("")
		data["hands"][ctx.author.id] = data["hands"][ctx.author.id][:-1]
	except:
		data["hands"][ctx.author.id] = []
	i = 0
	for num in range(arg):
		i = num
		try:
			data["hands"][ctx.author.id].append(deck[num])
		except:
			break
	deck = deck[i+1:]
	await ctx.send("**%s** drew **%s** card(s). The deck now has %s card(s) left." % (ctx.author.name, i+1, len(deck)))
	await ctx.message.delete()


@bot.command(brief="Reset the game")
async def reset(ctx):
	global deck, data
	suits = ["diamonds", "clubs", "hearts", "spades"]
	types = "ace two three four five six seven eight nine ten jack queen king".split(" ")
	deck = []
	data = {
		"inplay": [],
		"players": [],
		"hands": {}
	}
	for suit in suits:
		for type in types:
			deck.append("%s of %s" % (type, suit))
	await ctx.send("Deck reset!")
	await ctx.message.delete()


@bot.command(brief="Play some card in your hand", usage="[card]")
async def play(ctx, *, arg=""):
	global deck, data
	if arg == "":
		try:
			data["inplay"].insert(0, data["hands"][ctx.author.id][0])
			await ctx.send("**%s** played a **%s**!" % (ctx.author.name, data["hands"][ctx.author.id][0]))
			data["hands"][ctx.author.id].pop(0)
			await ctx.message.delete()
		except:
			await ctx.send("You have to draw some cards first!")
	else:
		if len(arg.split(", ")) == 1:
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
		else:
			args = arg.split(", ")
			cardsplayed = []
			await ctx.send("Playing multiple cards at a time is WIP!")


@bot.command(brief="Take the play pile")
async def take(ctx):
	global deck, data
	try:
		for card in data["inplay"]:
			data["hands"][ctx.author.id].append(card)
		data["inplay"] = []
		await ctx.send("**%s** took the entire in play pile!" % ctx.author.name)
		await ctx.message.delete()
	except:
		await ctx.send("Something went wrong -- maybe theres nothing in the play pile? Or you havent drawn any cards yet.")


@bot.command(brief="Show the amounts of cards left", usage="[all, piles, hands, or hand]")
async def count(ctx, type="all"):
	global deck, data
	if type == "all":
		deckcount = 0
		inplaycount = 0
		hands = ""
		for card in deck:
			deckcount += 1
		for card in data["inplay"]:
			inplaycount += 1
		for key in data["hands"]:
			handcount = 0
			for card in data["hands"][key]:
				handcount += 1
			hands = hands + "\n**%s:** %s cards" % (ctx.guild.get_member(key).name, handcount)
		await ctx.send("**Deck:** %s cards\n**In Play:** %s cards\n\n__**Hands:**__%s" % (deckcount, inplaycount, hands))
	elif type == "piles":
		deckcount = 0
		inplaycount = 0
		for card in deck:
			deckcount += 1
		for card in data["inplay"]:
			inplaycount += 1
		await ctx.send("**Deck:** %s cards\n**In Play:** %s cards" % (deckcount, inplaycount))
	elif type == "hands":
		hands = ""
		for key in data["hands"]:
			handcount = 0
			for card in data["hands"][key]:
				handcount += 1
			hands = hands + "\n**%s:** %s cards" % (ctx.guild.get_member(key).name, handcount)
		await ctx.send("__**Hands:**__%s" % (hands))
	elif type == "hand":
		handcount = 0
		for card in data["hands"][ctx.author.id]:
			handcount += 1
		await ctx.send("**%s's Hand:** %s cards" % (ctx.author.name, handcount))
	else:
		await ctx.send("Please use either all, piles, hands, or hand as an argument.")


@bot.command(brief="Find out how poopy jonathan is")
async def poopmeter(ctx):
	await ctx.send("Jonathan is %s percent poopy" % r.randint(75, 1200))


@bot.command(brief="Move a card from your hand to the bottom of the deck", usage="[card]")
async def discard(ctx, *, arg=""):
	global deck, data
	if arg == "":
		try:
			deck.insert(len(deck), data["hands"][ctx.author.id][0])
			await ctx.send("**%s** discarded a **%s**!" % (ctx.author.name, data["hands"][ctx.author.id][0]))
			data["hands"][ctx.author.id].pop(0)
			await ctx.message.delete()
		except:
			await ctx.send("You have to draw some cards first!")
	else:
		try:
			if arg in data["hands"][ctx.author.id]:
				deck.insert(len(deck), arg)
				data["hands"][ctx.author.id].remove(arg)
				await ctx.send("**%s** discarded a **%s**!" % (ctx.author.name, arg))
				await ctx.message.delete()
			else:
				await ctx.send("You dont have that card!")
		except:
			await ctx.send("You have to draw some cards first!")


@bot.command(brief="Move a card from your hand to the bottom of the in play pile", usage="[card]")
async def burn(ctx, *, arg=""):
	global deck, data
	if arg == "":
		try:
			data["inplay"].insert(len(data["inplay"]), data["hands"][ctx.author.id][0])
			await ctx.send("**%s** burned a **%s**!" % (ctx.author.name, data["hands"][ctx.author.id][0]))
			data["hands"][ctx.author.id].pop(0)
			await ctx.message.delete()
		except:
			await ctx.send("You have to draw some cards first!")
	else:
		try:
			if arg in data["hands"][ctx.author.id]:
				data["inplay"].insert(len(data["inplay"]), arg)
				data["hands"][ctx.author.id].remove(arg)
				await ctx.send("**%s** burned a **%s**!" % (ctx.author.name, arg))
				await ctx.message.delete()
			else:
				await ctx.send("You dont have that card!")
		except:
			await ctx.send("You have to draw some cards first!")


@bot.command(brief="Give a card from your hand to someone else", usage="[card], [person (id)]")
async def give(ctx, *, args):
	global deck, data
	try:
		args = args.split(", ")
		card = args[0]
		person = args[1].replace("<@!", "")
		person = int(person.replace(">", ""))
		try:
			if card in data["hands"][ctx.author.id]:
				data["hands"][person].insert(0, card)
				data["hands"][ctx.author.id].remove(card)
				await ctx.send("**%s** gave **%s** a **%s**!" % (ctx.author.name, ctx.guild.get_member(person).name, card))
				await ctx.message.delete()
			else:
				await ctx.send("You dont have that card!")
		except:
			await ctx.send("You have to draw some cards first!")
	except:
		await ctx.send("You have to use both arguments, seperated by a comma! Make sure you used the persons id, not their name.")


@bot.command(brief="Move some cards from the draw pile to the play pile", usage="<amount>")
async def show(ctx, arg="1"):
	global deck, data
	arg = int(arg)
	outputarray = []
	i = 0
	for num in range(arg):
		i = num
		try:
			data["inplay"].append(deck[num])
			outputarray.append(deck[num])
		except:
			break
	deck = deck[i+1:]
	await ctx.send("**%s** card(s) have been shown. They were:\n%s\n\nThe deck now has %s card(s) left." % (i+1, "\n".join(outputarray), len(deck)))


with open("T:/all/cardtoken.txt", "r") as token:
    bot.run(token.read())
