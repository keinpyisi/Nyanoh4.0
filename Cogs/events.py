import discord

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, MissingPermissions, CommandNotFound, MissingRequiredArgument, ExpectedClosingQuoteError, BotMissingPermissions

import traceback
import sys
import datetime

from Tools.Utils import Utils

from DataBase.Server import DBServer
from DataBase.Queue import DBQueue

# ------------------------ COGS ------------------------ #  

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        # If the bot leave a voice channel
        if (before.channel is not None) and (after.channel is None):
            if member == self.bot.user:

                player = self.bot.wavelink.get_player(before.channel.guild.id)
                if player.is_playing:
                    await player.destroy()
                DBQueue(self.bot.dbConnection).clear(before.channel.guild.id)
                DBServer(self.bot.dbConnection).clearMusicParameters(before.channel.guild.id, False, False)

        # if (before.channel is not None) and (after.channel is not before.channel):
        #     if (
        #         (self.bot.user.id in before.channel.voice_states.keys() and 
        #         len(before.channel.voice_states) == 1) 
        #         or 
        #         (member == self.bot.user)
        #     ):
        #         if member != self.bot.user:
        #             player = self.bot.wavelink.get_player(before.channel.guild.id)
        #             await player.disconnect()
                
        #         DBServer(self.bot.dbConnection).clearMusicParameters(before.channel.guild.id, False, False)

        # If the bot join a voice channel
        elif (before.channel is None) and (after.channel is not None):
            if member == self.bot.user:

                DBServer(self.bot.dbConnection).clearMusicParameters(after.channel.guild.id, False, False)


   

   
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        # If the bot is mentioned
        if self.bot.user in message.mentions:
            await message.channel.send(f"{message.author.mention} My prefix on this server is : `{self.bot.command_prefix}`", delete_after=10)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))
