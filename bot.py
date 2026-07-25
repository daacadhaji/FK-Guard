import discord
from discord.ext import commands
import asyncio


from config import (
    TOKEN,
    BOT_NAME
)

from database.database import setup_database


# ==========================
# SERVER ID
# ==========================

GUILD_ID = 1523186859172167750



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

                await self.load_extension(
                    cog
                )

                print(
                    f"✅ Loaded {cog}"
                )


            except Exception as e:

                print(
                    f"❌ Failed loading {cog}"
                )

                print(e)



        # ==========================
        # SYNC GUILD COMMANDS
        # ==========================

        try:

            guild = discord.Object(
                id=GUILD_ID
            )


            # Copy loaded slash commands
            # to this server

            self.tree.copy_global_to(
                guild=guild
            )


            synced = await self.tree.sync(
                guild=guild
            )


            print(
                f"✅ Synced {len(synced)} guild commands"
            )


        except Exception as e:

            print(
                "❌ Slash sync failed"
            )

            print(e)




# ==========================
# CREATE BOT
# ==========================

bot = FKGuard()



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

        await bot.start(
            TOKEN
        )



asyncio.run(main())