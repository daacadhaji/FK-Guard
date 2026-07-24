import discord
from discord.ext import commands
import asyncio


from config import (
    TOKEN,
    BOT_NAME
)

from database.database import setup_database


# YOUR SERVER ID HERE
GUILD_ID = 1523187103494832208


intents = discord.Intents.all()



class FKGuard(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        await setup_database()


        cogs = [

            "cogs.moderation",
            "cogs.automod",
            "cogs.logging",
            "cogs.utility",
            "cogs.owner"

        ]


        for cog in cogs:

            try:

                await self.load_extension(cog)

                print(
                    f"Loaded {cog}"
                )

            except Exception as e:

                print(
                    f"{cog}: {e}"
                )


        # Sync commands globally
        synced = await self.tree.sync()


        print(
            f"Synced {len(synced)} slash commands"
        )



bot = FKGuard()



@bot.event
async def on_ready():

    print(
        "━━━━━━━━━━━━━━━━"
    )

    print(
        f"{BOT_NAME} ONLINE"
    )

    print(
        bot.user
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



async def main():

    async with bot:

        await bot.start(
            TOKEN
        )



asyncio.run(main())