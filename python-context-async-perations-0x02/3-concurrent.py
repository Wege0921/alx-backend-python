#!/usr/bin/env python3
"""
3-concurrent.py
Run multiple async SQLite queries concurrently using aiosqlite and asyncio.gather.
"""

import asyncio
import aiosqlite

DB_PATH = "users.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    # Run both queries concurrently and gather results
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", all_users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
