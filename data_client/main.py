from database import BotDatabase
from datetime import datetime
from requests_cache import CachedSession


class DataClient:

    def __init__(self, database: BotDatabase) -> None:
        self.db = database.data
        self.check_interval = {
            'characters' : 86400 * 30 #after a month
        }
        self._session = CachedSession(
                            cache_name='g.fandom',
                            backend='filesystem',
                            expire_after=7200,
                            serializer='pickle',
                            allowable_methods='GET',
                            stale_if_error=True
        )


    @property
    def timestamp(self):
        return datetime.now()

    def exists(self, key: str):

        checker = self.db.list_collection_names(filter={'name': key})
        return len(checker) != 0
    

    def get_data(self, key: str):

        if self.exists(key):

            return self.db.get_collection(key).find({'', {'_id': 0}})[0]
    
    def save_data(self, key : str, data : dict):

        if self.exists(key):

            data_id =  self.db.get_collection(key).find({'', {'_id': 1}})[0]['_id']
            self.db.get_collection(key).update_one({'_id': data_id}, {'$set': data})
            return True
        else:

            self.db.key.insert_one(data)
    
    def pending_update(self, key: str):

        if self.exists(key):

            data = self.db.get_collection(key).find({'', {'_id': 0}})[0]

            timestamp_last = datetime.strptime(data['timestamp'], '%c')

            return (self.timestamp - timestamp_last).total_seconds() > self.check_interval[data['type']]
        
        else:

            return True

