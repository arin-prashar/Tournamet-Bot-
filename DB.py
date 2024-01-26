import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

uri=os.getenv('uri')
db = MongoClient(uri)

try:
    db.admin.command('ping')
    print("\nPinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def create(guild_id:int,tname:str,slots:int,team_size:int,role_m:int,role_p:int): #creates a new guild in the database
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        if tname in data.distinct("Tournament Name"):
            # throw a error
            return "Tournament Name already exists."
        x=data.count_documents({})
        dt={"_id":x+1,
            "Tournament Name":tname,
            "slots":slots,
            "team_size":team_size,
            "role_m":role_m,
            "role_p":role_p
            }
        # return the db id
        data_inserted_id=data.insert_one(dt)
        return data_inserted_id.inserted_id
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def delete(guild_id:int,T_id:int): #deletes a tournament from the config and the tournamnent db
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        data.delete_one({"_id":T_id})
        collection.drop_collection(str(T_id))
        data.update_many({"_id":{"$gt":T_id}},{"$inc":{"_id":-1}})
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def get(guild_id:int,T_id:int): #returns the tournament config
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        return data.find_one({"_id":T_id})
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def update(guild_id:int,T_id:int,slots:int,team_size:int,role:int): #updates the tournament config
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        data.update_one({"_id":T_id},{"$set":{"slots":slots,"team_size":team_size,"role":role}})
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def list(guild_id:int): #returns all the tournaments in the guild
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        return data.find()
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"

def register(guild_id:int,T_id:int,tname:str,manager_id:int,manager_name:str,player:List,player_name:List,IGN:List,UID:List): #registers a team to the tournament
    try:
        collection=db[str(guild_id)]
        data=collection[str(T_id)]
        if tname in data.distinct("Team Name"):
            # throw a error
            return "Team Name already exists."
        x=data.count_documents({})
        dt={"_id":x+1,
            "Team Name":tname,
            "Manager-ID":manager_id,
            "Manager_Name":manager_name,
            "Player-ID":player,
            "Player_Name":player_name,
            "IGN":IGN,
            "UID":UID
            }
        data.insert_one()
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"

def get_teams(guild_id:int,T_id:int): #returns all the teams in the tournament
    try:
        collection=db[str(guild_id)]
        data=collection[str(T_id)]
        return data.find()
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def get_team(guild_id:int,T_id:int,tname:str): #returns a team from the tournament
    try:
        collection=db[str(guild_id)]
        data=collection[str(T_id)]
        return data.find_one({"Team Name":tname})
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"