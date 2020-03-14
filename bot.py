#bot.py
import os
import time
import random
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands

messages = 0

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))

# bot = commands.Bot(command_prefix='!')
# bot.run(TOKEN)

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages
    while not client.is_closed():  
        try:
            with open("stats.txt", "a") as f:
                f.write(f"{time.time()}, Messages: {messages}\n")
                messages = 0

            await asyncio.sleep(120)
        except Exception as e:
            print(e)
            await asyncio.sleep(120)

@client.event
async def on_message(message):
    global messages
    messages += 1
    guild = client.get_guild(GUILD)
    channels = ["bot-spam"]
    bad_words = ['clout']

    for word in bad_words:  
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)      

    def returnCommandChannel():
        for channel in guild.channels:
            if channel.name=='bot-spam':
                return channel
                

    if str(message.channel) not in channels and message.content.startswith('!'):
        print('command posted in non-command channel')
        await message.channel.purge(limit=1)
        await message.channel.send(f'> {message.author.mention}\n> Please type your botcommands in the {returnCommandChannel().mention} channel\n> This message will self-destruct in 10 seconds!')
        await asyncio.sleep(10)
        await message.channel.purge(limit=1)
        


    if str(message.channel) in channels:
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi")
        elif message.content == "!users":
            await message.channel.send(f"# of Members {guild.member_count}")
        elif message.content == "!help":
            embed = discord.Embed(title='Help on bot', description='Some useful commands')
            embed.add_field(name='!hello', value="Greets the user")
            embed.add_field(name='!users', value="Prints number of users")
            await message.channel.send(embed=embed)

@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("recon") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="FORBIDDEN NAME")



client.loop.create_task(update_stats())

client.run(TOKEN)