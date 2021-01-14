import os
import sys
import yaml
import discord
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

# Checks two
# Change this to set the settings
config = {"botname": "Sheepy",
          "filterpings": True,
          "usechannels": [717758904527880253, 772839872557088769, 773980809471197235],
          "trainchannels": [[492412566430154783, 1000], [761462125696385047, 1000]],
          "corpus": ["chatterbot.corpus.english"]}

with open("token", "r") as tokenfile:
    token = tokenfile.read()

bot = discord.Client()

tasks = [False, False]


def printhelp():
    print("Help lol")


def printversion():
    print("Somer Version")


async def download():
    await bot.change_presence(activity=discord.Game(name=" downloading Message History"))
    os.system("rm chatlogs/*.tmp.yml")
    for trainchannel in config["trainchannels"]:
        channel = await bot.fetch_channel(trainchannel[0])
        counter = 0
        messages = [None] * trainchannel[1]
        async for message in channel.history(limit=trainchannel[1]):
            messages[counter] = message.content
            counter += 1
        messages.reverse()
        with open("chatlogs/" + str(trainchannel[0]) + ".tmp.yml", "w") as logfile:
            yaml.dump(messages, logfile)


async def train():
    corpustrainer = ChatterBotCorpusTrainer(chatbot)
    listtrainer = ListTrainer(chatbot)
    for corpus in config["corpus"]:
        corpustrainer.train(corpus)
    for log in os.listdir("chatlogs"):
        with open(log, "r") as logfile:
            log = yaml.load(logfile)
        listtrainer.train(log)


@bot.event
async def on_ready():
    print("Logged in!")
    args = sys.argv
    args.pop(0)
    for arg in args:
        if arg == "--help" or arg == "-?":
            printhelp()
            await bot.close()
            raise SystemExit(0)
        if arg == "--version" or arg == "-v":
            printversion()
            await bot.close()
            raise SystemExit(0)
        if arg == "--download" or arg == "-d":
            tasks[0] = True
        if arg == "--train" or arg == "-t":
            tasks[1] = True
        else:
            print(f"Unexspected {arg}")
            printhelp()
            await bot.close()
            raise SystemExit(1)
    if tasks[0]:
        await download()
    if tasks[1]:
        os.system("rm db.sqlite3")
        global chatbot
        chatbot = ChatBot(config["botname"])
        await train()
    else:
        chatbot = ChatBot(config["botname"])

bot.run(token)
