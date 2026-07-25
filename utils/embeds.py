import discord

from config import (
    BOT_NAME,
    MAIN_COLOR,
    SUCCESS_COLOR,
    ERROR_COLOR,
    WARNING_COLOR
)


def base_embed(
    title,
    description,
    color=MAIN_COLOR
):

    embed = discord.Embed(

        title=title,

        description=description,

        color=color

    )


    embed.set_footer(
        text=BOT_NAME
    )


    return embed



def success(
    message
):

    return base_embed(

        "✅ Success",

        message,

        SUCCESS_COLOR

    )



def error(
    message
):

    return base_embed(

        "❌ Error",

        message,

        ERROR_COLOR

    )



def warning(
    message
):

    return base_embed(

        "⚠️ Warning",

        message,

        WARNING_COLOR

    )



def info(
    message
):

    return base_embed(

        "🛡️ FK Guard",

        message,

        MAIN_COLOR

    )
