import datetime


def get_time():

    return datetime.datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )



def format_seconds(seconds):

    minutes, seconds = divmod(
        seconds,
        60
    )


    hours, minutes = divmod(
        minutes,
        60
    )


    if hours:

        return f"{hours}h {minutes}m"


    if minutes:

        return f"{minutes}m {seconds}s"


    return f"{seconds}s"



def clean_reason(reason):

    if not reason:

        return "No reason provided"


    return reason[:500]
