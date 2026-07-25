import discord
from discord.ext import commands
from discord import app_commands

from utils.embeds import success, info


class Utility(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # =====================
    # PING
    # =====================

    @app_commands.command(
        name="ping",
        description="Check bot latency"
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):

        latency = round(
            self.bot.latency * 1000
        )


        await interaction.response.send_message(

            embed=success(
                f"Pong! `{latency}ms`"
            )

        )



    # =====================
    # USER INFO
    # =====================

    @app_commands.command(
        name="userinfo",
        description="Show user information"
    )
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):

        member = member or interaction.user


        embed = info(

            f"""
👤 User:
{member}

🆔 ID:
{member.id}

📅 Joined:
{member.joined_at}

📅 Created:
{member.created_at}
"""

        )


        embed.set_thumbnail(
            url=member.display_avatar.url
        )


        await interaction.response.send_message(
            embed=embed
        )



    # =====================
    # SERVER INFO
    # =====================

    @app_commands.command(
        name="serverinfo",
        description="Show server information"
    )
    async def serverinfo(
        self,
        interaction: discord.Interaction
    ):

        guild = interaction.guild


        embed = info(

            f"""
🏠 Server:
{guild.name}

👥 Members:
{guild.member_count}

📁 Channels:
{len(guild.channels)}

🎭 Roles:
{len(guild.roles)}
"""

        )


        if guild.icon:

            embed.set_thumbnail(
                url=guild.icon.url
            )


        await interaction.response.send_message(
            embed=embed
        )



    # =====================
    # AVATAR
    # =====================

    @app_commands.command(
        name="avatar",
        description="Show avatar"
    )
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):

        member = member or interaction.user


        embed = info(
            f"{member.mention}'s avatar"
        )


        embed.set_image(
            url=member.display_avatar.url
        )


        await interaction.response.send_message(
            embed=embed
        )



    # =====================
    # ROLE INFO
    # =====================

    @app_commands.command(
        name="roleinfo",
        description="Show role information"
    )
    async def roleinfo(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):


        await interaction.response.send_message(

            embed=info(

                f"""
🎭 Role:
{role.name}

🆔 ID:
{role.id}

👥 Members:
{len(role.members)}
"""

            )

        )



    # =====================
    # CHANNEL INFO
    # =====================

    @app_commands.command(
        name="channelinfo",
        description="Show channel information"
    )
    async def channelinfo(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):


        await interaction.response.send_message(

            embed=info(

                f"""
📌 Channel:
{channel.name}

🆔 ID:
{channel.id}

📅 Created:
{channel.created_at}
"""

            )

        )



    # =====================
    # BOT INFO
    # =====================

    @app_commands.command(
        name="botinfo",
        description="Show bot information"
    )
    async def botinfo(
        self,
        interaction: discord.Interaction
    ):


        await interaction.response.send_message(

            embed=info(

                f"""
🛡️ FK Guard

Servers:
{len(self.bot.guilds)}

Users:
{len(self.bot.users)}

Discord.py:
{discord.__version__}
"""

            )

        )



async def setup(bot):

    await bot.add_cog(
        Utility(bot)
    )
