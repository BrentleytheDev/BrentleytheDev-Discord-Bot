import discord 
import json 
from pathlib import Path
from .config import(
    open_config,
    write_config
)
from .nsfw_detector import(
    clear_message_cache,
    nsfw_detect
)

async def setup_logging(key: str, channel_id: int):
            data = await open_config()
                
            if "logging" not in data:
                data["logging"] = {}
            
            data["logging"][key] = channel_id

            await write_config(data)

async def send_log(
    guild: discord.Guild,
    log_type: str,
    embed: discord.Embed
):

    try:
        data = await open_config()

    except (FileNotFoundError, json.JSONDecodeError):
        return 

    logging_data = data.get("logging", {})

    print(logging_data)

    channel_id = logging_data.get(log_type)

    print(f"channel_id = {channel_id}")

    if not channel_id:
        channel_id = logging_data.get("general-server-logging")

    if not channel_id:
        print("No logging channel found")
        return 

    #Get Discord channel
    channel = guild.get_channel(channel_id)

    if not channel:
        print("Channel object not found")
        return 

    print("Sending embed")

    await channel.send(embed=embed)

async def log_kick(member: discord.Member):
    async for log in member.guild.audit_logs(
            limit=1,
            action=discord.AuditLogAction.kick
        ):

            if log.target.id == member.id:

                reason = log.reason or "No reason provided"

                embed = discord.Embed(
                    title="👢 Member Kicked",
                    color=discord.Color.red()
                )

                embed.add_field(
                    name="User",
                    value=member.mention,
                    inline=False
                )

                embed.set_footer(
                    text=f"Reason: {reason}"
                )

                embed.set_thumbnail(
                    url=member.display_avatar.url
                )

                await send_log(
                    member.guild,
                    "kick-logging",
                    embed
                )

async def log_ban(guild: discord.Guild, member: discord.Member):
    async for log in member.guild.audit_logs(
            limit=1,
            action=discord.AuditLogAction.ban
        ):

            if log.target.id == member.id:

                reason = log.reason or "No reason provided"

                embed = discord.Embed(
                    title="🔨 Member Banned",
                    color=discord.Color.red()
                )

                embed.add_field(
                    name="User",
                    value=member.mention,
                    inline=False
                )

                embed.set_footer(
                    text=f"Reason: {reason}"
                )

                embed.set_thumbnail(
                    url=member.display_avatar.url
                )

                await send_log(
                    member.guild,
                    "ban-logging",
                    embed
                )

async def log_reaction(self, payload: discord.RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            return

        member = guild.get_member(payload.user_id)

        if member is None:
            return

        channel = guild.get_channel(payload.channel_id)

        if channel is None:
            return

        message = await channel.fetch_message(payload.message_id)

        embed = discord.Embed(
            title="Reaction Added",
            description=(
                f"{member.mention} reacted to "
                f"[{message.content or 'Message'}]({message.jump_url}) "
                f"with {payload.emoji} in {channel.mention}"
            ),
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        await send_log(
            guild,
            "reaction-add",
            embed
        )

async def log_delete_message(message: discord.Message):
        embed = discord.Embed(
            title="🗑️ Message Deleted",
            color=discord.Color.red()
        )

        embed.add_field(
            name="User",
            value=message.author.mention,
            inline=False
        )

        embed.add_field(
            name="Content",
            value=message.content or "No content",
            inline=False
        )

        embed.set_footer(
            text=f"User ID: {message.author.id}"
        )

        embed.add_field(
            name="Message Link",
            value=f"[Jump to Message]({message.jump_url})",
            inline=False
        )

        await send_log(
            message.guild,
            "delete-messages",
            embed
        )

async def log_bad_words(message: discord.Message):
        config = await open_config()
        bad_words = config.get("bad-words", [])

        message_content = message.content.lower()

        for word in bad_words:

            if word.lower() in message_content:

                embed = discord.Embed(
                    title="🚫 Bad Word Detected",
                    color=discord.Color.red()
                )

                embed.add_field(
                    name="User",
                    value=message.author.mention,
                    inline=False
                )

                embed.add_field(
                    name="Channel",
                    value=message.channel.mention,
                    inline=False
                )

                embed.add_field(
                    name="Message",
                    value=message.content,
                    inline=False
                )

                embed.add_field(
                    name="Message Link",
                    value=f"[Jump to Message]({message.jump_url})",
                    inline=False
                )

                await send_log(
                    message.guild,
                    "bad-word-logging",
                    embed
                )

                try:
                    await message.author.send(
                        "Your message was deleted because it contained a banned word!"
                    )
                except discord.Forbidden:
                    await message.channel.send(
                        f"{message.author.mention}, your message was deleted because it contained a banned word",
                        delete_after=5
                    )
                await message.delete()
                return

async def log_message_edit(before, after):
        print("Message edit event fired")

        if after.author.bot:
            return

        if (
            before.content == after.content
            and before.attachments == after.attachments
        ):
            return

        clear_message_cache(after.id)

        if await nsfw_detect(after):
            return

        embed = discord.Embed(
            title="✏️ Message Edited",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="User",
            value=before.author.mention,
            inline=False
        )

        embed.add_field(
            name="Before",
            value=before.content or "No content",
            inline=False
        )

        embed.add_field(
            name="After",
            value=after.content or "No content",
            inline=False
        )

        embed.set_footer(
            text=f"User ID: {before.author.id}"
        )

        embed.add_field(
            name="Message Link",
            value=f"[Jump to Message]({before.jump_url})",
            inline=False
        )

        await send_log(
            before.guild,
            "message-edits",
            embed
        )

async def member_join_log(member: discord.Member):
        embed = discord.Embed(
            title="👋 Member Joined",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green()
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        await send_log(
            member.guild,
            "join-logging",
            embed
        )