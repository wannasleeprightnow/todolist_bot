from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
DB_PATH = getenv("DB_PATH")

DATE_FORMAT = "%d.%m"