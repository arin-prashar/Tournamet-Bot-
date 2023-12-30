import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

passwd=os.getenv('PASSWD')
uri=f'mongodb+srv://dkg:{passwd}@cluster0.zehbxvy.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(uri)

# print the ip with subnet of machine
print("Your IP address is:")
os.system("curl ifconfig.me")

try:
    db.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def insert(guild_id:int,discord_id:int,discord_name:str,ign:str,uid:int)->str:
    #insert the user data into the database
    collection=db['Tournament']
    try:
        if collection[f'{guild_id}'].find_one({'discord_id':discord_id}):
            return 'Already exists'
        collection[f'{guild_id}'].insert_one({'discord_id':discord_id,'discord_name':discord_name,'ign':ign,'uid':uid})
        return 'Inserted'
    except:
        return 'Error'
        

def delete(guild_id:int,discord_id:int)->str:
    #delete the user data from the database
    collection=db['Tournament']
    try:
        collection[f'{guild_id}'].delete_one({'discord_id':discord_id})
        return 'Deleted'
    except:
        return 'Error'

def find(guild_id:int,discord_id:int)->str:
    #find the user data from the database
    collection=db['Tournament']
    try:
        data=collection[f'{guild_id}'].find_one({'discord_id':discord_id})
        if data:
            return data
        else:
            return 'Not found'
    except:
        return 'Error'

def list(guild_id:int)->List:
    #list all the users from the database
    collection=db['Tournament']
    try:
        x=[]
        data=collection[f'{guild_id}'].find()
        for i in data:
            x.append(i)
        if x==[]:
            return 'Empty'
        else:
            return x
    except:
        return 'Error'

def clear(guild_id:int)->str:
    #clear the database
    collection=db['Tournament']
    try:
        collection[f'{guild_id}'].drop()
        return 'Cleared'
    except:
        return 'Error'