from database.database import connect


async def add_warning(
    user_id,
    moderator_id,
    reason,
    time
):

    db = await connect()

    try:

        await db.execute(
            """
            INSERT INTO warnings
            (
                user_id,
                moderator_id,
                reason,
                time
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                moderator_id,
                reason,
                time
            )
        )

        await db.commit()

    finally:

        await db.close()



async def get_warnings(
    user_id
):

    db = await connect()

    try:

        cursor = await db.execute(
            """
            SELECT *
            FROM warnings
            WHERE user_id=?
            """,
            (
                user_id,
            )
        )

        return await cursor.fetchall()

    finally:

        await db.close()



async def clear_warnings(
    user_id
):

    db = await connect()

    try:

        await db.execute(
            """
            DELETE FROM warnings
            WHERE user_id=?
            """,
            (
                user_id,
            )
        )

        await db.commit()

    finally:

        await db.close()