# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from bot.utils.utils_functions import get_admins

#Главное меню
async def user_menu(texts, user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texts.reply_kb1, texts.reply_kb2)
    keyboard.row(texts.reply_kb3, texts.reply_kb4)
    keyboard.add(texts.refill)
    if user_id in get_admins():
        keyboard.add(texts.reply_admin)
    return keyboard