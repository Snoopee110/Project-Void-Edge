from discord.ext import commands
import discord
from discord.ui import Button
from handlers.database import Database
from handlers.badges import Badges

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def view_user(self, ctx, user: discord.User):
        await ctx.defer()
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': user.id})
        if not user_data:
            await ctx.send('User not found.')
            return
        progress = int((user_data['xp'] / user_data['xp_to_next_level']) * 10)  # Assuming 10 steps for the XP bar
        xp_bar = '🟩' * progress + '⬜' * (10 - progress)
        embed = discord.Embed(title=f'User Data for {user.display_name}', color=discord.Color.blue()) if not user_data['is_bot'] \
           else discord.Embed(title=f'User Data for {user.display_name} (Bot)', color=discord.Color.green())
        embed.add_field(name='Username', value=user_data['username'], inline=True)
        embed.add_field(name='User ID', value=user_data['user_id'], inline=True)
        embed.add_field(name='Role', value=f'{user_data["role"] if user_data["role"] else "No Role"}', inline=True)
        embed.add_field(name='Level', value=user_data['level'], inline=True)
        embed.add_field(name='XP', value=f"{xp_bar} ({user_data['xp']}/{user_data['xp_to_next_level']})", inline=False)
        embed.add_field(name='Currency', value=user_data['currency'], inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    @commands.is_owner()
    async def give_badge(self, ctx, user: discord.User, badge):
        await ctx.defer()
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': user.id})
        if not user_data:
            await ctx.respond('User not found.')
            return
        badge = getattr(Badges, badge.upper())
        user_data['badges'].append(badge.name)
        db.universal_update('users', {'user_id': user.id}, {'$set': user_data})
        await ctx.respond(f'Gave {badge.name} to {user.display_name}.')

def setup(bot):
    bot.add_cog(Admin(bot))