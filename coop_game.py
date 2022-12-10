
from database import Database
import typing 

class COOPGenshin:
    def __init__(self, main_database: Database) -> None:

        self.coop_db = main_database.coop.gi
        self.warn_db = main_database.warns.gi
        self.profile_db = main_database.profiles.gi

        self.roles = main_database.roles.gi

        self.roles_map = {}

    
    def carry_roles_map(self):

        for role in self.roles.find({}, {'_id': 0}):
            self.roles_map = {**self.roles_map, **role}
        
    def profile_template(self, discord_id: int, rank: int, img: str, color: int , description: str, thumb: str, profiles : typing.Union[list, dict]):

        return {
            'rank': rank,
            'img': img,
            'color': color,
            'description': description,
            'thumb': thumb,
            'profiles': profiles,
            'discord_id' : discord_id
        }
    
    def genshin_profile_template(self, uid: int, region: str, rank: int):

        return {
            'uid': uid,
            'region': region,
            'rank': rank
        }

    

    def get_user_profile(self, discord_id: str):

        checker = list(self.profile_db.find({'discord_id': discord_id}, {'_id': 0}))[0]

        if len(checker) != 0:
            return checker
        else:
            self.profile_db.insert_one(self.profile_template(discord_id, 10, 'https://notsetup.com', 123901, 'asdasd', '', []))

            return self.profile_template(discord_id, 10, 'https://notsetup.com', 123901, 'asdasd', '', [])
    

    def update_user_profile(self, discord_id : str, updated_data : dict):
        checker = list(self.profile_db.find({'discord_id': discord_id}, {'_id': 1}))[0]

        if len(checker) != 0:
            self.profile_db.update_one({'_id': checker}, {'$set': updated_data})
            return True


    
