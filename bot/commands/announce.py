import discord
import json
import re
from discord.ext import commands
from discord import app_commands

from utils.config import open_config

EMOJI_REGEX = re.compile(r"<a?:\w+:(\d+)>")

class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_color(self, name: str):
        colors = {
            "red": discord.Color.red(),
            "green": discord.Color.green(),
            "blue": discord.Color.blue(),
            "gold": discord.Color.gold(),
            "purple": discord.Color.purple(),
            "default": discord.Color.blurple()
        }
        return colors.get(name.lower(), discord.Color.blurple())

    @app_commands.command(name="announce", description="Make an announcement!")
    async def announce(
        self,
        interaction: discord.Interaction,
        title: str,
        message: str,
        thumbnail: str | None = None,
        banner : str | None = None
    ):
        config = await open_config()
        ann = config.get("announcement", {})

        channel_id = int(ann.get("channel_id"))
        if not channel_id:
            return await interaction.response.send_message(
                "No announcement channel set in config.json",
                ephemeral=True
            )

        color_name = ann.get("color", "blue")

        embed = discord.Embed(
            title=title,
            description=message,
            color=self.get_color(color_name)
        )

        embed.set_footer(
            text=f"Annoucment by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        if thumbnail:
            match = EMOJI_REGEX.fullmatch(thumbnail)

            if match:
                emoji_id = match.group(1)

                if thumbnail.startswith("<a:"):
                    thumbnail_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
                else:
                    thumbnail_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"

                embed.set_thumbnail(url=thumbnail_url)

            else:
                embed.set_thumbnail(url=thumbnail)

        if banner:
            if banner.lower().endswith(".mp4"):
                embed.add_field(
                    name="Video",
                    value=banner,
                    inline=False
                )
            else:
                embed.set_image(url=banner)

        ping_role_id = ann.get("ping_role_id")
        content = None

        if ping_role_id:
            role = interaction.guild.get_role(ping_role_id)
            if role:
                content = role.mention

        channel = interaction.guild.get_channel(channel_id)

        if not channel:
              return await interaction.response.send_message(
               "Announcement channel not found.",
               ephemeral=True
              )

        await channel.send(
            content=content,
            embed=embed,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

        await interaction.response.send_message(
            f"Announcement sent to {channel.mention}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Announcement(bot))