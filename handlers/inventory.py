from enum import Enum
from handlers.database import Database
import discord

class ItemEnums(Enum):
    # Pet Items
    BasicPetFood = ('Basic Food', 0, 'Basic food for pets.')

    #region property getters
    @property
    def name(self):
        return self.value[0]

    @property
    def emoji(self):
        return self.value[1]

    @property
    def description(self):
        return self.value[2]
    #endregion

class Inventory:
    # Inventory Handler Class
    def __init__(self):
        self.db = Database()

    def add_item(self, user_id: int, item: ItemEnums, amount: int):
        user_data = self.db.universal_find_one('users', {'user_id': user_id})
        if not user_data:
            return
        if item.name in user_data['inventory']:
            user_data['inventory'][item.name] += amount
        else:
            user_data['inventory'][item.name] = amount
        self.db.universal_update('users', {'user_id': user_id}, {'$set': user_data})

    def remove_item(self, user_id: int, item: ItemEnums, amount: int):
        user_data = self.db.universal_find_one('users', {'user_id': user_id})
        if not user_data:
            return
        if item.name in user_data['inventory']:
            user_data['inventory'][item.name] -= amount
        else:
            return
        self.db.universal_update('users', {'user_id': user_id}, {'$set': user_data})

    def get_inventory(self, user_id: int):
        user_data = self.db.universal_find_one('users', {'user_id': user_id})
        if not user_data:
            return
        return user_data['inventory']

    def get_item(self, user_id: int, item: ItemEnums):
        user_data = self.db.universal_find_one('users', {'user_id': user_id})
        if not user_data:
            return
        if item.name in user_data['inventory']:
            return user_data['inventory'][item.name]
        else:
            return 0
