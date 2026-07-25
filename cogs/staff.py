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

    @commands.hybrid_command(
        name="staff",
        description="Manage FK staff roles"
    )
    @app_commands.describe(
        action="Choose add or remove",
        member="Select the member",
        role="Choose the staff prefix"
    )
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Add", value="add"),
            app_commands.Choice(name="Remove", value="remove")
        ],
        role=[
            app_commands.Choice(name="🛡️ Head", value="head"),
            app_commands.Choice(name="⚙️ Admin", value="admin"),
            app_commands.Choice(name="🔨 Moderator", value="moderator"),
            app_commands.Choice(name="🎫 Ticket Helper", value="ticket")
        ]
    )
    @commands.has_permissions(administrator=True)
    async def staff(
        self,
        ctx: commands.Context,
        action: str,
        member: discord.Member,
        role: str
    ):

        await ctx.defer()

        action = action.lower()
        role = role.lower()

        if role not in STAFF_ROLES:
            await ctx.followup.send("❌ Invalid role.")
            return

        role_id, role_name = STAFF_ROLES[role]

        staff_role = ctx.guild.get_role(role_id)

        if staff_role is None:
            await ctx.followup.send("❌ Staff role not found.")
            return

        try:

            if action == "add":

                if staff_role in member.roles:
                    await ctx.followup.send("⚠️ Member already has this role.")
                    return

                await member.add_roles(
                    staff_role,
                    reason=f"Added by {ctx.author}"
                )

                title = "🛡️ Staff Role Added"

            elif action == "remove":

                if staff_role not in member.roles:
                    await ctx.followup.send("⚠️ Member doesn't have this role.")
                    return

                await member.remove_roles(
                    staff_role,
                    reason=f"Removed by {ctx.author}"
                )

                title = "🗑️ Staff Role Removed"

            else:
                await ctx.followup.send("❌ Action must be **add** or **remove**.")
                return

        except discord.Forbidden:
            await ctx.followup.send(
                "❌ I don't have permission to manage that role. Make sure my role is above the staff roles."
            )
            return

        except Exception as e:
            await ctx.followup.send(f"❌ Error: `{e}`")
            return

        embed = discord.Embed(
            title=title,
            color=0x8A2BE2
        )

        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="Prefix",
            value=role_name,
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=ctx.author.mention,
            inline=False
        )

        await ctx.followup.send(embed=embed)

        log_channel = ctx.guild.get_channel(STAFF_LOG_CHANNEL)

        if log_channel:

            log_embed = discord.Embed(
                title=title,
                color=0x8A2BE2
            )

            log_embed.add_field(
                name="Member",
                value=member.mention,
                inline=False
            )

            log_embed.add_field(
                name="Prefix",
                value=role_name,
                inline=False
            )

            log_embed.add_field(
                name="Moderator",
                value=ctx.author.mention,
                inline=False
            )

            log_embed.set_footer(
                text="⭐ 𝓕𝓚 • Staff Logs"
            )

            await log_channel.send(embed=log_embed)


async def setup(bot):
    await bot.add_cog(Staff(bot))
    print("✅ Staff System Loaded")