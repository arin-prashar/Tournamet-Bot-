import discord
from discord.ext import commands
from discord.utils import get
import random
import DB as DB


class Config(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create(self,ctx):
        await ctx.send("Enter the tournament name:\nType `cancel` to cancel the command.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        tname=msg.content

        await ctx.send("Enter the number of slots:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        slots=msg.content

        await ctx.send("Enter the team size:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        team_size=msg.content
        while True:
            await ctx.send("Ping the role that the **user** gets on successful Registeration:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await ctx.send("Command cancelled.")
                return
            role=get(ctx.guild.roles,id=int(msg.content[3:-1]))
            if role==None:
                await ctx.send("Role not found.")
                continue
            break
        def colr():
            return random.randint(0, 0xFFFFFF)
        T_id=DB.create(ctx.guild.id,tname,slots,team_size,role.id)
        if T_id=="Tournament Name already exists.": #if the tournament name already exists
            await ctx.send("Tournament Name already exists.")
            return
        if T_id=="Error": #if there is an error
            await ctx.send("Error")
            return
        embed=discord.Embed(title="Tournament Created",description="Tournament Created Successfully",color=colr())
        embed.add_field(name="Tournament Name",value=tname,inline=False)
        embed.add_field(name="Tournament ID",value=T_id,inline=False)
        embed.add_field(name="Slots",value=slots,inline=False)
        embed.add_field(name="Team Size",value=team_size,inline=False)
        embed.add_field(name="Role",value=role.mention,inline=False)
        await ctx.send(embed=embed)    
    
    @create.error
    async def create_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament name.")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete(self,ctx):
        await ctx.send("Enter the tournament ID:\nType `cancel` to cancel the command.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        T_id=msg.content
        DB.delete(ctx.guild.id,T_id)
        await ctx.send("Tournament Deleted Successfully.")

    @delete.error
    async def delete_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get(self,ctx):
        await ctx.send("Enter the tournament ID:\nType `cancel` to cancel the command.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        T_id=msg.content
        data=DB.get(ctx.guild.id,T_id)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        embed=discord.Embed(title="Tournament Config",description="Tournament Config",color=0x00ff00)
        embed.add_field(name="Tournament Name",value=data["Tournament Name"],inline=False)
        embed.add_field(name="Tournament ID",value=data["_id"],inline=False)
        embed.add_field(name="Slots",value=data["slots"],inline=False)
        embed.add_field(name="Team Size",value=data["team_size"],inline=False)
        embed.add_field(name="Role",value=get(ctx.guild.roles,id=data["role"]).mention,inline=False)
        await ctx.send(embed=embed)

    @get.error
    async def get_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def update(self,ctx):
        await ctx.send("Enter the tournament ID:\nType `cancel` to cancel the command.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        T_id=msg.content
        data=DB.get(ctx.guild.id,T_id)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        await ctx.send("Enter the new tournament name:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        tname=msg.content

        await ctx.send("Enter the new number of slots:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        slots=msg.content

        await ctx.send("Enter the new team size:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        team_size=msg.content
        while True:
            await ctx.send("Ping the role that the **user** gets on successful Registeration:\nType `cancel` to cancel the command.")
            msg = await self.bot.wait_for('message', check=check)
            if msg.content=="cancel":
                await ctx.send("Command cancelled.")
                return
            role=get(ctx.guild.roles,id=int(msg.content[3:-1]))
            if role==None:
                await ctx.send("Role not found.")
                continue
            break
        DB.update(ctx.guild.id,T_id,tname,slots,team_size,role.id)
        await ctx.send("Tournament Updated Successfully.")

    @update.error
    async def update_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify a tournament ID.")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list(self,ctx):
        data=DB.list(ctx.guild.id)
        if data==None:
            await ctx.send("No tournaments found.")
            return
        embed=discord.Embed(title="Tournament List",description="Tournament List",color=0x00ff00)
        for i in data:
            embed.add_field(name="Tournament Name",value=i["Tournament Name"],inline=False)
            embed.add_field(name="Tournament ID",value=i["_id"],inline=False)
            embed.add_field(name="Slots",value=i["slots"],inline=False)
            embed.add_field(name="Team Size",value=i["team_size"],inline=False)
            embed.add_field(name="Role",value=get(ctx.guild.roles,id=i["role"]).mention,inline=False)
        await ctx.send(embed=embed)

    @list.error
    async def list_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You do not have the required permissions.")

    # list command we have till now 
            # !create
            # !delete
            # !get
            # !update
            # !list
            












async def setup(bot):
    await bot.add_cog(Config(bot))