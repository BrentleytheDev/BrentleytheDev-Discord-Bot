import discord
import json

from discord.ext import commands

from utils.log import(
    send_log,
    log_kick,
    log_ban,
    log_reaction,
    log_delete_message,
    log_bad_words,
    log_message_edit,
    member_join_log
)
from utils.nsfw_detector import (
    nsfw_detect,
    clear_message_cache,
)

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

      await member_join_log(member)

    # Log edited messages
    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before: discord.Message,
        after: discord.Message
    ):

      await log_message_edit(before, after)

    # Log deleted messages
    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message: discord.Message
    ):

        if message.author.bot:
            return

        await log_delete_message(message)

    # Log kicks and bans
    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member: discord.Member
    ):
        await log_kick(member)

        await log_ban(member.guild, member)

    # Log reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent
    ):

        await log_reaction(self, payload)

    #Log bad words
    @commands.Cog.listener()
    async def on_message(
        self,
        message: discord.Message
    ):
        if message.author.bot:
            return

        if await nsfw_detect(message):
            return

        await log_bad_words(message)


async def setup(bot):
    await bot.add_cog(Events(bot))