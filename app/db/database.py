from contextlib import asynccontextmanager

class Database:
    def __init__(self, db_pool):
        self._pool = db_pool
        self._create_chat_sessions()

    @asynccontextmanager
    async def acquire_connection(self):
        async with self._pool.acquire() as conn:
            try:
                yield conn
            finally:
                self._pool.release(conn)

    async def _create_chat_sessions(self):
        async with self.acquire_connection() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id SERIAL PRIMARY KEY,
                    user1_id INTEGER NOT NULL,
                    user2_id INTEGER NOT NULL,
                    room_id VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    unique (user1_id, user2_id)
                );
                """
            )

    async def add_chat_session(self, user1_id, user2_id, room_id):
        async with self.acquire_connection() as conn:
            await conn.execute(
                """
                INSERT INTO chat_sessions (user1_id, user2_id, room_id)
                VALUES ($1, $2, $3);
                ON CONFLICT (user1_id, user2_id) DO UPDATE 
                SET room_id = EXCLUDED.room_id;
                """,
                user1_id, user2_id, room_id
            )


