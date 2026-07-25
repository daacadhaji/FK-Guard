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
    @commands.has_permissions(
        administrator=True
    )
    async def staff(
        self,
        ctx,
        action: str,
        member: discord.Member,
        role: str
    ):

        await ctx.defer()

        action = action.lower()
        role = role.lower()



        if role not in STAFF_ROLES:

            await ctx.followup.send(
                "❌ Invalid staff role."
            )

            return



        role_id, role_name = STAFF_ROLES[role]


        staff_role = ctx.guild.get_role(
            role_id
        )


        if staff_role is None:

            await ctx.followup.send(
                "❌ Role not found."
            )

            return



        # ADD ROLE

        if action == "add":


            if staff_role in member.roles:

                await ctx.followup.send(
                    "⚠️ Member already has this role."
                )

                return



            await member.add_roles(
                staff_role
            )


            title = "🛡️ Staff Role Added"



        # REMOVE ROLE

        elif action == "remove":


            if staff_role not in member.roles:

                await ctx.followup.send(
                    "⚠️ Member doesn't have this role."
                )

                return



            await member.remove_roles(
                staff_role
            )


            title = "🗑️ Staff Role Removed"



        else:

            await ctx.followup.send(
                "❌ Action must be add or remove."
            )

            return




        # RESPONSE EMBED

        embed = discord.Embed(
            title=title,
            description=(

                f"👤 Member: {member.mention}\n"
                f"🎖️ Prefix: **{role_name}**\n"
                f"👮 Action by: {ctx.author.mention}"

            ),
            color=0x8A2BE2
        )


        await ctx.followup.send(
            embed=embed
        )




        # STAFF LOGS

        log_channel = ctx.guild.get_channel(
            STAFF_LOG_CHANNEL
        )


        if log_channel:


            log_embed = discord.Embed(

                title=title,

                description=(

                    f"👤 **Member:** {member.mention}\n"
                    f"🎖️ **Prefix:** {role_name}\n"
                    f"👮 **Action by:** {ctx.author.mention}"

                ),

                color=0x8A2BE2
            )


            log_embed.set_footer(
                text="⭐ 𝓕𝓚 • Staff Logs"
            )


            await log_channel.send(
                embed=log_embed
            )




async def setup(bot):

    await bot.add_cog(
        Staff(bot)
    )

    print("✅ Staff System Loaded")