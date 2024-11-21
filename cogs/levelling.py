import discord
from discord.ext import commands
from handlers.database import Database
from handlers import config
from handlers.badges import LevelBadges, Badges

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
                'xp_to_next_level': config.xp_levelup_formula,
                'level': config.xp_starting_level,
                'currency': 0,
                'inventory': [],
                'badges': [],
                'featured_badges': []
            }
            db.universal_insert('users', user_data)
            return
        old_level = user_data['level']
        user_data['xp'] += config.xp_per_message
        if user_data['xp'] >= user_data['xp_to_next_level']:
            user_data['level'] += 1
            user_data['xp'] = 0
            user_data['xp_to_next_level'] = int((old_level + 1) * (old_level + 2) + 14)
            # Award badges for reaching certain levels
            for level_badge in LevelBadges:
                if user_data['level'] == level_badge.level:
                    user_data['badges'].append(level_badge.name)
        db.universal_update('users', {'user_id': message.author.id}, {'$set': user_data})

    @commands.slash_command()
    async def profile(self, ctx):
        await ctx.defer()
        featured_badges = []
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
        if not user_data:
            await ctx.respond('User not found.')
            return
        progress = int((user_data['xp'] / user_data['xp_to_next_level']) * 10)
        xp_bar = '🟩' * progress + '⬜' * (10 - progress)
        embed = discord.Embed(title=f'User Data for {ctx.author.display_name}', color=discord.Color.blue())
        embed.add_field(name='Level', value=user_data['level'], inline=True)
        embed.add_field(name='XP', value=f'{xp_bar} ({user_data["xp"]}/{user_data["xp_to_next_level"]})', inline=True)
        for badge in user_data['badges']:
            badge = Badges.from_name(badge)
            featured_badges.append(badge)
        embed.add_field(name='Featured Badges', value='\n'.join([f'{badge.emoji} {badge.name}' for badge in featured_badges]), inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def set_featured_badges(self, ctx, badge1, badge2, badge3):
        await ctx.defer()
        db = Database()
        user_data = db.universal_find_one('users', {'user_id': ctx.author.id})
        if not user_data:
            await ctx.respond('User not found.')
            return
        badges = [badge1.capitalize(), badge2.capitalize(), badge3.capitalize()]
        for badge in badges:
            badge = Badges.from_name(badge)
            if badge.name not in user_data['badges']:
                await ctx.respond(f'You do not have the {badge.name} badge.')
                return
            if badge.name in user_data['featured_badges']:
                await ctx.respond(f'You already have the {badge.name} badge featured.')
                return
            user_data['featured_badges'].append(badge.name)
        db.universal_update('users', {'user_id': ctx.author.id}, {'$set': user_data})
        await ctx.respond('Featured badges set.')

def setup(bot):
    bot.add_cog(Levelling(bot))