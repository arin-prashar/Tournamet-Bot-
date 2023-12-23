import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

bot=commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')
    print("Logged in as: " + bot.user.name + "\n")
    bot.activity = discord.Activity(type=discord.ActivityType.watching, name="You")
    await bot.change_presence(activity=bot.activity)


#send dm to the command user and with prompts to enter his Ingame name and User ID
@bot.command()
async def register(ctx):
    await ctx.author.send("Please enter your Ingame name:")
    name = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    await ctx.author.send("Please enter your User ID:")
    uid = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    try:
        int(uid.content)
    except ValueError:
        await ctx.author.send("Please enter a valid User ID!")
        return
    await ctx.author.send("Thank you for registering!")
    await ctx.author.send("Your Ingame name is: " + name.content)
    await ctx.author.send("Your User ID is: " + uid.content)
    await ctx.author.send("dsicord userid is :" + str(ctx.author.id))
    
    # insert(name.content, uid.content)

bot.run(os.getenv('TOKEN'))