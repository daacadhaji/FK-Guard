import discord
from discord.ext import commands
from discord import app_commands

from config import OWNER_ID, GUILD_ID

from utils.embeds import success, error


class Owner(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    async def owner_check(
        self,
        interaction
    ):

        if interaction.user.id != OWNER_ID:

            await interaction.response.send_message(

                embed=error(
                    "Owner only command."
                ),

                ephemeral=True

            )

            return False


        return True



    # =====================
    # SYNC
    # =====================

    @app_commands.command(
        name="sync",
        description="Sync slash commands"
    )
    async def sync(
        self,
        interaction
    ):

        if not await self.owner_check(
            interaction
        ):

            return


        guild = discord.Object(
            id=GUILD_ID
        )

        self.bot.tree.copy_global_to(
            guild=guild
        )

        synced = await self.bot.tree.sync(
            guild=guild
        )


        await interaction.response.send_message(

            embed=success(

                f"Synced {len(synced)} guild commands."

            )

        )



    # =====================
    # CLEAR GLOBAL COMMANDS
    # =====================
    # One-time cleanup: removes any commands that were previously
    # registered globally (e.g. from an old /sync call), which is
    # what caused every command to show up twice. Run this once,
    # then only ever use guild-scoped /sync from now on.

    @app_commands.command(
        name="clearglobal",
        description="Remove stale global slash commands (run once)"
    )
    async def clearglobal(
        self,
        interaction
    ):

        if not await self.owner_check(
            interaction
        ):

            return


        self.bot.tree.clear_commands(
            guild=None
        )

        await self.bot.tree.sync(
            guild=None
        )


        await interaction.response.send_message(

            embed=success(

                "Cleared global commands. It may take a few minutes "
                "for Discord to stop showing the duplicates."

            )

        )



    # =====================
    # STATUS
    # =====================

    @app_commands.command(
        name="status",
        description="Bot status"
    )
    async def status(
        self,
        interaction
    ):

        if not await self.owner_check(
            interaction
        ):

            return


        await interaction.response.send_message(

            embed=success(

                f"""
Online ✅

Servers:
{len(self.bot.guilds)}

Users:
{len(self.bot.users)}
"""

            )

        )



    # =====================
    # SHUTDOWN
    # =====================

    @app_commands.command(
        name="shutdown",
        description="Shutdown bot"
    )
    async def shutdown(
        self,
        interaction
    ):

        if not await self.owner_check(
            interaction
        ):

            return


        await interaction.response.send_message(

            embed=success(
                "Shutting down..."
            )

        )


        await self.bot.close()



async def setup(bot):

    await bot.add_cog(
        Owner(bot)
    )