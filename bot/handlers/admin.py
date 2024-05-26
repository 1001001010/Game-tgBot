from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 

from bot.data.loader import dp, bot
from bot.data.config import lang_ru, lang_en, db
from bot.utils.utils_functions import get_language, ded, send_admins, get_admins, convert_date, func__arr_game, is_number
from bot.filters.filters import IsAdmin
from bot.keyboards.inline import admin_menu, kb_admin_settings, back_to_adm_m, mail_types, \
                                 kb_adm_promo, admin_user_menu, edit_game_menu, edit_game_stats, \
                                 edit_game_chance, kb_edit_network
                                 
from bot.state.admin import admin_main_settings, Newsletter, Newsletter_photo, AdminSettingsEdit, \
                            AdminCoupons, AdminFind, AdminBanCause, AdminGame_edit, AdminRevorkPrice, \
                            AdminPlusPrice, АdminMethod

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
    bowling_info = await db.get_game_settings(name='bowling')
    dice_info = await db.get_game_settings(name='dice')
    all_deposits = await db.all_deposit()
    summ_deposits = 0
    for row in all_deposits:
        summ_deposits += float(row['total_pay'])
        
    for user in all_users:
        if int(user['reg_date_unix']) - int(settings['profit_day']) >= 0:
            show_users_day += 1

        if int(user['reg_date_unix']) - int(settings['profit_week']) >= 0:
            show_users_week += 1
        all_user += 1

    msg = f"""📊 Статистика
    
    <b>Пользователи:</b>
    👥 Всего пользователей: <code>{all_user}</code>  чел.
    👥 Ползователей за неделю <code>{show_users_week}</code>  чел.
    👥 Пользователей за день <code>{show_users_day}</code>  чел.
        
    <b>Всего пополненно:</b> <code>{summ_deposits}</code> 💎
    
    <b>Игры:</b>
    🎰 Слоты: 
    ╠🧮 Коэффициент: <code>X{slots_info['factor']}</code> 
    ╚💰 Мин. ставка: <code>{slots_info['min_bet']}</code>🪙 
    
    🎲 Кости: 
    ╠🧮 Коэффициент: <code>X{dice_info['factor']}</code> 
    ╚💰 Мин. ставка: <code>{dice_info['min_bet']}</code>🪙 
    
    🏀 Баскетбол:
    ╠🧮 Коэффициент: <code>X{basketball_info['factor']}</code> 
    ╚💰 Мин. ставка: <code>{basketball_info['min_bet']}</code>🪙 
    
    🎳 Боулинг:
    ╠🧮 Коэффициент: <code>X{bowling_info['factor']}</code> 
    ╚💰 Мин. ставка: <code>{bowling_info['min_bet']}</code>🪙 
    
    ⚽ Футбол:
    ╠🧮 Коэффициент: <code>X{football_info['factor']}</code> 
    ╚💰 Мин. ставка: <code>{football_info['min_bet']}</code>🪙 
    
    🪙 Монетка:
    ╠🧮 Коэффициент: <code>X{coin_info['factor']}</code> 
    ╠💰 Мин. ставка: <code>{coin_info['min_bet']}</code>🪙 
    ╠📈 Шанс победы: <code>{int(coin_info['chance_real'])*100}</code>% 
    ╚📉 Демо шанс: <code>{int(coin_info['chance_demo'])*100}</code>%

    👨‍💻 Всего администраторов: {admin_count}\n"""
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
        msgg = ded(text.admin_open_profile.format(name=name,
                                                user_id=user_id,
                                                total_refill=total_refill,
                                                balance=balance,
                                                demo_balance=demo_balance,
                                                lang=lang,
                                                tr=user['total_pay'],
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
                                                referalst_summa=user['total_refill']))
        referal_list = await db.get_userAll(ref_id=user_id)
        for refik in referal_list:
            user = await db.get_user(user_id=int(refik['user_id']))
            name = f"@{user['user_name']}"
            if user['user_name'] == "":
                us = await bot.get_chat(user['user_id'])
                name = us.get_mention(as_html=True)
            msgg += f"{name}\n "
        await message.answer(msgg, reply_markup=await admin_user_menu(texts=text, user_id=user_id))
        
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
        msgg = ded(text.admin_open_profile.format(name=name,
                                                user_id=user_id,
                                                total_refill=total_refill,
                                                balance=balance,
                                                demo_balance=demo_balance,
                                                lang=lang,
                                                tr=user['total_pay'],
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
                                                referalst_summa=user['total_refill']))
        referal_list = await db.get_userAll(ref_id=user_id)
        for refik in referal_list:
            user = await db.get_user(user_id=int(refik['user_id']))
            name = f"@{user['user_name']}"
            if user['user_name'] == "":
                us = await bot.get_chat(user['user_id'])
                name = us.get_mention(as_html=True)
            msgg += f"{name}\n "
        await call.answer(msgg, reply_markup=await admin_user_menu(texts=text, user_id=user_id))
        
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
    msgg = ded(text.admin_open_profile.format(name=name,
                                            user_id=user_id,
                                            total_refill=total_refill,
                                            balance=balance,
                                            demo_balance=demo_balance,
                                            lang=lang,
                                            tr=user['total_pay'],
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
                                            referalst_summa=user['total_refill']))
    referal_list = await db.get_userAll(ref_id=user_id)
    for refik in referal_list:
        user = await db.get_user(user_id=int(refik['user_id']))
        name = f"@{user['user_name']}"
        if user['user_name'] == "":
            us = await bot.get_chat(user['user_id'])
            name = us.get_mention(as_html=True)
        msgg += f"{name}\n "
    await msg.answer(msgg, reply_markup=await admin_user_menu(texts=text, user_id=user_id))

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
        await call.message.answer(lang.admin_edit_factor)
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
    await state.finish()

@dp.message_handler(IsAdmin(), state=AdminGame_edit.value)
async def func_edit_game_two(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number(message.text) == True:
        await state.update_data(value=message.text)
        data = await state.get_data()
        russian_game = func__arr_game(lang=lang, game_name=data['game'])
        if data['param'] == 'factor':
            await db.update_game_settings(factor=data['value'], name=data['game'])
            await send_admins(f"<b>❗ Администратор @{message.from_user.username} изменил <code>Коэффициент</code> в игре <code>{russian_game}</code> на <code>X{data['value']}</code></b>")
            await message.answer("Успешно изменено")
            await message.answer(lang.vibor_game_to_edit, reply_markup=edit_game_menu(texts=lang))
        elif data['param'] == 'min_bet':
            await db.update_game_settings(min_bet=data['value'], name=data['game'])
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
    await state.update_data(type=type, user_id=user_id)
    
@dp.message_handler(IsAdmin(), state=AdminRevorkPrice.summa)
async def func_edit_game_two(message: Message, state: FSMContext):
    texts = await get_language(message.from_user.id)
    if is_number(message.text) == True:
        data = await state.get_data()
        if data['type'] == 'balance':
            await db.update_user(id=data['user_id'], balance=int(message.text))
        elif data['type'] == 'demo':
            await db.update_user(id=data['user_id'], test_balance=int(message.text))
        await message.answer("Успешно")
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
        await message.answer(ded(texts.admin_open_profile.format(name=name,
                                                                    user_id=user_id,
                                                                    total_refill=total_refill,
                                                                    balance=balance,
                                                                    demo_balance=demo_balance,
                                                                    lang=lang,
                                                                    tr=user['total_pay'],
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
                                                                    referalst_summa=user['total_refill'])), reply_markup=await admin_user_menu(texts=texts, user_id=user_id))
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
    if is_number(message.text) == True:
        data = await state.get_data()
        user = await db.get_user(user_id=data['user_id'])
        if data['type'] == 'balance':
            await db.update_user(id=data['user_id'], balance=int(user['balance'])+int(message.text))
        elif data['type'] == 'demo':
            await db.update_user(id=data['user_id'], test_balance=int(user['test_balance'])+int(message.text))
        await message.answer("Успешно")
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
        await message.answer(ded(texts.admin_open_profile.format(name=name,
                                                                    user_id=user_id,
                                                                    total_refill=total_refill,
                                                                    balance=balance,
                                                                    demo_balance=demo_balance,
                                                                    lang=lang,
                                                                    tr=user['total_pay'],
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
                                                                    referalst_summa=user['total_refill'])), reply_markup=await admin_user_menu(texts=texts, user_id=user_id))
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
    if is_number(message.text):
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
        await message.answer("Успешно измененно!")
        await state.finish()
    else: 
        await message.answer(lang.need_number)
    
