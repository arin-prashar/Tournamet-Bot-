import discord
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import DB

class Register_Option_BTNS(discord.ui.View):
    def __init(self):
        super().__init__()

    @discord.ui.button(label="Register",style=discord.ButtonStyle.green)
    async def register(self,button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.send_message("Enter the tournament ID:\nType `cancel` to cancel the command.")

    @discord.ui.button(label="Unregister",style=discord.ButtonStyle.red)
    async def unregister(self,button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.send_message("Enter the tournament ID:\nType `cancel` to cancel the command.")

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
        asyncio.sleep(5)
        if res=="Success":
            await channel_id.send("Successfully Registered.")
        await channel_id.delete()

    async def add_toDB(self,ctx,channel_id,data,tname,T_id):
            def check(m):
                return m.author == ctx.author and m.channel == channel_id
            await channel_id.send("Mention The Team Manager:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await channel_id.send("Command cancelled.")
                return
            manager=msg.content
            manager_id=int(manager[3:-1])
            manager_name=get(ctx.guild.members,id=manager_id).name
            player_id=[int]
            player_name=[str]
            ING=[str]
            UID=[int]
            while i < data["team_size"]:
                await channel_id.send(f"Mentino the player {i+1}:\nType `cancel` to cancel the command.")
                msg = await self.bot.wait_for('message', check=check)
                if msg.content=="cancel":
                    await channel_id.send("Command cancelled.")
                    return
                player=msg.content
                player_id.append(int(player[3:-1]))
                player_name.append(get(ctx.guild.members,id=player_id).name)
                await channel_id.send(f"Enter the IGN of player {i+1}:\nType `cancel` to cancel the command.")
                msg = await self.bot.wait_for('message', check=check)
                if msg.content=="cancel":
                    await channel_id.send("Command cancelled.")
                    return
                ING.append(msg.content)
                await channel_id.send(f"Enter the UID of player {i+1}:\nType `cancel` to cancel the command.")
                msg = await self.bot.wait_for('message', check=check)
                if msg.content=="cancel":
                    await channel_id.send("Command cancelled.")
                    return
                UID.append(int(msg.content))
                i+=1
            DB.register(ctx.guild.id,T_id,tname,manager_id,manager_name,player_id,player_name,ING,UID)
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

    @unregister.error
    async def unregister_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")

    @commands.command()
    async def test(self,ctx):
        view=Register_Option_BTNS()
        await ctx.send("Select an option",view=view)
        await view.wait()

async def setup(bot):
    await bot.add_cog(Register(bot))