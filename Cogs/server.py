import discord
from discord.ext import commands
import asyncio, discord, os, re, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct, shutil, tempfile
from DataBase.Queue import DBQueue

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # @commands.command(name = "support",
    #                 usage="",
    #                 description = "Give a link to join the support server.")
    # @commands.cooldown(1, 2, commands.BucketType.member)
    # async def support(self, ctx):
    #     embed=discord.Embed(title="Support server :", description=f"Join the support server : https://discord.gg/f2UMbk95bv", color=discord.Colour.random())
    #     embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
    @commands.command(pname = "server",
     aliases=["se","servers","ls"],
                    usage="",
                    description = "Server List")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def listservers(self, ctx):
        count=0
            
        for server  in self.bot.guilds:
                    embed = discord.Embed(title=f"__**{self.bot.user.name.upper()} Server Lists**__", description="List of all Servers", color=0xF8AA2A)
       
                    
                    count+=1
                    embed.add_field(name="**{}.{}**".format(count,server.name), value="{}".format(server.id), inline=True)
                            
                    
                        
                    embed.set_footer(text="Bot Created by #htut#0854, Modified By #Krul#6348")
                    await ctx.channel.send(embed=embed)
        
            
        
        
		

    # @commands.command(name = "github",
    #                 usage="",
    #                 description = "Give the github link of the bot.")
    # @commands.cooldown(1, 2, commands.BucketType.member)
    # async def github(self, ctx):
    #     embed=discord.Embed(title="Github link :", description=f"See the code of {self.bot.user.mention} on GitHub : https://github.com/Darkempire78/Music-Discord-Bot", color=discord.Colour.random())
    #     embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)

                # @commands.command(name = "vote",
                #                 usage="",
                #                 description = "Give the Top.gg link to vote for the bot.")
                # @commands.cooldown(1, 2, commands.BucketType.member)
                # async def vote(self, ctx):
                #     embed=discord.Embed(title="Vote link :", description=f"Vote for {self.bot.user.mention} on Top.gg : https://top.gg/bot/796749718217555978/vote", color=discord.Colour.random())
                #     embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
                #     await ctx.send(embed=embed)
    @commands.command(pname = "musicserver",
     aliases=["ms","mus"],
                    usage="",
                    description = "Music Playing Server List")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def listplayingservers(self, ctx):
            playingServerCount = DBQueue(self.bot.dbConnection).countServerPlayingItems()
           
            


            embed = discord.Embed(title=f"__**{self.bot.user.name.upper()} Server Lists**__", description="List of all Servers", color=0xF8AA2A)
            
            for serverid,serveruser in playingServerCount:
                    embed.add_field(name="**{}**".format("Playing In "), value="{}".format(serverid))
            
                
            embed.set_footer(text="Bot Created by #htut#0854, Modified By #Krul#6348")
            await ctx.channel.send(embed=embed)
        

def setup(bot):
    bot.add_cog(server(bot))