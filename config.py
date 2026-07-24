import os
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("TOKEN")

OWNER_ID = int(
    os.getenv("OWNER_ID", 0)
)


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "database.db"
)


LOG_CHANNEL_ID = int(
    os.getenv(
        "LOG_CHANNEL_ID",
        0
    )
)


# FK Guard Theme

BOT_NAME = "🛡️ 𝓕𝓚 𝓖𝓾𝓪𝓻𝓭"

MAIN_COLOR = 0x00FFFF

SUCCESS_COLOR = 0x00FF00

ERROR_COLOR = 0xFF0000

WARNING_COLOR = 0xFFA500