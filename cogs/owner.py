import discord
from discord.ext import commands
from discord import app_commands

from config import OWNER_ID

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


        synced = await self.bot.tree.sync()


        await interaction.response.send_message(

            embed=success(

                f"Synced {len(synced)} commands."

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