import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from handlers import (
    start_handler,
    add_task_handler,
    view_day_handler,
    delete_task_handler,
    finish_task_handler
    )
from db.db import close_db
from config import TOKEN

COMMAND_HANDLERS = {
    "start": start_handler,
    "add": add_task_handler,
    "view": view_day_handler,
    "delete": delete_task_handler,
    "finish": finish_task_handler
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))
    application.run_polling()
    

if __name__ == "__main__":
    main()
    close_db()
