from telebot.async_telebot import AsyncTeleBot

from utils.config import TOKEN
from utils.exceptions import *
from utils.date_validate import date_validate
from handlers import *

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
async def send_welcome_and_help(message):
    await bot.reply_to(message, 
                       "\n".join(["/add <дата> <дело> - добавляет дело в список даты.",
                        "/view_day <дата> - выводит список дел даты.",
                        "/delete_task <дата> <номер дела> - удаляет дело из списка даты. Номер дела - из команды /view_day",
                        "/finish_task <дата> <номер дела> - отмечает дело завершеным. Номер дела - из команды /view_day"])
                       )
    
    
@bot.message_handler(commands=["add"])
async def add_task(message):
    planned_date, *task_text = message.text.split(" ")[1:]
    task_text = " ".join(task_text).capitalize()
    telegram_user_id = message.chat.id
 
    try:
        await date_validate(planned_date)
        await add_task_handler(
            task_text=task_text,
            planned_date=planned_date,
            telegram_user_id=telegram_user_id
        )
    except ValueError:
        await bot.reply_to(
            message,
            "Введена дата в неверном формате."
        )
        return
    except TaskIsAlreadyPlanned:
        await bot.reply_to(message, "Это дело уже запланировано!")
    else:
        await bot.reply_to(
        message,
        f'Дело "{task_text}" запланировано на {planned_date}.'
        )


@bot.message_handler(commands=["view"])
async def view_day(message):
    date = message.text.split(" ")[1]
    telegram_user_id = message.chat.id

    try:
        await date_validate(date)
    except ValueError:
        await bot.reply_to(
            message,
            "Введена дата в неверном формате."
        )
        return
    
    days_tasks: str | None = await view_day_hadler(
        date=date,
        telegram_user_id=telegram_user_id
    )
    
    if days_tasks:
        await bot.reply_to(
            message, 
            f'Вот дела, которые Вы запланировали на {date}:\n{days_tasks}'
            )
    else:
        await bot.reply_to(
            message,
            f'На {date} ничего не запланировано!'
        )


@bot.message_handler(commands=["delete"])
async def delete_task(message):
    date, task_number = message.text.split(" ")[1:]
    telegram_user_id = message.chat.id
    
    try:
        await date_validate(date)
        task_text: str = await delete_task_handler(
            date=date,
            task_number=task_number,
            telegram_user_id=telegram_user_id,
        )
    except ValueError:
        await bot.reply_to(
            message,
            "Введена дата в неверном формате."
        )
        return
    except TaskNotExists:
        await bot.reply_to(
            message, 
            f"Дела под таким номером не существует!"
            )
    else:
        await bot.reply_to(
            message, 
            f'"{task_text}" было удалено из Ваших планов на {date}.'
            )


@bot.message_handler(commands=["finish"])
async def finish_task(message):
    date, task_number = message.text.split(" ")[1:]
    telegram_user_id = message.chat.id
    
    try:
        await date_validate(date)
        task_text: str = await finish_task_handler(
            date=date,
            task_number=task_number,
            telegram_user_id=telegram_user_id,
        )
    except ValueError:
        await bot.reply_to(
            message,
            "Введена дата в неверном формате."
        )
        return
    except TaskNotExists:
        await bot.reply_to(
            message, 
            f"Дела под таким номером не существует!"
            )
    except TaskIsAlreadyFinished:
        await bot.reply_to(
            message, 
            f"Это дело уже завершено!"
            )
    else:
        await bot.reply_to(
            message, 
            f'"{task_text}" завершено!'
            )
