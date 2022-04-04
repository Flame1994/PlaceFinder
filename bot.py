# bot.py
import os

import discord
import asyncio
from PIL import Image
import requests
from io import BytesIO
import random
import math
from dotenv import load_dotenv
from discord.ext import commands
from math import sqrt

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

IGNORE_COLOR = (217, 0, 255)

COLORS = (
    (109, 0, 26), # burgundy
    (190, 0, 57), # dark red
    (255, 69, 0), # red
    (255, 168, 0), # orange
    (255, 214, 53), # yellow
    (255, 248, 184), # pale yellow
    (0, 163, 104), # dark green
    (0, 204, 120), # green
    (126, 237, 86), # light green
    (0, 117, 111), # dark teal
    (0, 158, 170), # teal
    (0, 204, 192), # light teal
    (36, 80, 164), # dark blue
    (54, 144, 234), # blue
    (81, 233, 244), # light blue
    (73, 58, 193), # indigo
    (106, 92, 255), # periwinkle
    (148, 179, 255), # lavender
    (129, 30, 159), # dark purple
    (180, 74, 192), # purple
    (228, 171, 255), # pale purple
    (222, 16, 127), # magenta
    (255, 56, 129), # pink
    (255, 153, 170), # light pink
    (109, 72, 47), # dark brown
    (156, 105, 38), # brown
    (255, 180, 112), # beige
    (0, 0, 0), # black
    (81, 82, 82), # dark gray
    (137, 141, 144), # gray
    (212, 215, 217), # light gray
    (255, 255, 255), # white
)

map_colors = {
    (109, 0, 26): 'Burgundy',
    (190, 0, 57): 'Dark Red',
    (255, 69, 0): 'Red',
    (255, 168, 0): 'Orange',
    (255, 214, 53): 'Yellow',
    (255, 248, 184): 'Pale Yellow',
    (0, 163, 104): 'Dark Green',
    (0, 204, 120): 'Green',
    (126, 237, 86): 'Light Green',
    (0, 117, 111): 'Dark Teal',
    (0, 158, 170): 'Teal',
    (0, 204, 192): 'Light Teal',
    (36, 80, 164): 'Dark Blue',
    (54, 144, 234): 'Blue',
    (81, 233, 244): 'Light Blue',
    (73, 58, 193): 'Indigo',
    (106, 92, 255): 'Periwinkle',
    (148, 179, 255): 'Lavender',
    (129, 30, 159): 'Dark Purple',
    (180, 74, 192): 'Purple',
    (228, 171, 255): 'Pale Purple',
    (222, 16, 127): 'Magenta',
    (255, 56, 129): 'Pink',
    (255, 153, 170): 'Light Pink',
    (109, 72, 47): 'Dark Brown',
    (156, 105, 38): 'Brown',
    (255, 180, 112): 'Beige',
    (0, 0, 0): 'Black',
    (81, 82, 82): 'Dark Gray',
    (137, 141, 144): 'Gray',
    (212, 215, 217): 'Light Gray',
    (255, 255, 255): 'White',
}

def ignore_color(r, g, b):
    return (r, g, b) == IGNORE_COLOR

def count_ignore_colors(rgb_im, width, height):
    counter = 0
    for y in range (0, height):
        for x in range (0, width):
            if rgb_im.getpixel((x, y)) == IGNORE_COLOR:
                counter = counter + 1
    return counter

def closest_color(r, g, b):
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def get_colour_name(rgb):
    return map_colors[rgb]

@bot.command(name='test')
async def place(ctx, x1, y1, x2, y2, image, seconds=60):
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

        response = requests.get(image)
        img = Image.open(BytesIO(response.content))

        ImageWidth, ImageHeight = img.size
        rgb_im = img.convert('RGB')
        count = count_ignore_colors(rgb_im, ImageWidth, ImageHeight)
        size = size - count

        if width != ImageWidth:
            await ctx.send('Image width ({}) does not fit into specified grid width ({})'.format(ImageWidth, width))

        elif height != ImageHeight:
            await ctx.send('Image height ({}) does not fit into specified grid height ({})'.format(ImageHeight, height))

        else:
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

                for y in range (y1, y2):
                    for x in range(x1, x2):
                        if not users:
                            break
                        r, g, b = rgb_im.getpixel((x % x1, y % y1))
                        if not ignore_color(r, g, b):
                            u = users.pop()
                            rgb = closest_color(r,g,b)
                            color_name = get_colour_name(rgb)
                            await ctx.send(u.mention + ' place "{}" on assigned pixel [{},{}]: https://www.reddit.com/r/place/?cx='.format(color_name, x, y) + str(x) + '&cy=' + str(y))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
