# Required libraries for Discord bot functionality and async operations, load secret credentials.

import discord 
import asyncio
import os 

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

class Client(commands.Bot):
    async def setup_hook(self):
          commands_dir = Path(__file__).resolve().parent / "commands"

          for file in commands_dir.glob("*.py"):
              if file.name.startswith("_") or file.name == "__init__.py":
                  continue

              extension_name = f"commands.{file.stem}"
              await self.load_extension(extension_name)
              print(f"Loaded extension: {extension_name}")

          synced = await self.tree.sync()
          print(f"Synced {len(synced)}")

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