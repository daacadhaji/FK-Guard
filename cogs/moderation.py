import discord
from discord.ext import commands
from discord import app_commands

import datetime

from utils.embeds import success, error, warning
from utils.helpers import clean_reason, get_time

from database.models import (
    add_warning,
    get_warnings,
    clear_warnings
)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # =====================
    # BAN
    # =====================

    @app_commands.command(
        name="ban",
        description="Ban a member"
    )
    @app_commands.checks.has_permissions(
        ban_members=True
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):

        reason = clean_reason(reason)

        try:

            await member.ban(
                reason=reason
            )

            await interaction.response.send_message(
                embed=success(
                    f"{member.mention} has been banned.\nReason: {reason}"
                )
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                embed=error(
                    "I cannot ban this user. Check my role position."
                ),
                ephemeral=True
            )


    # =====================
    # KICK
    # =====================

    @app_commands.command(
        name="kick",
        description="Kick a member"
    )
    @app_commands.checks.has_permissions(
        kick_members=True
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):

        reason = clean_reason(reason)

        try:

            await member.kick(
                reason=reason
            )

            await interaction.response.send_message(
                embed=success(
                    f"{member.mention} kicked.\nReason: {reason}"
                )
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                embed=error(
                    "I cannot kick this user."
                ),
                ephemeral=True
            )


    # =====================
    # TIMEOUT
    # =====================

    @app_commands.command(
        name="timeout",
        description="Timeout a member"
    )
    @app_commands.checks.has_permissions(
        moderate_members=True
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = "No reason provided"
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        try:

            until = (
                datetime.datetime.now(
                    datetime.timezone.utc
                )
                +
                datetime.timedelta(
                    minutes=minutes
                )
            )


            await member.timeout(
                until,
                reason=reason
            )


            await interaction.followup.send(

                embed=success(
                    f"""
🔇 User timed out

User:
{member.mention}

Duration:
{minutes} minutes

Reason:
{reason}
"""
                )

            )


        except discord.Forbidden:

            await interaction.followup.send(

                embed=error(
                    """
I cannot timeout this user.

Check:
• My role is above the user
• I have Moderate Members permission
"""
                )

            )


        except Exception as e:

            print(e)

            await interaction.followup.send(

                embed=error(
                    "An unexpected error happened."
                )

            )



    # =====================
    # REMOVE TIMEOUT
    # =====================

    @app_commands.command(
        name="untimeout",
        description="Remove timeout"
    )
    @app_commands.checks.has_permissions(
        moderate_members=True
    )
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        try:

            await member.timeout(
                None
            )


            await interaction.response.send_message(

                embed=success(
                    f"{member.mention} timeout removed."
                )

            )


        except discord.Forbidden:

            await interaction.response.send_message(

                embed=error(
                    "I cannot remove this timeout."
                ),

                ephemeral=True

            )



    # =====================
    # WARN
    # =====================

    @app_commands.command(
        name="warn",
        description="Warn a member"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):

        try:

            await add_warning(

                member.id,
                interaction.user.id,
                reason,
                get_time()

            )

            # DM the warned member
            try:

                await member.send(

                    embed=warning(
                        f"⚠️ You have received a warning in **{interaction.guild.name}**.\n\n"
                        f"**Reason:** {reason}"
                    )

                )

            except discord.Forbidden:
                pass

            await interaction.response.send_message(

                embed=warning(
                    f"⚠️ {member.mention} has been warned.\n\nReason: **{reason}**"
                )

            )

        except Exception as e:

            print(f"Warn Error: {e}")

            await interaction.response.send_message(

                embed=error(
                    "Failed to warn the member."
                ),

                ephemeral=True

            )


    # =====================
    # WARNINGS
    # =====================

    @app_commands.command(
        name="warnings",
        description="View a member's warnings"
    )
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        try:

            data = await get_warnings(
                member.id
            )

            if not data:

                await interaction.response.send_message(

                    embed=success(
                        f"{member.mention} has no warnings."
                    )

                )

                return

            text = ""

            for warn in data:

                text += (
                    f"**Warning ID:** {warn[0]}\n"
                    f"**Reason:** {warn[3]}\n"
                    f"**Date:** {warn[4]}\n\n"
                )

            await interaction.response.send_message(

                embed=warning(text)

            )

        except Exception as e:

            print(f"Warnings Error: {e}")

            await interaction.response.send_message(

                embed=error(
                    "Failed to retrieve warnings."
                ),

                ephemeral=True

            )


    # =====================
    # CLEAR WARNINGS
    # =====================

    @app_commands.command(
        name="clearwarnings",
        description="Clear all warnings for a member"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def clearwarnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        try:

            await clear_warnings(
                member.id
            )

            await interaction.response.send_message(

                embed=success(
                    f"✅ Cleared all warnings for {member.mention}."
                )

            )

        except Exception as e:

            print(f"ClearWarnings Error: {e}")

            await interaction.response.send_message(

                embed=error(
                    "Failed to clear warnings."
                ),

                ephemeral=True

            )


    # =====================
    # CLEAR MESSAGES
    # =====================

    @app_commands.command(
        name="clear",
        description="Delete a specific number of messages"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        if amount < 1:

            await interaction.response.send_message(

                embed=error(
                    "Amount must be at least 1."
                ),

                ephemeral=True

            )

            return


        if amount > 100:

            await interaction.response.send_message(

                embed=error(
                    "You can only delete up to 100 messages at a time."
                ),

                ephemeral=True

            )

            return


        await interaction.response.defer(
            ephemeral=True
        )


        try:

            deleted = await interaction.channel.purge(
                limit=amount
            )


            await interaction.followup.send(

                embed=success(
                    f"🧹 Deleted **{len(deleted)}** messages."
                ),

                ephemeral=True

            )


        except discord.Forbidden:

            await interaction.followup.send(

                embed=error(
                    "I don't have permission to delete messages."
                ),

                ephemeral=True

            )


        except Exception as e:

            print(f"Clear Error: {e}")

            await interaction.followup.send(

                embed=error(
                    "An error occurred while deleting messages."
                ),

                ephemeral=True

            )


    # =====================
    # CLEAR ALL MESSAGES
    # =====================

    @app_commands.command(
        name="clearall",
        description="Delete every message in this channel"
    )
    @app_commands.checks.has_permissions(
        manage_messages=True
    )
    async def clearall(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )


        try:

            deleted = await interaction.channel.purge(
                limit=None
            )


            await interaction.followup.send(

                embed=success(
                    f"🧹 Successfully deleted **{len(deleted)}** messages."
                ),

                ephemeral=True

            )


        except discord.Forbidden:

            await interaction.followup.send(

                embed=error(
                    "I don't have permission to delete messages."
                ),

                ephemeral=True

            )


        except Exception as e:

            print(f"ClearAll Error: {e}")

            await interaction.followup.send(

                embed=error(
                    "Failed to clear this channel."
                ),

                ephemeral=True

            )

    # =====================
    # LOCK
    # =====================

    @app_commands.command(
        name="lock",
        description="Lock channel"
    )
    @app_commands.checks.has_permissions(
        manage_channels=True
    )
    async def lock(
        self,
        interaction: discord.Interaction
    ):

        try:

            overwrite = interaction.channel.overwrites_for(
                interaction.guild.default_role
            )

            overwrite.send_messages = False


            await interaction.channel.set_permissions(

                interaction.guild.default_role,

                overwrite=overwrite

            )


            await interaction.response.send_message(

                embed=success(
                    "Channel locked."
                )

            )

        except discord.Forbidden:

            await interaction.response.send_message(

                embed=error(
                    "I don't have permission to edit this channel."
                ),

                ephemeral=True

            )



    # =====================
    # UNLOCK
    # =====================

    @app_commands.command(
        name="unlock",
        description="Unlock channel"
    )
    @app_commands.checks.has_permissions(
        manage_channels=True
    )
    async def unlock(
        self,
        interaction: discord.Interaction
    ):

        try:

            overwrite = interaction.channel.overwrites_for(
                interaction.guild.default_role
            )

            overwrite.send_messages = True


            await interaction.channel.set_permissions(

                interaction.guild.default_role,

                overwrite=overwrite

            )


            await interaction.response.send_message(

                embed=success(
                    "Channel unlocked."
                )

            )

        except discord.Forbidden:

            await interaction.response.send_message(

                embed=error(
                    "I don't have permission to edit this channel."
                ),

                ephemeral=True

            )



async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )
