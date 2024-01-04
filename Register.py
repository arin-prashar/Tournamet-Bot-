import discord
from discord.ext import commands
from discord.utils import get
import random
import DB


class Register(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def register(self,ctx):
        await ctx.send("Enter the tournament ID:\nType `cancel` to cancel the command.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        T_id=msg.content
        T_id=int(T_id)
        data=DB.get(ctx.guild.id,T_id)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        if data["slots"]==0:
            await ctx.send("Tournament is full.")
            return
        # registeration in a seprate channel created by the bot
        await ctx.send("Enter the team name:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        tname=msg.content
        if tname in data["Tournament Name"]:
            await ctx.send("Team name already exists.")
            return
        

        channel_id=await ctx.guild.create_text_channel(f"{tname}")
        await channel_id.set_permissions(ctx.guild.default_role,read_messages=False)
        await channel_id.set_permissions(ctx.guild.me,read_messages=True)
        await channel_id.set_permissions(ctx.author,read_messages=True)
        await ctx.send(f"Continue Registeration Here: {channel_id.mention}")
        
        res=await self.add_toDB(ctx,channel_id,data,tname,T_id)
        if res=="Success":
            await channel_id.send("Successfully Registered.")
            await channel_id.delete()
            return

    async def add_toDB(self,ctx,channel_id,data,tname,T_id):
            def check(m):
                return m.author == ctx.author and m.channel == channel_id
            await channel_id.send("Mention the Players:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await ctx.send("Command cancelled.")
                return
            players=msg.content.split()
            if len(players)!=data["team_size"]:
                await ctx.send("Invalid number of players.")
                return
            for player in players:
                player=player.strip()
                if player[0:2]=="<@" and player[-1]==">":
                    continue
                else:
                    await ctx.send("Invalid player.{player}")
                    return
            player_name=[]
            for player in players:
                player_n=get(ctx.guild.members,id=int(player[2:-1]))
                player_name.append(player_n.name)
            # ingame name and UID
            await channel_id.send("Enter the ingame name of players seprated by **,**:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await ctx.send("Command cancelled.")
                return
            ign=msg.content.split(",")
            for i in range(data["team_size"]):
                ign[i]=ign[i].strip()
            while len(ign)!=data["team_size"]:
                uid.pop()
            await channel_id.send("Enter the UID:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await ctx.send("Command cancelled.")
                return
            uid=msg.content.split(",")
            for i in range(data["team_size"]):
                uid[i]=uid[i].strip()
            while len(uid)!=data["team_size"]:
                uid.pop()
            # add to DB
            DB.register(ctx.guild.id,T_id,tname,players,player_name,ign,uid)
            return "Success"
        

    @register.error
    async def register_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")

    @commands.command()
    async def confirm(self,ctx,T_id:int,tname:str):
        data=DB.get_team(ctx.guild.id,T_id,tname)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        auth_id="<@"+str(ctx.author.id)+">"
        if auth_id in data["Player-ID"]:
            await ctx.send("Team Registered.")
        
    @confirm.error
    async def confirm_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")

    
    @commands.command()
    async def unregister(self,ctx,T_id:int,tname:str):
        data=DB.get_team(ctx.guild.id,T_id,tname)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        auth_id="<@"+str(ctx.author.id)+">"
        if auth_id in data["Player-ID"]:
            DB.unregister(ctx.guild.id,T_id,tname)
            await ctx.send("Team Unregistered.")
            return
        await ctx.send("Team not found.")

async def setup(bot):
    await bot.add_cog(Register(bot))