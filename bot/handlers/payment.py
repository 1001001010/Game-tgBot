from AsyncPayments.cryptoBot import AsyncCryptoBot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext


from bot.data.loader import dp, bot
from bot.data.config import cryptobot_token
from bot.keyboards.inline import payment_method_back
from bot.state.users import UserPayment
from bot.utils.utils_functions import is_number, get_language
cryptoBot = AsyncCryptoBot(cryptobot_token)

@dp.callback_query_handler(text_startswith='payment', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    type_payment = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer("Введите сумму пополнения: ", reply_markup=payment_method_back())
    await UserPayment.amount.set()
    await state.update_data(method=type_payment)
    
@dp.message_handler(state=UserPayment.amount)
async def functions_profile_get(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number(message.text):
        await state.update_data(amount = message.text)
        data = await state.get_data()
        if data['method'] == 'cryptobot':
            link = await cryptoBot.create_invoice(amount=float(data['amount']), currency_type='fiat', fiat='RUB')
            print(link.pay_url)  
        elif data['method'] == 'xrocket':
            print("Xroket еще нет :(((")
    else:
        await message.answer(lang.need_number)