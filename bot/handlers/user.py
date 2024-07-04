import os
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 
from datetime import datetime

from bot.data.loader import dp, bot
from bot.data.config import lang_ru, lang_en, db, admin_chat, pay_chat
from bot.keyboards.inline import back_to_user_menu, support_inll, kb_profile, back_to_profile, \
                                choose_languages_kb, game_menu, payment_method, kb_vivod_zayavka, kb_vivod_moneta, \
                                kb_network, yes_or_no_vivod, kb_rework_network, yes_or_no_cheack
from bot.utils.utils_functions import get_language, ded, is_number, gen_id
from bot.state.users import UsersCoupons, UserVivid
from bot.utils.converter import convert_rub_to_usd

#Открытие пополнения
@dp.message_handler(text=lang_ru.refill, state="*")
@dp.message_handler(text=lang_en.refill, state="*")
async def func__refill(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    await message.answer(lang.refil_sposob, reply_markup=payment_method())
    
@dp.callback_query_handler(text='payment_method', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.refil_sposob, reply_markup=payment_method())

#Открытие Профиля
@dp.message_handler(text=lang_ru.reply_kb2, state="*")
@dp.message_handler(text=lang_en.reply_kb2, state="*")
async def func__profile(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    user_info = await db.get_user(user_id = message.from_user.id)
    bott = await bot.get_me()
    bot_name = bott.username
    ref_link = f"<code>https://t.me/{bot_name}?start={user_info['user_id']}</code>"
    photo_path = InputFile('./bot/data/photo/profile.png')
    ref_lvl = user_info['ref_lvl']
    #Получение имени реффера 
    reffer_name = user_info['ref_first_name']
    if reffer_name is None:
        reffer = lang.nobody
    else:
        reffer = f"<a href='tg://user?id={user_info['ref_id']}'>{reffer_name}</a>"
        
    # await bot.send_photo(user_info['user_id'], 
    #                     photo=photo_path, 
    await message.answer(ded(lang.open_profile(
                        user_id=user_info['user_id'], 
                        user_name=user_info['user_name'], 
                        balance=round(float(user_info['balance']), 2),
                        test_balance=round(float(user_info['test_balance']), 2), 
                        referals=user_info['ref_count'], 
                        referals_sum=user_info['total_refill'], 
                        refer_lvl=ref_lvl, 
                        balance_vivod=round(float(user_info['vivod']), 2), 
                        reffer = reffer,
                        refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, 
                                                                             user_id=message.from_user.id))

@dp.callback_query_handler(text="back_to_profile", state="*")
async def user_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    user_info = await db.get_user(user_id = call.from_user.id)
    bott = await bot.get_me()
    bot_name = bott.username
    ref_link = f"<code>https://t.me/{bot_name}?start={user_info['user_id']}</code>"
    photo_path = InputFile('./bot/data/photo/profile.png')
    ref_lvl = user_info['ref_lvl']
    #Получение имени реффера 
    reffer_name = user_info['ref_first_name']
    if reffer_name is None:
        reffer = lang.nobody
    else:
        reffer = f"<a href='tg://user?id={user_info['ref_id']}'>{reffer_name}</a>"
        
    await call.message.answer(ded(lang.open_profile(
                                user_id=user_info['user_id'], 
                                user_name=user_info['user_name'], 
                                balance=round(float(user_info['balance']), 2),
                                test_balance=round(float(user_info['test_balance']), 2), 
                                referals=user_info['ref_count'], 
                                referals_sum=user_info['total_refill'], 
                                refer_lvl=ref_lvl, 
                                balance_vivod=round(float(user_info['vivod']), 2), 
                                reffer = reffer,
                                refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, 
                                                                                    user_id=call.from_user.id)
    )
    # await bot.send_photo(user_info['user_id'], 
    #                     photo=photo_path, 
    #                     caption=ded(lang.open_profile(
    #                     user_id=user_info['user_id'], 
    #                     user_name=user_info['user_name'], 
    #                     balance=round(float(user_info['balance']), 2),
    #                     test_balance=round(float(user_info['test_balance']), 2), 
    #                     referals=user_info['ref_count'], 
    #                     referals_sum=user_info['total_refill'], 
    #                     refer_lvl=ref_lvl, 
    #                     balance_vivod=round(float(user_info['vivod']), 2), 
    #                     reffer = reffer,
    #                     refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, 
    #                                                                          user_id=call.from_user.id))

#Открытие FAQ
@dp.message_handler(text=lang_ru.reply_kb3, state="*")
@dp.message_handler(text=lang_en.reply_kb3, state="*")
async def func__profile(message: Message, state: FSMContext):
    await state.finish()
    msg = await db.get_settings(id=1)
    # await message.answer(msg['FAQ'], parse_mode='html')
    photo_path = InputFile('./bot/data/photo/faq.png')
    # await bot.send_photo(message.from_user.id, photo_path, msg['FAQ'], parse_mode='html')
    await message.answer(msg['FAQ'], parse_mode='html')

#Запрос демо баланса
@dp.callback_query_handler(text='test_balance', state="*")
async def get_test_balance(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    user_info = await db.get_user(user_id = call.from_user.id)
    if user_info['request_test'] == 0:
        await call.message.delete()
        await db.update_user(id = call.from_user.id, 
                             request_test=1, 
                             test_balance=25)
        await call.answer(lang.yes_demo)
        bott = await bot.get_me()
        bot_name = bott.username
        ref_link = f"<code>https://t.me/{bot_name}?start={user_info['user_id']}</code>"
        photo_path = InputFile('./bot/data/photo/profile.png')
        user_info = await db.get_user(user_id = call.from_user.id)
        reffer_name = user_info['ref_first_name']
        ref_lvl = user_info['ref_lvl']
        if reffer_name is None:
            reffer = lang.nobody
        else:
            reffer = f"<a href='tg://user?id={user_info['ref_id']}'>{reffer_name}</a>"
        # await bot.send_photo(user_info['user_id'], 
        #                 photo=photo_path, 
        #                 caption=ded(lang.open_profile(
        #                 user_id=user_info['user_id'], 
        #                 user_name=user_info['user_name'], 
        #                 balance=round(float(user_info['balance']), 2),
        #                 test_balance=round(float(user_info['test_balance']), 2), 
        #                 referals=user_info['ref_count'], 
        #                 referals_sum=user_info['total_refill'], 
        #                 refer_lvl=ref_lvl, 
        #                 balance_vivod=round(float(user_info['vivod']), 2), 
        #                 reffer = reffer,
        #                 refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, 
        #                                                                      user_id=call.from_user.id))
        await call.message.answer(ded(lang.open_profile(
                        user_id=user_info['user_id'], 
                        user_name=user_info['user_name'], 
                        balance=round(float(user_info['balance']), 2),
                        test_balance=round(float(user_info['test_balance']), 2), 
                        referals=user_info['ref_count'], 
                        referals_sum=user_info['total_refill'], 
                        refer_lvl=ref_lvl, 
                        balance_vivod=round(float(user_info['vivod']), 2), 
                        reffer = reffer,
                        refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, 
                                                                             user_id=call.from_user.id))
    elif user_info['request_test'] == 1:
        await call.answer(lang.no_demo)

#Открытие Support
@dp.message_handler(text=lang_ru.reply_kb4, state="*")
@dp.message_handler(text=lang_en.reply_kb4, state="*")
async def sup_open(message: Message, state: FSMContext):
    await state.finish()
    s = await db.get_settings(id=1)
    lang = await get_language(message.from_user.id)
    get_support = s['support']
    if get_support == "None" or get_support == "-" or get_support == "":
        msg = lang.no_support
    else:
        msg = lang.yes_support

    if get_support == "None" or get_support == "-" or get_support == "":
        kb = back_to_profile(texts=lang)
    else:
        kb = await support_inll(texts=lang)
    photo_path = InputFile('./bot/data/photo/helper.png')
    # await bot.send_photo(message.from_user.id, 
    #                      photo=photo_path, 
    #                      caption=msg, 
    #                      reply_markup=kb)
    await message.answer(msg, reply_markup=kb)

#Промокод 
@dp.callback_query_handler(text="promo", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await UsersCoupons.here_coupon.set()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(lang.promo_act, reply_markup=back_to_profile(texts=lang))

@dp.message_handler(state=UsersCoupons.here_coupon)
async def functions_profile_get(message: Message, state: FSMContext):
    await state.finish()
    coupon = message.text
    lang = await get_language(message.from_user.id)
    if await db.get_coupon_search(coupon=coupon) is None:
        await message.answer(lang.no_coupon.format(coupon=coupon))
    else:
        cop = (await db.get_coupon_search(coupon=coupon))["coupon"]
        uses = (await db.get_coupon_search(coupon=coupon))["uses"]
        summa = (await db.get_coupon_search(coupon=coupon))["summa_promo"]
        user_id = message.from_user.id
        user = await db.get_user(user_id=user_id)
        activ_cop = await db.get_activate_coupon(user_id=user_id, 
                                                 coupon_name=cop)
        if uses == 0:
            await message.answer(lang.no_uses_coupon)
            await db.delete_coupon(coupon=coupon)
        elif activ_cop is None:
            new_balance = int(user['balance']) + int(summa)

            await db.update_user(user_id, balance=new_balance)
            await db.update_coupon(coupon, uses=int(uses) - 1)
            await db.add_activ_coupon(user_id)
            await db.activate_coupon(user_id=user_id, coupon=coupon)
            await message.answer(lang.yes_coupon.format(summa=summa))
        elif activ_cop["coupon_name"] == cop:
            await message.answer(lang.yes_uses_coupon)
            
#Смена языка
@dp.callback_query_handler(text="change_language", state="*")
async def user_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text="<b>Выберите язык / Select language</b>", reply_markup=await choose_languages_kb())
    
#Открытие Меню игр
@dp.message_handler(text=lang_ru.reply_kb1, state="*")
@dp.message_handler(text=lang_en.reply_kb1, state="*")
async def func__game(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    photo_path = InputFile('./bot/data/photo/game.png')
    # await bot.send_photo(message.from_user.id, 
    #                      photo=photo_path, 
    #                      caption=lang.game_menu, 
    #                      reply_markup=game_menu(texts=lang))
    await message.answer(lang.game_menu, reply_markup=game_menu(texts=lang))
    
@dp.callback_query_handler(text="back_to_game_menu", state="*")
async def user_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    photo_path = InputFile('./bot/data/photo/game.png')
    # await bot.send_photo(call.from_user.id, 
    #                      photo=photo_path, 
    #                      caption=lang.game_menu, 
    #                      reply_markup=game_menu(texts=lang))
    await call.message.answer(lang.game_menu, 
                         reply_markup=game_menu(texts=lang))
    
@dp.callback_query_handler(text="withdrawal", state="*")
async def user_lang(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    balance = await db.get_user(user_id = call.from_user.id)
    await call.message.answer(lang.summa_vivoda.format(balance=balance['balance']))
    await UserVivid.amount.set()
    
@dp.message_handler(state=UserVivid.amount)
async def functions_profile_get(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    user = await db.get_user(user_id=message.from_user.id)
    if is_number(message.text):
        if float(user['balance']) >= float(message.text):
            await state.update_data(amount = message.text)
            await message.answer(lang.need_Crypto, reply_markup=kb_vivod_moneta())
            # await UserVivid.method.set()
        else:
            await message.answer(lang.need_balance)
    else:
        await message.answer(lang.need_number)
        
@dp.callback_query_handler(text_startswith='back_to_method', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    amount = call.data.split(":")[1]
    await state.update_data(amount = amount)
    user = await db.get_user(user_id=call.from_user.id)
    await call.message.answer(lang.need_Crypto, reply_markup=kb_vivod_moneta())

@dp.callback_query_handler(text='check', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    data = await state.get_data()
    user = await db.get_user(user_id=call.from_user.id)
    settings_info = await db.get_settings(id=1)
    comma = settings_info['Commission_check']
    min_summa = settings_info['Minimum_check']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if float(data['amount']) <= float(min_summa):
        await call.message.answer(lang.need_balance)
    else:
        await db.add_vivod(user_id=call.from_user.id, 
                           summa=data['amount'], 
                           network='NULL', 
                           status='not confirmed', 
                           data=time, 
                           adress='NULL')
        vivod_id = await db.get_vivod(user_id=call.from_user.id, 
                                      data=time)
        await call.message.answer(ded(lang.Confirmation_msg_chek.format(amount_vivod=data['amount'], 
                                                                        comma_vivod=round(((float(data['amount']) * float(comma) / 100)), 2), 
                                                                        full_summa=float(data['amount']) - (float(data['amount']) * float(comma) / 100))), 
                                                                        reply_markup=yes_or_no_cheack(vivod_id=vivod_id['id']))
        
@dp.callback_query_handler(text_startswith='ok_check', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    status = call.data.split(":")[1]
    vivod_id = call.data.split(":")[2]
    vivod = await db.get_vivod(id=vivod_id)
    # print(vivod)
    user = await db.get_user(user_id=call.from_user.id)
    settings_info = await db.get_settings(id=1)
    if status == 'yes':
        await call.message.answer(lang.succes_msg)
        await db.update_user(id=call.from_user.id, 
                             balance=float(user['balance']-float(vivod['summa'])))
        usdt_summa_vivod = convert_rub_to_usd(float(vivod['summa']))
        usdt_comma = convert_rub_to_usd(float(settings_info['Commission_check']))
        if user['user_name'] == "":
                us = await bot.get_chat(call.from_user.id)
                name = us.get_mention(as_html=True)
        else:
            name = f"@{user['user_name']}"
        msg = f"""
        Новая заявка от {name}
        ID: {call.from_user.id}
        Дата и время: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        💰 Сумма: <code>${round(usdt_summa_vivod, 2)}</code> | <code>{float(vivod['summa'])}</code>
        💵 Сумма с учетом комиссии: <code>${round((float(usdt_summa_vivod) - ((float(usdt_summa_vivod) * float(settings_info['Commission_check']) / 100))), 2)}</code> | <code>{float(vivod['summa']) - (float(vivod['summa']) * float(settings_info['Commission_check']) / 100)}</code>
        🪙 Метод: <code>🧾 Чек</code>
        💚  Комиссия: <code>{float(settings_info['Commission_check'])}</code>
        """
        await bot.send_message(admin_chat, ded(msg), reply_markup=kb_vivod_zayavka(summa=vivod['summa'], 
                                                                                   vivod_id=vivod_id))
    else:
        await db.update_vivod(id=vivod_id, status='canceled')
        await call.message.answer(lang.otklon_vivod, reply_markup=back_to_profile(lang))
    
@dp.callback_query_handler(text_startswith='moneta', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    moneta = call.data.split(":")[1]
    await state.update_data(method = moneta)
    data = await state.get_data()
    await call.message.answer(lang.need_network, reply_markup=kb_network(lang=lang, 
                                                                         summa=data['amount']))
    # await UserVivid.adress.set()

@dp.callback_query_handler(text_startswith='network', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    network = call.data.split(":")[1]
    if network == 'TON':
        network_name = 'The Open Network (TON)'
    elif network == 'TRC20':
        network_name = 'TRON (TRC20)'
    elif network == 'ERC20':
        network_name = 'Ethereum (ERC20)'
    elif network == 'BER20':
        network_name = 'BNB Smart Chain (BER20)'
    await state.update_data(network = network_name)
    await call.message.answer(lang.need_adress)
    await UserVivid.adress.set()

@dp.message_handler(state=UserVivid.adress)
async def functions_profile_get(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    await state.update_data(adress = message.text)
    data = await state.get_data()
    settings_info = await db.get_settings(id=1)
    if data['network'] == 'The Open Network (TON)':
        if len(data['adress']) == 48 and  str(data['adress'])[:2] == 'UQ':
            comma = settings_info['Commission_TON']
            if float(comma) >= float(data['amount']):
                await message.answer(lang.no_money)
            else:
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await db.add_vivod(user_id=message.from_user.id, 
                                   summa=data['amount'], 
                                   network=data['network'], 
                                   status='not confirmed', 
                                   data=time, 
                                   adress=data['adress'])
                vivod_id = await db.get_vivod(user_id=message.from_user.id, 
                                              status='not confirmed', 
                                              data=time)
                await message.answer(ded(lang.Confirmation_msg.format(network=data['network'],
                                                                      adress=data['adress'],
                                                                      amount_vivod=data['amount'],
                                                                      comma_vivod=comma,
                                                                      full_summa=(float(data['amount'])-float(comma)))), reply_markup=yes_or_no_vivod(vivod_id=vivod_id['id']))
        else: 
            await message.answer(lang.need_real_adress.format(crypto=data['network']), 
                                                              reply_markup=kb_rework_network(lang=lang))
    elif data['network'] == 'TRON (TRC20)':
        comma = settings_info['Commission_TRC20']
        if len(data['adress']) == 34 and  str(data['adress'])[:1] == 'T':
            comma = settings_info['Commission_TON']
            if float(comma) >= float(data['amount']):
                await message.answer(lang.no_money)
            else:
                await db.add_vivod(user_id=message.from_user.id, 
                                   summa=data['amount'], 
                                   network=data['network'], 
                                   status='not confirmed',
                                   data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                   adress=data['adress'])
                vivod_id = await db.get_vivod(user_id=message.from_user.id, status='not confirmed')
                await message.answer(ded(lang.Confirmation_msg.format(network=data['network'],
                                                        adress=data['adress'],
                                                        amount_vivod=data['amount'],
                                                        comma_vivod=comma,
                                                        full_summa=(float(data['amount'])-float(comma)))), reply_markup=yes_or_no_vivod(vivod_id=vivod_id['id']))
        else: 
            await message.answer(lang.need_real_adress.format(crypto=data['network']), reply_markup=kb_rework_network(lang=lang))
    elif data['network'] == 'Ethereum (ERC20)':
        comma = settings_info['Commission_ERC20']
        if len(data['adress']) == 42 and  str(data['adress'])[:2] == '0x':
            comma = settings_info['Commission_TON']
            if float(comma) >= float(data['amount']):
                await message.answer(lang.no_money)
            else:
                await db.add_vivod(user_id=message.from_user.id, 
                                   summa=data['amount'], 
                                   network=data['network'], 
                                   status='not confirmed', 
                                   data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                   adress=data['adress'])
                vivod_id = await db.get_vivod(user_id=message.from_user.id, status='not confirmed')
                await message.answer(ded(lang.Confirmation_msg.format(network=data['network'],
                                                        adress=data['adress'],
                                                        amount_vivod=data['amount'],
                                                        comma_vivod=comma,
                                                        full_summa=(float(data['amount'])-float(comma)))), reply_markup=yes_or_no_vivod(vivod_id=vivod_id['id']))
        else: 
            await message.answer(lang.need_real_adress.format(crypto=data['network']), 
                                                              reply_markup=kb_rework_network(lang=lang))
    elif data['network'] == 'BNB Smart Chain (BER20)':
        comma = settings_info['CommissionBER20']
        if len(data['adress']) == 42 and  str(data['adress'])[:2] == '0x':
            comma = settings_info['Commission_TON']
            if float(comma) >= float(data['amount']):
                await message.answer(lang.no_money)
            else:
                await db.add_vivod(user_id=message.from_user.id, 
                                   summa=data['amount'], 
                                   network=data['network'], 
                                   status='not confirmed', 
                                   data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                   adress=data['adress'])
                vivod_id = await db.get_vivod(user_id=message.from_user.id, status='not confirmed')
                await message.answer(ded(lang.Confirmation_msg.format(network=data['network'],
                                                                      adress=data['adress'],
                                                                      amount_vivod=data['amount'],
                                                                      comma_vivod=comma,
                                                                      full_summa=(float(data['amount'])-float(comma)))), reply_markup=yes_or_no_vivod(vivod_id=vivod_id['id']))
        else: 
            await message.answer(lang.need_real_adress.format(crypto=data['network']), reply_markup=kb_rework_network(lang=lang))

@dp.callback_query_handler(text_startswith='ok_vivod', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    status = call.data.split(":")[1]
    if status == 'yes':
        user = await db.get_user(user_id=call.from_user.id)
        if user['user_name'] == "":
            us = await bot.get_chat(call.from_user.id)
            name = us.get_mention(as_html=True)
        else:
            name = f"@{user['user_name']}"
        id = call.data.split(":")[2]
        await db.update_vivod(id=id, status='Waiting')
        comma = await db.get_settings(id=1)
        info_vivod = await db.get_vivod(id=id)
        if info_vivod['network'] == 'The Open Network (TON)':
            comma = comma['Commission_TON']
        elif info_vivod['network'] == 'TRON (TRC20)':
            comma = comma['Commission_TRC20']
        elif info_vivod['network'] == 'Ethereum (ERC20)':
            comma = comma['Commission_ERC20']
        elif info_vivod['network'] == 'BNB Smart Chain (BER20)':
            comma = comma['CommissionBER20']
            
        usdt_summa_vivod = convert_rub_to_usd(float(info_vivod['summa']))
        usdt_comma = convert_rub_to_usd(float(comma))
        usdt_summa_vivod = round(usdt_summa_vivod, 2)
        usdt_comma = round(usdt_comma, 2)
        msg = f"""
        Новая заявка от {name}
        ID: {call.from_user.id}
        Дата и время: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        💰 Сумма: <code>${usdt_summa_vivod}</code> | <code>{float(info_vivod['summa'])}</code>
        💵 Сумма с учетом комиссии: <code>${round((float(usdt_summa_vivod) - float(usdt_comma)), 2)}</code> | <code>{(float(info_vivod['summa']) - float(comma))}</code>
        🪙 Сеть: <code>{info_vivod['network']}</code>
        💎 Адресс: <code>{info_vivod['adress']}</code>
        💚  Комиссия: <code>${usdt_comma}</code> | <code>{float(comma)}</code>
        """
        await bot.send_message(admin_chat, ded(msg), reply_markup=kb_vivod_zayavka(summa=info_vivod['summa'], 
                                                                                   vivod_id=id))
        await db.update_user(id=user['user_id'], balance=float(user['balance']-float(info_vivod['summa'])))
        await call.message.answer(lang.succes_msg)
    else:
        await db.update_vivod(id=call.data.split(":")[2], status='canceled')
        await call.message.answer(lang.otklon_vivod, reply_markup=back_to_profile(lang))
        
@dp.callback_query_handler(text_startswith='vivod', state="*")
async def func_value(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    status = call.data.split(":")[1]
    summa = call.data.split(":")[2]
    vivod_id = call.data.split(":")[3]
    vivod_info = await db.get_vivod(id=vivod_id)
    user = await db.get_user(user_id=vivod_info['user_id'])
    if status == 'yes':
        await db.update_vivod(id=vivod_id, status='accepted')
        await db.add_check(unix=gen_id(), 
                           user_id=user['user_id'], 
                           transaction_type='withdrawal', 
                           conclusion_id=vivod_id, 
                           summa=float(summa))
        await db.update_user(id=vivod_info['user_id'], 
                             vivod=float(user['vivod'])+float(summa))
        if vivod_info['adress'] == 'NULL':
            await bot.send_message(pay_chat, ded(f"""
                                                ✅ Успешная выплата!
                                                
                                                📅 Дата: <code>{vivod_info['data']}</code>
                                                💰 Сумма: <code>{vivod_info['summa']}</code>₽
                                                📶 Сеть: <code>🧾 Чек</code>
                                                """))
            await bot.send_message(vivod_info['user_id'], lang.vivod_success_msg_check)
        else: 
            await bot.send_message(pay_chat, ded(f"""
                                    ✅ Успешная выплата!
                                    
                                    📅 Дата: <code>{vivod_info['data']}</code>
                                    💰 Сумма: <code>{vivod_info['summa']}₽</code>
                                    📶 Сеть: <code>{vivod_info['network']}</code>
                                        """))
            await bot.send_message(vivod_info['user_id'], lang.vivod_success_msg)
    elif status == 'no':
        await db.update_vivod(id=vivod_id, 
                              status='rejected')
        await bot.send_message(vivod_info['user_id'], lang.vivod_mimo)
        await db.update_user(id=vivod_info['user_id'], 
                             balance=float(user['balance'])+float(summa))