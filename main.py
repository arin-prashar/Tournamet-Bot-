import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import argparse

# 2 args ,first is dbpass, second is token
parser = argparse.ArgumentParser()
# no var argument
parser.add_argument('--t', type=str, help='Discord bot token', required=True)
args = parser.parse_args()
os.environ['TOKEN'] = args.t

import DB 
load_dotenv()


bot=commands.Bot(command_prefix='!',intents=discord.Intents.all())
slot=40
rle=1187975519959003166
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is ready.')
    print("Logged in as: " + bot.user.name + "\n")
    bot.activity = discord.Activity(type=discord.ActivityType.playing, name="With at Spectral Eclipse")
    await bot.change_presence(activity=bot.activity)


#send dm to the command user and with prompts to enter his Ingame name and User ID
@bot.command()
async def rr(ctx,role:discord.Role):
    # reaction role
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
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
    if payload.channel_id==1187975459959492618:
        if payload.emoji.name=='🎮':
            guild=bot.get_guild(payload.guild_id)
            role=get(guild.roles,id=rle)
            def check(m):
                return m.author==payload.member and m.channel==payload.member.dm_channel
            await payload.member.send('Enter your Ingame name')
            msg=await bot.wait_for('message',check=check)
            ign=msg.content
            await payload.member.send('Enter your User ID')
            msg=await bot.wait_for('message',check=check)
            uid=int(msg.content)

            res=DB.insert(payload.guild_id,payload.member.id,payload.member.name,ign,uid)
            if res=='Already exists':
                await payload.member.send('Already registered for the tournament')
            elif res=='Error':
                await payload.member.send('Error occured')
            elif res=='Inserted':
                slot-=1
            await payload.member.add_roles(role)
            await payload.member.send('You have been registered for the tournament')
            await log(payload)

async def log(payload):
    # reaction role
        guild=bot.get_guild(payload.guild_id)
        member=guild.get_member(payload.user_id)
        ign=DB.find(payload.guild_id,payload.user_id)['ign']
        uid=DB.find(payload.guild_id,payload.user_id)['uid']
        msg=f'''```json
Discord ID: {member.id}
Discord Name: {member.name}
Ingame Name: {ign}
User ID: {uid}```'''
        await bot.get_channel(1188017123595919400).send(msg)

@bot.command()
async def slots(ctx,n:int):
    #slots
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    global slots
    slot:int=n

@bot.command()
async def add(ctx,mem:discord.Member,ign:str,uid:int):
    #add a user to the tournament
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    global slot
    if slot==0:
        await ctx.send('Slots are full')
        return
    DB.insert(ctx.guild.id,mem.id,mem.name,ign,uid)
    slot-=1
    await ctx.send('Added')

@bot.command()
async def remove(ctx,mem:discord.Member):
    #remove a user from the tournament
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    DB.delete(ctx.guild.id,mem.id)
    await mem.remove_roles(get(ctx.guild.roles,id=rle))
    slot+=1
    await ctx.send('Removed')

@bot.command()
async def find(ctx,mem:discord.Member):
    #find a user in the tournament
    data=DB.find(ctx.guild.id,mem.id)
    if data=='Not found':
        await ctx.send('Not found')
        return
    # formatting the data    
    embed=discord.Embed(title='User Data',description='',color=0x00ff00)
    embed.set_thumbnail(url=mem.avatar)
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=ctx.author.avatar)
    embed.add_field(name='Discord Name',value=data['discord_name'],inline=False)
    embed.add_field(name='Discord ID',value=data['discord_id'],inline=False)
    embed.add_field(name='Ingame Name',value=data['ign'],inline=False)
    embed.add_field(name='User ID',value=data['uid'],inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
    #list all the users in the tournament
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    data=DB.list(ctx.guild.id)
    if data=='Empty':
        await ctx.send('Empty')
        return
    # formatting the data
    for i in data:
        embed=discord.Embed(title='User Data',description='',color=0x00ff00)
        embed.set_thumbnail(url=ctx.guild.get_member(i['discord_id']).avatar)
        embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=ctx.author.avatar)
        embed.add_field(name='Discord Name',value=i['discord_name'],inline=False)
        embed.add_field(name='Discord ID',value=i['discord_id'],inline=False)
        embed.add_field(name='Ingame Name',value=i['ign'],inline=False)
        embed.add_field(name='User ID',value=i['uid'],inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    #clear the tournament
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    global slot
    slot=40
    DB.clear(ctx.guild.id)
    await ctx.send('Cleared')

@bot.command()
async def update(ctx,mem:discord.Member,ign:str,uid:int):
    #update the user data
    if ctx.author.bot:
        return
    # admin only
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('Only admins can use this command')
        return
    DB.update(ctx.guild.id,mem.id,ign,uid)
    await ctx.send('Updated')

@bot.command()
async def help(ctx):
    #help
    embed=discord.Embed(title='Commands',description='List of commands',color=0x00ff00)
    embed.add_field(name='!rr <role>',value='Reaction role',inline=False)
    embed.add_field(name='!slots <number>',value='Set the number of slots',inline=False)
    embed.add_field(name='!add <member> <ign> <uid>',value='Add a member to the tournament',inline=False)
    embed.add_field(name='!remove <member>',value='Remove a member from the tournament',inline=False)
    embed.add_field(name='!find <member>',value='Find a member in the tournament',inline=False)
    embed.add_field(name='!list',value='List all the members in the tournament',inline=False)
    embed.add_field(name='!clear',value='Clear the tournament',inline=False)
    embed.add_field(name='!update <member> <ign> <uid>',value='Update the member data',inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv('TOKEN'))