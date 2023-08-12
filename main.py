from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv
from telebot.types import MessageAutoDeleteTimerChanged
import aiosqlite

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
async def send_welcome_and_help(message):
    await bot.reply_to(message, "привет!")
    
    
@bot.message_handler(commands={"add"})
async def add_task(message):
    planned_date, task_text = message.text.split(" ")[1:]
    user_id = message.chat.id
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute(f"""INSERT INTO tasks
(user_id, task_text, planned_date, added_at, finished_at)
VALUES({user_id}, '{task_text}', '{planned_date}', current_timestamp, current_timestamp);
""", )
        await db.commit()


@bot.message_handler(commands=["view"])
async def view_day(message):
    date = message.text.split(" ")[1]
    user_id = message.chat.id
    
    async with aiosqlite.connect("db.sqlite") as db:
        async with db.execute(f"""SELECT task_text 
FROM tasks
WHERE user_id = {user_id} AND planned_date LIKE '%{date}%'""") as cursor:
            days_plans = [plan[0] async for plan in cursor]

    await bot.reply_to(message, '\n'.join(days_plans))

    
if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.polling())
