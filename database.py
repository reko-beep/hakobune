from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import *



class BotDatabase:

    def __init__(self) -> None:

        self.client = MongoClient('mongodb://127.0.0.1/', port=27017)

        self.lfg : Database  = self.client.lfg
        self.profiles : Database = self.client.profiles
        self.coop : Database = self.client.coop
        self.warns: Database = self.client.warns
        self.roles : Database = self.client.roles
        self.data : Database = self.client.data


    def lfg_template(self, game_name: str, game_url : str, members: list = []):

        return {
            'name': game_name, 
            'url': game_url,
            'type': '',
            'members': members
        }
    
    def profile_template(self, member : str,  game_prefix: str, data : dict):
    
        checker = self.profiles

    def collection(self, database_name: str, item_id : str) -> Collection:
       
        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)
        print(filter)
        if len(checker) != 0:
            return self.client[database_name][item_id]
        else:
            return self.client[database_name].create_collection(item_id)

    def document(self, database_name : str, item_id : str, return_id : bool = False) -> dict:

        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)        
        if len(checker) != 0:
            dict__ = {}
            id_filter = 1 if return_id else 0            
            for doc in self.client[database_name][item_id].find({}, {'_id': id_filter}):
                
                dict__ = {**dict__, **doc}
            
            return dict__
        
        return None
        
    def update(self, database_name: str, item_id: str, updated_data: dict) -> bool:

        filter = {"name": item_id}
        checker = self.client[database_name].list_collection_names(filter=filter)        
        if len(checker) != 0:
            dict__ = {}
            id_filter = 1     
            if len(list(self.client[database_name][item_id].find({}, {'_id': id_filter}))) != 0: 
                id_ = list(self.client[database_name][item_id].find({}, {'_id': id_filter}))[0]['_id']
                self.client[database_name][item_id].update_one({'_id': id_}, {'$set': updated_data})
            else:
                self.client[database_name][item_id].insert_one(updated_data)


            
            return True
             
        return False




