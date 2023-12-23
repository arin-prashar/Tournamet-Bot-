import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import DB

load_dotenv()

bot=commands.Bot(command_prefix='!',intents=discord.Intents.all())
slot=40
rle=1188099693549465732
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is ready.')
    print("Logged in as: " + bot.user.name + "\n")
    bot.activity = discord.Activity(type=discord.ActivityType.watching, name="You")
    await bot.change_presence(activity=bot.activity)


#send dm to the command user and with prompts to enter his Ingame name and User ID
@bot.command()
async def rr(ctx,role:discord.Role):
    # reaction role
    global rle
    rle=role.id
    msg = await ctx.send('React with 🎮 to register for tournament')
    await msg.add_reaction('🎮')

@bot.event
async def on_raw_reaction_add(payload):
    # reaction role
    global slot,rle
    if payload.member.bot:
        return
    if payload.channel_id==1100772553724792935:
        if payload.emoji.name=='🎮':
            guild=bot.get_guild(payload.guild_id)
            role=guild.get_role(rle)
            await payload.member.send('Do you want to register for the tournament? (yes/no)')
            option=await bot.wait_for('message')
            if option.content=='no':
                return
            await payload.member.send('Enter your Ingame name')
            msg=await bot.wait_for('message')
            ign=msg.content
            await payload.member.send('Enter your User ID')
            while True:
                msg=await bot.wait_for('message')
                try:
                    uid=int(msg.content)
                    break
                except:
                    await payload.member.send('Invalid User ID')
                    await payload.member.send('Please Send UID again')
                DB.insert(payload.guild_id,payload.member.id,payload.member.name,ign,uid)
                await payload.member.add_roles(role)
                slot-=1
                return

@bot.command()
async def slots(ctx,n:int):
    #slots
    global slots
    slot:int=n

@bot.command()
async def add(ctx,mem:discord.Member,ign:str,uid:int):
    #add a user to the tournament
    global slot
    if slot==0:
        await ctx.send('Slots are full')
        return
    DB.insert(ctx.guild.id,mem.id,mem.name,ign,uid)
    await ctx.send('Added')

@bot.command()
async def remove(ctx,mem:discord.Member):
    #remove a user from the tournament
    DB.delete(ctx.guild.id,mem.id)
    await ctx.send('Removed')

@bot.command()
async def find(ctx,mem:discord.Member):
    #find a user in the tournament
    data=DB.find(ctx.guild.id,mem.id)
    await ctx.send(data)

@bot.command()
async def list(ctx):
    #list all the users in the tournament
    data=DB.list(ctx.guild.id)
    await ctx.send(data)

@bot.command()
async def clear(ctx):
    #clear the tournament
    DB.clear(ctx.guild.id)
    await ctx.send('Cleared')

@bot.command()
async def update(ctx,mem:discord.Member,ign:str,uid:int):
    #update the user data
    DB.update(ctx.guild.id,mem.id,ign,uid)
    await ctx.send('Updated')

@bot.command()
async def help(ctx):
    #help
    embed=discord.Embed(title='Commands',description='List of commands',color=0x00ff00)
    embed.add_field(name='!slots',value='Set the number of slots in the tournament',inline=False)
    embed.add_field(name='!add',value='Add a user to the tournament',inline=False)
    embed.add_field(name='!remove',value='Remove a user from the tournament',inline=False)
    embed.add_field(name='!find',value='Find a user in the tournament',inline=False)
    embed.add_field(name='!list',value='List all the users in the tournament',inline=False)
    embed.add_field(name='!clear',value='Clear the tournament',inline=False)
    embed.add_field(name='!update',value='Update the user data',inline=False)
    embed.add_field(name='!rr',value='Reaction role',inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv('TOKEN'))