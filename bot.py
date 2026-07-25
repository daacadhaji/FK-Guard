import asyncio
import traceback

import discord
from discord.ext import commands
from discord import app_commands

from config import (
    TOKEN,
    BOT_NAME,
    GUILD_ID
)

from database.database import setup_database


# ==========================
# INTENTS
# ==========================

intents = discord.Intents.all()


# ==========================
# BOT CLASS
# ==========================

class FKGuard(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        # ==========================
        # DATABASE
        # ==========================

        await setup_database()


        # ==========================
        # LOAD COGS
        # ==========================

        cogs = [

            "cogs.moderation",
            "cogs.automod",
            "cogs.logging",
            "cogs.utility",
            "cogs.owner",
            "cogs.staff"

        ]


        for cog in cogs:

            try:

                await self.load_extension(cog)

                print(
                    f"✅ Loaded {cog}"
                )

            except Exception:

                print(
                    f"❌ Failed loading {cog}"
                )

                traceback.print_exc()


        # ==========================
        # SYNC GUILD COMMANDS
        # ==========================

        try:

            guild = discord.Object(
                id=GUILD_ID
            )

            # Remove previously synced guild commands
            self.tree.clear_commands(
                guild=guild
            )

            # Copy all loaded commands
            self.tree.copy_global_to(
                guild=guild
            )

            synced = await self.tree.sync(
                guild=guild
            )

            print(
                f"✅ Synced {len(synced)} guild commands"
            )

        except Exception:

            print(
                "❌ Slash sync failed"
            )

            traceback.print_exc()


# ==========================
# CREATE BOT
# ==========================

bot = FKGuard()


# ==========================
# GLOBAL SLASH COMMAND ERROR HANDLER
# ==========================
# Handles errors from plain app_commands.command slash commands.
# Without this, a failed permission check or unhandled exception
# leaves the interaction with no response ("thinking..." forever).

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    if isinstance(error, app_commands.MissingPermissions):

        message = "❌ You don't have permission to use this command."

    elif isinstance(error, app_commands.CheckFailure):

        message = "❌ You can't use this command right now."

    else:

        print(f"Unhandled app command error: {error}")
        traceback.print_exc()

        message = "❌ Something went wrong running that command."

    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                message,
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    except discord.HTTPException:
        pass


# ==========================
# GLOBAL HYBRID/PREFIX COMMAND ERROR HANDLER
# ==========================
# Hybrid commands (like /staff) dispatch errors through this event
# instead of bot.tree.error, even when invoked as a slash command.
# Without this, a failed check on a hybrid command hangs forever
# because nothing ever responds to the interaction.

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):

        message = "❌ You don't have permission to use this command."

    elif isinstance(error, commands.CheckFailure):

        message = "❌ You can't use this command right now."

    else:

        print(f"Unhandled command error: {error}")
        traceback.print_exc()

        message = "❌ Something went wrong running that command."

    try:

        if ctx.interaction is not None:

            if ctx.interaction.response.is_done():

                await ctx.interaction.followup.send(
                    message,
                    ephemeral=True
                )

            else:

                await ctx.interaction.response.send_message(
                    message,
                    ephemeral=True
                )

        else:

            await ctx.send(message)

    except discord.HTTPException:
        pass


# ==========================
# READY EVENT
# ==========================

@bot.event
async def on_ready():

    print(
        "━━━━━━━━━━━━━━━━"
    )

    print(
        f"🛡️ {BOT_NAME} ONLINE"
    )

    print(
        f"Bot: {bot.user}"
    )

    print(
        f"ID: {bot.user.id}"
    )

    print(
        "━━━━━━━━━━━━━━━━"
    )

    await bot.change_presence(

        activity=discord.Activity(

            type=discord.ActivityType.watching,

            name="Server Security 🛡️"

        )

    )


# ==========================
# START BOT
# ==========================

async def main():

    if not TOKEN:

        raise ValueError(
            "❌ TOKEN missing from .env"
        )

    async with bot:

        await bot.start(TOKEN)


if __name__ == "__main__":

    asyncio.run(main())