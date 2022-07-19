import discord

from Tools.Utils import Utils

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle




async def sendPlayingSongEmbed(self, channel, track): 

    player = self.bot.wavelink.get_player(channel.guild.id)
    
    # Volume
    volume = player.volume
    
    # Track duration
    trackDuration = await Utils().durationFormat(track.duration)
    
    # Queue size and duration
    queueSizeAndDuration = DBQueue(self.bot.dbConnection).queueSizeAndDuration(channel.guild.id)
    if queueSizeAndDuration:
        queueDuration = int(queueSizeAndDuration[0])
        queueDuration = await Utils().durationFormat(queueDuration)
        queueSize = queueSizeAndDuration[1]
    else:
        queueSize = 0
        queueDuration = "00:00"
    
    # Title
    trackTitle = track.title.replace("*", "\\*")
    volume=100
    # Loop and LoopQueue
    isLoop = str(DBServer(self.bot.dbConnection).displayServer(channel.guild.id)[2])
    isLoopQueue = str(DBServer(self.bot.dbConnection).displayServer(channel.guild.id)[3])
   

    

    
    # Embed 
    embed=discord.Embed(title="Playing Song :", description=f"**[{trackTitle}]({track.uri})**", color=0xFFD1DC)
    if track.thumb:
        embed.set_thumbnail(url=track.thumb)
    embed.add_field(name="Requested by :", value=f"`{track.requester}`", inline=True)
    embed.add_field(name="Duration :", value=f"`{trackDuration}`", inline=True)
    embed.add_field(name="Lyrics :", value=f"`{self.bot.command_prefix}lyrics`", inline=True)
    embed.add_field(name="Queue :", value=f"`{queueSize} song(s) ({queueDuration})`", inline=True)
    msg =await channel.send(embed=embed)
    await msg.add_reaction("\u25B6\uFE0F")
    await msg.add_reaction("\u23F8\uFE0F")
    await msg.add_reaction("\u23ED\uFE0F")
    await msg.add_reaction("\U0001f3b5")
    #Loop
    await msg.add_reaction("\U0001f501")
    #QUEYE
    await msg.add_reaction("\U0001f4dd")
    #STAT
    await msg.add_reaction("\U0001f4ca")
    #CLEAR QUEUE
    await msg.add_reaction("\U0001f5d1\uFE0F")
    #LEAVE
    await msg.add_reaction("\U0001f6aa")


    
   
