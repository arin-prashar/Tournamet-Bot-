import discord
from discord.ext import commands
from discord.utils import get
import DB as DB

class Seed(commands.Cog):
    def  __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    def seed(ctx):
        pass



async def setup(bot):
    await bot.add_cog(Seed(bot))