from AsyncPayments.cryptoBot import AsyncCryptoBot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
# from xrocket import PayAPI
import requests

from bot.data.loader import dp, bot
# from bot.data.config import cryptobot_token, xrocket_token, db
from bot.data.config import cryptobot_token, db
from bot.keyboards.inline import payment_method_back, kb_payment_link, crypto
from bot.state.users import UserPayment
from bot.utils.utils_functions import is_number, get_language, gen_id
from bot.utils.converter import RubToTon, RubToScale, RubToHedge, RubToAmbr, RubToTake, \
                                RubToTnx, RubToBolt, RubToGrbs, RubToJusdt
cryptoBot = AsyncCryptoBot(cryptobot_token)
# xRoketApi = PayAPI(api_key=xrocket_token)

@dp.callback_query_handler(text_startswith='payment', state="*")
async def func_payment(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    type_payment = call.data.split(":")[1]
    await call.message.delete()
    if type_payment == 'cryptobot':
        await call.message.answer(lang.need_summa_cryptobot, reply_markup=payment_method_back())
        await UserPayment.amount.set()
        await state.update_data(method=type_payment, coin=None)
    elif type_payment == 'xrocket':
        await call.message.answer(lang.need_summa_cryptobot, reply_markup=payment_method_back())
        await UserPayment.amount.set()
        await state.update_data(method=type_payment, coin=None)
        # TONCOIN, SCALE, HEDGE, AMBR, TAKE, TNX, nKOTE, BOLT, GRBS, jUSDT
        # cheque = await xRoketApi.invoice_create(amount=1, currency='jUSDT')
        # await call.message.answer(lang.vibor_crypto, reply_markup=crypto())
    
# @dp.callback_query_handler(text_startswith='valute', state="*")
# async def func_value(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     await call.message.delete()
#     lang = await get_language(call.from_user.id)
#     moneta = call.data.split(":")[1]
#     amount = call.data.split(":")[2]
#     if moneta == 'TONCOIN':
#         crypto = await RubToTon(float(amount))
#     # elif moneta == 'SCALE':
#     #     crypto = await RubToScale(float(amount))
#     # elif moneta == 'HEDGE':
#     #     crypto = await RubToHedge(float(amount))
#     # elif moneta == 'AMBR':
#     #     crypto = await RubToAmbr(float(amount))
#     # elif moneta == 'TAKE':
#     #     crypto = await RubToTake(float(amount))
#     # elif moneta == 'TNX':
#     #     crypto = await RubToTnx(float(amount))
#     elif moneta == 'BOLT':
#         crypto = await RubToBolt(float(amount))
#     elif moneta == 'GRBS':
#         crypto = await RubToGrbs(float(amount))
#     elif moneta == 'jUSDT':
#         crypto = await RubToJusdt(float(amount))
#     cheque = await xRoketApi.invoice_create(amount=float(crypto), currency=moneta)
#     id = cheque['data']['id']
#     link = cheque['data']['link']
#     await call.message.answer(lang.payment_link, reply_markup=kb_payment_link(lang=lang, link=link, pay_id=id, method='xrocket', summa=amount))
            
            
    # cheque = await xRoketApi.invoice_create(amount=1, currency='jUSDT')
    # await call.message.answer(lang.vibor_crypto, reply_markup=crypto())
    # await call.message.answer(lang.need_summa_xRoket.format(coin=moneta), reply_markup=payment_method_back())
    # await UserPayment.amount.set()
    # await state.update_data(method='xrocket', coin=moneta)
    
@dp.message_handler(state=UserPayment.amount)
async def functions_profile_get(message: Message, state: FSMContext):
    lang = await get_language(message.from_user.id)
    if is_number(message.text):
        await state.update_data(amount = message.text)
        data = await state.get_data()
        if data['method'] == 'cryptobot':
            link = await cryptoBot.create_invoice(amount=float(data['amount']), currency_type='fiat', fiat='RUB')
            await message.answer(lang.payment_link, reply_markup=kb_payment_link(lang=lang, link=link.pay_url, pay_id=link.invoice_id, method='cryptobot', summa=None))
        elif data['method'] == 'xrocket':
            await message.answer(lang.vibor_crypto, reply_markup=crypto(amount=data['amount']))
            # cheque = await xRoketApi.invoice_create(amount=float(data['amount']), currency=data['coin'])
            # print(cheque)
            # id = cheque['data']['id']
            # link = cheque['data']['link']
            # await message.answer(lang.payment_link, reply_markup=kb_payment_link(lang=lang, link=link, pay_id=id, method='xrocket'))
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
            # await call.message.delete() #Убрать комментарий
            await call.message.answer('✅ Счет успешно пополнен и зачислен на баланс\n\n🍀 Приятной игры 🍀')
            user = await db.get_user(user_id = call.from_user.id)
            
            await db.add_check(unix=gen_id(), user_id=user['user_id'], transaction_type='deposit', conclusion_id=None, summa=float(invoices.amount))
            if user['ref_id'] is not None:
                referral = await db.get_user(user_id = user['ref_id'])
                user_ref_lvl = referral['ref_lvl']
                game_sett = await db.get_settings(id=1)
                percent = game_sett[f'ref_percent_{user_ref_lvl}']
                ego_procent = float(invoices.amount) * float(percent / 100)
                await db.update_user(id=referral['user_id'], balance=float(referral['balance']) + float(ego_procent), total_refill = float(referral['total_refill']) + float(ego_procent))
                await bot.send_message(referral['user_id'], lang.ref_plus_balance.format(percent=ego_procent))
            await db.update_user(id=call.from_user.id, balance=float(user['balance']) + float(invoices.amount), total_pay=float(user['total_pay']) + float(invoices.amount))
    # elif method == 'xrocket':
    #     invoices = await xRoketApi.invoice_info(invoice_id=pay_id)
    #     status = invoices['data']['status']
    #     if status == 'active':
    #     # if status == 'paid':
    #         await call.answer(lang.not_pay)
    #     if status == 'paid':
    #     # elif status == 'active':
    #         await call.message.delete()
    #         summa = call.data.split(":")[3]
    #         await call.message.answer('✅ Счет успешно пополнен и зачислен на баланс\n\n🍀 Приятной игры на Clams Casino 🍀')
    #         user = await db.get_user(user_id = call.from_user.id)
    #         # rub_amount = TonToRub(float(invoices['data']['amount']))
    #         # rub_amount = round(rub_amount, 2)
    #         if user['ref_id'] is not None:
    #             referral = await db.get_user(user_id = user['ref_id'])
    #             user_ref_lvl = referral['ref_lvl']
    #             game_sett = await db.get_settings(id=1)
    #             percent = game_sett[f'ref_percent_{user_ref_lvl}']
    #             ego_procent = float(float(summa) * float(percent / 100))
    #             await db.update_user(id=referral['user_id'], balance=float(referral['balance']) + float(ego_procent), total_refill = float(referral['total_refill']) + float(ego_procent))
    #             await bot.send_message(referral['user_id'], lang.ref_plus_balance.format(percent=ego_procent))
    #         await db.update_user(id=call.from_user.id, balance=float(user['balance']) + float(summa), total_pay=float(user['total_pay']) + float(summa))