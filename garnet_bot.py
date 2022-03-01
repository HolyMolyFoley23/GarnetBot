#!/usr/bin/env python3

import discord
import os
from discord.ext import commands
import garnet_helper
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)

CURR_DIR = os.path.dirname(__file__)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    garnet_helper.load_data()

for filename in os.listdir(os.path.join(CURR_DIR,r'cogs')):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
