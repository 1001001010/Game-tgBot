import random
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import re
from aiogram import types
from aiogram.types.dice import DiceEmoji

from bot.data.loader import dp, bot
from bot.data.config import db, game_slots
from bot.keyboards.inline import kb_back_to_game_menu, game_next
from bot.utils.utils_functions import get_language, ded, func__arr_game, is_number
from bot.filters.filters import IsAdmin
from bot.state.users import UsersBet, UsersGame

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
    min_bet = await db.get_game_settings(name=data['game'])
    user = await db.get_user(user_id=message.from_user.id)  
    game_settings = await db.get_game_settings(name=data['game'])
    if is_number(data['bet']) == True:
        if int(data['bet']) < int(min_bet['min_bet']):
            await message.answer(f"Минимальная ставка: {min_bet['min_bet']} 🪙")
        else:
            emoji_text = func__arr_game(lang=lang, game_name=data['game'])
            emoji = emoji_text.split(" ")[0]
            if data['type_bet'] == 'demo':
                if int(user['test_balance']) < int(data['bet']):
                    await message.answer(lang.no_money)
                else:
                    await db.update_user(id=user['user_id'], test_balance=(int(user['test_balance'])-int(data['bet'])))
                    if emoji == '🏀':
                        result = await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                    elif emoji == '🎰':
                        result = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                    elif emoji == '🎲':
                        result = await message.answer_dice(emoji=DiceEmoji.DICE)
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        if result.dice['value'] == 6:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = int(new_balance['test_balance'])+int(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=int(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=int(new_balance['test_balance'])+int(data['bet'])*float(game_settings['factor']))))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else: 
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=int(user['test_balance'])-int(data['bet']))))
                    elif emoji == '⚽':
                        result = await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                    elif emoji == '🪙':
                        result = await message.answer("Тут надо другую функцию прописывать")
            elif data['type_bet'] == 'real':
                if int(user['balance']) < int(data['bet']):
                    await message.answer(lang.no_money)
                else:
                    await db.update_user(id=user['user_id'], amount_all_games=int(user['amount_all_games']+1))
                    await db.update_user(id=user['user_id'], balance=(int(user['balance'])-int(data['bet'])))
                    
                    if emoji == '🏀':
                        result = await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                        await db.update_user(id=user['user_id'], amount_basketball=int(user['amount_basketball']+1))
                        if result.dice['value'] in [4, 5, 6]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = int(new_balance['balance'])+int(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=int(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=int(new_balance['balance'])+int(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=int(user['balance'])-int(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            
                    elif emoji == '🎰':
                        result = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                        await db.update_user(id=user['user_id'], amount_slots=int(user['amount_slots']+1))
                    elif emoji == '🎲':
                        result = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await db.update_user(id=user['user_id'], amount_dice=int(user['amount_dice']+1))
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        await db.update_user(id=user['user_id'], amount_bowling=int(user['amount_bowling']+1))
                        if result.dice['value'] == 6:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = int(new_balance['balance'])+int(data['bet'])*int(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=int(data['bet'])*int(game_settings['factor']), kef=game_settings['factor'], balance=int(new_balance['balance'])+int(data['bet'])*int(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else: 
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=int(user['balance'])-int(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '⚽':
                        result = await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                        await db.update_user(id=user['user_id'], amount_football=int(user['amount_football']+1))
                        await message.answer(result.dice['value'])
                        # if result.dice['value'] in [4, 5, 6]:
                        #     new_balance = await db.get_user(user_id=message.from_user.id)
                        #     balance = int(new_balance['balance'])+int(data['bet'])*float(game_settings['factor'])
                        #     await message.answer(ded(lang.win_game(summ=int(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=int(new_balance['balance'])+int(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                        #     await db.update_user(id=user['user_id'], balance=balance)
                        # else:
                        #     await message.answer(ded(lang.lose_game(summ=data['bet'], balance=int(user['balance'])-int(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🪙':
                        await db.update_user(id=user['user_id'], amount_coin=int(user['amount_coin']+1))
                        result = await message.answer("Тут надо другую функцию прописывать")
    else:
        await message.answer(lang.need_number)
    await state.finish()
    
@dp.callback_query_handler(IsAdmin(), text_startswith='user_use_balance', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()