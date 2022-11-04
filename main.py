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
# importing modules
import pandas as pd

import requests
import json
from csv import reader
import csv
from sqlalchemy import create_engine
# importing modules
import sys


import numpy as np
from tensorflow.keras.models import load_model
import random
import os
from datetime import datetime
from threading import Timer

ROOT_DIR = os.path.dirname(os.path.abspath("main.py"))
from discord.utils import get
# converter=ROOT_DIR+"/AI/converter.json"
# modelpath=ROOT_DIR+"/AI/AI/"
# chatbot = load_model(modelpath)

# cantencode = set() 



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
    ReimuAcc_Name=data["ReimuAcc_Name"]
    ReimuDB_Name=data["ReimuDB_Name"]
    ReimuPort=data["ReimuPort"]
    ReimuPass=data["ReimuPass"]
    


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

# db_connection_str = "mysql+pymysql://"+ReimuAcc_Name+ ":" +ReimuPass +"@localhost"+":"+str(ReimuPort)+"/"+ ReimuDB_Name
# print(db_connection_str)
# db_connection = create_engine(db_connection_str)
# training_data = pd.read_sql('Select distinct patterns , tags from encrypted_data', con=db_connection)
# enc_data = "INSERT INTO data_get (patterns, tags) VALUES (%s, %s)"
# #fitting TfIdfVectorizer with training data to preprocess inputs
# training_data["patterns"] = training_data["patterns"].str.lower()
# vectorizer = TfidfVectorizer(ngram_range=(1, 2))
# vectorizer.fit(training_data["patterns"])

# # fitting LabelEncoder with target variable(tags) for inverse transformation of predictions
# le = LabelEncoder()
# le.fit(training_data["tags"])

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

# transforming input and predicting intent
# def predict_tag(inp_str):
#     inp_data_tfidf = vectorizer.transform([inp_str]).toarray()
#     predicted_proba = chatbot.predict(inp_data_tfidf)
#     encoded_label = [np.argmax(predicted_proba)]
#     predicted_tag = le.inverse_transform(encoded_label)[0]
    
    
    
#     return predicted_tag
# defining chat function
# def start_chat(inp):
#     append=""
#     data = {}
#     for char in inp:
      
#       if(encode(char) is None):
#                 break
#       char=encode(char)
#       append+=char

#     if inp:
                
#                 tag = predict_tag(append)
#                 sql="Select distinct patterns,tags from raw_data where tags = '"+tag+"' ORDER BY RAND() LIMIT 1"
#                 result = db_connection.execute(sql)
#                 for row in result:
#                   data['patterns'] = str(row[0])
#                   data['tags']=str(row[1])
                
#                 val = (str(inp), str(data['tags']))
#                 db_connection.execute(enc_data,val)
#                 return data['patterns']

#                 # json_data = json.dumps(data)
                
#                 # print(json_data)        
              

                
#     else:
#                   print("NO DATA")
#                   return "None"          
    
              
        

    
        


async def status_task():
    count=1
    while True:
        print(datetime.now())
        try:
            for guild in bot.guilds:
                player = bot.wavelink.get_player(guild.id)
                if player.is_connected:
                    print("Player Conected ")
                    if player.is_playing:
                        print("Player Playing ")
                        pass
                    else:
                        print("Player Not Playing ")
                        if(count%20==0):
                            await player.destroy()
                            await player.disconnect()

                        print("Player Not Playing HELPPP" + str(count))
                    pass
                else:
                    print("Player Not Conected ")
                    pass
                    
        except:
            print("PLAYER NULL")
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
        await asyncio.sleep(5)
        count+=1

        

#timer.cancel() # cancels the timer, but not the job, if it's already started    

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
    await status_task()
    
    
    print("----------------------------")
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)
    # while(True):
    #     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =random.choice("abcde")))     
@bot.event
async def on_member_join(member):
    roletoadd=DBQueue(bot.dbConnection).unrole_search(member.guild.id ) 
                
    this_role = get(member.guild.roles, id=int(roletoadd[0][0]))

                
                
    await member.add_roles(this_role)
    print("HERE")
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
            try:
                
                raise Exception('I know Python!')
                 #await message.channel.send(str(start_chat(str(content))))
            except Exception as e:
                print(e)
                await message.channel.send("If you are verifying, Wrong Captcha nya~")

                #await message.channel.send("Please Type in Myanmar Language If you want to talk to me Nya~")

                
                
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
