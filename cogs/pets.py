import discord
from discord.ext import commands
from discord.ui import View, Button, Select
from handlers.InventoryEnums import InventoryEnums


class PetItemSelect(Select):
    super().__init__(custom_id=None, min_values=1, max_values=25, options=None, disabled=False)

    async def callback(self, interaction: discord.Interaction):
        pass


class PetActionButton(Button):
    super().__init__(label=None, custom_id=None, emoji=None, disabled=False)

    async def callback(self, interaction: discord.Interaction):
        if self.custom_id == 'pet_feed':
            # Connect to the database and make sure that hunger is set to 100
            # Make sure that the user has pet food in their inventory first.
            pass
        elif self.custom_id == 'pet_play':
            # Connect to the database and make sure that happiness is set to 100
            # If the user has a "toy" item, give the user the option to use it for extra happiness
            pass
        elif self.custom_id == 'pet_cancel':
            # Disable the buttons on the current view.
            pass


class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Pets(bot))
