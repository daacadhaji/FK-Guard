from discord.ext import commands



def moderator():

    async def predicate(ctx):

        if ctx.author.guild_permissions.manage_messages:

            return True


        raise commands.MissingPermissions(
            ["manage_messages"]
        )


    return commands.check(
        predicate
    )



def administrator():

    async def predicate(ctx):

        if ctx.author.guild_permissions.administrator:

            return True


        raise commands.MissingPermissions(
            ["administrator"]
        )


    return commands.check(
        predicate
    )



def owner():

    from config import OWNER_ID


    async def predicate(ctx):

        if ctx.author.id == OWNER_ID:

            return True


        raise commands.CheckFailure(
            "Owner only command"
        )


    return commands.check(
        predicate
    )