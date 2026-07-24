import aiosqlite

from config import DATABASE_PATH


async def connect():
    return await aiosqlite.connect(
        DATABASE_PATH
    )


async def setup_database():

    db = await connect()

    try:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS warnings(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                moderator_id INTEGER,

                reason TEXT,

                time TEXT

            )
            """
        )


        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings(

                guild_id INTEGER PRIMARY KEY,

                log_channel INTEGER,

                automod INTEGER DEFAULT 1

            )
            """
        )


        await db.commit()


    finally:

        await db.close()