# - *- coding: utf- 8 - *-
import configparser
from bot.data.config import lang_en, lang_ru
from bot.data.config import db
from bot.data.loader import bot

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