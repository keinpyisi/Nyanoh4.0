import discord
from discord.ext import commands
import asyncio, discord, os, re, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct, shutil, tempfile

class Ping(commands.Cog):
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
    @commands.command(pname = "ping",
                    usage="",
                    description = "Pong~")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
        before_typing = time.monotonic()
        await ctx.trigger_typing()
        after_typing = time.monotonic()
        ms = int((after_typing - before_typing) * 1000)
        msg = '{} , 📈 Average ping to API: {} ms'.format(ctx.message.author.mention, ms)
        await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())
		

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


def setup(bot):
    bot.add_cog(Ping(bot))