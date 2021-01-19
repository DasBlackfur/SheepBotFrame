import os
import sys
import yaml
import discord
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

with open("config.yml", "r") as file:
    config = yaml.load(file)

bot = discord.Client()

tasks = [False, False]
finished = False


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
        with open(f"chatlogs/{log}", "r") as logfile:
            log = yaml.load(logfile)
        listtrainer.train(log)


@bot.event
async def on_ready():
    global chatbot
    print("Logged in!")
    args = sys.argv
    args.pop(0)
    for arg in args:
        if arg == "--help" or arg == "-?":
            printhelp()
            await bot.close()
            raise SystemExit(0)
        elif arg == "--version" or arg == "-v":
            printversion()
            await bot.close()
            raise SystemExit(0)
        elif arg == "--download" or arg == "-d":
            tasks[0] = True
        elif arg == "--train" or arg == "-t":
            tasks[1] = True
        else:
            print(f"Unexspected {arg}")
            printhelp()
            await bot.close()
            raise SystemExit(1)
    if tasks[0]:
        await download()
        print("Finished download!")
    if tasks[1]:
        os.system("rm db.sqlite3")
        chatbot = ChatBot(config["botname"])
        await train()
        print("Finished train!")
    else:
        chatbot = ChatBot(config["botname"])

bot.run(config["token"])
