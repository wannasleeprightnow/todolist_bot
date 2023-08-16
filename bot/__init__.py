import asyncio

from main import bot
from db.db import close_db

if __name__ == "__main__":
    asyncio.run(bot.polling())
    close_db()
