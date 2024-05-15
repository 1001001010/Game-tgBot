# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.data.config import db

async def choose_languages_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    langs = await db.get_all_languages()

    for lang in langs:
        keyboard.add(InlineKeyboardButton(lang['name'], callback_data=f"change_language:{lang['language']}"))

    return keyboard

def admin_menu(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("🖤 Общие настройки", callback_data="settings"))
    kb.append(InlineKeyboardButton("🎲 Доп. настройки", callback_data="extra_settings"))
    kb.append(InlineKeyboardButton("🔍 Искать", callback_data="find:"))
    kb.append(InlineKeyboardButton("Промокод", callback_data="adm_promo"))
    kb.append(InlineKeyboardButton("📌 Рассылка", callback_data="mail_start"))
    kb.append(InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_m"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[4], kb[3])
    keyboard.add(kb[2], kb[5])
    keyboard.add(kb[6])

    return keyboard

def admin_settings(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.reply_kb3, callback_data="settings_faq"))
    kb.append(InlineKeyboardButton(texts.reply_kb4, callback_data="settings_supp"))
    kb.append(InlineKeyboardButton(texts.back_to_adm_m, callback_data="back_to_adm_m"))
    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def back_to_adm_m(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton(texts.back_to_adm_m, callback_data="back_to_adm_m"))
    keyboard.add(kb[0])

    return keyboard

def mail_types(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.mail_only_text, callback_data=f"rmail:text"))
    kb.append(InlineKeyboardButton(texts.mail_with_photo, callback_data=f"rmail:photo"))
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_adm_m"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def opr_mail_text():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("✅ Да, хочу", callback_data=f"mail_start_text:yes"))
    kb.append(InlineKeyboardButton("❌ Нет, не хочу", callback_data=f"mail_start_text:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def opr_mail_photo():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton("✅ Да, хочу", callback_data=f"mail_start_photo:yes"))
    kb.append(InlineKeyboardButton("❌ Нет, не хочу", callback_data=f"mail_start_photo:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def back_to_user_menu(texts):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(texts.back, callback_data="back_to_m"))

    return keyboard

async def support_inll(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []
    s = await db.get_settings(id=1)
    kb.append(InlineKeyboardButton(texts.support_inl, url=s['support']))

    keyboard.add(kb[0])

    return keyboard

async def kb_profile(texts, user_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    user_info = await db.get_user(user_id = user_id)
    if user_info['request_test'] == 0:
        keyboard.add(InlineKeyboardButton(texts.test_balance, callback_data="test_balance"))

    kb.append(InlineKeyboardButton(texts.promo, callback_data='promo'))
    kb.append(InlineKeyboardButton(texts.change_language, callback_data='change_language'))
    keyboard.add(kb[0], kb[1])
    return keyboard

def kb_adm_promo(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.new_promo, callback_data="promo_create"))
    kb.append(InlineKeyboardButton(texts.del_promo, callback_data="promo_delete"))

    keyboard.add(kb[0], kb[1])
    return keyboard