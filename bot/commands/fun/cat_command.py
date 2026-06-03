import discord
import aiohttp
import time
from discord.ext import commands
from discord import app_commands

class cat_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cat", description="A fun command that gets a random cat!")
    async def cat(self, interaction: discord.Interaction):

        image_url = f"https://cataas.com/cat?width=380&height=520&t={int(time.time())}"
        
        embed = discord.Embed(title="🐱 Random Cat")

        embed.set_image(url=image_url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(cat_command(bot))