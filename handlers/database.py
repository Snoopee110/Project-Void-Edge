# A wrapper class for the pymongo library that only makes a single connection to the mongodb instance.
import pymongo
import os
import asyncio

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client.get_database(os.getenv('BOT_ID'))
        self.universal_db = self.client.get_database('global_user_data')

    #region Bot Specific Database Functions
    def find(self, collection, query):
        return self.db[collection].find(query)

    def find_one(self, collection, query):
        return self.db[collection].find_one(query)

    def insert(self, collection, document):
        return self.db[collection].insert_one(document)

    def update(self, collection, query, document):
        return self.db[collection].update_one(query, document)

    def delete(self, collection, query):
        return self.db[collection].delete_one(query)
    #endregion

    #region Universal Database Functions
    def universal_find(self, collection, query):
        return self.universal_db[collection].find(query)

    def universal_find_one(self, collection, query):
        return self.universal_db[collection].find_one(query)

    def universal_insert(self, collection, document):
        return self.universal_db[collection].insert_one(document)

    def universal_update(self, collection, query, document):
        return self.universal_db[collection].update_one(query, document)

    def universal_delete(self, collection, query):
        return self.universal_db[collection].delete_one(query)
    #endregion
