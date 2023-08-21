from telegram import Update
from telegram.ext import ContextTypes

from db.db import *
from db.sql import *

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""Привет! Это телеграм-бот-todo_list, он нужен для ведения списка дел. Вот его команды:
/add <дата> <дело> — добавляет дело в список даты.
/view_day <дата> — выводит список дел даты.
/delete_task <дата> <номер дела> — удаляет дело из списка даты. Номер дела — из команды /view_day.
/finish_task <дата> <номер дела> — отмечает дело завершеным. Номер дела — из команды /view_day.""")


async def add_task_handler(
    update: Update, 
    context : ContextTypes.DEFAULT_TYPE) -> None:
    planned_date, *task_text = update.message.text.split(" ")[1:]
    task_text = " ".join(task_text).capitalize()
    telegram_user_id = update.message.chat_id
    
    tasks = await fetch_all(
        sql=CHECK_TASK_COPY,
        params=(task_text, planned_date, telegram_user_id)
        )
    
    if [task for task in tasks]:
        await update.message.reply_text("Это дело уже запланировано!")
        return
    
    await execute(
        sql=ADD_TASK,
        params=(telegram_user_id, task_text, planned_date)
    )
    
    await update.message.reply_text(f'Дело "{task_text}" запланировано на {planned_date}.')
    
    
async def view_day_handler(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE) -> None:
    date = update.message.text.split(" ")[1]
    telegram_user_id = update.message.chat_id

    days_tasks = [task for task in await fetch_all(
        sql=DAYS_TASKS,
        params=(telegram_user_id, date)
    )]
    
    if not days_tasks:
        await update.message.reply_text(f'На {date} ничего не запланировано!')
        return

    for number, task_info in enumerate(days_tasks):
        task_text = task_info[0]
        
        if task_info[1]:
            date, time = task_info[1].split(" ")
            task = f'{number + 1}. {task_text}. \nБыло выполнено {date} в {time}.'
        else:
            task =  f'{number + 1}. {task_text}.'
        
        days_tasks[number] = task
    
    days_tasks = "\n".join(days_tasks)
    
    await update.message.reply_text(f'Вот дела, которые Вы запланировали на {date}:\n{days_tasks}') 


async def delete_task_handler(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE) -> None:
    date, task_number = update.message.text.split(" ")[1:]
    telegram_user_id = update.message.chat_id
    
    
    days_tasks = [task for task in await fetch_all(
        sql=DAYS_TASKS,
        params=(telegram_user_id, f"%{date}%")
    )]
    
    try:
        task_text = days_tasks[int(task_number) - 1][0]
    except IndexError:
        await update.message.reply_text("Дела под таким номером не существует!")
        return
    
    await execute(
        sql=DELETE_TASK, 
        params=(telegram_user_id, task_text)
        )
    
    await update.message.reply_text(f'"{task_text}" было удалено из Ваших планов на {date}.')


async def finish_task_handler(
    update: Update, 
    context : ContextTypes.DEFAULT_TYPE) -> None:
    date, task_number = update.message.text.split(" ")[1:]
    telegram_user_id = update.message.chat_id

    days_tasks = [task for task in await fetch_all(
        sql=DAYS_TASKS,
        params=(telegram_user_id, f"%{date}%")
    )]
    
    try:
        task_text, finished_date = days_tasks[int(task_number) - 1]
    except IndexError:
        await update.message.reply_text("Дела под таким номером не существует!")

        return
    
    if not finished_date:
        await execute(
            sql=FINISH_TASK, 
            params=(telegram_user_id, task_text)
            )
        await update.message.reply_text(f'"{task_text}" завершено!')
    else:
        await update.message.reply_text("Это дело уже завершено!")
    