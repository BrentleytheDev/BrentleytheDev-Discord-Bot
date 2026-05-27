# Import Discord bot libraries and load environment variables
import discord 
import os 

from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

# Creates a class called Client to initialize our bot
class Client(commands.Bot):
    async def setup_hook(self):
          commands_dir = Path(__file__).resolve().parent / "commands"
          
          # Looks in commands directory and skips loading __init__.py or _ files
          for file in commands_dir.glob("*.py"):
              if file.name.startswith("_") or file.name == "__init__.py":
                  continue

              extension_name = f"commands.{file.stem}"
              await self.load_extension(extension_name)
              print(f"Loaded extension: {extension_name}")

          synced = await self.tree.sync()
          print(f"Synced {len(synced)}")

    async def on_ready(self):
        print(f'\u2705 Successfully logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f'Message from {message.author}: {message.content}')

        # Allow commands to work inside on_message
        await self.process_commands(message)

intents = discord.Intents.default()
# We enabled message_content so Discord bot can use messages
intents.message_content = True

# Load bot token from environment variables
Discord_bot_token = os.getenv("DISCORD_TOKEN")

client = Client(command_prefix="!", intents=intents)
client.run(Discord_bot_token)