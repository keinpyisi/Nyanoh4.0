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

from urllib.request import Request, urlopen
import requests 
from requests_html import HTMLSession
from bs4 import BeautifulSoup
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

def parse_results(response):
    print(response)
    css_identifier_result = ".GyAeWb"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".tF2Cxc"
    
    results = response.html.find(css_identifier_result)

    output = []
   
    for result in results:
        
        lyric=result.find('div')[62]
       
       

        # item = {
        #     'title': result.find(css_identifier_title, first=True).text,
        #     'link': result.find(css_identifier_link, first=True).attrs['href'],
        #     'text': result.find(css_identifier_text, first=True).text
        # }
        
        output.append(lyric.text)
        
    return output

def get_source(url):
  
    try:
        response=requests.get(url, headers = {'User-agent': 'your bot 0.1'})
        # session = HTMLSession()
        # response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    
    response = get_source(query)
    
    return response
# mybytes = urlopen(req).read()


# html = mybytes.decode("utf8")
# data= parse_results(req)








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

        
        
        if songnametemp[-1] == ' ':
            songnametemp=songnametemp[:-1]

        url = "https://www.google.com/search"
        params = {'q':songnametemp,'sclient':'gws-wiz-serp'}


        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        print(urlparse.urlunparse(url_parts))


     
        
        lyrics=parse_results(get_results(urlparse.urlunparse(url_parts)))
        # print(len(data))
        # for text in data:
        #     print(text)
        # print(url)
        
        embed=discord.Embed(title="Lyrics of :", description=f"**[{songnametemp}]**", color=0xFFD1DC)
        
        embed.add_field(name="Lyrics :", value=lyrics, inline=True)
        
        await ctx.send(embed=embed,allowed_mentions=discord.AllowedMentions.all())
		

def setup(bot):
    bot.add_cog(Lyrics(bot))
