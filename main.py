from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv
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
VALUES({user_id}, '{task_text}', '{planned_date}', current_timestamp, null);
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
    await bot.reply_to(message, "\n".join([f"{number + 1}. {plan}" for number, plan in enumerate(days_plans)]))


@bot.message_handler(commands=["delete"])
async def delete_task(message):
    date, task_number = message.text.split(" ")[1:]
    user_id = message.chat.id
    
    async with aiosqlite.connect("db.sqlite") as db:
        async with db.execute(f"""SELECT task_text 
FROM tasks
WHERE user_id = {user_id} AND planned_date LIKE '%{date}%'""") as cursor:
            task_text = [plan[0] async for plan in cursor][int(task_number)]
    
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute(f"""DELETE FROM tasks
WHERE user_id = {user_id} AND task_text = '{task_text}'""")
        await db.commit()


@bot.message_handler(commands=["finish"])
async def finish_task(message):
    date, task_number = message.text.split(" ")[1:]
    user_id = message.chat.id
    
    async with aiosqlite.connect("db.sqlite") as db:
        async with db.execute(f"""SELECT task_text 
FROM tasks
WHERE user_id = {user_id} AND planned_date LIKE '%{date}%'""") as cursor:
            task_text = [plan[0] async for plan in cursor][int(task_number)]
    
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute(f"""UPDATE tasks
SET finished_at = current_timestamp
WHERE user_id = {user_id} AND task_text = '{task_text}'""")
        await db.commit()
    
    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.polling())
