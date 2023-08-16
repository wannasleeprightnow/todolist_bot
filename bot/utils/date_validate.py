from datetime import datetime

from utils.config import DATE_FORMAT

async def date_validate(input_date: str):
    return str(datetime.strptime(input_date, DATE_FORMAT))
    