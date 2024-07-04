from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.data.loader import dp, bot
from bot.data.config import db
from bot.keyboards.reply import user_menu
from bot.keyboards.inline import admin_menu, choose_languages_kb, sub, back_to_user_menu
from bot.utils.utils_functions import get_language, convert_ref
from bot.filters.filters import IsAdmin, IsBan, IsSub, IsWork

#Проверка на бан
@dp.message_handler(IsBan(), state="*")
async def is_ban(message: Message, state: FSMContext):
    await state.finish()
    user = await db.get_user(user_id=message.from_user.id)
    lang = await get_language(message.from_user.id)
    await message.answer(lang.is_ban_text.format(ban_msg=user['ban_cause']))

@dp.message_handler(IsWork(), state="*")
async def is_work(message: Message, state: FSMContext):
    await state.finish()
    texts = await get_language(message.from_user.id)
    await message.answer(texts.is_work_text)


@dp.callback_query_handler(IsWork(), state="*")
async def is_work(call: CallbackQuery, state: FSMContext):
    await state.finish()
    texts = await get_language(call.from_user.id)
    await call.answer(texts.is_work_text)

@dp.callback_query_handler(IsBan(), state="*")
async def is_ban(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await db.get_user(user_id=call.from_user.id)
    lang = await get_language(call.from_user.id)
    await call.answer(lang.is_ban_text.format(ban_msg=user['ban_cause']))
    
@dp.callback_query_handler(IsSub(), state="*")
async def is_subs(call: CallbackQuery, state: FSMContext):
    await state.finish()
    texts = await get_language(call.from_user.id)
    await call.message.answer(texts.no_sub, reply_markup=sub())


@dp.message_handler(IsSub(), state="*")
async def is_subs(msg: Message, state: FSMContext):
    await state.finish()
    texts = await get_language(msg.from_user.id)
    await msg.answer(texts.no_sub, reply_markup=sub())
    
@dp.callback_query_handler(text=['subprov'])
async def sub_prov(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if call.message.chat.type == 'private':
        user = await db.get_user(user_id=call.from_user.id)
        lang = await get_language(call.from_user.id)
        kb = await user_menu(texts=lang, user_id=call.from_user.id)
        await call.message.answer(lang.welcome, reply_markup=kb)
    
@dp.message_handler(commands=['start'], state="*")
async def main_start(message: Message, state: FSMContext):
    await state.finish()
    user = await db.get_user(user_id=message.from_user.id)
    lang = await get_language(message.from_user.id)
    kb = await user_menu(texts=lang, user_id=message.from_user.id)
    s = await db.get_only_settings()
    if message.get_args() == "":
            await message.answer(lang.welcome, reply_markup=kb)
    else:
        if await db.get_user(user_id=int(message.get_args())) is None:
                await message.answer(lang.welcome, reply_markup=kb)
        else:
            if user['ref_id'] is not None:
                await message.answer(lang.yes_reffer)
            else:
                reffer = await db.get_user(user_id=int(message.get_args()))
                if reffer['user_id'] == message.from_user.id:
                    await message.answer(lang.invite_yourself)
                else:
                    user_ref_count = reffer['ref_count']
                    msg = lang.new_refferal.format(user_name=user['user_name'],
                                                    user_ref_count=user_ref_count + 1,
                                                    convert_ref=convert_ref(lang, user_ref_count + 1))

                    await db.update_user(message.from_user.id, ref_id=reffer['user_id'],
                                            ref_user_name=reffer['user_name'], ref_first_name=reffer['first_name'])
                    await db.update_user(reffer['user_id'], ref_count=user_ref_count + 1)

                    await bot.send_message(chat_id=reffer['user_id'], text=msg)

                    if reffer['ref_count'] + 1 == s['ref_lvl_1']:
                        remain_refs = s['ref_lvl_2'] - (reffer['ref_count'] + 1)
                        text = lang.new_ref_lvl.format(new_lvl=1, next_lvl=2, remain_refs=remain_refs,
                                                        convert_ref=convert_ref(lang, remain_refs))
                        await bot.send_message(chat_id=reffer['user_id'], text=text)
                        await db.update_user(reffer['user_id'], ref_lvl=1)
                    elif reffer['ref_count'] + 1 == s['ref_lvl_2']:
                        remain_refs = s['ref_lvl_3'] - (reffer['ref_count'] + 1)
                        text = lang.new_ref_lvl.format(new_lvl=2, next_lvl=3, remain_refs=remain_refs,
                                                        convert_ref=convert_ref(lang, remain_refs))
                        await bot.send_message(chat_id=reffer['user_id'],
                                                text=text)
                        await db.update_user(reffer['user_id'], ref_lvl=2)
                    elif reffer['ref_count'] + 1 == s['ref_lvl_3']:
                        await bot.send_message(chat_id=reffer['user_id'],
                                                text=lang.max_ref_lvl)
                        await db.update_user(reffer['user_id'], ref_lvl=3)

                    name = f"@{user['user_name']}"
                    if user['user_name'] == "":
                        us = await bot.get_chat(user['id'])
                        name = us.get_mention(as_html=True)
                    await message.answer(lang.welcome, reply_markup=kb)

@dp.callback_query_handler(text_startswith="change_language:", state="*")
async def change_language_(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang_short_name = call.data.split(":")[1]
    await db.update_user(id=call.from_user.id, language=lang_short_name)
    await call.message.delete()
    
@dp.callback_query_handler(text='back_to_m', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await bot.send_message(call.from_user.id, lang.welcome, reply_markup=await user_menu(texts=lang, 
                                                                                         user_id=call.from_user.id))
    
@dp.callback_query_handler(IsAdmin(), text='back_to_adm_m', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.admin_menu, reply_markup=admin_menu(texts=lang))