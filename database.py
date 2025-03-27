import asyncpg
import asyncio


class Database:
    def __init__(self, database: str) -> None:
        self.database = database
        self.connection = None

    async def __aenter__(self) -> "Database":
        self.connection = await asyncpg.connect(self.database)
        return self

    async def __aexit__(self, *exc) -> None:
        if self.connection:
            await self.connection.close()

    async def create_table(self) -> None:
        query = """
                CREATE TABLE IF NOT EXISTS groups (
                    chat_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    username TEXT,       -- Username (@username)
                    first_name TEXT,     -- Имя пользователя
                    last_name TEXT,      -- Фамилия пользователя
                    messages_count INTEGER DEFAULT 0,
                    PRIMARY KEY (chat_id, user_id)
                )
                """
        await self.connection.execute(query)

    async def insert_data(self, params: tuple) -> None:
        query = """
                INSERT INTO groups (chat_id, user_id, username, first_name, last_name, messages_count)
                VALUES ($1, $2, $3, $4, $5, 1)
                ON CONFLICT (chat_id, user_id) 
                DO UPDATE SET 
                    messages_count = groups.messages_count + 1,
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name;
                """
        await self.connection.execute(query, *params)
