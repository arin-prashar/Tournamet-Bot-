import discord  
from discord import ui
from discord.ui import Button,View
from discord.ext import commands
from discord.utils import get
import asyncio
import DB
    

class Register_Option_Btns(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Register",style=discord.ButtonStyle.green,emoji="✅")
    async def register(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Register",ephemeral=True)
        print("Register")

    @discord.ui.button(label="Unregister",style=discord.ButtonStyle.danger,emoji="❌")
    async def unregister(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message("Unregister",ephemeral=True)
        print("Unregister")
    


class Register(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def open_registerations(ctx,TID):
        Buttons=Register_Option_Btns()
        tourn_data=DB.get(ctx.guild.id,TID) # type: ignore
        embed=discord.Embed(title="Register for the tournament",description="Tournament Details",color=0x00ff00)
        embed.add_field(name="Tournament Name",value=tourn_data,inline=False)
        embed.add_field(name="Tournament ID",value=TID,inline=False)
        embed.add_field(name="Registerations Open",value="Yes",inline=False)
        embed.add_field(name="Number of Slots",value=None,inline=False)

async def setup(bot):
    await bot.add_cog(Register(bot))