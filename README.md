# Telegram-bot-todolist
## Команды бота
- `/add {дата} {текст дела}` — добавляет дело в список даты.
- `/finish {дата} {номер дела}` — отмечает дело завершеным. Номер дела — из команды /view_day.
- /`delete {дата} {номер дела}` — удаляет дело из списка даты. Номер дела — из команды /view_day.
- `/view {дата}` — выводит список дел даты.

Дата должна вводиться в формате dd.mm.

## Запуск

Требуется Python3.11.

Создание директории и клонирование репозитория:

```bash
mkdir todolist_bot
cd todolist_bot
git clone https://github.com/enoughtless/todolist_bot.git .
```

Создание и активация виртуального окружения:

```bash
python3 -m venv venv
# Для linux
source venv/bin/activate
# Для windows
source venv\Scripts\activate.bat
```

Токен нужно получить у @BotFather и подставить его в значение TOKEN.

```bash
echo "TOKEN = ""
DB_PATH = "bot/db/db.sqlite"" > .env
```

Обновление pip, установка зависимостей и запуск:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 bot/__main__.py
```