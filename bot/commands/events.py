import discord 

from discord.ext import commands 

from utils.log import send_log 

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog loaded")

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

    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message: discord.Message
    ):
        if message.author.bot:
            return

        embed = discord.Embed(
            title="Message Deleted",
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

    async def on_ready(self):
        print(f'\u2705 Successfully logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f'Message from {message.author}: {message.content}')

        # Allow commands to work inside on_message
        await self.process_commands(message)

async def setup(bot):
    await bot.add_cog(Events(bot))