import discord 
import asyncio
import os 
import json 

from discord.ext import commands 
from discord import app_commands
from pathlib import Path
from utils.log import setup_logging
from utils.log import send_log
from utils.config import CONFIG_PATH

class BadWordsConfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    async def config_update(self, word: str):
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        data.setdefault("bad-words", [])

        if word not in data["bad-words"]:
            data["bad-words"].append(word)

        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @app_commands.command(name="badwords", description="Set bad word to config")
    async def badwords(
        self,
        interaction: discord.Interaction,
        bad_word: str
    ):
        await interaction.response.defer(ephemeral=True)


        updated = {}

        try:
            await self.config_update(bad_word.lower())

            await interaction.followup.send(
                embed=discord.Embed(
                    title="Bad Word Added",
                    description=f"{bad_word} is now blocked",
                    color=discord.Color.green()
                )
            )

        except Exception as e:
               print(f"Failed ❌ to add bad word to config: {e}")
               await interaction.followup.send(
                embed = discord.Embed(
                    title="❌ Error",
                    description="Could not add bad word to config",
                    color=discord.Color.red()
                )
            )

async def setup(bot):
    await bot.add_cog(BadWordsConfig(bot))