# - *- coding: utf- 8 - *-
import configparser
import time
from datetime import datetime
from bot.data.config import lang_en, lang_ru
from bot.data.config import db
from bot.data.loader import bot
from datetime import datetime
from typing import Union
import pytz
from bot.data.config import game_slots

# Получение админов
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins:
        admins.remove("")
    while " " in admins:
        admins.remove(" ")

    admins = list(map(int, admins))

    return admins

# Получение текущего unix времени
def get_unix(full=False):
    if full:
        return time.time_ns()
    else:
        return int(time.time())

#Рассылка админам
async def send_admins(msg, photo=None, file=None):
    for admin in get_admins():
        if photo:
            await bot.send_photo(chat_id=admin, photo=photo, caption=msg)
        elif file:
            await bot.send_document(chat_id=admin, document=file, caption=msg)
        else:
            await bot.send_message(chat_id=admin, text=msg)
            
async def get_language(user_id):
    lang = (await db.get_user(user_id=user_id))['language']
    if lang == "ru":
        return lang_ru
    elif lang == "en":
        return lang_en
    
# Удаление отступов в многострочной строке ("""text""")
def ded(get_text: str) -> str:
    if get_text is not None:
        split_text = get_text.split("\n")
        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop()
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:].strip()

            save_text.append(text)
        get_text = "\n".join(save_text)
    else:
        get_text = ""

    return get_text


# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():
    await db.update_settings(profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:00
async def update_profit_week():
    await db.update_settings(profit_week=get_unix())
    
# Конвертация unix в дату и даты в unix
def convert_date(from_time, full=True, second=True) -> Union[str, int]:
    from bot.data.config import BOT_TIMEZONE

    if "-" in str(from_time):
        from_time = from_time.replace("-", ".")

    if str(from_time).isdigit():
        if full:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
        elif second:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M")
        else:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
    else:
        if " " in str(from_time):
            cache_time = from_time.split(" ")

            if ":" in cache_time[0]:
                cache_date = cache_time[1].split(".")
                cache_time = cache_time[0].split(":")
            else:
                cache_date = cache_time[0].split(".")
                cache_time = cache_time[1].split(":")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            x_hour, x_minute, x_second = cache_time[0], cache_time[1], cache_time[2]

            from_time = f"{x_day}.{x_month}.{x_year} {x_hour}:{x_minute}:{x_second}"
        else:
            cache_date = from_time.split(".")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            from_time = f"{x_day}.{x_month}.{x_year}"

        if " " in str(from_time):
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y %H:%M:%S").timestamp())
        else:
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y").timestamp())

    return to_time

#Работа с массивом игры
def func__arr_game(game_name, lang):
    english_game_name = game_name
    russian_game_name = game_slots.get(english_game_name)
    game_name_text = getattr(lang, russian_game_name)
     
    return game_name_text

# Проверка ввода на число
def is_number(get_number: Union[str, int, float]) -> bool:
    if str(get_number).isdigit():
        return True
    else:
        if "," in str(get_number): get_number = str(get_number).replace(",", ".")

        try:
            float(get_number)
            return True
        except ValueError:
            return False
        
def convert_ref(lang, ref):
    ref = int(ref)
    refs = lang.ref_s

    if ref % 10 == 1 and ref % 100 != 11:
        count = 0
    elif 2 <= ref % 10 <= 4 and (ref % 100 < 10 or ref % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{refs[count]}"

async def autobackup_db():
    db_path = "bot/data/database.db"
    with open(db_path, "rb") as data:
        for admin in get_admins():
            await bot.send_document(chat_id=admin, document=data, caption="<b>⚙️ АвтоБэкап базы данных ⚙️</b>")