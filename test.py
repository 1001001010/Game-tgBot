import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType
import random

bot = Bot(token='5851624722:AAGB2LVdgGgaUAcOIwD0pM8POuIsFY8bAm4')
dp = Dispatcher(bot)

@dp.message_handler(lambda message: message.text == '🏀')
async def throw_ball(message: types.Message):
    print("всеэ")
    success_rate = 1  # Шанс попадания 70%
    if random.random() < success_rate:
        await message.answer("Поздравляю, мяч попал в корзину! 🎉🏀")
    else:
        await message.answer("Мяч промахнулся... Попробуйте еще раз! 🏀")
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Используйте executor.start_polling вместо loop