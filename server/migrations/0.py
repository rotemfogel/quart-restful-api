from quart_db import Connection


async def migrate(connection: Connection) -> None:
    await connection.execute(
        """
        CREATE TABLE cards (
          id       SERIAL NOT NULL PRIMARY KEY,
          question text   NOT NULL UNIQUE,
          answer   text   NOT NULL
        );
        """
    )


async def valid_migration(connection: Connection) -> bool:
    result = await connection.fetch_one(
        """
        SELECT COUNT(1) AS exists
          FROM information_schema.TABLES
         WHERE table_name = 'cards';
    """
    )
    return result.get("exists") == 1
