import os
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 

from bot.data.config import lang_ru, lang_en
from bot.data.loader import dp, bot
from bot.data.config import db
from bot.state.users import UsersCoupons
from bot.keyboards.inline import back_to_user_menu, support_inll, kb_profile, back_to_profile, choose_languages_kb, game_menu
from bot.utils.utils_functions import get_language, ded

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
    await bot.send_photo(user_info['user_id'], 
                        photo=photo_path, 
                        caption=ded(lang.open_profile(
                        user_id=user_info['user_id'], 
                        user_name=user_info['user_name'], 
                        balance=user_info['balance'],
                        test_balance=user_info['test_balance'], 
                        referals=None, 
                        referals_sum=None, 
                        refer_lvl=None, 
                        balance_vivod=None, 
                        refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, user_id=message.from_user.id))

#Открытие FAQ
@dp.message_handler(text=lang_ru.reply_kb3, state="*")
@dp.message_handler(text=lang_en.reply_kb3, state="*")
async def func__profile(message: Message, state: FSMContext):
    await state.finish()
    msg = await db.get_settings(id=1)
    await message.answer(msg['FAQ'], parse_mode='html')

#Запрос демо баланса
@dp.callback_query_handler(text='test_balance', state="*")
async def get_test_balance(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    user_info = await db.get_user(user_id = call.from_user.id)
    if user_info['request_test'] == 0:
        await call.message.delete()
        await db.update_user(id = call.from_user.id, request_test=1, test_balance=25)
        await call.answer(lang.yes_demo)
        bott = await bot.get_me()
        bot_name = bott.username
        ref_link = f"<code>https://t.me/{bot_name}?start={user_info['user_id']}</code>"
        photo_path = InputFile('./bot/data/photo/profile.png')
        user_info = await db.get_user(user_id = call.from_user.id)
        await bot.send_photo(user_info['user_id'], 
                        photo=photo_path, 
                        caption=ded(lang.open_profile(
                        user_id=user_info['user_id'], 
                        user_name=user_info['user_name'], 
                        balance=user_info['balance'],
                        test_balance=user_info['test_balance'], 
                        referals=None, 
                        referals_sum=None, 
                        refer_lvl=None, 
                        balance_vivod=None, 
                        refer_link=ref_link)), reply_markup=await kb_profile(texts=lang, user_id=call.from_user.id))
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
        kb = back_to_user_menu(texts=lang)
    else:
        kb = await support_inll(texts=lang)
    photo_path = InputFile('./bot/data/photo/helper.png')
    await bot.send_photo(message.from_user.id, photo=photo_path, caption=msg, reply_markup=kb)

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
        activ_cop = await db.get_activate_coupon(user_id=user_id, coupon_name=cop)
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
    await bot.send_photo(message.from_user.id, photo=photo_path, caption=lang.game_menu, reply_markup=game_menu(texts=lang))