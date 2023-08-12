from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
async def send_welcome_and_help(message):
    await bot.reply_to(message, "привет!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.polling())
