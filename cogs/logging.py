import discord
from discord.ext import commands


from config import LOG_CHANNEL_ID


class Logging(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    async def send_log(
        self,
        text
    ):

        if LOG_CHANNEL_ID == 0:

            return


        channel = self.bot.get_channel(
            LOG_CHANNEL_ID
        )


        if channel:

            await channel.send(
                text
            )



    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):

        await self.send_log(

            f"👋 Member joined: {member}"

        )



    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member
    ):

        await self.send_log(

            f"🚪 Member left: {member}"

        )



    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message
    ):

        if message.author.bot:

            return


        await self.send_log(

            f"""
🗑️ Message Deleted

User:
{message.author}

Channel:
{message.channel}

Content:
{message.content}
"""

        )



    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before,
        after
    ):

        if before.author.bot:

            return


        await self.send_log(

            f"""
✏️ Message Edited

User:
{before.author}

Before:
{before.content}

After:
{after.content}
"""

        )



    @commands.Cog.listener()
    async def on_member_ban(
        self,
        guild,
        user
    ):

        await self.send_log(

            f"🔨 User banned: {user}"

        )



async def setup(bot):

    await bot.add_cog(
        Logging(bot)
    )
