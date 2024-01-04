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
        await ctx.send("Enter the team name:\nType `cancel` to cancel the command.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.content=="cancel":
            await ctx.send("Command cancelled.")
            return
        tname=msg.content
        collection=DB.db[str(ctx.guild.id)]
        data=collection[str(T_id)]
        if tname in data.distinct("Team Name"):
            await ctx.send("Team Name already exists.")
            return
        x=data.count_documents({})
        data_inserted_id = data.insert_one({"_id":x+1,"Team Name":tname,"Members":[],"Captain":ctx.author.id})
        collection=DB.db[str(ctx.guild.id)]
        data=collection["Tournament Config"]
        data.update_one({"_id":T_id},{"$inc":{"slots":-1}})
        await ctx.send("Team Registered Successfully")
        role=get(ctx.guild.roles,id=data["role"])
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been given the role {role.mention}")
        















async def setup(bot):
    await bot.add_cog(Register(bot))