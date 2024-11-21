# A wrapper class for the pymongo library that only makes a single connection to the mongodb instance.
import pymongo

class Database:
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.get_default_database()

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

    def count(self, collection):
        return self.db[collection].count()

    def close(self):
        self.client.close()