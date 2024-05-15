from bot.data.loader import dp, bot
import random
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from bot.utils.utils_functions import get_language, ded
from bot.data.config import game_slots
from bot.data.config import db
from bot.filters.filters import IsAdmin

# @dp.message_handler(lambda message: message.text == '🏀')
# async def throw_ball(message: types.Message):
#     success_rate = 1  # Шанс попадания 70%
#     if random.random() < success_rate:
#         await message.answer("Поздравляю, мяч попал в корзину! 🎉🏀")
#     else:
#         await message.answer("Мяч промахнулся... Попробуйте еще раз! 🏀")

@dp.callback_query_handler(IsAdmin(), text_startswith='game', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    #Получение игры, в которую пользователь играет 
    english_game_name = call.data.split(":")[1]
    russian_game_name = game_slots.get(english_game_name)
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    game_name_text = getattr(lang, russian_game_name)
    user = await db.get_user(user_id = call.from_user.id)
    #####################################################
    
    await call.message.answer(ded(lang.bet_msg(game_name_text=game_name_text, 
                                               min_bet=None, 
                                               user_balance=user['balance'])))