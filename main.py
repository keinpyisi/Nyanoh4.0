#!/usr/bin/env python3

from email import message
import random 
from DataBase.Connection import DBConnection
import discord
import wavelink
import os
import json
import tekore # Spotify
import asyncio
from discord.ext import commands
from pathlib import Path
import string
# Import the following modules
from captcha.image import ImageCaptcha
from Tools.Utils import Utils
import os
from DataBase.Server import DBServer
from DataBase.Queue import DBQueue

ROOT_DIR = os.path.dirname(os.path.abspath("main.py"))


class createEmojiList:
    def __init__(self, emojiList):
        self.youtubeLogo = emojiList["YoutubeLogo"]
        self.spotifyLogo = emojiList["SpotifyLogo"]
        self.soundcloudLogo = emojiList["SoundcloudLogo"]
        self.deezerLogo = emojiList["DeezerLogo"]
        self.true = emojiList["True"]
        self.false = emojiList["False"]
        self.alert = emojiList["Alert"]

class createLavalink:
    def __init__(self):
        with open(ROOT_DIR+"/configuration.json", "r") as config:
            data = json.load(config)

        self.host = data["lavalinkHost"]
        self.port = data["lavalinkPort"]
        self.restUri = data["lavalinkRestUri"]
        self.password = data["lavalinkPassword"]
        self.identifier = data["lavalinkIdentifier"]
        self.region = data["lavalinkRegion"]

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

with open(ROOT_DIR+"/configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

    spotifyClientId = data["spotifyClientId"]
    spotifyClientSecret = data["spotifyClientSecret"]

    dblToken = data["dblToken"]


with open(ROOT_DIR+"/emojis.json", "r") as emojiList:
    emojiList = json.load(emojiList)
    emojiList = {
        "YoutubeLogo": emojiList["YouTubeLogo"],
        "SpotifyLogo": emojiList["SpotifyLogo"],
        "SoundcloudLogo": emojiList["SoundCloudLogo"],
        "DeezerLogo": emojiList["DeezerLogo"],
        "True": emojiList["True"],
        "False": emojiList["False"],
        "Alert": emojiList["Alert"] 
    }


intents = discord.Intents.all()
bot = commands.Bot(prefix, intents = intents)
ctxs=""
# Spotify
if (spotifyClientId != ""):
    spotifyAppToken = tekore.request_client_token(spotifyClientId, spotifyClientSecret)
    bot.spotify = tekore.Spotify(spotifyAppToken, asynchronous=True)

# Lavalink
bot.lavalink = createLavalink()

# Top.gg
bot.dblToken = dblToken

# Emojis
bot.emojiList = createEmojiList(emojiList)

# Help
bot.remove_command("help") # To create a personal help command 

# Database
bot.dbConnection = DBConnection()


async def status_task():
    while True:
        serverCount = len(bot.guilds)
        data=[]        
        currentTrack = DBQueue(bot.dbConnection).getAlltSong()
        if(currentTrack is not None):
            data.append(currentTrack[0][0])
        data.append("In "+str(serverCount)+" Servers")
        data.append("{}help for Help.".format(prefix))
        data.append("Made By htut#0854")
        data.append("Modified By Krul#6348")
        data.append("KonNyaro")
        ran=random.choice(data)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name =str(ran))) 
        await asyncio.sleep(10)
        
    

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir(ROOT_DIR+"/Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    # Check if each server is in the DB
    print("Database check")
    servers = DBServer(bot.dbConnection).display()
    servers = DBServer(bot.dbConnection).display()
    serversId = [int(i[0]) for i in servers]
    for guild in bot.guilds:
        if guild.id not in serversId:
            DBServer(bot.dbConnection).add(guild.id, "?", False, False, "")
            print(f"* {guild.name} ({guild.id}) added")
    bot.loop.create_task(status_task())
    print("----------------------------")
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)
    # while(True):
    #     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =random.choice("abcde")))     
@bot.event
async def on_member_join(member):
    image = ImageCaptcha(width = 280, height = 90)
    
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(8))
    # generate the image of the given text
    data = image.generate(password)
    # write the image on the given file and save it
    image.write(password, 'CAPTCHA.png')
    file = discord.File('CAPTCHA.png', filename="CAPTCHA.png")

    message="Please Sent Verification Code -> to me"
    embed=discord.Embed(title="Verification Please", description=message, color=discord.Colour.random())
    
    DBQueue(bot.dbConnection).capcha_add(str(password),str(member.id),str(member.guild.id))
      
    DBQueue(bot.dbConnection).unverify_add(str(member.guild.id),str(member.id),str(member.name))
    
    await member.send(embed=embed,file=file)   

@bot.event
async def on_message(message):
    content=message.content
    userid=message.author.id
    data=DBQueue(bot.dbConnection).capcha_search(str(content),userid )
    msg="Wrong Capcha nya~"
    if content.startswith(prefix):
         if prefix+":" in content:
            pass
         else:
            await message.add_reaction('\u2705')
    if message.guild is None and not message.author.bot:
        
        if(data != None):
            #capchaverify
            if(len(data)>0):
                DBQueue(bot.dbConnection).capchaverify(str(content),userid )
                msg="Capcha Verified. Please sent !nyanoh in specfic server"

            await message.channel.send(msg)
    else:

            await bot.process_commands(message) 
    
@bot.event
async def on_reaction_add(reaction, user):
        global ctxs
        ctx=ctxs
        print(ctx)
        if(ctxs is not None):
             #Loop
   
            
            if user != bot.user:
                if str(reaction.emoji) == "\u23EE\uFE0F":
                    print("RESUME")
                    
                if str(reaction.emoji) == "\u23F8\uFE0F":
                    
                    await ctx.invoke(bot.get_command('pause'))
                
               
                if str(reaction.emoji) == "\u23ED\uFE0F":
                     await ctx.invoke(bot.get_command('skip'))
                if str(reaction.emoji) == "\U0001f3b5":
                     await ctx.invoke(bot.get_command('lyrics'))
                if str(reaction.emoji) == "\u25B6\uFE0F":
                    await ctx.invoke(bot.get_command('resume'))

                if str(reaction.emoji) == "\U0001f501":
                    await ctx.invoke(bot.get_command('loop'))
                if str(reaction.emoji) == "\U0001f4dd":
                    await ctx.invoke(bot.get_command('queue'))
                if str(reaction.emoji) == "\U0001f4ca":
                    await ctx.invoke(bot.get_command('stats'))
                if str(reaction.emoji) == "\U0001f5d1\uFE0F":
                    await ctx.invoke(bot.get_command('clear'))
                if str(reaction.emoji) == "\U0001f6aa":
                    await ctx.invoke(bot.get_command('logout'))
        else:
            print("CTX IS NONE")       


@bot.command(name = "ctx",description = "Skip the current music.")
async def rps(ctx):
    global ctxs
    print(ctxs)   
    ctxs=ctx
    message = str(ctx.message.content)
    await ctx.send(message)

# ------------------------ RUN ------------------------ # 
bot.run(token)
