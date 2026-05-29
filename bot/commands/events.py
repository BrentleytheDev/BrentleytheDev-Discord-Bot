import discord

from discord.ext import commands

from utils.log import send_log


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog loaded")
        print(f"✅ Successfully logged in as {self.bot.user}")

    # Log member joins
    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

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

    # Log edited messages
    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before: discord.Message,
        after: discord.Message
    ):

        print("Message edit event fired")

        if before.author.bot:
            return

        if before.content == after.content:
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

        await send_log(
            before.guild,
            "message-edits",
            embed
        )

    # Log deleted messages
    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message: discord.Message
    ):

        if message.author.bot:
            return

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

        await send_log(
            message.guild,
            "delete-messages",
            embed
        )

    # Log kicks and bans
    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member: discord.Member
    ):

        # Log kicks
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

        # Log bans
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

    # Log reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ):

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
            title="😀 Reaction Added",
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


async def setup(bot):
    await bot.add_cog(Events(bot))