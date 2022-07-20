import discord
from discord.ext import commands

from Tools.Check import Check
from Tools.Utils import Utils
import re
from DataBase.Queue import DBQueue
from discord.utils import get
class CogQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "set-verify-channel",
                    aliases=["vchannel"],
                    usage="",
                    description = "Set Verify Channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def channel_add(self, ctx,*args):
        if args is None: return

        # author = ctx.message.author
        # user_name = author.name
        # DBQueue(self.bot.dbConnection).verify_add(ctx.guild.id,ctx.message.author.id,user_name ) 
        id = re.findall("\d+", str(args[0]))[0]
     
        channel =  self.bot.get_channel(int(id))
        
       
        
        DBQueue(self.bot.dbConnection).channel_add(str(ctx.guild.id),str(id),str(channel))
        msg = 'Verify Channel: {} , Has been Setup'.format(args[0])
        await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())
    
    

    @commands.command(name = "fan",
                    aliases=["vfan"],
                    usage="",
                    description = "Verify Now")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def fan(self, ctx):
        # if args is None: return
        print("HERE?")
        author = ctx.message.author
        user_name = author.name
        # id = re.findall("\d+", str(args[0]))[0]
     
        # channelname =  self.bot.get_channel(int(id))
        role_id=967461702532759552
        
        capchacheck=DBQueue(self.bot.dbConnection).capcha_verifysearch(ctx.message.author.id,ctx.guild.id )
        if(len(capchacheck)!=0):
            msg="Check My Message in DM , you Baka Nyamrats.You Need to Verify Captcha Nya~"
        else: 
            #DBQueue(self.bot.dbConnection).verify_add(ctx.guild.id,ctx.message.author.id,user_name ) 
            
                DBQueue(self.bot.dbConnection).verify_add(ctx.guild.id,ctx.message.author.id,user_name )
                roletoadd=DBQueue(self.bot.dbConnection).role_search(ctx.guild.id ) 
                
                this_role = get(ctx.guild.roles, id=int(roletoadd[0][0]))

                
                
                await author.add_roles(this_role)
                msg = 'Verified'.format(user_name)
            
        await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())

        # msg = 'Verify Channel: {} , Has been Setup'.format(args[0])
        # await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())

    @commands.command(name = "set-role",
                    aliases=["vrole"],
                    usage="",
                    description = "Set Role ")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def role_add(self, ctx,*args):
        if args is None: return

        # author = ctx.message.author
        # user_name = author.name
        # DBQueue(self.bot.dbConnection).verify_add(ctx.guild.id,ctx.message.author.id,user_name ) 
        
        roleid = re.findall("\d+", str(args[0]))[0]
       
        
       
        
        DBQueue(self.bot.dbConnection).role_add(str(roleid),str(ctx.guild.id))
        msg = 'Verify Role: {} , Has been Setup'.format(args[0])
        await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())
    @commands.command(name = "set-unrole",
                    aliases=["nrole"],
                    usage="",
                    description = "Set Unverified Role ")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def unrole_add(self, ctx,*args):
        if args is None: return

        # author = ctx.message.author
        # user_name = author.name
        # DBQueue(self.bot.dbConnection).verify_add(ctx.guild.id,ctx.message.author.id,user_name ) 
        
        roleid = re.findall("\d+", str(args[0]))[0]
       
        
       
        
        DBQueue(self.bot.dbConnection).unrole_add(str(roleid),str(ctx.guild.id))
        msg = 'Verify Role: {} , Has been Setup'.format(args[0])
        await ctx.send(msg,allowed_mentions=discord.AllowedMentions.all())

def setup(bot):
    bot.add_cog(CogQueue(bot))
