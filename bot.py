# bot.py
import os

import discord
import asyncio
import random
import math
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.command(name='place')
async def place(ctx, x1, y1, x2, y2, seconds=60):
    if x2 < x1:
        await ctx.send('Second x coordinate can\'t be less than first x coordinate')

    elif y2 < y1:
        await ctx.send('Second y coordinate can\'t be less than first y coordinate')

    else:
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        width = x2 - x1 + 1
        height = y2 - y1 + 1
        size = width * height

        waiting = await ctx.send('Waiting for {} people to opt-in ({}s remaining). Coordinates set between {},{} and {},{}.'.format(size, seconds, x1, y1, x2, y2))
        reaction = "👍"
        await waiting.add_reaction(emoji=reaction)

        def check(reaction, user):
            return reaction.message == waiting and reaction.emoji ==  '👍' and waiting.author != user

        users = []
        completed = False
        while completed is False:
            try:
                reaction, user = await bot.wait_for('reaction_add', check=check, timeout=int(seconds))
                users.append(user)
            except asyncio.TimeoutError:
                completed = True

        userCount = len(users)

        if not users:
            await ctx.send('Unfortunately, no users opted in.')
        else:
            await ctx.send('{} / {} users opted in. Assigning pixels that I can...'.format(userCount, size))

            for x in range(x1, x2):
                for y in range (y1, y2):
                    if not users:
                        break
                    u = users.pop()
                    await ctx.send(u.mention + ' assigned pixel: https://www.reddit.com/r/place/?cx=' + str(x) + '&cy=' + str(y))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
