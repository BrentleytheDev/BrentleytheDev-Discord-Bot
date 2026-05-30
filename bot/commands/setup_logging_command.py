import discord 
import asyncio
import os 
import json 

from discord.ext import commands 
from discord import app_commands
from pathlib import Path
from utils.log import setup_logging
from utils.log import send_log

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "automod" / "config.json"

async def setup(bot):
        await bot.add_cog(Logging(bot))

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="logging_channel", description="Set a logging channel")
    async def logging_channel(
        self,
        interaction,
        general: discord.TextChannel,
        bans: discord.TextChannel = None,
        kicks: discord.TextChannel = None,
        message_edits: discord.TextChannel = None,
        delete_message: discord.TextChannel = None,
        join_logging: discord.TextChannel = None,
        react_message: discord.TextChannel = None
    ):
        await interaction.response.defer(ephemeral=True)

        fields = {
            "general": (general, "general-server-logging"),
            "bans": (bans, "ban-logging"),
            "kicks": (kicks, "kick-logging"),
            "message_edits": (message_edits, "message-edits"),
            "delete_message": (delete_message, "delete-messages"),
            "join_logging": (join_logging, "join-logging"),
            "react_message": (react_message, "react-message")
        }

        updated = {}

        try:
             for name, (channel, key) in fields.items():
                 if channel:
                       await setup_logging(key, channel.id)
                       updated[name] = channel.mention

             if not updated:
                  await interaction.followup.send("You didn't provide any channels.")
                  return


             await interaction.followup.send(
                embed = discord.Embed(
                        title="Logging channel configured",
                        description=f"General server logs will be sent to {channel.mention}.",
                        color=discord.Color.green()
                    )
             )
        except:
             print("Failed ❌")
