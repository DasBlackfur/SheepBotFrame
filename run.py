import discord

file = open("TOKEN", "r")
token = file.read()
file.close()

bot = discord.Client()

bot.run(token)