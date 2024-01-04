import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
load_dotenv()

bot=commands.Bot(command_prefix='!',intents=discord.Intents.all())
bot.remove_command('help')

cogs=['Config','Register','Seed']
@bot.event
async def on_ready():
    print('Bot is ready.')
    print("Logged in as: " + bot.user.name + "\n")
    bot.activity = discord.Activity(type=discord.ActivityType.playing, name="With at Spectral Eclipse")
    for cog in cogs:
        await bot.load_extension(cog)
        print(f"Loaded {cog}")
    await bot.change_presence(activity=bot.activity)

@bot.command()
async def help(ctx):
    #help
    embed=discord.Embed(title='Commands',description='List of commands',color=0x00ff00)
    embed.add_field(name='!create',value='Creates a tournament.',inline=False)
    embed.add_field(name='!delete',value='Deletes a tournament.',inline=False)
    embed.add_field(name='!get',value='Gets a tournament.',inline=False)
    embed.add_field(name='!update',value='Updates a tournament.',inline=False)
    embed.add_field(name='!list',value='Lists all tournaments.',inline=False)
    embed.add_field(name='!register',value='Registers a team.',inline=False)
    embed.add_field(name='!seed',value='Seeds a tournament.',inline=False)
    embed.add_field(name='!unregister',value='Unregisters a team.',inline=False)
    embed.add_field(name='!confirm',value='Confirms Your entry.',inline=False)
    embed.add_field(name='!help',value='Shows this message.',inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv('TOKEN'))