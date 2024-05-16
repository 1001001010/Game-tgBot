from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 
import asyncio

from bot.data.config import lang_ru, lang_en
from bot.data.loader import dp, bot
from bot.data.config import db
from bot.utils.utils_functions import get_language, ded, send_admins, get_admins, convert_date, func__arr_game
from bot.filters.filters import IsAdmin
from bot.state.admin import admin_main_settings, Newsletter, Newsletter_photo, AdminSettingsEdit, \
                            AdminCoupons, AdminFind, AdminBanCause, AdminGame_edit
                            
from bot.keyboards.inline import admin_menu, admin_settings, back_to_adm_m, mail_types, \
                                 kb_adm_promo, admin_user_menu, edit_game_menu, edit_game_stats, \
                                 edit_game_chance

#Открытие Профиля
@dp.message_handler(IsAdmin(), text=lang_ru.reply_admin, state="*")
@dp.message_handler(IsAdmin(), text=lang_en.reply_admin, state="*")
async def func__admin_menu(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    await message.answer(lang.admin_menu, reply_markup=admin_menu(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text='settings', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(lang.admin_settings, reply_markup=admin_settings(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text='settings_faq', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.admin_edit_faq, reply_markup=back_to_adm_m(texts=lang))
    await admin_main_settings.faq.set()
    
@dp.message_handler(IsAdmin(), state=admin_main_settings.faq)
async def adm_edit_faq(message: Message, state: FSMContext):
    msg = message.parse_entities()
    lang = await get_language(message.from_user.id)
    await state.update_data(msg=msg)
    data = await state.get_data()
    await db.update_settings(FAQ=data['msg'])
    await message.answer(lang.faq_success, reply_markup=admin_menu(texts=lang))
    await state.finish()
#Статистика
@dp.callback_query_handler(IsAdmin(), text='stats', state="*")
async def open_stats(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    all_user, show_users_week, show_users_day = 0, 0, 0
    all_users = await db.all_users()
    settings = await db.get_only_settings()
    admin_count = len(get_admins())
    for user in all_users:
        if int(user['reg_date_unix']) - int(settings['profit_day']) >= 0:
            show_users_day += 1

        if int(user['reg_date_unix']) - int(settings['profit_week']) >= 0:
            show_users_week += 1
        all_user += 1

    msg = f"""Статистика
    
    Всего пользователей: {all_user}
    Ползователей за неделю {show_users_week}
    Пользователей за день {show_users_day}

    Всего администраторов: {admin_count}"""
    await call.message.answer(ded(msg))

#Рассылка
@dp.callback_query_handler(IsAdmin(), text_startswith="mail_start", state="*")
async def func_newsletter(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.admin_mail, reply_markup=mail_types(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text_startswith="rmail", state="*")
async def func_newsletter(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    type_id = call.data.split(":")[1]
    lang = await get_language(call.from_user.id)
    if type_id == 'text':
        await call.message.answer(lang.admin_newsletter, reply_markup=back_to_adm_m(texts=lang))
        await Newsletter.msg.set()
    elif type_id == 'photo':
        await call.message.answer(lang.admin_text_send, reply_markup=back_to_adm_m(texts=lang))
        await Newsletter_photo.msg.set()
    
@dp.message_handler(IsAdmin(), state=Newsletter_photo.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await state.update_data(msg=msg)
    lang = await get_language(message.from_user.id)
    await message.answer(lang.admin_photo_send, reply_markup=back_to_adm_m(texts=lang))
    await Newsletter_photo.photo.set()
    
@dp.message_handler(IsAdmin(), content_types=['photo'], state=Newsletter_photo.photo)
async def mail_photo_starts(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_photo(chat_id=user_id, photo=data['photo'] ,caption=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()
    
@dp.message_handler(IsAdmin(), state=Newsletter.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await state.update_data(msg=msg)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_message(chat_id=user_id, text=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()
    
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_supp", state="*")
async def settings_set_sup(call: CallbackQuery):
    await AdminSettingsEdit.here_support.set()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text("<b>⚙️ Введите ссылку на пользователя (https://t.me/юзернейм)</b>"
                                 "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=back_to_adm_m(texts=lang))
    
@dp.message_handler(IsAdmin(), state=AdminSettingsEdit.here_support)
@dp.message_handler(IsAdmin(), text="-", state=AdminSettingsEdit.here_support)
async def settings_sup_set(message: Message, state: FSMContext):
    await state.finish()
    if message.text.startswith("https://t.me/") or message.text == "-":
        await db.update_settings(support=message.text)
        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил Тех. Поддержку на: \n{message.text}</b>")
        await message.answer("<b>✅ Готово! Тех. Поддержка была изменена!</b>")
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/юзернейм)</b> ")

#Прмокод
@dp.callback_query_handler(IsAdmin(), text="adm_promo", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.promo_menu, reply_markup=kb_adm_promo(texts=lang))

@dp.callback_query_handler(IsAdmin(), text="promo_create", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminCoupons.here_name_promo.set()

@dp.message_handler(IsAdmin(), state=AdminCoupons.here_name_promo)
async def here_name_promo(msg: Message, state: FSMContext):
    name = msg.text
    await msg.answer(f"<b>❗ Введите кол-во использований</b>")
    await state.update_data(cache_name_for_add_promo=name)
    await AdminCoupons.here_uses_promo.set()

@dp.message_handler(IsAdmin(), state=AdminCoupons.here_uses_promo)
async def here_uses_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await msg.answer("<b>❗ Введите сумму промокода</b>")
        await state.update_data(cache_uses_for_add_promo=int(msg.text))
        await AdminCoupons.here_discount_promo.set()
    else:
        await msg.answer("<b>❗ Кол-во использований должно быть числом!</b>")

@dp.message_handler(IsAdmin(), state=AdminCoupons.here_discount_promo)
async def here_discount_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            name = data['cache_name_for_add_promo']
            uses = data['cache_uses_for_add_promo']
        await state.finish()
        summa_promo = int(msg.text)
        await db.create_coupon(name, uses, summa_promo)
        await msg.answer(
            f"<b>✅ Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и суммой <code>{summa_promo}</code> был создан!</b>")
        await send_admins(
            f"<b>❗ Администратор  @{msg.from_user.username} создал Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и скидкой <code>{summa_promo}</code></b>")
    else:
        await msg.answer("<b>❗ Скидка должна быть числом!</b>")

@dp.callback_query_handler(IsAdmin(), text="promo_delete", state="*")
async def promo_del(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminCoupons.here_name_for_delete_promo.set()


@dp.message_handler(IsAdmin(), state=AdminCoupons.here_name_for_delete_promo)
async def promo_delete(msg: Message, state: FSMContext):
    promo = await db.get_promo(coupon=msg.text)
    if promo == None:
        await msg.answer(f"<b>❌ Промокода <code>{msg.text}</code> не существует!</b>")
    else:
        await db.delete_coupon(msg.text)
        await state.finish()
        await msg.answer(f"<b>✅ Промокод <code>{msg.text}</code> был удален</b>")
        await send_admins(f"<b>❗ Администратор  @{msg.from_user.username} удалил Промокод <code>{msg.text}</code></b>")
        
#Открытие профился из админки
@dp.callback_query_handler(IsAdmin(), text="find_user", state="*")
async def find_profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text("<b>❗ Введите ID, имя или @username пользователя</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminFind.here_user.set()
    
@dp.message_handler(IsAdmin(), state=AdminFind.here_user)
async def find_profile_op(message: Message, state: FSMContext):
    text = await get_language(message.from_user.id)
    if message.text.isdigit():
        user = await db.get_user(user_id=message.text)
    elif message.text.startswith("@"):
        user = await db.get_user(user_name=message.text.split("@")[1])
    else:
        user = await db.get_user(first_name=message.text)

    if user is None:
        await message.reply("<b>❗ Такого пользователя нет! Перепроверьте данные!</b>")
    else:
        await state.finish()
        
        name = user['user_name']
        user_id = user['user_id']
        if not name:
            us = await bot.get_chat(user_id)
            name = us.get_mention(as_html=True)
        total_refill = convert_date(user['reg_date_unix'])
        balance = user['balance']
        demo_balance = user['test_balance'] 
        lang = user['language']
        if user['is_ban'] == True:
            ban_status = '⛔ Заблокирован'
            cause_ban = f"☝ Причина блокировки: <code>{user['ban_cause']}</code>\n"
        elif user['is_ban'] == False:
            ban_status = '🟢 Разблокирован'
            cause_ban = '' 
        else:
            ban_status = "❗ Непредвиденная ошибка, обратитесь к разработчику софта"
            cause_ban = ''
        tr = None # Надо изменить
        count_refers = None # Надо изменить
        referalst_summa = None # Надо изменить
        msg = f"""<b>👤 Профиль:
                💎 Юзер: {name} 
                🆔 ID: <code>{user_id}</code>
                📅 Дата регистрации: <code>{total_refill}</code>
                
                💰 Баланс: <code>{balance}</code>
                🏦 Демо баланс: <code>{demo_balance}</code>
                
                ⚙️ Язык бота: <code>{lang}</code>
                💵 Всего пополнено: <code>{tr}</code>
                
                🔗 Статус блокировки: <code>{ban_status}</code>
                {cause_ban}
                👥 Рефералов: <code>{count_refers} чел</code>
                💎 Заработано с рефералов: <code>{referalst_summa}</code>
                📜 Список рефералов: </b>"""
        await message.answer(ded(msg), reply_markup=await admin_user_menu(texts=text, user_id=user_id))
        
@dp.callback_query_handler(IsAdmin(), text_startswith="block", state="*")
async def find_profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    text = await get_language(call.from_user.id)
    ban_or_unban = call.data.split(":")[1]
    print(ban_or_unban)
    user_id = call.data.split(":")[2]
    if ban_or_unban == 'ban':
        await call.message.answer(text.why_ban)
        await AdminBanCause.cause.set()
        await state.update_data(user_id=user_id)
    elif ban_or_unban == 'unban':
        await db.update_user(id=user_id, is_ban=False, ban_cause=None)
        user = await db.get_user(user_id=user_id)
        name = user['user_name']
        user_id = user['user_id']
        if not name:
            us = await bot.get_chat(user_id)
            name = us.get_mention(as_html=True)
        total_refill = convert_date(user['reg_date_unix'])
        balance = user['balance']
        demo_balance = user['test_balance'] 
        lang = user['language']
        if user['is_ban'] == True:
            ban_status = '⛔ Заблокирован'
            cause_ban = f"☝ Причина блокировки: <code>{user['ban_cause']}</code>\n"
        elif user['is_ban'] == False:
            ban_status = '🟢 Разблокирован'
            cause_ban = '' 
        else:
            ban_status = "❗ Непредвиденная ошибка, обратитесь к разработчику софта"
            cause_ban = ''
        tr = None # Надо изменить
        count_refers = None # Надо изменить
        referalst_summa = None # Надо изменить
        msg = f"""<b>👤 Профиль:
                💎 Юзер: {name} 
                🆔 ID: <code>{user_id}</code>
                📅 Дата регистрации: <code>{total_refill}</code>
                
                💰 Баланс: <code>{balance}</code>
                🏦 Демо баланс: <code>{demo_balance}</code>
                
                ⚙️ Язык бота: <code>{lang}</code>
                💵 Всего пополнено: <code>{tr}</code>
                
                🔗 Статус блокировки: <code>{ban_status}</code>
                {cause_ban}
                👥 Рефералов: <code>{count_refers} чел</code>
                💎 Заработано с рефералов: <code>{referalst_summa}</code>
                📜 Список рефералов: </b>"""
        await call.message.answer(ded(msg), reply_markup=await admin_user_menu(texts=text, user_id=user_id))
    
@dp.message_handler(IsAdmin(), state=AdminBanCause.cause)
async def cause_ban_edit(msg: Message, state: FSMContext):
    await state.update_data(cause=msg.text)
    data = await state.get_data()
    text = await get_language(msg.from_user.id)
    await db.update_user(data['user_id'], is_ban=True, ban_cause=data['cause'])
    user = await db.get_user(user_id=data['user_id'])
    name = user['user_name']
    user_id = user['user_id']
    if not name:
        us = await bot.get_chat(user_id)
        name = us.get_mention(as_html=True)
    total_refill = convert_date(user['reg_date_unix'])
    balance = user['balance']
    demo_balance = user['test_balance'] 
    lang = user['language']
    if user['is_ban'] == True:
        ban_status = '⛔ Заблокирован'
        cause_ban = f"☝ Причина блокировки: <code>{user['ban_cause']}</code>\n"
    elif user['is_ban'] == False:
        ban_status = '🟢 Разблокирован'
        cause_ban = '' 
    else:
        ban_status = "❗ Непредвиденная ошибка, обратитесь к разработчику софта"
        cause_ban = ''
    tr = None # Надо изменить
    count_refers = None # Надо изменить
    referalst_summa = None # Надо изменить
    msgg = f"""<b>👤 Профиль:
            💎 Юзер: {name} 
            🆔 ID: <code>{user_id}</code>
            📅 Дата регистрации: <code>{total_refill}</code>
            
            💰 Баланс: <code>{balance}</code>
            🏦 Демо баланс: <code>{demo_balance}</code>
            
            ⚙️ Язык бота: <code>{lang}</code>
            💵 Всего пополнено: <code>{tr}</code>
            
            🔗 Статус блокировки: <code>{ban_status}</code>
            {cause_ban}
            👥 Рефералов: <code>{count_refers} чел</code>
            💎 Заработано с рефералов: <code>{referalst_summa}</code>
            📜 Список рефералов: </b>"""
    await msg.answer(ded(msgg), reply_markup=await admin_user_menu(texts=text, user_id=user_id))
    
#Открытие меню доп. настроек
@dp.callback_query_handler(IsAdmin(), text="extra_settings", state="*")
async def find_profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))

@dp.callback_query_handler(IsAdmin(), text_startswith="edit_game", state="*")
async def find_game_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    en_name_game = call.data.split(":")[1]
    lang = await get_language(call.from_user.id)
    game_name = en_name_game
    game_name = func__arr_game(lang=lang, game_name=game_name)
    await call.message.answer(lang.adm_edit_game_menu.format(game_name=game_name), reply_markup=await edit_game_stats(texts=lang, game_name=en_name_game))

@dp.callback_query_handler(IsAdmin(), text_startswith="edit", state="*")
async def func_edit_game(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    param = call.data.split(":")[1]
    game = call.data.split(":")[2]
    if param == 'factor':
        await AdminGame_edit.value.set()
        await state.update_data(game=game)
        await state.update_data(param=param)
        await call.message.answer(lang.admin_edit_min_bet)
    elif param == 'min_bet':
        await AdminGame_edit.value.set()
        await state.update_data(game=game)
        await state.update_data(param=param)
        await call.message.answer(lang.admin_edit_min_bet)
    elif param == 'real_chance':
        await call.message.answer(lang.admin_edit_real_chance, reply_markup=edit_game_chance(type_dep='chance_real', game=game, texts=lang))
    elif param == 'demo_chance':
        await call.message.answer(lang.admin_edit_demo_chance, reply_markup=edit_game_chance(type_dep='chance_demo', game=game, texts=lang))

@dp.callback_query_handler(IsAdmin(), text_startswith="chance_edit", state="*")
async def func_chance_game(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    game = call.data.split(":")[1]
    param = call.data.split(":")[2]
    percent = call.data.split(":")[3]
    rus_game_name = func__arr_game(lang=lang, game_name=game)
    if param == 'chance_real':
        await db.update_game_settings(chance_real=int(percent)/100, name=game)
        await send_admins(f"<b>❗ Администратор @{call.from_user.username} изменил <code>Реальный шанс</code> в игре <code>{rus_game_name}</code> на <code>{int(percent)/100}</code>%</b>")
        await call.answer("Успешно изменено")
        await call.message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
    elif param == 'chance_demo':
        await db.update_game_settings(chance_demo=int(percent)/100, name=game)
        await send_admins(f"<b>❗ Администратор @{call.from_user.username} изменил <code>Демо шанс</code> в игре <code>{rus_game_name}</code> на <code>{int(percent)/100}</code>%</b>")
        await call.answer("Успешно изменено")
        await call.message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))

@dp.message_handler(IsAdmin(), state=AdminGame_edit.value)
async def func_edit_game_two(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    print(data)