from typing import Iterable
import aiosqlite
import asyncio

from config import DB_PATH


async def _get_db() -> aiosqlite.Connection:
    if not getattr(_get_db, "db", None):
        db = await aiosqlite.connect(DB_PATH)
        _get_db.db = db

    return _get_db.db


async def execute(
    sql: str,
    params: tuple | None = None
    ) -> None:
    db = await _get_db()
    args: tuple = (sql, params)
    await db.execute(*args)
    await db.commit()
    

async def get_cursor(
    sql: str,
    params: tuple | None = None
    ) -> aiosqlite.Cursor:
    db = await _get_db()
    args: tuple = (sql, params)
    cursor = await db.execute(*args)
    return cursor


def close_db() -> None:
    asyncio.run(_async_close_db())


async def _async_close_db() -> None:
    await (await _get_db()).close()


async def fetch_all(
    sql: str,
    params: tuple | None = None
    ) -> Iterable:
    cursor = await get_cursor(sql, params)
    result = await cursor.fetchall()
    await cursor.close()
    return result
