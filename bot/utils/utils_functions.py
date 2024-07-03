# - *- coding: utf- 8 - *-
import configparser
import time
from datetime import datetime
from typing import Union
import pytz
import uuid
import random
from bot.data.config import lang_en, lang_ru, game_slots, db, BOT_TIMEZONE
from bot.data.loader import bot

def get_admins():
    """ Получение администраторов

    Returns:
        admins: Список администраторов
    """
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

def get_unix(full=False):
    """ Получение текущего unix времени

    Args:
        full (bool, optional): Полное число или нет. Defaults to False.

    Returns:
        time: Текущее unix время
    """
    if full:
        return time.time_ns()
    else:
        return int(time.time())

async def send_admins(msg, photo=None, file=None):
    """ Рассылка администраторам

    Args:
        msg (string): Сообщение
        photo (string, optional): Фото. Defaults to None.
        file (string, optional): Файл. Defaults to None.
    """
    for admin in get_admins():
        if photo:
            await bot.send_photo(chat_id=admin, photo=photo, caption=msg)
        elif file:
            await bot.send_document(chat_id=admin, document=file, caption=msg)
        else:
            await bot.send_message(chat_id=admin, text=msg)
            
async def get_language(user_id):
    """ Получение языка

    Args:
        user_id (string): Айди пользователя
        
    Returns:
        lang: Язык, на котором отправить сообщение пользователю
    """
    lang = (await db.get_user(user_id=user_id))['language']
    if lang == "ru":
        return lang_ru
    elif lang == "en":
        return lang_en

def ded(get_text: str) -> str:
    """ Удаление отступов в многострочной строке ('''text''')

    Args:
        get_text (str): _description_

    Returns:
        get_text: Текст без отступов
    """
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


async def update_profit_day():
    """ 
    Автоматическая очистка ежедневной статистики после 00:00
    """
    await db.update_settings(profit_day=get_unix())

async def update_profit_week():
    """ Автоматическая очистка еженедельной статистики в понедельник 00:00
    """
    await db.update_settings(profit_week=get_unix())
    
def convert_date(from_time, full=True, second=True) -> Union[str, int]:
    """ Конвертация из unix в дату и обратно

    Args:
        from_time : Время
        full (bool, optional): Полное unix время или нет. Defaults to True.
        second (bool, optional): С Секундами. Defaults to True.

    Returns:
        Union[str, int]: Конвертированное время
    """

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

def func__arr_game(game_name, lang):
    """ Работа с массивом игры

    Args:
        game_name (string): Название игры
        lang (string): Язык

    Returns:
        game_name_text: Полученное название игры
    """
    english_game_name = game_name
    russian_game_name = game_slots.get(english_game_name)
    game_name_text = getattr(lang, russian_game_name)
     
    return game_name_text

def is_number_2(get_number: Union[str, int, float]) -> bool:
    """ Проверка ввода на число

    Args:
        get_number (Union[str, int, float]): Введенная строка

    Returns:
        bool: Является строка числом или нет
    """
    if str(get_number).isdigit():
        return True
    else:
        if "," in str(get_number): get_number = str(get_number).replace(",", ".")
        try:
            float(get_number)
            return True
        except ValueError:
            return False
        
def is_number(get_number: Union[str, int, float]) -> bool:
    """ Проверка ввода на число

    Args:
        get_number (Union[str, int, float]): Введенная строка

    Returns:
        bool: Является строка числом или нет
    """
    if str(get_number).isdigit():
        return True
    else:
        # if "," in str(get_number): get_number = str(get_number).replace(",", ".")
        # try:
        #     float(get_number)
        #     return True
        # except ValueError:
            return False

def convert_ref(lang, ref):
    """ Склонение колличества рефералова

    Args:
        lang (string): язык
        ref (integer): кол-во рефералов

    Returns:
        refs: Склонение
    """
    ref = int(ref)
    refs = lang.ref_s

    if ref % 10 == 1 and ref % 100 != 11:
        count = 0
    elif 2 <= ref % 10 <= 4 and (ref % 100 < 10 or ref % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{refs[count]}" 

def gen_id(len_id: int = 16) -> int:
    """ Генерация уникального айди

    Args:
        len_id (int, optional): Длина сгенерированного айди. Defaults to 16.

    Returns:
        int: Уникальный айди
    """
    mac_address = uuid.getnode()
    time_unix = int(str(time.time_ns())[:len_id])
    random_int = int(''.join(random.choices('0123456789', k=len_id)))

    return mac_address + time_unix + random_int

async def autobackup_db():
    """ 
    Автобэкап БД
    """
    db_path = "bot/data/database.db"
    with open(db_path, "rb") as data:
        for admin in get_admins():
            await bot.send_document(chat_id=admin, document=data, caption="<b>💾 АвтоБэкап базы данных 🧮</b>")