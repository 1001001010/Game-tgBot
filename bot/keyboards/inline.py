# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.data import config
from bot.data.config import db

def kb_rework_network(lang):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton(lang.edit_network, callback_data=f"moneta:USDT"))

    keyboard.add(kb[0])

    return keyboard

async def kb_edit_network(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []
    settings = await db.get_settings(id=1)
    kb.append(InlineKeyboardButton(f"The Open Network (TON) | {settings['Commission_TON']}", callback_data=f"new_Edit_network:TON"))
    kb.append(InlineKeyboardButton(f"TRON (TRC20) | {settings['Commission_TRC20']}", callback_data=f"new_Edit_network:TRC20"))
    kb.append(InlineKeyboardButton(f"Ethereum (ERC20) | {settings['Commission_ERC20']}", callback_data=f"new_Edit_network:ERC20"))
    kb.append(InlineKeyboardButton(f"BNB Smart Chain (BER20) | {settings['CommissionBER20']}", callback_data=f"new_Edit_network:BER20"))
    kb.append(InlineKeyboardButton(texts.back_to_adm_m, callback_data="back_to_adm_m"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])

    return keyboard

def kb_network(lang, summa):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("The Open Network (TON)", callback_data=f"network:TON"))
    kb.append(InlineKeyboardButton("TRON (TRC20)", callback_data=f"network:TRC20"))
    kb.append(InlineKeyboardButton("Ethereum (ERC20)", callback_data=f"network:ERC20"))
    kb.append(InlineKeyboardButton("BNB Smart Chain (BER20)", callback_data=f"network:BER20"))
    kb.append(InlineKeyboardButton(lang.back_vivod_to_method, callback_data=f"back_to_method:{summa}"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])

    return keyboard

def yes_or_no_vivod(vivod_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("✅ Подтвердить", callback_data=f"ok_vivod:yes:{vivod_id}"))
    kb.append(InlineKeyboardButton("❌ Отменить", callback_data=f"ok_vivod:no:{vivod_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard


def yes_or_no_cheack(vivod_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("✅ Подтвердить", callback_data=f"ok_check:yes:{vivod_id}"))
    kb.append(InlineKeyboardButton("❌ Отменить", callback_data=f"ok_check:no:{vivod_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def kb_vivod_zayavka(summa, vivod_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("✅ Принять", callback_data=f"vivod:yes:{summa}:{vivod_id}"))
    kb.append(InlineKeyboardButton("❌ Отклонить", callback_data=f"vivod:no:{summa}:{vivod_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def kb_vivod_moneta():
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton("USDT", callback_data=f"moneta:USDT"))
    kb.append(InlineKeyboardButton("🧾 Чек/check", callback_data=f"check"))
    keyboard.add(kb[0])
    keyboard.add(kb[1])

    return keyboard

def kb_payment_link(lang, method, link, pay_id, summa):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton(lang.pay_link, url=link))
    kb.append(InlineKeyboardButton(lang.pay_id, callback_data=f"cheak_pay:{method}:{pay_id}:{summa}"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])

    return keyboard

def game_next(game, type_balance, lang, bet):
    keyboard = InlineKeyboardMarkup()
    kb = []
    kb.append(InlineKeyboardButton(lang.go_next, callback_data=f"play_next:{game}:{type_balance}:{bet}"))
    kb.append(InlineKeyboardButton(lang.back, callback_data="back_to_game_menu"))

    keyboard.add(kb[0])
    keyboard.add(kb[1])

    return keyboard

def payment_method():
    keyboard = InlineKeyboardMarkup()
    kb=[]
    kb.append(InlineKeyboardButton('💠 CryptoBot', callback_data="payment:cryptobot"))
    # kb.append(InlineKeyboardButton('🚀 xRocket', callback_data="payment:xrocket"))
    
    keyboard.add(kb[0])
    return keyboard

def crypto(amount):
    keyboard = InlineKeyboardMarkup()
    kb=[]
    kb.append(InlineKeyboardButton('TONCOIN', callback_data=f"valute:TONCOIN:{amount}"))
    # kb.append(InlineKeyboardButton('SCALE', callback_data=f"valute:SCALE:{amount}"))
    # kb.append(InlineKeyboardButton('HEDGE', callback_data=f"valute:HEDGE:{amount}"))
    # kb.append(InlineKeyboardButton('AMBR', callback_data=f"valute:AMBR:{amount}"))
    # kb.append(InlineKeyboardButton('TAKE', callback_data=f"valute:TAKE:{amount}"))
    # kb.append(InlineKeyboardButton('TNX', callback_data=f"valute:TNX:{amount}"))
    kb.append(InlineKeyboardButton('BOLT', callback_data=f"valute:BOLT:{amount}"))
    kb.append(InlineKeyboardButton('GRBS', callback_data=f"valute:GRBS:{amount}"))
    kb.append(InlineKeyboardButton('jUSDT', callback_data=f"valute:jUSDT:{amount}"))
    kb.append(InlineKeyboardButton('Отмена', callback_data="payment_method"))
    
    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[4])
    return keyboard

def choose_vertical(lang, type_balance, bet):
    keyboard = InlineKeyboardMarkup()
    kb=[]
    kb.append(InlineKeyboardButton(lang.Eagle, callback_data=f"monetka:eagle:{type_balance}:{bet}"))
    kb.append(InlineKeyboardButton(lang.Tails, callback_data=f"monetka:tails:{type_balance}:{bet}"))
    
    keyboard.add(kb[0], kb[1])
    return keyboard

def payment_method_back():
    keyboard = InlineKeyboardMarkup()
    kb=[]
    kb.append(InlineKeyboardButton('⬅️ Вернуться', callback_data=f"payment_method"))
    # kb.append(InlineKeyboardButton('xRocket', callback_data="payment:xrocket"))
    
    keyboard.add(kb[0])
    return keyboard

def sub():
    s = InlineKeyboardMarkup()
    s.row(InlineKeyboardButton(text='Подписаться', url=config.channel_url))
    s.row(InlineKeyboardButton(text="Проверить ✅", callback_data='subprov'))

    return s

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
    kb.append(InlineKeyboardButton("👤 Пользователь", callback_data="find_user"))
    kb.append(InlineKeyboardButton("🧾 Чек", callback_data="find_check"))
    kb.append(InlineKeyboardButton("🎫 Промокод", callback_data="adm_promo"))
    kb.append(InlineKeyboardButton("📌 Рассылка", callback_data="mail_start"))
    kb.append(InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    kb.append(InlineKeyboardButton("💾 Бэкап БД", callback_data="backup"))
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_m"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[4], kb[5])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[6], kb[7])
    keyboard.add(kb[8])

    return keyboard

async def kb_admin_settings(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    s = await db.get_only_settings()
    ref_percent_1 = s['ref_percent_1']
    ref_percent_2 = s['ref_percent_2']  
    ref_percent_3 = s['ref_percent_3']
    ref_percent_cheack = s['Commission_check']
    min_cheack = s['Minimum_check']
    work = s['is_work']
    if work == "True":
        work_emoji = "✅"
    else:
        work_emoji = "❌"
    
    kb.append(InlineKeyboardButton(texts.reply_kb3, callback_data="settings_faq"))
    kb.append(InlineKeyboardButton(texts.reply_kb4, callback_data="settings_supp"))
    kb.append(InlineKeyboardButton(f"2️⃣ Изменить кол-во рефералов для 2 лвла", callback_data="ref_lvl_edit:2"))
    kb.append(InlineKeyboardButton(f"3️⃣ Изменить кол-во рефералов для 3 лвла", callback_data="ref_lvl_edit:3"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 1 лвл. | {ref_percent_1}%", callback_data="ref_percent:edit:1"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 2 лвл. | {ref_percent_2}%", callback_data="ref_percent:edit:2"))
    kb.append(InlineKeyboardButton(f"Реф. Процент 3 лвл. | {ref_percent_3}%", callback_data="ref_percent:edit:3"))
    kb.append(InlineKeyboardButton("🌐 Комиссия сети", callback_data="comma_network"))
    kb.append(InlineKeyboardButton(f"🧾 Комиссия | {ref_percent_cheack}%", callback_data="new_Edit_network:check"))
    kb.append(InlineKeyboardButton(f"🧾 Мин. сумма | {min_cheack}", callback_data="MinimumSumma"))
    kb.append(InlineKeyboardButton(texts.back_to_adm_m, callback_data="back_to_adm_m"))
    kb.append(InlineKeyboardButton(f"Тех. Работы | {work_emoji}", callback_data="work:on_off"))
    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[11])
    keyboard.add(kb[2])
    keyboard.add(kb[3])
    keyboard.add(kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[6])
    keyboard.add(kb[7])
    keyboard.add(kb[8], kb[9])
    keyboard.add(kb[10])

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
    # kb.append(InlineKeyboardButton(texts.change_language, callback_data='change_language'))
    # kb.append(InlineKeyboardButton(texts.refill, callback_data='refil_balance'))
    kb.append(InlineKeyboardButton(texts.conclusion, callback_data='withdrawal'))
    # keyboard.add(kb[0], kb[1])
    keyboard.add(kb[0])
    keyboard.add(kb[1])
    return keyboard

def kb_adm_promo(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.new_promo, callback_data="promo_create"))
    kb.append(InlineKeyboardButton(texts.del_promo, callback_data="promo_delete"))

    keyboard.add(kb[0], kb[1])
    return keyboard

async def kb_back_to_game_menu(texts, user_id, min_bet, type_balance, game):
    keyboard = InlineKeyboardMarkup()
    kb = []
    user = await db.get_user(user_id = user_id)
    if type_balance == 'real':
        if user['test_balance'] > 0 and user['test_balance'] >= min_bet:
            keyboard.add(InlineKeyboardButton(texts.use_demo, callback_data=f"user_use_balance:demo:{game}"))
    elif type_balance == 'demo':
        keyboard.add(InlineKeyboardButton(texts.use_real, callback_data=f"user_use_balance:real:{game}"))
        
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_game_menu"))

    keyboard.add(kb[0])
    return keyboard

def back_to_profile(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_profile"))

    keyboard.add(kb[0])
    return keyboard

def game_menu(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.game_slots, callback_data="game:slots"))
    kb.append(InlineKeyboardButton(texts.game_coin, callback_data="game:coin"))
    kb.append(InlineKeyboardButton(texts.game_basketball, callback_data="game:basketball"))
    kb.append(InlineKeyboardButton(texts.game_football, callback_data="game:football"))
    kb.append(InlineKeyboardButton(texts.game_bowling, callback_data="game:bowling"))
    kb.append(InlineKeyboardButton(texts.game_dice, callback_data="game:dice"))
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_profile"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[4], kb[5])
    keyboard.add(kb[6])
    return keyboard

async def admin_user_menu(texts, user_id):
    keyboard = InlineKeyboardMarkup()
    kb = []
    user = await db.get_user(user_id=user_id)
    if user['is_ban'] == True:
        keyboard.add(InlineKeyboardButton(texts.adm_user_unban, callback_data=f"block:unban:{user_id}"))
    elif user['is_ban'] == False:
        keyboard.add(InlineKeyboardButton(texts.adm_user_ban, callback_data=f"block:ban:{user_id}"))
    kb.append(InlineKeyboardButton(texts.adm_user_revork_bal, callback_data=f"revork:balance:{user_id}"))
    kb.append(InlineKeyboardButton(texts.adm_user_give_bal, callback_data=f"give:balance:{user_id}"))
    kb.append(InlineKeyboardButton(texts.adm_user_revork_demo, callback_data=f"revork:demo:{user_id}"))
    kb.append(InlineKeyboardButton(texts.adm_user_give_demo, callback_data=f"give:demo:{user_id}"))
    kb.append(InlineKeyboardButton("🧾 Отправить чек", callback_data=f"send_check:{user_id}"))
    
    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[4])
    return keyboard

def edit_game_menu(texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(texts.game_slots, callback_data="edit_game:slots"))
    kb.append(InlineKeyboardButton(texts.game_coin, callback_data="edit_game:coin"))
    kb.append(InlineKeyboardButton(texts.game_basketball, callback_data="edit_game:basketball"))
    kb.append(InlineKeyboardButton(texts.game_football, callback_data="edit_game:football"))
    kb.append(InlineKeyboardButton(texts.game_bowling, callback_data="edit_game:bowling"))
    kb.append(InlineKeyboardButton(texts.game_dice, callback_data="edit_game:dice"))
    kb.append(InlineKeyboardButton(texts.back, callback_data="back_to_adm_m"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3])
    keyboard.add(kb[4], kb[5])
    keyboard.add(kb[6])
    return keyboard

async def edit_game_stats(texts, game_name):
    keyboard = InlineKeyboardMarkup()
    kb = []
    game_stats = await db.get_game_settings(name=game_name)

    kb.append(InlineKeyboardButton(texts.adm_edit_factor.format(factor=game_stats['factor']), callback_data=f"edit:factor:{game_name}")) #Коэффициент 'X'
    kb.append(InlineKeyboardButton(texts.min_bet.format(min_bet=game_stats['min_bet']), callback_data=f"edit:min_bet:{game_name}")) #Мин. ставка 
    kb.append(InlineKeyboardButton(texts.back, callback_data=f"extra_settings")) #Назад

    keyboard.add(kb[0])
    keyboard.add(kb[1])
    if game_name == 'coin': 
        keyboard.add(InlineKeyboardButton(texts.real_chance.format(real_chance=game_stats['chance_real']*100), callback_data=f"edit:real_chance:{game_name}")) #Шанс победы для реал денег
        keyboard.add(InlineKeyboardButton(texts.demo_chance.format(demo_chance=game_stats['chance_demo']*100), callback_data=f"edit:demo_chance:{game_name}")) #Шанс победы для демо режима
    keyboard.add(kb[2])
    return keyboard

def edit_game_chance(type_dep, game, texts):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton('0%', callback_data=f"chance_edit:{game}:{type_dep}:0"))
    kb.append(InlineKeyboardButton('10%', callback_data=f"chance_edit:{game}:{type_dep}:10"))
    kb.append(InlineKeyboardButton('20%', callback_data=f"chance_edit:{game}:{type_dep}:20"))
    kb.append(InlineKeyboardButton('30%', callback_data=f"chance_edit:{game}:{type_dep}:30"))
    kb.append(InlineKeyboardButton('40%', callback_data=f"chance_edit:{game}:{type_dep}:40"))
    kb.append(InlineKeyboardButton('50%', callback_data=f"chance_edit:{game}:{type_dep}:50"))
    kb.append(InlineKeyboardButton('60%', callback_data=f"chance_edit:{game}:{type_dep}:60"))
    kb.append(InlineKeyboardButton('70%', callback_data=f"chance_edit:{game}:{type_dep}:70"))
    kb.append(InlineKeyboardButton('80%', callback_data=f"chance_edit:{game}:{type_dep}:80"))
    kb.append(InlineKeyboardButton('90%', callback_data=f"chance_edit:{game}:{type_dep}:90"))
    kb.append(InlineKeyboardButton('100%', callback_data=f"chance_edit:{game}:{type_dep}:100"))
    kb.append(InlineKeyboardButton(texts.back, callback_data=f"edit_game:{game}"))

    keyboard.add(kb[0])
    keyboard.add(kb[1], kb[2], kb[3])
    keyboard.add(kb[4], kb[5], kb[6])
    keyboard.add(kb[7], kb[8], kb[9])
    keyboard.add(kb[10])
    keyboard.add(kb[11])

    return keyboard