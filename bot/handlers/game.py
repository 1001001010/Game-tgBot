import random
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import re
from aiogram import types
from aiogram.types.dice import DiceEmoji

from bot.data.loader import dp, bot
from bot.data.config import db, game_slots, win_coin_sticker_id, lose_coin_sticker_id
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
                        if result.dice['value'] in [4, 5, 6]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], test_balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🎰':
                        result = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
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
                        result = await message.answer_dice(emoji=DiceEmoji.DICE)
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        if result.dice['value'] == 6:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else: 
                            await message.answer(ded(lang.lose_game(summ=data['bet'], test_balance=float(user['test_balance'])-float(data['bet']))))
                    elif emoji == '⚽':
                        result = await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
                        if result.dice['value'] in [3, 4, 5]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], test_balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🪙':
                        if random.uniform(0, 1) < game_settings['chance_demo'] :
                            await bot.send_sticker(message.from_user.id, win_coin_sticker_id)
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['test_balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], test_balance=balance)
                        else:
                            await bot.send_sticker(message.from_user.id, lose_coin_sticker_id)
                            await message.answer(ded(lang.lose_game(summ=data['bet'], test_balance=float(user['test_balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                        
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
                        await message.answer('Бросьте ваш кубик, для этого отправьте <code>🎲</code>')
                        # result = await message.answer_dice(emoji=DiceEmoji.DICE)
                        await db.update_user(id=user['user_id'], amount_dice=float(user['amount_dice']+1))
                        await UsersGame.cube.set()
                        await state.update_data(type_bet='real', game=data['game'], bet=data['bet'])
                    elif emoji == '🎳':
                        result = await message.answer_dice(emoji=DiceEmoji.BOWLING)
                        await db.update_user(id=user['user_id'], amount_bowling=float(user['amount_bowling']+1))
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
                        if result.dice['value'] in [3, 4, 5]:
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                    elif emoji == '🪙':
                        await db.update_user(id=user['user_id'], amount_coin=float(user['amount_coin']+1))
                        if random.uniform(0, 1) < game_settings['chance_real'] :
                            await bot.send_sticker(message.from_user.id, win_coin_sticker_id)
                            new_balance = await db.get_user(user_id=message.from_user.id)
                            balance = float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor'])
                            await message.answer(ded(lang.win_game(summ=float(data['bet'])*float(game_settings['factor']), kef=game_settings['factor'], balance=float(new_balance['balance'])+float(data['bet'])*float(game_settings['factor']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                            await db.update_user(id=user['user_id'], balance=balance)
                        else:
                            await bot.send_sticker(message.from_user.id, lose_coin_sticker_id)
                            await message.answer(ded(lang.lose_game(summ=data['bet'], balance=float(user['balance'])-float(data['bet']))), reply_markup=game_next(lang=lang, bet=data['bet'], type_balance=data['type_bet'], game=data['game']))
                        
    else:
        await message.answer(lang.need_number)
    await state.finish()

    
    
# @dp.callback_query_handler(text_startswith='user_use_balance', state="*")
# async def back_to_menu(call: CallbackQuery, state: FSMContext):
#     await state.finish()

@dp.message_handler(commands=['foot'])
async def roll_dice(message: types.Message):
    data = await bot.send_dice(message.chat.id, emoji='⚽')
    await bot.send_message(message.chat.id, f'значение футбол {data.dice.value}')