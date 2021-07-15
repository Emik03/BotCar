import discord
import glob
import json
import os
import os.path
import math
import np
import random
import re
from datetime import datetime
from dotenv import load_dotenv
from edit import *

load_dotenv()

client = discord.Client()

def create_embed(title, description):
    return discord.Embed(title=title, description=description)

def to_ordinal(number):
    return f'{number}th' if (number // 10 % 10 == 1 or number % 10 > 3 or number % 10 == 0) else str(number) + ['st', 'nd', 'rd'][(number % 10) - 1]

TOKEN = os.getenv('DISCORD_TOKEN')
JSON_TEMPLATE = '{\n}'

videos_length = 0

def create_json(filename):
    if not os.path.isfile(filename):
        with open(filename) as f:
            f.write(JSON_TEMPLATE)

def dups(a):
    uniques, counts = np.unique(a, return_counts=True)
    return uniques[np.where(counts > 1)]

def linter():
    videos = glob.glob(VIDEO_DIRECTORY) + glob.glob(IMAGE_DIRECTORY)
    filename = 'user_data.json'

    create_json(filename)

    with open(filename, 'r') as file:
        data = json.loads(file.read())

        # for video in videos:
            # if not video.replace('E:/!!!/absolute elite memes/cars\\', '').replace('.mp4', '').replace('.png', '') in data[str(344886499373875212)]:
                # print(video)

        for d in data:
            if dups(data[d]).size > 0:
                print(f'<car cleanup> video "{dups(data[d])}" from {d} is a duplicated car entry!')

            for video in data[d]:
                v = f'E:/!!!/absolute elite memes/cars\\\\{video}'

                if not f'{v}.png' in videos and f'{v}.mp4' in videos:
                    print(f'<car cleanup> video "{video}" from {d} is an illegal car entry!')

linter()

async def leaderboards(message):
    filename = 'frequency_data.json'
    
    create_json(filename)

    with open(filename, 'r') as file:
        data = json.loads(file.read())
        length = 0
        files = len(glob.glob(VIDEO_DIRECTORY) + glob.glob(IMAGE_DIRECTORY) )

        for d in data:
            length += data[d]
    
    filename = 'user_data.json'
    
    create_json(filename)

    with open(filename, 'r') as file:
        data = json.loads(file.read())
        list = []
        
        for d in data:
            with open('name_data.json', 'r') as other_file:
                other_data = json.loads(other_file.read())
                list.append((other_data[d], len(data[d])))

    list.sort(key=lambda tup: tup[1])
    
    if len(list) > 5:
        list = list[-5:]

    list.reverse()

    title = f'car of fame (posted {length} cars in total)'
    description = ''
    index = 0

    for l in list:
        index += 1
        max_format = '**' if l[1] == files else ''
        separator = '🚗🚙' if index % 2 == 0 else '🚙🚗'
        description += f'{index}. {separator[0]} **{l[0]}** with {max_format}{l[1]}/{files}{max_format} cars {separator[1]}\n\n'

    await message.channel.send(embed=create_embed(title, description))

def post(content, author):
    length = len(content)

    filename = 'name_data.json'
    
    create_json(filename)

    with open(filename, 'r') as file:
        data = json.loads(file.read())
        data[author.id] = author.name

    os.remove(filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    while len(content):
        videos = glob.glob(VIDEO_DIRECTORY) + glob.glob(IMAGE_DIRECTORY) 
        videos_length = len(videos)
        matches = []

        try:
            regex = re.compile(content.lower())
            matches = [ s for s in videos if regex.search(s.replace('E:/!!!/absolute elite memes/cars\\', '').replace('.mp4', '').replace('.png', '')) != None ]
        except:
            content = content[:-1]
            continue

        if len(matches) != 0:
            video = random.choice(matches)
            preview = video.replace('E:/!!!/absolute elite memes/cars\\', '').replace('.mp4', '').replace('.png', '')
            title = ''

            filename = 'frequency_data.json'
            
            create_json(filename)

            with open(filename, 'r') as file:
                data = json.loads(file.read())
                id = str(preview)
                times_format = 'time'

                if id not in data:
                    data[id] = 0
                    times_format = 'EVER SEEN'

                # for match in matches:
                #     if match.replace('E:/!!!/absolute elite memes/cars\\', '').replace('.mp4', '').replace('.png', '') not in data:
                #         print(match)

                data[id] += 1
                times_seen = data[id]

            os.remove(filename)

            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)

            filename = 'user_data.json'

            with open(filename, 'r') as file:
                data = json.loads(file.read())
                description = f'already seen'
                id = str(author.id)

                if id not in data:
                    data[id] = []

                if preview not in data[id]:
                    data[id].append(preview)
                    description = f'**+1**'
                    title = 'NEW '
                    
                description += f' ({len(data[id])}/{videos_length})' if len(data[id]) < videos_length else ' (**all cars obtained**)'
            
            os.remove(filename)

            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
                
            return (create_embed(f'{title}[{preview}] (found {len(matches)}, {to_ordinal(times_seen)} {times_format})', f'🚗 {math.floor(len(content) / length * 100)}% accuracy, {description} 🚙'), discord.File(video))

        content = content[:-1]
    return (create_embed('no car found', '🚗 choot choot 🚙 (0% accuracy)'), discord.File(DEFAULT))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    if not len(content):
        return

    if (message.content == '🚗' or message.content == '🚙'):
        await leaderboards(message)
        return

    if str(message.channel.type) != 'private' and content.find('🚗 ') != 0 and content.find('🚙 ') != 0:
        return
        
    # print(f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}]: {content}')

    content = content.replace('🚗 ', '').replace('🚙 ', '')
    (embed, file) = post(content, message.author)

    await message.channel.send(embed=embed, file=file)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('dm me for cars :) [info: https://github.com/Emik03/BotCar]'))
    print(f'Monday, May 3, 2021, 3:22PM')

client.run(TOKEN)
