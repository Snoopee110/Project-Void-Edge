import discord
from discord.ext import commands
from handlers.database import Database
from handlers import config
from handlers.badges import LevelBadges, Badges
from handlers.roles import Roles

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': message.author.id})
        if not user_data:
            user_data = {
                'user_id': message.author.id,
                'username': message.author.name,
                'is_bot': message.author.bot,
                'role': None,
                'xp': 0,
                'xp_to_next_level': int((1 + 1) * (1 + 2) + 14),
                'level': config.xp_starting_level,
                'currency': 0,
                'inventory': [],
                'badges': [],
                'featured_badges': []
            }
            db.universal_insert('users', user_data)
            return
        new_level = user_data['level'] + 1
        user_data['xp'] += config.xp_per_message
        if user_data['xp'] >= user_data['xp_to_next_level']:
            user_data['level'] += 1
            user_data['xp'] = 0
            user_data['xp_to_next_level'] = int((new_level + 1) * (new_level + 2) + 14)
            # Award badges for reaching certain levels
            for level_badge in LevelBadges:
                if user_data['level'] >= level_badge.level:
                    user_data['badges'].append(level_badge.name)
        db.universal_update('users', {'user_id': message.author.id}, {'$set': user_data})

    @commands.slash_command()
    async def profile(self, ctx):
        msg = await ctx.respond(f'{config.loading_emoji} Fetching profile...')
        featured_badges = []
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
        if not user_data:
            await msg.edit(content=f'Sorry, {ctx.author.mention}, you don\'t have a profile yet.\n\nSend a message to '
                                   f'start earning XP and badges!')
            return
        role = Roles.from_name(user_data['role']) if user_data['role'] is not None else None
        progress = int((user_data['xp'] / user_data['xp_to_next_level']) * 10)
        xp_bar = '🟩' * progress + '⬜' * (10 - progress)
        embed = discord.Embed(title=f'{role.emoji if role is not None else ""} {ctx.author.display_name}\'s Profile', color=discord.Color.blue())
        embed.add_field(name='Level', value=user_data['level'], inline=True)
        embed.add_field(name='XP', value=f'{xp_bar} ({user_data["xp"]}/{user_data["xp_to_next_level"]})', inline=True)
        for badge in user_data['featured_badges']:
            badge = Badges.from_name(badge)
            featured_badges.append(badge)
        embed.add_field(name='Featured Badges', value='\n'.join([f'{badge.emoji}  {badge.name}' for badge in featured_badges]), inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await msg.edit(content=None, embed=embed)

    @commands.slash_command()
    async def set_featured_badge(self, ctx, badge):
        msg = await ctx.respond(f'{config.loading_emoji} Setting featured badge...')
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
        user_featured_badges = user_data['featured_badges']
        badge = getattr(Badges, badge.upper())
        if not user_data:
            await msg.edit(content='User not found.')
            return
        if badge.name in user_data['featured_badges']:
            await msg.edit(content=f'You already have the {badge.name} badge featured.')
            return
        if len(user_data['featured_badges']) >= 3:
            await msg.edit(content='You can only feature up to 3 badges.')
            return
        if badge.name not in user_data['badges']:
            await msg.edit(content=f'You do not have the {badge.name} badge.')
            return
        user_featured_badges.append(badge.name)
        user_data['featured_badges'] = user_featured_badges
        db.universal_update('users', {'user_id': ctx.author.id}, {'$set': user_data})
        await msg.edit(content=f'Set badge {badge.emoji} {badge.name} as a featured badge.')

    @commands.slash_command()
    async def remove_featured_badge(self, ctx, badge):
        msg = await ctx.respond(f'{config.loading_emoji} Removing featured badge...')
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
        user_featured_badges = user_data['featured_badges']
        badge = getattr(Badges, badge.upper())
        if not user_data:
            await ctx.respond('User not found.')
            return
        if badge.name not in user_data['featured_badges']:
            await ctx.respond(f'You do not have the {badge.name} badge featured.')
            return
        user_featured_badges.remove(badge.name)
        user_data['featured_badges'] = user_featured_badges
        db.universal_update('users', {'user_id': ctx.author.id}, {'$set': user_data})
        await msg.edit(content=f'Removed badge {badge.emoji} {badge.name} from featured badges.')

def setup(bot):
    bot.add_cog(Levelling(bot))