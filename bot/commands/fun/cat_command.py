import discord
import aiohttp
import time
from discord.ext import commands
from discord import app_commands
import random
import io
import os

class cat_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cat", description="A fun command that gets a random cat!")
    async def cat(self, interaction: discord.Interaction):

        seed = random.randint(1, 10_000_000)
        image_url = f"https://cataas.com/cat?width=380&height=520&seed={seed}"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status != 200:
                    return await interaction.response.send_message(
                        "Failed to fetch cat image.",
                        ephemeral=True
                    )

                image_data = await resp.read()

        os.makedirs("cats", exist_ok=True)

        local_path = f"cats/{seed}.jpg"

        with open(local_path, "wb") as f:
            f.write(image_data)

        file = discord.File(
            io.BytesIO(image_data),
            filename="cat.jpg"
        )
        
        embed = discord.Embed(title="🐱 Random Cat")

        embed.set_image(url="attachment://cat.jpg")

        await interaction.response.send_message(
            embed=embed,
            file=file
        )

        os.remove(local_path)

async def setup(bot):
    await bot.add_cog(cat_command(bot))