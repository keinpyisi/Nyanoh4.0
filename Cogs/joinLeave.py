import discord
from discord.ext import commands

import wavelink
from pathlib import Path

from Tools.Check import Check

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer
from threading import Timer
import youtube_dl
import asyncio
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class CogJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # @commands.command(name = "join",
    #                 aliases=["j"],
    #                 usage="",
    #                 description = "Add the bot in your voice channel")
    # @commands.guild_only()
    # @commands.cooldown(1, 5, commands.BucketType.member)
    # async def join(self, ctx):
        
    #     if not await Check().userInVoiceChannel(ctx, self.bot): return 
    #     if not await Check().botNotInVoiceChannel(ctx, self.bot): return 

    #     channel = ctx.author.voice.channel
        
    #     player = self.bot.wavelink.get_player(ctx.guild.id)
    #     await player.connect(channel.id)

    #     # Clear all the queue
    #     DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
    #     # Clear all server music parameters
    #     DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
        
    #     await ctx.send(f"{ctx.author.mention} Connected in **`{channel.name}`**!")
        

    @commands.command(name = "leave",
                    aliases=["dc","quit"],
                    usage="",
                    description = "Leave the bot of your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def leave(self, ctx):

        if not await Check().botInVoiceChannel(ctx, self.bot): return

        if not ctx.author.guild_permissions.administrator:
            if not await Check().userInVoiceChannel(ctx, self.bot): return 
            if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        player = self.bot.wavelink.get_player(ctx.guild.id)
        channelId = player.channel_id
        channel = self.bot.get_channel(channelId)

        if player.is_playing:
            await player.destroy()
        await player.disconnect()

        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)

        await ctx.channel.send(f"{ctx.author.mention} Disconnected from **`{channel.name}`**!")
        
    @commands.command(name = "miku",
                    aliases=["mk"],
                    usage="",
                    description = "Add the Miku in your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def nya(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botNotInVoiceChannel(ctx, self.bot): return 

        # channel = ctx.author.voice.channel
        
        # player = self.bot.wavelink.get_player(ctx.guild.id)
        # await player.connect(channel.id)
        channel = ctx.message.author.voice.channel
        await channel.connect()

        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
        # ROOT_DIR = str(Path(__file__).parent.parent) # This is your Project Root
        
        
        # audio_source = discord.FFmpegPCMAudio("/Users/keinpyisi/Documents/php8/Music-Discord-Bot/Assets/sounds_Smol_nyanoh.wav")
        # if not await Check().botIsPlaying(ctx, self.bot): await player.play(audio_source)
        
        # # await ctx.send(f"{ctx.author.mention} Connected in **`{channel.name}`**!")
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url("https://github.com/keinpyisi/Database/raw/main/sounds_Smol_nyanoh.wav", loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
                while voice_channel.is_playing():
                    await asyncio.sleep(1)
                await voice_channel.disconnect()
                channel = ctx.author.voice.channel
        
            player = self.bot.wavelink.get_player(ctx.guild.id)
            await player.connect(channel.id)

                # Clear all the queue
            DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
                # Clear all server music parameters
            DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
 
               
                
                
                 
            
        except:
            await ctx.send("The bot is not connected to a voice channel.")
    @commands.command(name = "join",
                    aliases=["j"],
                    usage="",
                    description = "Add the bot in your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def join(self, ctx):
        # if not await Check().userInVoiceChannel(ctx, self.bot): return 
        # if not await Check().botNotInVoiceChannel(ctx, self.bot): return 

        # channel = ctx.author.voice.channel
        
        # player = self.bot.wavelink.get_player(ctx.guild.id)
        # await player.connect(channel.id)
        

        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
        # ROOT_DIR = str(Path(__file__).parent.parent) # This is your Project Root
        
        
        # audio_source = discord.FFmpegPCMAudio("/Users/keinpyisi/Documents/php8/Music-Discord-Bot/Assets/sounds_Smol_nyanoh.wav")
        # if not await Check().botIsPlaying(ctx, self.bot): await player.play(audio_source)
        
        # # await ctx.send(f"{ctx.author.mention} Connected in **`{channel.name}`**!")
        try :
            channel = ctx.message.author.voice.channel
            await channel.connect()
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url("https://github.com/keinpyisi/Database/raw/main/sounds_Smol_nyanoh.wav", loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), after = lambda e: asyncio.run_coroutine_threadsafe(voice_channel.disconnect(), self.bot.loop))
                # print(voice_channel.is_playing())
                # while voice_channel.is_playing():
                #     if(voice_channel.is_playing()==False):

                #         print(False)
                # player = self.bot.wavelink.get_player(ctx.guild.id)
                # await player.connect(channel.id)
                # channel = ctx.author.voice.channel
        
           

                # Clear all the queue
            DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
                # Clear all server music parameters
            DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
 
               
                
                
                 
            
        except Exception as e:
            await ctx.send(e)
        

def setup(bot):
    bot.add_cog(CogJoinLeave(bot))
