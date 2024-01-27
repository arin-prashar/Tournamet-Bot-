from ast import Dict
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List,Dict

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
        config=collection["Tournament Config"]
        data=config.find_one({"_id":T_id})
        return data
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    
def update(guild_id:int,T_id:int,t_name:str,slots:int,team_size:int,role:int): #updates the tournament config
    try:
        collection=db[str(guild_id)]
        data=collection["Tournament Config"]
        data.update_one({"_id":T_id},{"$set":{"Tournament Name":t_name,"slots":slots,"team_size":team_size,"role":role} })
    except Exception as e:
        print(e)
        return f"Error \n{e}\n\n"
    