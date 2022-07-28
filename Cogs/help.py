import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help',
                        usage="(commandName)",
                        description = "Display the help message.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break 
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break 

            if commandName2 is None:
                await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} No command found!")   
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} COMMAND :**", description="Nyajestic Bot", color=0xFFD1DC)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**NAME :**", value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**ALIASES :**", value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                embed.add_field(name=f"**USAGE :**", value=f"{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(name=f"**DESCRIPTION :**", value=f"{commandName2.description}", inline=False)
                embed.set_footer(text="Bot Created by #htut#0854, Modified By #Krul#6348")
                await ctx.channel.send(embed=embed)
        else:
            message1 = (f"""
            **help (command) :** Display the help list or the help data for a specific command.\n
           
            **invite :** Give a link to invite the bot.
           
            **play <Url/Query> :** Search on youtube and play the music.
            **search <Query> :** Search a song on youtube.
            **nowplaying :** Display data about the current song.
            **join :** Add the bot to your voice channel.
            **leave :** Remove the bot of your voice channel.
            **pause :** Pause the current song.
            **resume :** Resume the current song.
            **volume <0-100> :** Change the bot's volume.
            **queue :** Display the queue.
            **move <IndexFrom> <IndexTo> :** Move a song in the queue.   
            """)

            message2 = (f"""
            **remove <Index> :** Remove the song with its index.
            **clear :** Clear the queue.
            **replay :** Replay the current song.
            **reload :** Reload the current song.
            **loop :** Enable or disable the loop mode.
            **loopqueue :** Enable or disable the loop queue mode.

            **playlist add <Url> :** Add a track to your playlist.
            **playlist remove <Index> :** Remove a track to your playlist.
            **playlist display :** Display playlist's songs.
            **playlist load :** Add the whole playlist to the queue.
            **ping : ** Bonk Nyanoh
            **stats :** Display the bot's stats.
            """)

            # **shuffle :** Shuffle the queue.
            # **removedupes :** Remove all duplicates song from the queue.
            # **leavecleanup :** Remove absent user's songs from the queue.

            embed = discord.Embed(title=f"__**{self.bot.user.name.upper()} Help**__", description="List of all commands", color=0xF8AA2A)
           
            for command  in self.bot.commands:
                
                if(str(command) == "capnya" or str(command) == "listservers"):
                    pass
                else:

                    embed.add_field(name="**{}{}**".format(self.bot.command_prefix,command), value="{}".format(command.description), inline=True)
        
            
            embed.set_footer(text="Bot Created by #htut#0854, Modified By #Krul#6348")
            await ctx.channel.send(embed=embed)

           

            

            # embed = discord.Embed(title=f"", description=f"{message2}", color=0xFFD1DC)
            # embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            # embed.set_footer(text="Bot Created by #htut#0854, Modified By #Krul#6348")
            # await ctx.channel.send(embed=embed)

            

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
