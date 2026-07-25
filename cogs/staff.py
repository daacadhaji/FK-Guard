import discord
from discord.ext import commands
from discord import app_commands

from config import STAFF_LOG_CHANNEL


STAFF_ROLES = {

    "head": (
        1523302581399584818,
        "🛡️ 𝓕𝓚 •"
    ),

    "admin": (
        1523303053695127613,
        "⚙️ 𝓕𝓚 •"
    ),

    "moderator": (
        1523303816013938718,
        "🔨 𝓕𝓚 •"
    ),

    "ticket": (
        1523304281443139694,
        "🎫 𝓕𝓚 •"
    )
}


class Staff(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="staff",
        description="Manage FK staff roles"
    )
    @app_commands.describe(
        action="Choose add or remove",
        member="Select staff member",
        role="Choose staff role"
    )
    @app_commands.choices(
        action=[
            app_commands.Choice(
                name="Add",
                value="add"
            ),
            app_commands.Choice(
                name="Remove",
                value="remove"
            )
        ],
        role=[
            app_commands.Choice(
                name="🛡️ FK Head",
                value="head"
            ),
            app_commands.Choice(
                name="⚙️ FK Admin",
                value="admin"
            ),
            app_commands.Choice(
                name="🔨 FK Moderator",
                value="moderator"
            ),
            app_commands.Choice(
                name="🎫 FK Ticket",
                value="ticket"
            )
        ]
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def staff(
        self,
        interaction: discord.Interaction,
        action: str,
        member: discord.Member,
        role: str
    ):

        await interaction.response.defer()

        action = action.lower()
        role = role.lower()


        if role not in STAFF_ROLES:

            await interaction.followup.send(
                "❌ Invalid staff role."
            )

            return


        role_id, role_name = STAFF_ROLES[role]


        staff_role = interaction.guild.get_role(
            role_id
        )


        if staff_role is None:

            await interaction.followup.send(
                "❌ Role not found."
            )

            return


        # ADD ROLE

        if action == "add":

            if staff_role in member.roles:

                await interaction.followup.send(
                    "⚠️ Member already has this role."
                )

                return

            try:

                await member.add_roles(
                    staff_role
                )

            except discord.Forbidden:

                await interaction.followup.send(
                    "❌ I can't assign this role. My role needs to be "
                    "positioned above it in Server Settings → Roles."
                )

                return

            title = "🛡️ Staff Role Added"


        # REMOVE ROLE

        elif action == "remove":

            if staff_role not in member.roles:

                await interaction.followup.send(
                    "⚠️ Member doesn't have this role."
                )

                return

            try:

                await member.remove_roles(
                    staff_role
                )

            except discord.Forbidden:

                await interaction.followup.send(
                    "❌ I can't remove this role. My role needs to be "
                    "positioned above it in Server Settings → Roles."
                )

                return

            title = "🗑️ Staff Role Removed"


        else:

            await interaction.followup.send(
                "❌ Action must be add or remove."
            )

            return


        # RESPONSE EMBED

        embed = discord.Embed(
            title=title,
            description=(

                f"👤 Member: {member.mention}\n"
                f"🎖️ Prefix: **{role_name}**\n"
                f"👮 Action by: {interaction.user.mention}"

            ),
            color=0x8A2BE2
        )


        await interaction.followup.send(
            embed=embed
        )


        # STAFF LOGS

        log_channel = interaction.guild.get_channel(
            STAFF_LOG_CHANNEL
        )


        if log_channel:

            log_embed = discord.Embed(

                title=title,

                description=(

                    f"👤 **Member:** {member.mention}\n"
                    f"🎖️ **Prefix:** {role_name}\n"
                    f"👮 **Action by:** {interaction.user.mention}"

                ),

                color=0x8A2BE2
            )


            log_embed.set_footer(
                text="⭐ 𝓕𝓚 • Staff Logs"
            )


            try:

                await log_channel.send(
                    embed=log_embed
                )

            except discord.Forbidden:
                pass



async def setup(bot):

    await bot.add_cog(
        Staff(bot)
    )

    print("✅ Staff System Loaded")
