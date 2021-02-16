import os
import sys
import yaml
import discord
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

with open("config.yml", "r") as file:
    config = yaml.load(file)

bot = discord.Client()

tasks = [False, False]
finished = False


def printhelp():
    printversion()
    print("Thanks for using SheepBotFrame!")
    print("Possible command options:")
    print("--help     (-?) Displays this help page")
    print("--version  (-v) Displays the version")
    print("--download (-d) Adds downloading chatlogs to the task list")
    print("--train    (-t) Added training to the task list")


def printversion():
    print("SheepBotFrame Beta 1.49")


def remove_mention(m, s, i):
    if m == "s":
        return s[0:i] + s[i + 21:]
    elif m == "l":
        return s[:i] + s[i + 22:]


async def download():
    print("Starting download...")
    await bot.change_presence(activity=discord.Game(name=" downloading Message History"))
    os.system("rm chatlogs/*.tmp.yml")
    for trainchannel in config["trainchannels"]:
        channel = await bot.fetch_channel(trainchannel[0])
        to_fetch = trainchannel[1]
        messages = [""] * to_fetch
        counter = 0
        latest = datetime.datetime.now()
        while to_fetch > 0:
            print(f"{trainchannel[1]-to_fetch}/{trainchannel[1]} Messages Downloaded", end='\r')
            async for message in channel.history(limit=500, before=latest):
                if message.content is None:
                    print("Found Null message, skipping...")
                else:
                    messages[counter] = message.content
                counter += 1
                latest = message.created_at
            to_fetch -= 1000
        messages.reverse()
        with open("chatlogs/"+ str(trainchannel[0])+".tmp.yml", "w") as logfile:
            yaml.dump(messages, logfile)
        # channel = await bot.fetch_channel(trainchannel[0])
        # counter = 0
        # messages = [None] * trainchannel[1]
        # async for message in channel.history(limit=trainchannel[1]):
        #     if message.content is None:
        #         print("Found Null message, ignoring...")
        #     else:
        #         messages[counter] = message.content
        #     counter += 1
        # messages.reverse()
        # with open("chatlogs/" + str(trainchannel[0]) + ".tmp.yml", "w") as logfile:
        #     yaml.dump(messages, logfile)


async def train():
    print("Starting training...")
    await bot.change_presence(activity=discord.Game(name=" training, training and training..."))
    corpustrainer = ChatterBotCorpusTrainer(chatbot)
    listtrainer = ListTrainer(chatbot)
    for corpus in config["corpus"]:
        corpustrainer.train(corpus)
    for log in os.listdir("chatlogs"):
        with open(f"chatlogs/{log}", "r") as logfile:
            log = yaml.load(logfile)
        listtrainer.train(log)


async def startup():
    global chatbot
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
    global finished
    finished = True
    print("Starting to listen to messages...")
    await bot.change_presence(activity=discord.Game(name=" listening for messages!"))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=" listening for messages!"))
    print("Logged in!")
    if not finished:
        await startup()


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.channel.id in config["usechannels"]:
            if message.content.startswith(config["excludeprefix"]):
                return
            else:
                if finished:
                    response = chatbot.get_response(message.content)
                    response = response.__str__()
                    if config["filterpings"]:
                        position = response.find("<@!")
                        while position != -1:
                            response = remove_mention("l", response, position)
                            position = response.find("<@!")
                        position = response.find("<@")
                        while position != -1:
                            response = remove_mention("s", response, position)
                            position = response.find("<@")
                    await message.channel.send(response)
                    print(f"Input was given: '{message.content}', this output was found: '{response}'")
                else:
                    await message.channel.send("Sorry, the Bot is still performing some tasks.")


bot.run(config["token"])
