import os
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 

from bot.data.config import lang_ru, lang_en
from bot.data.loader import dp, bot
from bot.data.config import db
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
                        referals=None, 
                        referals_sum=None, 
                        refer_lvl=None, 
                        balance_vivod=None, 
                        refer_link=ref_link)))
    
#Открытие FAQ
@dp.message_handler(text=lang_ru.reply_kb3, state="*")
@dp.message_handler(text=lang_en.reply_kb3, state="*")
async def func__profile(message: Message, state: FSMContext):
    await state.finish()
    msg = await db.get_settings(id=1)
    await message.answer(msg['FAQ'], parse_mode='html')