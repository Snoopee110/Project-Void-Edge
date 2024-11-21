import discord
from discord.ext import commands
import config
import datetime
import asyncio
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

# Generic print statements :)
time = datetime.datetime.now()
formatted_time = time.strftime('%d/%m/%Y %H:%M')
buildNumber = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
print(f'Starting bot...')
print(f'Version: V{os.environ.get("BOT_VERSION")}')
print(f'Time of launch: {formatted_time}')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    if os.environ.get("IS_DEV") == 'True':
        print(f'Bot is in development mode. Setting correct version.')
        await bot.change_presence(activity=discord.Game(name=f'V{os.environ.get("BOT_VERSION")} DEV'))
    else:
        print(f'Bot is in development mode. Setting correct version.')
        await bot.change_presence(activity=discord.Game(name=f'V{os.environ.get("BOT_VERSION")} Build {buildNumber}'))
    print(f'Bot is logged in.\nLogged in as: {bot.user.name} (ID: {bot.user.id})')

    print('Syncing commands...')
    await bot.sync_commands(force=True)


# Load the cogs from the cogs folder
if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename in os.getenv("ACTIVE_COGS"):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

# Run the bot
bot.run(os.environ.get('TOKEN'))
