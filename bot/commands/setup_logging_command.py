import discord 
import asyncio
import os 
import json 

from discord.ext import commands 
from discord import app_commands
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "automod" / "config.json"

async def setup(bot):
        await bot.add_cog(Logging(bot))

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="logging_channel", description="Set the general logging channel")
    async def logging_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer(ephemeral=True)
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
                
                if "logging" not in data:
                    data["logging"] = {}
                data["logging"]["general-server-logging"] = channel.id

                with CONFIG_PATH.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

                await interaction.followup.send(
                    embed = discord.Embed(
                        title="Logging channel configured",
                        description=f"General server logs will be sent to {channel.mention}.",
                        color=discord.Color.green()
                    )
                )
        except:
             print("Failed :(")