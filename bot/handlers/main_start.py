from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.data.loader import dp, bot
from bot.keyboards.reply import user_menu
from bot.utils.utils_functions import get_language

#Обработка команды /start
@dp.message_handler(commands=['start'], state="*")
async def func_main_start(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    await bot.send_message(message.from_user.id, lang.welcome, reply_markup=await user_menu(texts=lang, user_id=message.from_user.id))