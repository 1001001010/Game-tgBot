from AsyncPayments.cryptoBot import AsyncCryptoBot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext


from bot.data.loader import dp, bot
from bot.data.config import cryptobot_token, db
from bot.keyboards.inline import payment_method_back, kb_payment_link
from bot.state.users import UserPayment
from bot.utils.utils_functions import is_number, get_language
cryptoBot = AsyncCryptoBot(cryptobot_token)

@dp.callback_query_handler(text_startswith='payment', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    type_payment = call.data.split(":")[1]
    await call.message.delete()
    await call.message.answer(lang.need_summa, reply_markup=payment_method_back())
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
            await message.answer(lang.payment_link, reply_markup=kb_payment_link(lang=lang, link=link.pay_url, pay_id=link.invoice_id, method='cryptobot'))
        elif data['method'] == 'xrocket':
            print("Xroket еще нет :(((")
    else:
        await message.answer(lang.need_number)
        
@dp.callback_query_handler(text_startswith='cheak_pay', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    method = call.data.split(":")[1]
    pay_id = call.data.split(":")[2]
    lang = await get_language(call.from_user.id)
    if method == 'cryptobot':
        invoices = await cryptoBot.get_invoices(invoice_ids=pay_id)
        invoices = invoices[0]
        if invoices.status == 'active':
            await call.answer(lang.not_pay)
        if invoices.status == 'paid':
            # await call.message.delete()
            await call.answer(lang.yes_pay)
            user = await db.get_user(user_id = call.from_user.id)
            if user['ref_id'] is not None:
                referral = await db.get_user(user_id = user['ref_id'])
                user_ref_lvl = referral['ref_lvl']
                game_sett = await db.get_settings(id=1)
                percent = game_sett[f'ref_percent_{user_ref_lvl}']
                ego_procent = float(invoices.amount) * float(percent / 100)
                await db.update_user(id=referral['user_id'], balance=float(referral['balance']) + float(ego_procent), total_refill = float(referral['total_refill']) + float(ego_procent))
                await bot.send_message(referral['user_id'], lang.ref_plus_balance.format(percent=ego_procent))
            await db.update_user(id=call.from_user.id, balance=float(user['balance']) + float(invoices.amount))