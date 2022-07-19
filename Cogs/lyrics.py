import discord
from discord.ext import commands
import asyncio, discord, os, re, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct, shutil, tempfile
# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
import lyricsgenius
from ytmusicapi import YTMusic



GENIUS_API_TOKEN = "_IYvadJRCx6ZwYjmE-v0cQ5qRhRyeUJhoO4o0i0Uc5JVGY6UsPzEIWOtgDApuAC2"

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response
# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []
    
    response = request_artist_info(artist_name, page)
    
    json = response.json()

        # Collect up to song_cap song objects from artist
    song_info = []
    for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)
    
        # Collect song URL's from song objects
    for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)
    
    return songs[0]
# Scrape lyrics from a Genius.com song URL
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def scrape_song_lyrics(url):
    print(url)
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    
    lyrics = html.find('div', class_='Lyrics__Container-sc-1ynbvzw-6 YYrds')
    lyrics=striphtml(str(lyrics).replace("<br/>", "\n"))
    # line=lyrics.splitlines()
    # print(str(line)+"\n")
  
    # for data in lyrics:
    #     print(data)
    #     data+=data+"\n"

    # #remove identifiers like chorus, verse, etc
    # lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    # # #remove empty lines
    # # lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])  
    
    return lyrics


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


   
    @commands.command(pname = "lyrics",
                    usage="",
                    aliases=["ly","lr","lyric","lc"],
                    description = "Get Lyrics")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def lyrics(self, ctx):
        
        await ctx.trigger_typing()
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_playing:
            return await ctx.channel.send(f"{ctx.author.mention} There is currently no song!")
        
        
        
        songnametemp=str(player.current)

        ytmusic = YTMusic()
        search_results = ytmusic.search(songnametemp)
        artist=search_results[0]['artists'][0]['name']
        songname=search_results[0]['title']
        songname=re.sub("\(.*?\)","()",songname)
        songname=re.sub("\(.*?\)", "", songname)
        songname=songname.replace(",", "")
        
        
        if songname[-1] == ' ':
            songname=songname[:-1]

        
        artist=artist.replace(" ", "-").lower()
        artist=artist.join(word[0].upper() + word[1:] for word in artist.split())
       
        songname=songname.replace(" ", "-").lower()
        url="https://genius.com/"+artist+"-"+songname+"-lyrics"
        
        # https://genius.com/Kizuna-ai-hai-domo-english-lyrics
        lyrics= scrape_song_lyrics(url)
        print(url)
        
        embed=discord.Embed(title="Lyrics of :", description=f"**[{search_results[0]['artists'][0]['name']}]({search_results[0]['title']})**", color=0xFFD1DC)
        
        embed.add_field(name="Lyrics :", value=lyrics, inline=True)
        
        await ctx.send(embed=embed,allowed_mentions=discord.AllowedMentions.all())
		

def setup(bot):
    bot.add_cog(Lyrics(bot))
