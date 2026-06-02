import discord
import aiohttp
from discord.ext import commands
from discord import app_commands

class cat_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cat", description="A fun command that gets a random cat!")
    async def cat(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search?has_breeds=1"
            ) as resp:
                data = await resp.json()

        cat = data[0]
        image_url = cat["url"]

        embed = discord.Embed(title="🐱 Random Cat")

        if cat.get("breeds"):
            breed = cat["breeds"][0]

            embed.add_field(
                name="Breed",
                value=breed.get("name", "Unknown"),
                inline=False
            )

            if breed.get("temperament"):
                embed.add_field(
                    name="temperament",
                    value=breed["temperament"][:1024],
                    inline=False
                )

        else:
            embed.add_field(
                name="Breed",
                value="Unknown",
                inline=False
            )

        embed.set_image(url=image_url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(cat_command(bot))