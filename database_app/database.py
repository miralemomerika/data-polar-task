from contextlib import asynccontextmanager

import asyncpg
from core_app.settings import settings

pool = None


async def init_pool():
    global pool
    pool = await asyncpg.create_pool(settings.DATABASE_URI.unicode_string())


@asynccontextmanager
async def get_connection():
    global pool
    if pool is None:
        await init_pool()
    async with pool.acquire() as connection:
        yield connection


async def close_pool():
    global pool
