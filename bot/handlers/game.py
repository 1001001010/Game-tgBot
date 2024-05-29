import random
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import re
from aiogram import types
from aiogram.types.dice import DiceEmoji
import asyncio

from bot.data.loader import dp, bot
from bot.data.config import db, game_slots, win_coin_sticker_id, lose_coin_sticker_id
from bot.keyboards.inline import kb_back_to_game_menu, game_next, choose_vertical
from bot.utils.utils_functions import get_language, ded, func__arr_game, is_number
from bot.filters.filters import IsAdmin
from bot.state.users import UsersBet
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserCube(StatesGroup):
    cube = State()
    type_bet = State()
    bet = State()

async def my_sleep():
    await asyncio.sleep(3.1)

@dp.callback_query_handler(text_startswith='game', state="*")
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
        if float(data['bet']) < float(min_bet['min_bet']):
            await message.answer(f"Минимальная ставка: {min_bet['min_bet']} 🪙")
        else:
            emoji_text = func__arr_game(lang=lang, game_name=data['game'])
            emoji = emoji_text.split(" ")[0]
            if data['type_bet'] == 'demo':
                if float(user['test_balance']) < float(data['bet']):
                    await message.answer(lang.no_money)
                else:
                    await db.update_user(id=user['user_id'], test_balance=(float(user['test_balance'])-float(data['bet'])))
                    if emoji == '🏀':
                        result = await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                        await db.update_user(id=user['user_id'], amount_basketball=float(user['amount_basketball']+1))
                        await my_sleep()
                        if result.dice['value'] in [4, 5, 6]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎰':
                        result = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                        await my_sleep()
                        if result.dice['value'] in [1, 22, 43]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        elif result.dice['value'] in [64]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*5
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*5)), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎲':
                        await message.answer(lang.your_cube)
                        result1 = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        await message.answer(lang.enemy_cube)
                        result2 = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        if result1.dice['value'] > result2.dice['value']:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']) 
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        elif result1.dice['value'] == result2.dice['value']:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])
                            await message.answer(ded(lang.bank_money), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        await my_sleep()
                        if result.dice['value'] == 6:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else: 
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['test_balance'])-float(data['bet']))))
                    elif emoji == '⚽':
                        result = await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                        await my_sleep()
                        if result.dice['value'] in [3, 4, 5]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🪙':
                        await message.answer(lang.choose_coin, reply_markup=choose_vertical(lang=lang, type_balance=data['type_bet'], bet=data['bet']))
            ####РЕАЛ####
            elif data['type_bet'] == 'real':
                if float(user['balance']) < float(data['bet']):
                    await message.answer(lang.no_money)
                else:
                    await db.update_user(id=user['user_id'], amount_all_games=float(user['amount_all_games']+1))
                    await db.update_user(id=user['user_id'], balance=(float(user['balance'])-float(data['bet'])))
                    
                    if emoji == '🏀':
                        result = await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                        await db.update_user(id=user['user_id'], amount_basketball=float(user['amount_basketball']+1))
                        await my_sleep()
                        if result.dice['value'] in [4, 5, 6]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎰':
                        result = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                        await db.update_user(id=user['user_id'], amount_slots=float(user['amount_slots']+1))
                        await my_sleep()
                        if result.dice['value'] in [1, 22, 43]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        elif result.dice['value'] in [64]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*5
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*5)), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎲':
                        await message.answer(lang.your_cube)
                        result1 = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        await message.answer(lang.enemy_cube)
                        result2 = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        if result1.dice['value'] > result2.dice['value']:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']) 
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        elif result1.dice['value'] == result2.dice['value']:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])
                            await message.answer(ded(lang.bank_money), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        await db.update_user(id=user['user_id'], amount_bowling=float(user['amount_bowling']+1))
                        await my_sleep()
                        if result.dice['value'] == 6:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else: 
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '⚽':
                        result = await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                        await db.update_user(id=user['user_id'], amount_football=float(user['amount_football']+1))
                        await my_sleep()
                        if result.dice['value'] in [3, 4, 5]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🪙':
                        await message.answer(lang.choose_coin, reply_markup=choose_vertical(lang=lang, type_balance=data['type_bet'], bet=data['bet']))
    else:
        await message.answer(lang.need_number)
    await state.finish()

    
    
@dp.callback_query_handler(text_startswith='play_next', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    game = call.data.split(":")[1]
    type_balance = call.data.split(":")[2]
    bet = call.data.split(":")[3]
    lang = await get_language(call.from_user.id)
    user = await db.get_user(user_id=call.from_user.id)  
    game_settings = await db.get_game_settings(name=game)
    if float(bet) < float(game_settings['min_bet']):
        await call.message.answer(f"Минимальная ставка: {game_settings['min_bet']} 🪙")
    else:
        emoji_text = func__arr_game(lang=lang, game_name=game)
        emoji = emoji_text.split(" ")[0]
        if type_balance == 'demo':
            if float(user['test_balance']) < float(bet):
                await call.message.answer(lang.no_money)
            else:
                await db.update_user(id=user['user_id'], test_balance=(float(user['test_balance'])-float(bet)))
                if emoji == '🏀':
                    result = await call.message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                    await db.update_user(id=user['user_id'], amount_basketball=float(user['amount_basketball']+1))
                    await my_sleep()
                    if result.dice['value'] in [4, 5, 6]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎰':
                    result = await call.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                    await my_sleep()
                    if result.dice['value'] in [1, 22, 43]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    elif result.dice['value'] in [64]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*5
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*5)), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎲':
                    await call.message.answer(lang.your_cube)
                    result1 = await call.message.answer_dice(emoji=DiceEmoji.DICE)
                    await my_sleep()
                    await call.message.answer(lang.enemy_cube)
                    result2 = await call.message.answer_dice(emoji=DiceEmoji.DICE)
                    await my_sleep()
                    if result1.dice['value'] > result2.dice['value']:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']) 
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    elif result1.dice['value'] == result2.dice['value']:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)
                        await call.message.answer(ded(lang.bank_money), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎳':
                    result = await call.message.answer_dice(emoji=DiceEmoji.BOWLING)
                    await my_sleep()
                    if result.dice['value'] == 6:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    else: 
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance'])-float(bet))))
                elif emoji == '⚽':
                    result = await call.message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                    await my_sleep()
                    if result.dice['value'] in [3, 4, 5]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], test_balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🪙':
                    await call.message.answer(lang.choose_coin, reply_markup=choose_vertical(lang=lang, type_balance=type_balance, bet=bet))
        ####РЕАЛ####
        elif type_balance == 'real':
            if float(user['balance']) < float(bet):
                await call.message.answer(lang.no_money)
            else:
                await db.update_user(id=user['user_id'], amount_all_games=float(user['amount_all_games']+1))
                await db.update_user(id=user['user_id'], balance=(float(user['balance'])-float(bet)))
                
                if emoji == '🏀':
                    result = await call.message.answer_dice(emoji=DiceEmoji.BASKETBALL)
                    await db.update_user(id=user['user_id'], amount_basketball=float(user['amount_basketball']+1))
                    await my_sleep()
                    if result.dice['value'] in [4, 5, 6]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎰':
                    result = await call.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
                    await db.update_user(id=user['user_id'], amount_slots=float(user['amount_slots']+1))
                    await my_sleep()
                    if result.dice['value'] in [1, 22, 43]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], balance=balance)
                    elif result.dice['value'] in [64]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['balance'])+float(bet)*5
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*5)), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎲':
                        await call.message.answer(lang.your_cube)
                        result1 = await call.message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        await call.message.answer(lang.enemy_cube)
                        result2 = await call.message.answer_dice(emoji=DiceEmoji.DICE)
                        await my_sleep()
                        if result1.dice['value'] > result2.dice['value']:
                            new_balance = await db.get_user(user_id=call.from_user.id)
                            balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor']) 
                            await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                            await db.update_user(id=user['user_id'], balance=balance)
                        elif result1.dice['value'] == result2.dice['value']:
                            new_balance = await db.get_user(user_id=call.from_user.id)
                            balance = float(new_balance['balance'])+float(bet)
                            await call.message.answer(ded(lang.bank_money), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🎳':
                    result = await call.message.answer_dice(emoji=DiceEmoji.BOWLING)
                    await db.update_user(id=user['user_id'], amount_bowling=float(user['amount_bowling']+1))
                    await my_sleep()
                    if result.dice['value'] == 6:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], balance=balance)
                    else: 
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '⚽':
                    result = await call.message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                    await db.update_user(id=user['user_id'], amount_football=float(user['amount_football']+1))
                    await my_sleep()
                    if result.dice['value'] in [3, 4, 5]:
                        new_balance = await db.get_user(user_id=call.from_user.id)
                        balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                        await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                        await db.update_user(id=user['user_id'], balance=balance)
                    else:
                        await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance'])-float(bet))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                elif emoji == '🪙':
                    await call.message.answer(lang.choose_coin, reply_markup=choose_vertical(lang=lang, type_balance=type_balance, bet=bet))

@dp.callback_query_handler(text_startswith='monetka', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    coin = call.data.split(":")[1]
    type_balance = call.data.split(":")[2]
    bet = call.data.split(":")[3]
    lang = await get_language(call.from_user.id)
    game = 'coin'
    user = await db.get_user(user_id=call.from_user.id)  
    game_settings = await db.get_game_settings(name='coin')
    if type_balance == 'real':
        await db.update_user(id=user['user_id'], amount_coin=float(user['amount_coin']+1))
        if random.uniform(0, 1) < game_settings['chance_real']:
            if coin == 'eagle':
                await bot.send_sticker(call.from_user.id, win_coin_sticker_id)
                new_balance = await db.get_user(user_id=call.from_user.id)
                balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                await db.update_user(id=user['user_id'], balance=balance)
            elif coin == 'tails':
                await bot.send_sticker(call.from_user.id, lose_coin_sticker_id)
                new_balance = await db.get_user(user_id=call.from_user.id)
                balance = float(new_balance['balance'])+float(bet)*float(game_settings['factor'])
                await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                await db.update_user(id=user['user_id'], balance=balance)
        else:
            if coin == 'eagle':
                await bot.send_sticker(call.from_user.id, lose_coin_sticker_id)
                await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
            if coin == 'tails':
                await bot.send_sticker(call.from_user.id, win_coin_sticker_id)
                await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['balance']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
    elif type_balance == 'demo':
        if random.uniform(0, 1) < game_settings['chance_demo']:
            if coin == 'eagle':
                await bot.send_sticker(call.from_user.id, win_coin_sticker_id)
                new_balance = await db.get_user(user_id=call.from_user.id)
                balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                await db.update_user(id=user['user_id'], test_balance=balance)
            elif coin == 'tails':
                await bot.send_sticker(call.from_user.id, lose_coin_sticker_id)
                new_balance = await db.get_user(user_id=call.from_user.id)
                balance = float(new_balance['test_balance'])+float(bet)*float(game_settings['factor'])
                await call.message.answer(ded(lang.win_game(summ=float(bet)*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(bet)*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
                await db.update_user(id=user['user_id'], test_balance=balance)
        else:
            if coin == 'eagle':
                await bot.send_sticker(call.from_user.id, lose_coin_sticker_id)
                await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))
            if coin == 'tails':
                await bot.send_sticker(call.from_user.id, win_coin_sticker_id)
                await call.message.answer(ded(lang.lose_game(summ=bet, balance=float(user['test_balance']))), reply_markup=game_next(lang=lang, bet=bet, type_balance=type_balance, game=game))

# @dp.message_handler(content_types=['text'], state=UserCube.cube)
@dp.message_handler(state=UserCube.cube)
async def functions_profile_get(message: Message, state: FSMContext):
    await message.answer('Ваш бросок кубика')