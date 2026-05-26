# Required libraries for Discord bot functionality and async operations, load secret credentials.

import discord 
import asyncio
import os 

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()

class Client(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("commands.setup_logging_command")

    async def on_ready(self):
        print(f'\u2705 Successfully logined as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f'Message from {message.author}: {message.content}')

        await self.process_commands(message)

intents = discord.Intents.default()
intents.message_content = True

Discord_bot_token = os.getenv("DISCORD_TOKEN")

client = Client(command_prefix="!", intents=intents)
client.run(Discord_bot_token)