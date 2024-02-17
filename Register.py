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
        players=DB.get_players(interaction.guild.id)
        if interaction.user.id not in players:
            await interaction.response.send_message("Please add your self as a player by using >>register",ephemeral=True)
            return
        T_id=interaction.message.embeds[0].fields[1].value
        DB.add_player(interaction.guild.id,T_id,interaction.user.id)
        await interaction.response.send_message("Registered",ephemeral=True)
        

    @discord.ui.button(label="Unregister",style=discord.ButtonStyle.danger,emoji="❌")
    async def unregister(self,interaction:discord.Interaction,button:discord.ui.Button):
        players=DB.get_players(interaction.guild.id)
        if interaction.user.id not in players:
            await interaction.response.send_message("Please add your self as a player by using >>register",ephemeral=True)
            return
        T_id=interaction.message.embeds[0].fields[1].value
        DB.remove_player(interaction.guild.id,T_id,interaction.user.id)
        await interaction.response.send_message("Unregistered",ephemeral=True)    


class Register(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def open_registerations(self,ctx,TID:int):
        Buttons=Register_Option_Btns()
        data=DB.get(ctx.guild.id,TID)
        if data==None:
            await ctx.send("Tournament not found.")
            return
        embed=discord.Embed(title="Register for the tournament",description="Tournament Details",color=0x00ff00)
        embed.add_field(name="Tournament Name",value=data["Tournament Name"],inline=False) 
        embed.add_field(name="Tournament ID",value=data["_id"],inline=False) 
        embed.add_field(name="Slots",value=data["slots"],inline=False) 
        embed.add_field(name="Team Size",value=data["team_size"],inline=False)
        await ctx.send(embed=embed,view=Buttons) 

async def setup(bot):
    await bot.add_cog(Register(bot))
