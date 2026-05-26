# Required libraries for Discord bot functionality and async operations, load secret credentials.

import discord 
import asyncio
import os 

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class Client(discord.Client):
    async def on_ready(self):
        print(f'\u2705 Successfully logined as {self.user}')

intents = discord.Intents.default()
intents.message_content = True

Discord_bot_token = os.getenv("DISCORD_TOKEN")

client = Client(intents=intents)
client.run(Discord_bot_token)