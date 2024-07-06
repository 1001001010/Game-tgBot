# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from bot.data.config import db
from bot.utils.utils_functions import get_admins

async def user_menu(texts, user_id):
    """ Клавиатура главноего меню

    Args:
        texts (string): Язык текста
        user_id (integer): Айди пользователя

    Returns:
        keyboard: Клавиатура
    """
    pr_buttons = await db.get_all_pr_buttons()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(texts.reply_kb1, texts.reply_kb2)
    keyboard.add(texts.refill)
    keyboard.row(texts.reply_kb4, texts.reply_kb3)
    if user_id in get_admins():
        keyboard.add(texts.reply_admin)
    for button in pr_buttons:
            keyboard.add(button['name'])
    return keyboard