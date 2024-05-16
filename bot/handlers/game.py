import random
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import re

from bot.data.loader import dp, bot
from bot.data.config import db, game_slots
from bot.keyboards.inline import kb_back_to_game_menu
from bot.utils.utils_functions import get_language, ded, func__arr_game, is_number
from bot.filters.filters import IsAdmin
from bot.state.users import UsersBet, UsersGame

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import BoundFilter
import emoji

@dp.callback_query_handler(IsAdmin(), text_startswith='game', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    game_name = func__arr_game(lang=lang, game_name=call.data.split(":")[1])
    user = await db.get_user(user_id = call.from_user.id)
    game = await db.get_game_settings(name=call.data.split(":")[1])
    await call.message.answer(ded(lang.bet_msg(game_name_text=game_name, 
                                               min_bet=game['min_bet'], 
                                               user_balance=user['balance'])), 
                                                reply_markup=await kb_back_to_game_menu(texts=lang, 
                                                                                        user_id=call.from_user.id, 
                                                                                        min_bet=game['min_bet'], 
                                                                                        type_balance='real',
                                                                                        game=game['name']))
    await UsersBet.bet.set()
    await state.update_data(type_bet='real', game=call.data.split(":")[1])
    
#Переключение между Демо и Реал балансом
@dp.callback_query_handler(IsAdmin(), text_startswith='user_use_balance', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    type_balance = call.data.split(":")[1]
    game = call.data.split(":")[2]
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    game_name = func__arr_game(lang=lang, game_name=game)
    user = await db.get_user(user_id = call.from_user.id)
    game = await db.get_game_settings(name=game)
    if type_balance == 'real':
        await call.message.answer(ded(lang.bet_msg(game_name_text=game_name, 
                                                min_bet=game['min_bet'], 
                                                user_balance=user['balance'])), 
                                                    reply_markup=await kb_back_to_game_menu(texts=lang, 
                                                                                            user_id=call.from_user.id, 
                                                                                            min_bet=game['min_bet'], 
                                                                                            type_balance='real',
                                                                                            game=game['name']))
        await UsersBet.bet.set()
        await state.update_data(type_bet='real', game=game['name'])
        
    elif type_balance == 'demo':
        await call.message.answer(ded(lang.bet_msg_demo(game_name_text=game_name, 
                                        min_bet=game['min_bet'], 
                                        demo_balance=user['test_balance'])), 
                                            reply_markup=await kb_back_to_game_menu(texts=lang, 
                                                                                    user_id=call.from_user.id, 
                                                                                    min_bet=game['min_bet'], 
                                                                                    type_balance='demo',
                                                                                    game=game['name']))
        await UsersBet.bet.set()
        await state.update_data(type_bet='demo', game=game['name'])
        
#Получение ставки
@dp.message_handler(state=UsersBet.bet)
async def fun_get_game(message: Message, state: FSMContext):
    await state.update_data(bet=message.text)
    lang = await get_language(message.from_user.id)
    data = await state.get_data()
    print(data)
    user = await db.get_user(user_id=message.from_user.id)
    if is_number(data['bet']) == True:
        emoji_text = func__arr_game(lang=lang, game_name=data['game'])
        emoji = emoji_text.split(" ")[0]
        if data['type_bet'] == 'demo':
            await db.update_user(id=user['user_id'], test_balance=(int(user['test_balance'])-int(data['bet'])))
        elif data['type_bet'] == 'real':
            await db.update_user(id=user['user_id'], balance=(int(user['balance'])-int(data['bet'])))
        await message.answer(lang.yes_bet.format(emoji_game=emoji))
        await state.finish()
        await UsersGame.msg.set()
        await state.update_data(type_bet=data['type_bet'], bet=data['bet'], game=emoji)
    else:
        await message.answer(lang.need_number)