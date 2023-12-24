import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
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
    await mem.remove_roles(get(ctx.guild.roles,id=rle))
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