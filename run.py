import os
import sys
import yaml
import discord
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

config = {"botname": "Sheepy",
          "filterpings": True,
          "usechannels": [717758904527880253, 772839872557088769, 773980809471197235],
          "trainchannels": [[492412566430154783, 1000], [761462125696385047, 1000]],
          "corpus": ["chatterbot.corpus.english", "chatterbot.corpus.uswest"],
          "token": "NzU2NTgxNjQ0NTY3MTgzMzcw.X2T7kA.J7RthGGYMjgE_ZreLrGo2A3tCvg"}

file = open("token", "r")
token = file.read()
file.close()

bot = discord.Client()
chatbot = ChatBot(config["botname"])

tasks = [False, False]


def printhelp():
    print("Help lol")


def printversion():
    print("Somer Version")


async def download():
    for trainchannel in config["trainchannels"]:
        channel = await bot.fetch_channel(trainchannel[0])
        counter = 0
        messages = [None] * trainchannel[1]
        async for message in channel.history(limit=trainchannel[1]):
            messages[counter] = message.content
            counter += 1
        messages.reverse()


@bot.event
async def on_ready():
    print("Logged in!")
    args = sys.argv
    for arg in args:
        if arg == "--help" or "-?":
            printhelp()
            await bot.close()
        if arg == "--version" or "-v":
            printversion()
            await bot.close()
        if arg == "--download" or "-d":
            tasks[0] = True
        if arg == "--train" or "-t":
            tasks[1] = True
        else:
            print(f"Unexspected {arg}")
            printhelp()
            await bot.close()
    if tasks[0]:
        await download()


bot.run(token)
