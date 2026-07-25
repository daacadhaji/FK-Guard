import discord
from discord.ext import commands
import time
import datetime


from utils.embeds import warning


class AutoMod(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.messages = {}

        self.bad_words = [

            "badword1",
            "badword2"

        ]


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.guild is None:
            return


        content = message.content.lower()



        # ======================
        # BAD WORD FILTER
        # ======================

        for word in self.bad_words:

            if word in content:

                try:

                    await message.delete()

                    await message.channel.send(

                        embed=warning(

                            f"{message.author.mention}, bad language is not allowed."

                        )

                    )

                except discord.Forbidden:
                    pass

                return



        # ======================
        # ANTI INVITE
        # ======================

        if "discord.gg/" in content:

            try:

                await message.delete()

                await message.channel.send(

                    embed=warning(

                        "Discord invites are not allowed."

                    )

                )

            except discord.Forbidden:
                pass

            return



        # ======================
        # ANTI MASS MENTION
        # ======================

        if len(message.mentions) >= 5:

            try:

                await message.delete()

                await message.channel.send(

                    embed=warning(

                        "Mass mentioning is blocked."

                    )

                )

            except discord.Forbidden:
                pass

            return



        # ======================
        # ANTI CAPS
        # ======================

        letters = [
            x for x in message.content
            if x.isalpha()
        ]


        if len(letters) > 10:

            caps = sum(
                1 for x in letters
                if x.isupper()
            )


            if caps / len(letters) > 0.7:

                try:

                    await message.delete()

                    await message.channel.send(

                        embed=warning(

                            "Please avoid excessive caps."

                        )

                    )

                except discord.Forbidden:
                    pass

                return



        # ======================
        # ANTI SPAM
        # ======================

        now = time.time()


        user = message.author.id


        if user not in self.messages:

            self.messages[user] = []



        self.messages[user].append(now)



        self.messages[user] = [

            x for x in self.messages[user]

            if now - x < 5

        ]


        if len(self.messages[user]) >= 5:

            try:

                await message.delete()

            except discord.Forbidden:
                pass

            try:

                await message.author.timeout(
                    datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(seconds=30),
                    reason="Spam"
                )

            except discord.Forbidden:
                pass



async def setup(bot):

    await bot.add_cog(
        AutoMod(bot)
    )
