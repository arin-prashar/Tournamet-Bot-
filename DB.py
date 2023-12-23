import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

passwd=os.environ.get('DB_PASS')
uri=f'mongodb+srv://dkg:{passwd}@cluster0.zehbxvy.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(uri)

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
    collection[f'{guild_id}'].delete_one({'discord_id':discord_id})
    return 'Deleted'

def find(guild_id:int,discord_id:int)->str:
    #find the user data from the database
    collection=db['Tournament']
    data=collection[f'{guild_id}'].find_one({'discord_id':discord_id})
    return data

def list(guild_id:int)->List:
    #list all the users from the database
    collection=db['Tournament']
    data=collection[f'{guild_id}'].find()
    return data
