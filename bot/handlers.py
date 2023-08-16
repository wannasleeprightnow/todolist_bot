from db.db import *
from db.sql import *
from utils.exceptions import *


async def add_task_handler(
    task_text: str,
    planned_date: str,
    telegram_user_id: int
    ) -> None:
    
    tasks = await fetch_all(
        sql=CHECK_TASK_COPY,
        params=(task_text, planned_date, telegram_user_id)
        )
    
    if [task for task in tasks]:
        raise TaskIsAlreadyPlanned
    
    await execute(
        sql=ADD_TASK,
        params=(telegram_user_id, task_text, planned_date)
    )


async def view_day_hadler(
    date: str,
    telegram_user_id: int
    ) -> str | None:
    date = f"%{date}%"
    
    days_tasks = [task for task in await fetch_all(
        sql=DAYS_TASKS,
        params=(telegram_user_id, date)
    )]
    
    if not days_tasks:
        return
    
    for number, task_info in enumerate(days_tasks):
        task_text = task_info[0]
        
        if task_info[1]:
            date, time = task_info[1].split(" ")
            task = f'{number + 1}. {task_text}. \nБыло выполнено {date} в {time}.'
        else:
            task =  f'{number + 1}. {task_text}.'
        
        days_tasks[number] = task
    
    return "\n".join(days_tasks)


async def delete_task_handler(
    date: str,
    task_number: int,
    telegram_user_id: int
    ) -> str:
    
    task_text = list(await task_existence_check(
        date=date, 
        task_number=task_number, 
        telegram_user_id=telegram_user_id
    ))[0]
    
    await execute(
        sql=DELETE_TASK, 
        params=(telegram_user_id, task_text)
        )
    
    return task_text


async def finish_task_handler(
    date: str,
    task_number: int,
    telegram_user_id: int
) -> str:
    
    task_text, finished_date = list(await task_existence_check(
        date=date, 
        task_number=task_number, 
        telegram_user_id=telegram_user_id
    ))
    
    if not finished_date:
        await execute(
            sql=FINISH_TASK, 
            params=(telegram_user_id, task_text)
            )  
    else:
        raise TaskIsAlreadyFinished
    
    return task_text



async def task_existence_check(
    date: str,
    task_number: int,
    telegram_user_id: int
) -> tuple:

    date = f"%{date}%"
    
    days_tasks = [task for task in await fetch_all(
        sql=DAYS_TASKS,
        params=(telegram_user_id, date)
    )]
    
    try:
        task_text, finished_date = days_tasks[int(task_number) - 1]
        return task_text, finished_date
    except IndexError:
        raise TaskNotExists
