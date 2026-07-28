import discord
from discord.ext import commands
from discord import app_commands

from config import STAFF_LOG_CHANNEL


# Defined in priority order: highest-authority role first. If a
# member holds more than one staff role, the highest-priority one's
# prefix is the one shown in their nickname.

STAFF_ROLES = {

    "head": (
        1523302581399584818,
        "𓆩♖𓆪 𝓕𝓚 •"
    ),

    "core": (
        1531185251940962344,
        "𓆩♛𓆪 𝓕𝓚 •"
    ),

    "director": (
        1531185392483696800,
        "♔ 𝓕𝓚 •"
    ),

    "chiefadmin": (
        1523303053695127613,
        "🛡️ 𝓕𝓚 •"
    ),

    "assistantadmin": (
        1531185580405297333,
        "📜 𝓕𝓚 •"
    ),

    "moderator": (
        1523303816013938718,
        "𓆩⚒️𓆪 𝓕𝓚 •"
    ),

    "juniormod": (
        1531186095117697156,
        "⚖️ 𝓕𝓚 •"
    ),

    "trialmod": (
        1531186503726927912,
        "🗡️ 𝓕𝓚 •"
    ),

    "ticketsupervisor": (
        1523304281443139694,
        "📁 𝓕𝓚 •"
    ),

    "tickethelper": (
        1531187211306012765,
        "🎫 𝓕𝓚 •"
    ),

    "communitysupport": (
        1531187073133051914,
        "💬 𝓕𝓚 •"
    ),

    "eventdirector": (
        1531187798651048067,
        "🎉 𝓕𝓚 •"
    ),

    "eventmanager": (
        1531188003991584769,
        "🎭 𝓕𝓚 •"
    ),

    "developer": (
        1531188344200106135,
        "💻 𝓕𝓚 •"
    ),

    "botarchitect": (
        1531188745070448702,
        "🤖 𝓕𝓚 •"
    ),

    "staffteam": (
        1531188151115317332,
        "⚜️ 𝓕𝓚 •"
    ),

    "formerstaff": (
        1531178583115174061,
        "✦ 𝓕𝓚 •"
    ),
}


# Roles that count as an actual staff position. staffteam and
# formerstaff are auto-managed umbrella tags, not positions
# themselves — they're excluded here so the automatic logic below
# doesn't trigger off of them.

POSITION_KEYS = [
    key for key in STAFF_ROLES
    if key not in ("staffteam", "formerstaff")
]


# Moderator and everything above it (in hierarchy order) also grants
# Core Team automatically.

CORE_TEAM_TRIGGER_KEYS = [
    "head",
    "director",
    "chiefadmin",
    "assistantadmin",
    "moderator",
]


# Ticket Supervisor and Ticket Helper also grant Community Support
# automatically.

COMMUNITY_SUPPORT_TRIGGER_KEYS = [
    "ticketsupervisor",
    "tickethelper",
]


# These are auto-managed only — never directly selectable in the
# /staff dropdown.

AUTO_MANAGED_KEYS = (
    "core",
    "staffteam",
    "formerstaff",
    "communitysupport",
)


def get_role(guild, key):

    role_id, _ = STAFF_ROLES[key]

    return guild.get_role(role_id)


def holds_any(member, keys):

    held_ids = {r.id for r in member.roles}

    trigger_ids = {STAFF_ROLES[k][0] for k in keys}

    return bool(held_ids & trigger_ids)


ALL_PREFIXES = [
    name for _, name in STAFF_ROLES.values()
]


def strip_known_prefix(name):

    for prefix in ALL_PREFIXES:

        if name.startswith(prefix):

            return name[len(prefix):].lstrip()

    return name


def active_prefix_for(member):

    # STAFF_ROLES is defined in priority order — if a member holds
    # more than one staff role, the highest-priority one's prefix
    # wins.

    held_role_ids = {
        r.id for r in member.roles
    }

    for role_id, role_name in STAFF_ROLES.values():

        if role_id in held_role_ids:

            return role_name

    return None


async def sync_nickname(member):

    # Recomputes the member's nickname from scratch based on
    # whichever staff role(s) they actually hold right now. Called
    # after every add/remove so a removed role correctly falls back
    # to another staff role's prefix instead of just clearing it.

    base_name = strip_known_prefix(
        member.display_name
    )

    prefix = active_prefix_for(member)

    new_nick = (
        f"{prefix} {base_name}".strip()[:32]
        if prefix else
        base_name
    )

    if new_nick == member.name:

        await member.edit(nick=None)

    else:

        await member.edit(nick=new_nick)


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
            app_commands.Choice(name="Add", value="add"),
            app_commands.Choice(name="Remove", value="remove"),
        ],
        role=[
            app_commands.Choice(name="𓆩♖𓆪 Head of Staff", value="head"),
            app_commands.Choice(name="♔ Staff Director", value="director"),
            app_commands.Choice(name="🛡️ Chief Admin", value="chiefadmin"),
            app_commands.Choice(name="📜 Assistant Admin", value="assistantadmin"),
            app_commands.Choice(name="𓆩⚒️𓆪 Moderator", value="moderator"),
            app_commands.Choice(name="⚖️ Junior Moderator", value="juniormod"),
            app_commands.Choice(name="🗡️ Trial Moderator", value="trialmod"),
            app_commands.Choice(name="📁 Ticket Supervisor", value="ticketsupervisor"),
            app_commands.Choice(name="🎫 Ticket Helper", value="tickethelper"),
            app_commands.Choice(name="🎉 Event Director", value="eventdirector"),
            app_commands.Choice(name="🎭 Event Manager", value="eventmanager"),
            app_commands.Choice(name="💻 Developer", value="developer"),
            app_commands.Choice(name="🤖 Bot Architect", value="botarchitect"),
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

            extra_note = ""

            if role in POSITION_KEYS:

                staffteam_id, _ = STAFF_ROLES["staffteam"]
                formerstaff_id, _ = STAFF_ROLES["formerstaff"]

                staffteam_role = interaction.guild.get_role(staffteam_id)
                formerstaff_role = interaction.guild.get_role(formerstaff_id)

                if staffteam_role is None:

                    extra_note += (
                        f"\n⚠️ Staff Team role (ID {staffteam_id}) "
                        "not found in this server."
                    )

                if formerstaff_role is None:

                    extra_note += (
                        f"\n⚠️ Former Staff role (ID {formerstaff_id}) "
                        "not found in this server."
                    )

                try:

                    if staffteam_role and staffteam_role not in member.roles:

                        await member.add_roles(staffteam_role)
                        extra_note += "\n➕ Added **Staff Team** (default staff role)."

                    if formerstaff_role and formerstaff_role in member.roles:

                        await member.remove_roles(formerstaff_role)
                        extra_note += "\n➖ Removed **Former Staff** (active again)."

                except discord.Forbidden:

                    extra_note += (
                        "\n⚠️ Couldn't update Staff Team / Former "
                        "Staff — check my role position."
                    )

            if role in CORE_TEAM_TRIGGER_KEYS:

                core_role = get_role(interaction.guild, "core")

                if core_role is None:

                    core_id, _ = STAFF_ROLES["core"]

                    extra_note += (
                        f"\n⚠️ Core Team role (ID {core_id}) not "
                        "found in this server."
                    )

                try:

                    if core_role and core_role not in member.roles:

                        await member.add_roles(core_role)
                        extra_note += "\n➕ Added **Core Team**."

                except discord.Forbidden:

                    extra_note += (
                        "\n⚠️ Couldn't update Core Team — check my "
                        "role position."
                    )

            if role in COMMUNITY_SUPPORT_TRIGGER_KEYS:

                community_role = get_role(interaction.guild, "communitysupport")

                if community_role is None:

                    community_id, _ = STAFF_ROLES["communitysupport"]

                    extra_note += (
                        f"\n⚠️ Community Support role (ID "
                        f"{community_id}) not found in this server."
                    )

                try:

                    if community_role and community_role not in member.roles:

                        await member.add_roles(community_role)
                        extra_note += "\n➕ Added **Community Support**."

                except discord.Forbidden:

                    extra_note += (
                        "\n⚠️ Couldn't update Community Support — "
                        "check my role position."
                    )

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

            extra_note = ""

            if role in POSITION_KEYS:

                still_has_position = holds_any(member, POSITION_KEYS)

                staffteam_role = get_role(interaction.guild, "staffteam")
                formerstaff_role = get_role(interaction.guild, "formerstaff")

                if staffteam_role is None:

                    staffteam_id, _ = STAFF_ROLES["staffteam"]

                    extra_note += (
                        f"\n⚠️ Staff Team role (ID {staffteam_id}) "
                        "not found in this server."
                    )

                if formerstaff_role is None:

                    formerstaff_id, _ = STAFF_ROLES["formerstaff"]

                    extra_note += (
                        f"\n⚠️ Former Staff role (ID {formerstaff_id}) "
                        "not found in this server."
                    )

                if not still_has_position:

                    try:

                        if staffteam_role and staffteam_role in member.roles:

                            await member.remove_roles(staffteam_role)
                            extra_note += "\n➖ Removed **Staff Team** (no remaining staff role)."

                        if formerstaff_role and formerstaff_role not in member.roles:

                            await member.add_roles(formerstaff_role)
                            extra_note += "\n➕ Added **Former Staff**."

                    except discord.Forbidden:

                        extra_note += (
                            "\n⚠️ Couldn't update Staff Team / Former "
                            "Staff — check my role position."
                        )

            if role in CORE_TEAM_TRIGGER_KEYS:

                if not holds_any(member, CORE_TEAM_TRIGGER_KEYS):

                    core_role = get_role(interaction.guild, "core")

                    if core_role is None:

                        core_id, _ = STAFF_ROLES["core"]

                        extra_note += (
                            f"\n⚠️ Core Team role (ID {core_id}) not "
                            "found in this server."
                        )

                    try:

                        if core_role and core_role in member.roles:

                            await member.remove_roles(core_role)
                            extra_note += "\n➖ Removed **Core Team** (no remaining qualifying role)."

                    except discord.Forbidden:

                        extra_note += (
                            "\n⚠️ Couldn't update Core Team — check "
                            "my role position."
                        )

            if role in COMMUNITY_SUPPORT_TRIGGER_KEYS:

                if not holds_any(member, COMMUNITY_SUPPORT_TRIGGER_KEYS):

                    community_role = get_role(interaction.guild, "communitysupport")

                    if community_role is None:

                        community_id, _ = STAFF_ROLES["communitysupport"]

                        extra_note += (
                            f"\n⚠️ Community Support role (ID "
                            f"{community_id}) not found in this "
                            "server."
                        )

                    try:

                        if community_role and community_role in member.roles:

                            await member.remove_roles(community_role)
                            extra_note += "\n➖ Removed **Community Support** (no remaining qualifying role)."

                    except discord.Forbidden:

                        extra_note += (
                            "\n⚠️ Couldn't update Community Support "
                            "— check my role position."
                        )

            title = "🗑️ Staff Role Removed"


        else:

            await interaction.followup.send(
                "❌ Action must be add or remove."
            )

            return


        # NICKNAME SYNC
        # Recalculates the member's prefix from scratch based on
        # every staff role they hold after this change — so removing
        # one role correctly falls back to another one they still
        # hold, instead of just clearing the nickname.

        nick_note = ""

        try:

            await sync_nickname(member)

        except discord.Forbidden:

            nick_note = (
                "\n⚠️ Role updated, but I couldn't update the "
                "nickname (check my role position — I can't rename "
                "members with a higher or equal role, including the "
                "server owner)."
            )


        # RESPONSE EMBED

        embed = discord.Embed(
            title=title,
            description=(

                f"👤 Member: {member.mention}\n"
                f"🎖️ Role: **{role_name}**\n"
                f"👮 Action by: {interaction.user.mention}"
                f"{extra_note}"
                f"{nick_note}"

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
                    f"🎖️ **Role:** {role_name}\n"
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