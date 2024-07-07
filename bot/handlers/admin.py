from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import os
import asyncio

from bot.data.loader import dp, bot
from bot.data.config import lang_ru, lang_en, db
from bot.utils.utils_functions import get_language, ded, send_admins, get_admins, convert_date, func__arr_game, is_number_2, autobackup_db
from bot.filters.filters import IsAdmin
from bot.keyboards.inline import admin_menu, kb_admin_settings, back_to_adm_m, mail_types, \
                                 kb_adm_promo, admin_user_menu, edit_game_menu, edit_game_stats, \
                                 edit_game_chance, kb_edit_network, back_to_user_menu, mail_buttons_inl, \
                                 mail_buttons_current_inl, mail_buttons_type_inl, mail_buttons_edit_inl, \
                                 mail_btn, pr_buttons_inl, pr_buttons_back
                                 
from bot.state.admin import admin_main_settings, Newsletter, Newsletter_photo, AdminSettingsEdit, \
                            AdminCoupons, AdminFind, AdminBanCause, AdminGame_edit, AdminRevorkPrice, \
                            AdminPlusPrice, АdminMethod, АdminVivoCheack, АdminCheckSend, AdminMail, \
                            AdminPrButtons

#Открытие Профиля
@dp.message_handler(IsAdmin(), text=lang_ru.reply_admin, state="*")
@dp.message_handler(IsAdmin(), text=lang_en.reply_admin, state="*")
async def func__admin_menu(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    await message.answer(lang.admin_menu, reply_markup=admin_menu(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text='backup', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        await autobackup_db()
    except:
        pass
    
@dp.callback_query_handler(IsAdmin(), text='settings', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(lang.admin_settings, reply_markup=await kb_admin_settings(texts=lang))
    
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
    
@dp.callback_query_handler(IsAdmin(), text_startswith="work:on_off", state="*")
async def settings_vkl_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    s = await db.get_only_settings()
    status_work = s['is_work']

    if status_work == "True":
        await db.update_settings(is_work="False")
    if status_work == "False":
        await db.update_settings(is_work="True")

    lang = await get_language(call.from_user.id)
    await call.message.edit_text(lang.admin_settings, reply_markup=await kb_admin_settings(texts=lang))
    
#Статистика 
@dp.callback_query_handler(IsAdmin(), text='stats', state="*")
async def open_stats(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    all_user, show_users_week, show_users_day = 0, 0, 0
    all_users = await db.all_users()
    settings = await db.get_only_settings()
    admin_count = len(get_admins())
    slots_info = await db.get_game_settings(name='slots')
    coin_info = await db.get_game_settings(name='coin')
    basketball_info = await db.get_game_settings(name='basketball')
    football_info = await db.get_game_settings(name='football')
    darts_info = await db.get_game_settings(name='darts')
    bowling_info = await db.get_game_settings(name='bowling')
    dice_info = await db.get_game_settings(name='dice')
    all_deposits = await db.all_deposit()
    summ_deposits = 0
    summ_games = 0
    summ_slots = 0
    summ_basketball = 0
    summ_darts = 0
    summ_bowling = 0
    summ_football = 0
    summ_dice = 0
    summ_coin = 0
    for row in all_deposits:
        summ_deposits += float(row['total_pay'])
        
    for user in all_users:
        if int(user['reg_date_unix']) - int(settings['profit_day']) >= 0:
            show_users_day += 1

        if int(user['reg_date_unix']) - int(settings['profit_week']) >= 0:
            show_users_week += 1
        all_user += 1
        summ_games += int(user['amount_all_games'])
        summ_slots += int(user['amount_slots'])
        summ_dice += int(user['amount_dice'])
        summ_basketball += int(user['amount_basketball'])
        summ_darts += int(user['amount_darts'])
        summ_bowling += int(user['amount_bowling'])
        summ_football += int(user['amount_football'])
        summ_coin += int(user['amount_coin'])

    msg = f"""📊 Статистика

    <b>👥 Пользователи:</b>
    ♾️ Всего пользователей: <code>{all_user}</code> чел.
    📅 За неделю: <code>{show_users_week}</code> чел.
    ⌛ За день: <code>{show_users_day}</code> чел.

    <b>Всего пополненно:</b> <code>{round(float(summ_deposits), 2)}</code> 💎

    <b>Игры:</b>

    <b>Всего сыграно игр:</b> <code>{summ_games}</code>
    
    <b>🎰 Слоты:</b>
    Коэффициент: <code>X{slots_info['factor']}</code>
    Мин. ставка: ₽ <code>{slots_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_slots}</code>
    
    <b>🎲 Кости:</b>
    Коэффициент: <code>X{dice_info['factor']}</code>
    Мин. ставка: ₽ <code>{dice_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_dice}</code>

    <b>🏀 Баскетбол:</b>
    Коэффициент: <code>X{basketball_info['factor']}</code>
    Мин. ставка: ₽ <code>{basketball_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_basketball}</code>

    <b>🎳 Боулинг:</b>
    Коэффициент: <code>X{bowling_info['factor']}</code>
    Мин. ставка: ₽ <code>{bowling_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_bowling}</code>

    <b>⚽ Футбол:</b>
    Коэффициент: <code>X{football_info['factor']}</code>
    Мин. ставка: ₽ <code>{football_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_football}</code>
    
    <b>🎯 Дартс:</b>
    Коэффициент: <code>X{darts_info['factor']}</code>
    Мин. ставка: ₽ <code>{darts_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_darts}</code>

    <b>🪙 Монетка:</b>
    Коэффициент: <code>X{coin_info['factor']}</code>
    Мин. ставка: ₽ <code>{coin_info['min_bet']}</code>
    Всего сыграно игр: <code>{summ_coin}</code>
    Шанс победы: <code>{float(coin_info['chance_real'])*100}</code>%
    Демо шанс: <code>{float(coin_info['chance_demo'])*100}</code>%

    <b>👨‍💻 Администраторы:</b> {admin_count}\n"""
    for admin in get_admins():
        try:
            user = await db.get_user(user_id=admin)
            msg += f"@{user['user_name']}\n "
        except:
            msg += f"{admin}\n"
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
    
@dp.message_handler(IsAdmin(), content_types=['photo', 'video', 'animation'], state=Newsletter_photo.photo)
async def mail_photo_starts(message: Message, state: FSMContext):
    if message.photo:
        media = message.photo[-1].file_id
        media_type = 'photo'
    elif message.video:
        media = message.video.file_id
        media_type = 'video'
    elif message.animation:
        media = message.animation.file_id
        media_type = 'animation'

    await state.update_data(media=media, media_type=media_type)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            if data['media_type'] == 'photo':
                await bot.send_photo(chat_id=user_id, photo=data['media'], caption=data.get('msg', ''), reply_markup=await mail_btn())
            elif data['media_type'] == 'video':
                await bot.send_video(chat_id=user_id, video=data['media'], caption=data.get('msg', ''), reply_markup=await mail_btn())
            elif data['media_type'] == 'animation':
                await bot.send_animation(chat_id=user_id, animation=data['media'], caption=data.get('msg', ''), reply_markup=await mail_btn())
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
            await bot.send_message(chat_id=user_id, 
                                   text=data['msg'], reply_markup=await mail_btn())
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
        balance = round(float(user['balance']), 2)
        demo_balance = round(float(user['test_balance']), 2) 
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
        msgg = ded(text.admin_open_profile.format(name=name,
                                                user_id=user_id,
                                                total_refill=total_refill,
                                                balance=balance,
                                                demo_balance=round(float(demo_balance), 2),
                                                lang=lang,
                                                tr=round(float(user['total_pay']), 2),
                                                ban_status=ban_status,
                                                cause_ban=cause_ban,
                                                count_refers=user['ref_count'],
                                                vivod=user['vivod'],
                                                amount_all_games=user['amount_all_games'],
                                                amount_slots=user['amount_slots'],
                                                amount_dice=user['amount_dice'],
                                                amount_basketball=user['amount_basketball'],
                                                amount_bowling=user['amount_bowling'],
                                                amount_football=user['amount_football'],
                                                amount_coin=user['amount_coin'],
                                                amount_darts=user['amount_darts'],
                                                referalst_summa=round(float(user['total_refill']), 2)))
        referal_list = await db.get_userAll(ref_id=user_id)
        for refik in referal_list:
            user = await db.get_user(user_id=int(refik['user_id']))
            name = f"@{user['user_name']}"
            if user['user_name'] == "":
                us = await bot.get_chat(user['user_id'])
                name = us.get_mention(as_html=True)
            msgg += f"{name}\n "
        await message.answer(msgg, reply_markup=await admin_user_menu(texts=text, 
                                                                      user_id=user_id))

#Открытие чека из админки
@dp.callback_query_handler(IsAdmin(), text="find_check", state="*")
async def find_check_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text("<b>❗ Введите номер чека 🧾</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminFind.here_check.set()
    
@dp.message_handler(IsAdmin(), state=AdminFind.here_check)
async def find_profile_op(message: Message, state: FSMContext):
    text = await get_language(message.from_user.id)
    if message.text.isdigit():
        check_info = await db.get_check(unix=message.text)
        if check_info:
            check_type = 'Пополнение' if check_info['transaction_type'] == 'deposit' else 'Вывод'
            if check_info['transaction_type'] == 'deposit':
                await message.answer(ded(f"""
                                        🧾 Информаци о чеке: <code>{check_info['unix']}</code>
                                        
                                        🆔 ID: <code>{check_info['id']}</code>
                                        👑 Пользователь: <code>{check_info['user_id']}</code>
                                        ⭐️ Тип: <code>{check_type}</code>
                                        💰 Сумма: <code>{check_info['summa']}</code>
                                        """))
            else:
                withdrawal_info = await db.get_vivod(id=check_info['conclusion_id'])
                status_vivod = 'Отменено' if withdrawal_info['status'] == 'canceled' else 'Принят'
                adress = 'Чек' if withdrawal_info['network'] == 'NULL' and withdrawal_info['adress'] == 'NULL' else withdrawal_info['adress']
                network = withdrawal_info['network'] if withdrawal_info['network'] != 'NULL' else ''
                
                await message.answer(ded(f"""
                                        🧾 Информаци о чеке: <code>{check_info['unix']} </code>
                                        
                                        🆔 ID: <code>{check_info['id']}</code>
                                        👑 Пользователь: <code>{withdrawal_info['user_id']}</code>
                                        ⭐️ Тип: <code>{check_type}</code>
                                        💰 Сумма: <code>{check_info['summa']}</code>
                                        
                                        💸 Информация о выводе: 
                                        🆔 ID: <code>{withdrawal_info['id']}</code>
                                        📅 Дата: <code>{withdrawal_info['data']}</code>
                                        🌸 Статус: <code>{status_vivod}</code>
                                        📬 Адресс: <code>{adress}</code>
                                        <code>{network}</code>
                                        """))
            await state.finish()
        else:
            await message.answer("Чек не найден")
            await state.finish()
    else:
        await message.answer("Неверный формат чека")
        await state.finish()

@dp.callback_query_handler(IsAdmin(), text_startswith="block", state="*")
async def find_profile_open(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    text = await get_language(call.from_user.id)
    ban_or_unban = call.data.split(":")[1]
    user_id = call.data.split(":")[2]
    if ban_or_unban == 'ban':
        await call.message.answer(text.why_ban)
        await AdminBanCause.cause.set()
        await state.update_data(user_id=user_id)
    elif ban_or_unban == 'unban':
        await db.update_user(id=user_id, 
                             is_ban=False, 
                             ban_cause=None)
        user = await db.get_user(user_id=user_id)
        name = user['user_name']
        user_id = user['user_id']
        if not name:
            us = await bot.get_chat(user_id)
            name = us.get_mention(as_html=True)
        total_refill = convert_date(user['reg_date_unix'])
        balance = round(float(user['balance']), 2)
        demo_balance = round(float(user['test_balance']), 2) 
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
        msgg = ded(text.admin_open_profile.format(name=name,
                                                  user_id=user_id,
                                                  total_refill=total_refill,
                                                  balance=balance,
                                                  demo_balance=round(float(demo_balance), 2),
                                                  lang=lang,
                                                  tr=round(float(user['total_pay']), 2),
                                                  ban_status=ban_status,
                                                  cause_ban=cause_ban,
                                                  count_refers=user['ref_count'],
                                                  vivod=user['vivod'],
                                                  amount_all_games=user['amount_all_games'],
                                                  amount_slots=user['amount_slots'],
                                                  amount_dice=user['amount_dice'],
                                                  amount_basketball=user['amount_basketball'],
                                                  amount_bowling=user['amount_bowling'],
                                                  amount_football=user['amount_football'],
                                                  amount_coin=user['amount_coin'],
                                                  amount_darts=user['amount_darts'],
                                                  referalst_summa=round(float(user['total_refill']), 2)))
        referal_list = await db.get_userAll(ref_id=user_id)
        for refik in referal_list:
            user = await db.get_user(user_id=int(refik['user_id']))
            name = f"@{user['user_name']}"
            if user['user_name'] == "":
                us = await bot.get_chat(user['user_id'])
                name = us.get_mention(as_html=True)
            msgg += f"{name}\n "
        await call.answer(msgg, reply_markup=await admin_user_menu(texts=text, 
                                                                   user_id=user_id))
        
@dp.message_handler(IsAdmin(), state=AdminBanCause.cause)
async def cause_ban_edit(msg: Message, state: FSMContext):
    await state.update_data(cause=msg.text)
    data = await state.get_data()
    text = await get_language(msg.from_user.id)
    await db.update_user(data['user_id'], 
                         is_ban=True, 
                         ban_cause=data['cause'])
    user = await db.get_user(user_id=data['user_id'])
    name = user['user_name']
    user_id = user['user_id']
    if not name:
        us = await bot.get_chat(user_id)
        name = us.get_mention(as_html=True)
    total_refill = convert_date(user['reg_date_unix'])
    balance = round(float(user['balance']), 2)
    demo_balance = round(float(user['test_balance']), 2) 
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
    msgg = ded(text.admin_open_profile.format(name=name,
                                              user_id=user_id,
                                              total_refill=total_refill,
                                              balance=balance,
                                              demo_balance=round(float(demo_balance), 2),
                                              lang=lang,
                                              tr=round(float(user['total_pay']), 2),
                                              ban_status=ban_status,
                                              cause_ban=cause_ban,
                                              count_refers=user['ref_count'],
                                              vivod=user['vivod'],
                                              amount_all_games=user['amount_all_games'],
                                              amount_slots=user['amount_slots'],
                                              amount_dice=user['amount_dice'],
                                              amount_basketball=user['amount_basketball'],
                                              amount_bowling=user['amount_bowling'],
                                              amount_football=user['amount_football'],
                                              amount_coin=user['amount_coin'],
                                              amount_darts=user['amount_darts'],
                                              referalst_summa=round(float(user['total_refill']), 2)))
    referal_list = await db.get_userAll(ref_id=user_id)
    for refik in referal_list:
        user = await db.get_user(user_id=int(refik['user_id']))
        name = f"@{user['user_name']}"
        if user['user_name'] == "":
            us = await bot.get_chat(user['user_id'])
            name = us.get_mention(as_html=True)
        msgg += f"{name}\n "
    await msg.answer(msgg, reply_markup=await admin_user_menu(texts=text, 
                                                              user_id=user_id))

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
    game_name = func__arr_game(lang=lang, 
                               game_name=game_name)
    await call.message.answer(lang.adm_edit_game_menu.format(game_name=game_name), reply_markup=await edit_game_stats(texts=lang, 
                                                                                                                      game_name=en_name_game))

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
        await call.message.answer(lang.admin_edit_factor)
    elif param == 'min_bet':
        await AdminGame_edit.value.set()
        await state.update_data(game=game)
        await state.update_data(param=param)
        await call.message.answer(lang.admin_edit_min_bet)
    elif param == 'real_chance':
        await call.message.answer(lang.admin_edit_real_chance, reply_markup=edit_game_chance(type_dep='chance_real', 
                                                                                             game=game, 
                                                                                             texts=lang))
    elif param == 'demo_chance':
        await call.message.answer(lang.admin_edit_demo_chance, reply_markup=edit_game_chance(type_dep='chance_demo',
                                                                                             game=game, 
                                                                                             texts=lang))

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
        await db.update_game_settings(chance_real=int(percent)/100, 
                                      name=game)
        await send_admins(f"<b>❗ Администратор @{call.from_user.username} изменил <code>Реальный шанс</code> в игре <code>{rus_game_name}</code> на <code>{int(percent)/100}</code>%</b>")
        await call.answer("Успешно изменено")
        await call.message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
    elif param == 'chance_demo':
        await db.update_game_settings(chance_demo=int(percent)/100, 
                                      name=game)
        await send_admins(f"<b>❗ Администратор @{call.from_user.username} изменил <code>Демо шанс</code> в игре <code>{rus_game_name}</code> на <code>{int(percent)/100}</code>%</b>")
        await call.answer("Успешно изменено")
        await call.message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
    await state.finish()

@dp.message_handler(IsAdmin(), state=AdminGame_edit.value)
async def func_edit_game_two(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number_2(message.text) == True:
        await state.update_data(value=message.text)
        data = await state.get_data()
        russian_game = func__arr_game(lang=lang, game_name=data['game'])
        if data['param'] == 'factor':
            await db.update_game_settings(factor=data['value'], 
                                          name=data['game'])
            await send_admins(f"<b>❗ Администратор @{message.from_user.username} изменил <code>Коэффициент</code> в игре <code>{russian_game}</code> на <code>X{data['value']}</code></b>")
            await message.answer("Успешно изменено")
            await message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
        elif data['param'] == 'min_bet':
            await db.update_game_settings(min_bet=data['value'], 
                                          name=data['game'])
            await send_admins(f"<b>❗ Администратор @{message.from_user.username} изменил <code>Минимальную ставку</code> в игре <code>{russian_game}</code> на <code>{data['value']}</code>🪙</b>")
            await message.answer("Успешно изменено")
            await message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
    else:
        await message.answer(lang.need_number)
    await state.finish()

#Реворк баланса/демо баланса      
@dp.callback_query_handler(IsAdmin(), text_startswith="revork", state="*")
async def func_editit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    type = call.data.split(":")[1]
    user_id = call.data.split(":")[2]
    await call.message.answer(lang.wright_summ)
    await AdminRevorkPrice.summa.set()
    await state.update_data(type=type, 
                            user_id=user_id)
    
@dp.message_handler(IsAdmin(), state=AdminRevorkPrice.summa)
async def func_edit_game_two(message: Message, state: FSMContext):
    texts = await get_language(message.from_user.id)
    if is_number_2(message.text) == True:
        data = await state.get_data()
        if data['type'] == 'balance':
            await db.update_user(id=data['user_id'], 
                                 balance=int(message.text))
        elif data['type'] == 'demo':
            await db.update_user(id=data['user_id'], 
                                 test_balance=int(message.text))
        await message.answer("Успешно")
        user = await db.get_user(user_id=data['user_id'])
        name = user['user_name']
        user_id = user['user_id']
        if not name:
            us = await bot.get_chat(user_id)
            name = us.get_mention(as_html=True)
        total_refill = convert_date(user['reg_date_unix'])
        balance = round(float(user['balance']), 2)
        demo_balance = round(float(user['test_balance']), 2) 
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
        await message.answer(ded(texts.admin_open_profile.format(name=name,
                                                                 user_id=user_id,
                                                                 total_refill=total_refill,
                                                                 balance=balance,
                                                                 demo_balance=round(float(demo_balance), 2),
                                                                 lang=lang,
                                                                 tr=round(float(user['total_pay']), 2),
                                                                 ban_status=ban_status,
                                                                 cause_ban=cause_ban,
                                                                 count_refers=user['ref_count'],
                                                                 vivod=user['vivod'],
                                                                 amount_all_games=user['amount_all_games'],
                                                                 amount_slots=user['amount_slots'],
                                                                 amount_dice=user['amount_dice'],
                                                                 amount_basketball=user['amount_basketball'],
                                                                 amount_bowling=user['amount_bowling'],
                                                                 amount_football=user['amount_football'],
                                                                 amount_coin=user['amount_coin'],
                                                                 amount_darts=user['amount_darts'],
                                                                 referalst_summa=round(float(user['total_refill']), 2))), reply_markup=await admin_user_menu(texts=texts, 
                                                                                                                                                             user_id=user_id))
        await state.finish()
    else:
        await message.answer(texts.need_number)

#Выдача баланса/демо баланса
@dp.callback_query_handler(IsAdmin(), text_startswith="give", state="*")
async def func_editit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    type = call.data.split(":")[1]
    user_id = call.data.split(":")[2]
    await call.message.answer(lang.wright_summ)
    await AdminPlusPrice.summa.set()
    await state.update_data(type=type, user_id=user_id)
    
@dp.message_handler(IsAdmin(), state=AdminPlusPrice.summa)
async def func_edit_game_two(message: Message, state: FSMContext):
    texts = await get_language(message.from_user.id)
    if is_number_2(message.text) == True:
        data = await state.get_data()
        user = await db.get_user(user_id=data['user_id'])
        if data['type'] == 'balance':
            await db.update_user(id=data['user_id'], 
                                 balance=int(user['balance'])+int(message.text))
        elif data['type'] == 'demo':
            await db.update_user(id=data['user_id'], 
                                 test_balance=int(user['test_balance'])+int(message.text))
        await message.answer("Успешно")
        user = await db.get_user(user_id=data['user_id'])
        name = user['user_name']
        user_id = user['user_id']
        if not name:
            us = await bot.get_chat(user_id)
            name = us.get_mention(as_html=True)
        total_refill = convert_date(user['reg_date_unix'])
        balance = round(float(user['balance']), 2)
        demo_balance = round(float(user['test_balance']), 2) 
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
        await message.answer(ded(texts.admin_open_profile.format(name=name,
                                                                 user_id=user_id,
                                                                 total_refill=total_refill,
                                                                 balance=balance,
                                                                 demo_balance=round(float(demo_balance), 2),
                                                                 lang=lang,
                                                                 tr=round(float(user['total_pay']), 2),
                                                                 ban_status=ban_status,
                                                                 cause_ban=cause_ban,
                                                                 count_refers=user['ref_count'],
                                                                 vivod=user['vivod'],
                                                                 amount_all_games=user['amount_all_games'],
                                                                 amount_slots=user['amount_slots'],
                                                                 amount_dice=user['amount_dice'],
                                                                 amount_basketball=user['amount_basketball'],
                                                                 amount_bowling=user['amount_bowling'],
                                                                 amount_football=user['amount_football'],
                                                                 amount_coin=user['amount_coin'],
                                                                 amount_darts=user['amount_darts'],
                                                                 referalst_summa=round(float(user['total_refill']), 2))), reply_markup=await admin_user_menu(texts=texts, 
                                                                                                                                                             user_id=user_id))
        await state.finish()
    else:
        await message.answer(texts.need_number)

#Рефералка
@dp.callback_query_handler(text_startswith="ref_lvl_edit:", state="*")
async def ref_lvl_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()

    lvl = call.data.split(":")[1]

    await call.message.edit_text(f"<b>❗ Введите кол-во рефералов для {lvl} уровня</b>")
    await state.update_data(cache_lvl_for_edit_lvls=lvl)
    await AdminSettingsEdit.here_count_lvl_ref.set()
    
@dp.message_handler(state=AdminSettingsEdit.here_count_lvl_ref)
async def here_count_lvl_ref(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if message.text.isdigit():
        async with state.proxy() as data:
            lvl = data['cache_lvl_for_edit_lvls']
        count = int(message.text)

        if lvl == "1":
            await db.update_settings(ref_lvl_1=count)
        elif lvl == "2":
            await db.update_settings(ref_lvl_2=count)
        else:
            await db.update_settings(ref_lvl_3=count)

        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил кол-во рефералов для <code>{lvl}</code> уровня на <code>{count} чел</code></b>")
        await message.answer(
            f"<b>✅ Вы изменили кол-во рефералов для <code>{lvl}</code> уровня на <code>{count} чел</code></b>", reply_markup=back_to_adm_m(texts=lang))
        
@dp.callback_query_handler(IsAdmin(), text_startswith="ref_percent:edit:", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    await state.update_data(cache_ref_lvl_to_edit_percent=call.data.split(":")[2])
    await AdminSettingsEdit.here_ref_percent.set()
    await call.message.edit_text(f"<b>⚙️ Введите новый процент для {call.data.split(':')[2]} реферального уровня:</b>")
    
@dp.message_handler(IsAdmin(), state=AdminSettingsEdit.here_ref_percent)
async def settings_ref_per_set(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    async with state.proxy() as data:
        lvl = data['cache_ref_lvl_to_edit_percent']

    await state.finish()

    if not message.text.isdigit():
        return await message.answer("<b>❌ Введите число!</b>")

    if lvl == "1":
        await db.update_settings(ref_percent_1=int(message.text))
    elif lvl == "2":
        await db.update_settings(ref_percent_2=int(message.text))
    elif lvl == "3":
        await db.update_settings(ref_percent_3=int(message.text))

    await send_admins(
        f"<b>❗ Администратор  @{message.from_user.username} изменил процент для {lvl} реферального уровня на: \n{message.text}</b>")
    await message.answer(f"<b>✅ Готово! Процент для {lvl} реферального уровня изменен!</b>", reply_markup=back_to_adm_m(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text="comma_network", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer("Выберите сеть для изменения: ", reply_markup=await kb_edit_network(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text="MinimumSumma", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f"Введите минимальную сумма для вывода чеком")
    await АdminVivoCheack.percent.set()
    
@dp.message_handler(IsAdmin(), state=АdminVivoCheack.percent)
async def settings_ref_per_set(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number_2(message.text):
        await state.update_data(percent=message.text)
        data = await state.get_data()
        await db.update_settings(Minimum_check=data['percent'])
        await message.answer("Минимальная сумма успешно установлена")
        await state.finish()
    else: 
        await message.answer(lang.need_number)
    
@dp.callback_query_handler(IsAdmin(), text_startswith="send_check", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    lang = await get_language(call.from_user.id)
    await call.message.answer("Перешлите чек для отправки пользователю", reply_markup=back_to_user_menu(lang))
    await АdminCheckSend.check.set()
    await state.update_data(user_id=user_id)
    
@dp.message_handler(IsAdmin(), state=АdminCheckSend.check)
async def settings_ref_per_set(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.send_message(user_id, message.text)
    await state.finish()
    
@dp.callback_query_handler(IsAdmin(), text_startswith="new_Edit_network", state="*")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    method = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer(f"Введите комиссию для {method}")
    await АdminMethod.percent.set()
    await state.update_data(method=method)
    
@dp.message_handler(IsAdmin(), state=АdminMethod.percent)
async def settings_ref_per_set(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number_2(message.text):
        await state.update_data(percent=message.text)
        data = await state.get_data()
        if data['method'] == 'TON':
            await db.update_settings(id=1, Commission_TON=data['percent'])
        elif data['method'] == 'TRC20':
            await db.update_settings(id=1, Commission_TRC20=data['percent'])
        elif data['method'] == 'ERC20':
            await db.update_settings(id=1, Commission_ERC20=data['percent'])
        elif data['method'] == 'BER20':
            await db.update_settings(id=1, CommissionBER20=data['percent'])
        elif data['method'] == 'check':
            await db.update_settings(id=1, Commission_check=data['percent'])
        await message.answer("Успешно измененно!")
        await state.finish()
    else: 
        await message.answer(lang.need_number)
    
#Кнопки в рассылке
@dp.callback_query_handler(IsAdmin(), text='mail_buttons', state='*')
async def mail_buttons(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Настройки', reply_markup=mail_buttons_inl())
    
@dp.callback_query_handler(IsAdmin(), text_startswith='mail_buttons:', state='*')
async def mail_buttons_(call: CallbackQuery, state: FSMContext):
    await state.finish()

    action = call.data.split(":")[1]

    if action == 'add':
        await call.message.edit_text('<b>❗ Введите название кнопки:</b>')
        await AdminMail.here_name_for_add_mail_button.set()
    elif action == 'current':
        if len(await db.get_all_mail_buttons()) > 0:
            await call.message.edit_text('<b>❗ Выберите кнопку:</b>', reply_markup=await mail_buttons_current_inl())
        else:
            await call.answer('❗ На данный момент кнопок нет!')
            
@dp.message_handler(IsAdmin(), state=AdminMail.here_name_for_add_mail_button)
async def mail_buttons__(msg: Message, state: FSMContext):
    await state.finish()

    async with state.proxy() as data:
        data['name_mail_btn'] = msg.text

    await msg.reply('<b>❗ Выберите тип кнопки:</b>', reply_markup=mail_buttons_type_inl())
    
@dp.callback_query_handler(IsAdmin(), text_startswith="add_mail_buttons:", state='*')
async def mail_buttons_(call: CallbackQuery):

    typ = call.data.split(":")[1]

    if typ == 'link':
        await call.message.edit_text('<b>❗ Введите ссылку:</b>')
        await AdminMail.here_link_for_add_mail_button.set()
    # elif typ == 'profile':
        
@dp.message_handler(state=AdminMail.here_link_for_add_mail_button)
async def __mail_buttons__(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name_mail_btn']

    if 'http://' in msg.text or 'https://' in msg.text:
        try:
            await db.create_mail_button(name, f'link|{msg.text}')
        except BaseException as err:
            print(err)

        await msg.reply('<b>✅ Успешно!</b>')
        await state.finish()
    else:
        await msg.reply("Введите ссылку!")
        
@dp.callback_query_handler(IsAdmin(), text_startswith='butedit_mail_button:', state='*')
async def edit_mail_button(call: CallbackQuery, state: FSMContext):
    await state.finish()

    btn_id = call.data.split(":")[1]
    btn = await db.get_mail_button(btn_id)

    await call.message.edit_text(f"<b>✨ Кнопка: {btn['name']}</b>", reply_markup=mail_buttons_edit_inl(btn_id))
    
@dp.callback_query_handler(IsAdmin(), text_startswith='butedits_mail_btn:', state='*')
async def edits_mail_btn(call: CallbackQuery, state: FSMContext):
    await state.finish()

    action = call.data.split(":")[1]
    btn_id = call.data.split(":")[2]

    async with state.proxy() as data:
        data['btn_id'] = btn_id

    if action == 'edit_name':
        await call.message.edit_text('<b>❗ Введите новое название для кнопки:</b>')
        await AdminMail.here_new_name_for_mail_button.set()
    elif action == 'del':
        await db.delete_mail_button(btn_id)
        if len(await db.get_all_mail_buttons()) > 0:
            await call.message.edit_text('<b>❗ Выберите кнопку:</b>', reply_markup=await mail_buttons_current_inl())
        else:
            await call.message.edit_text('Настройки', reply_markup=mail_buttons_inl())
            
@dp.message_handler(IsAdmin(), state=AdminMail.here_new_name_for_mail_button)
async def here_new_name_for_mail_button(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        btn_id = data['btn_id']

    await state.finish()
    await db.update_mail_button(btn_id, name=msg.text)
    await msg.reply("<b>✅ Успешно!</b>")
    if len(await db.get_all_mail_buttons()) > 0:
        await msg.answer('<b>❗ Выберите кнопку:</b>', reply_markup=await mail_buttons_current_inl())
    else:
        await msg.answer('Настройки', reply_markup=mail_buttons_inl())
        
@dp.callback_query_handler(text='pr_buttons', state='*')
async def pr_buttons(c: CallbackQuery, state: FSMContext):
    await state.finish()

    await c.message.edit_text(f'<b>❗ Выберите действие:</b>', reply_markup=pr_buttons_inl())
    
@dp.callback_query_handler(text_startswith='pr_button:', state='*')
async def pr_buttons2(c: CallbackQuery, state: FSMContext):
    await state.finish()
    if c.data.split(':')[1] == 'create':
        await c.message.edit_text(f'<b>❗ Введите название кнопки:</b>', reply_markup=pr_buttons_back())
        await AdminPrButtons.here_name_pr_button_create.set()
    elif c.data.split(':')[1] == 'delete':
        await c.message.edit_text(f'<b>❗ Введите название кнопки:</b>', reply_markup=pr_buttons_back())
        await AdminPrButtons.here_name_pr_button_delete.set()


@dp.message_handler(state=AdminPrButtons.here_name_pr_button_create)
async def pr_buttons3(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_pr_button_create'] = msg.text

    await msg.reply('<b>❗ Теперь введи текст кнопки: \n❗Можно использовать Telegram Разметку</b> ')
    await AdminPrButtons.here_txt_pr_button_create.set()


@dp.message_handler(state=AdminPrButtons.here_txt_pr_button_create)
async def pr_buttons4(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['txt_pr_button_create'] = msg.parse_entities(as_html=True)
    await msg.reply('<b>❗ Теперь отправь фото кнопки: \n'
                    '❗ Если не хотите, чтоб было фото, отправьте <code>-</code></b>')
    await AdminPrButtons.here_photo_pr_button_create.set()


@dp.message_handler(state=AdminPrButtons.here_photo_pr_button_create, content_types=['photo'])
@dp.message_handler(state=AdminPrButtons.here_photo_pr_button_create, text='-')
async def pr_buttons5(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name_pr_button_create']
        txt = data['txt_pr_button_create']
    await state.finish()
    try:
        photo = msg.photo[-1].file_id
    except:
        photo = msg.text

    await db.create_pr_button(name, txt, photo)
    await msg.reply('<b>✅ Кнопка успешно создана!</b>')


@dp.message_handler(state=AdminPrButtons.here_name_pr_button_delete)
async def pr_buttons6(msg: Message, state: FSMContext):
    await state.finish()
    try:
        await db.delete_pr_button(msg.text)
        await msg.reply('<b>✅ Кнопка успешно удалена!</b>')
    except Exception as err:
        await msg.reply(f'<b>❗ Произошла ошибка при удалении кнопки: {err}</b>')