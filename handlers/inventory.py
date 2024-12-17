from enum import Enum
from handlers.database import Database
import discord

class ItemEnums(Enum):
    BasicPetFood = ('Basic Food', 0, 'Basic food for pets.')

class Inventory:
    # Inventory Handler Class
    def __init__(self):
        self.db = Database()

    async def get(self, ctx, user_id: int):
        pass

    async def add_item(self, ctx, item: ItemEnums, user_id: int):
        pass

    