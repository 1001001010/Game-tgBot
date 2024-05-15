from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 
import asyncio

from bot.data.config import lang_ru, lang_en
from bot.data.loader import dp, bot
from bot.data.config import db
from bot.utils.utils_functions import get_language, ded, send_admins, get_admins
from bot.filters.filters import IsAdmin
from bot.state.admin import admin_main_settings, Newsletter, Newsletter_photo, AdminSettingsEdit, AdminCoupons
from bot.keyboards.inline import admin_menu, admin_settings, back_to_adm_m, mail_types, opr_mail_text, opr_mail_photo, kb_adm_promo

#Открытие Профиля
@dp.message_handler(IsAdmin(), text=lang_ru.reply_admin, state="*")
@dp.message_handler(IsAdmin(), text=lang_en.reply_admin, state="*")
async def func__admin_menu(message: Message, state: FSMContext):
    await state.finish()
    lang = await get_language(message.from_user.id)
    await message.answer(lang.admin_menu, reply_markup=admin_menu(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text='settings', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.delete()
    await call.message.answer(lang.admin_settings, reply_markup=admin_settings(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text='settings_faq', state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.admin_edit_faq, reply_markup=back_to_adm_m(texts=lang))
    await admin_main_settings.faq.set()
    
@dp.message_handler(IsAdmin(), state=admin_main_settings.faq)
async def adm_edit_faq(message: Message, state: FSMContext):
    msg = message.parse_entities()
    lang = await get_language(message.from_user.id)
    await state.update_data(msg=msg)
    data = await state.get_data()
    await db.update_settings(FAQ=data['msg'])
    await message.answer(lang.faq_success, reply_markup=admin_menu(texts=lang))
    await state.finish()
#Статистика
@dp.callback_query_handler(IsAdmin(), text='stats', state="*")
async def open_stats(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    all_user, show_users_week, show_users_day = 0, 0, 0
    all_users = await db.all_users()
    settings = await db.get_only_settings()
    admin_count = len(get_admins())
    for user in all_users:
        if int(user['reg_date_unix']) - int(settings['profit_day']) >= 0:
            show_users_day += 1

        if int(user['reg_date_unix']) - int(settings['profit_week']) >= 0:
            show_users_week += 1
        all_user += 1

    msg = f"""Статистика
    
    Всего пользователей: {all_user}
    Ползователей за неделю {show_users_week}
    Пользователей за день {show_users_day}

    Всего администраторово: {admin_count}"""
    await call.message.answer(ded(msg))

#Рассылка
@dp.callback_query_handler(IsAdmin(), text_startswith="mail_start", state="*")
async def func_newsletter(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.admin_mail, reply_markup=mail_types(texts=lang))
    
@dp.callback_query_handler(IsAdmin(), text_startswith="rmail", state="*")
async def func_newsletter(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    type_id = call.data.split(":")[1]
    lang = await get_language(call.from_user.id)
    if type_id == 'text':
        await call.message.answer(lang.admin_newsletter, reply_markup=back_to_adm_m(texts=lang))
        await Newsletter.msg.set()
    elif type_id == 'photo':
        await call.message.answer(lang.admin_text_send, reply_markup=back_to_adm_m(texts=lang))
        await Newsletter_photo.msg.set()
    
@dp.message_handler(IsAdmin(), state=Newsletter_photo.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await state.update_data(msg=msg)
    lang = await get_language(message.from_user.id)
    await message.answer(lang.admin_photo_send, reply_markup=back_to_adm_m(texts=lang))
    await Newsletter_photo.photo.set()
    
@dp.message_handler(IsAdmin(), content_types=['photo'], state=Newsletter_photo.photo)
async def mail_photo_starts(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_photo(chat_id=user_id, photo=data['photo'] ,caption=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()
    
@dp.message_handler(IsAdmin(), state=Newsletter.msg)
async def func_newsletter_text(message: Message, state: FSMContext):
    msg = message.parse_entities()
    await state.update_data(msg=msg)
    data = await state.get_data()
    await send_admins(f"<b>❗ Администратор @{message.from_user.username} запустил рассылку!</b>")
    users = await db.all_users()
    yes_users, no_users = 0, 0
    for user in users:
        user_id = user['id']
        try:
            user_id = user['user_id']
            await bot.send_message(chat_id=user_id, text=data['msg'])
            yes_users += 1
        except:
            no_users += 1

    new_msg = f"""
<b>💎 Всего пользователей: <code>{len(await db.all_users())}</code>
✅ Отправлено: <code>{yes_users}</code>
❌ Не отправлено (Бот заблокирован): <code>{no_users}</code></b>
    """

    await message.answer(new_msg)
    await state.finish()
    
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_supp", state="*")
async def settings_set_sup(call: CallbackQuery):
    await AdminSettingsEdit.here_support.set()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text("<b>⚙️ Введите ссылку на пользователя (https://t.me/юзернейм)</b>"
                                 "❕ Отправьте <code>-</code> чтобы оставить пустым.", reply_markup=back_to_adm_m(texts=lang))
    
@dp.message_handler(IsAdmin(), state=AdminSettingsEdit.here_support)
@dp.message_handler(IsAdmin(), text="-", state=AdminSettingsEdit.here_support)
async def settings_sup_set(message: Message, state: FSMContext):
    await state.finish()
    if message.text.startswith("https://t.me/") or message.text == "-":
        await db.update_settings(support=message.text)
        await send_admins(
            f"<b>❗ Администратор  @{message.from_user.username} изменил Тех. Поддержку на: \n{message.text}</b>")
        await message.answer("<b>✅ Готово! Тех. Поддержка была изменена!</b>")
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/юзернейм)</b> ")

#Прмокод
@dp.callback_query_handler(text="adm_promo", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    lang = await get_language(call.from_user.id)
    await call.message.answer(lang.promo_menu, reply_markup=kb_adm_promo(texts=lang))

@dp.callback_query_handler(text="promo_create", state="*")
async def promo_create(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminCoupons.here_name_promo.set()

@dp.message_handler(state=AdminCoupons.here_name_promo)
async def here_name_promo(msg: Message, state: FSMContext):
    name = msg.text
    await msg.answer(f"<b>❗ Введите кол-во использований</b>")
    await state.update_data(cache_name_for_add_promo=name)
    await AdminCoupons.here_uses_promo.set()

@dp.message_handler(state=AdminCoupons.here_uses_promo)
async def here_uses_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        await msg.answer("<b>❗ Введите сумму промокода</b>")
        await state.update_data(cache_uses_for_add_promo=int(msg.text))
        await AdminCoupons.here_discount_promo.set()
    else:
        await msg.answer("<b>❗ Кол-во использований должно быть числом!</b>")

@dp.message_handler(state=AdminCoupons.here_discount_promo)
async def here_discount_promo(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            name = data['cache_name_for_add_promo']
            uses = data['cache_uses_for_add_promo']
        await state.finish()
        summa_promo = int(msg.text)
        await db.create_coupon(name, uses, summa_promo)
        await msg.answer(
            f"<b>✅ Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и суммой <code>{summa_promo}</code> был создан!</b>")
        await send_admins(
            f"<b>❗ Администратор  @{msg.from_user.username} создал Промокод <code>{name}</code> с кол-вом использований <code>{uses}</code> и скидкой <code>{summa_promo}</code></b>")
    else:
        await msg.answer("<b>❗ Скидка должна быть числом!</b>")

@dp.callback_query_handler(text="promo_delete", state="*")
async def promo_del(call: CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_language(call.from_user.id)
    await call.message.edit_text(f"<b>❗ Введите название промокода</b>", reply_markup=back_to_adm_m(texts=lang))
    await AdminCoupons.here_name_for_delete_promo.set()


@dp.message_handler(state=AdminCoupons.here_name_for_delete_promo)
async def promo_delete(msg: Message, state: FSMContext):
    promo = await db.get_promo(coupon=msg.text)
    print(promo)
    if promo == None:
        await msg.answer(f"<b>❌ Промокода <code>{msg.text}</code> не существует!</b>")
    else:
        await db.delete_coupon(msg.text)
        await state.finish()
        await msg.answer(f"<b>✅ Промокод <code>{msg.text}</code> был удален</b>")
        await send_admins(f"<b>❗ Администратор  @{msg.from_user.username} удалил Промокод <code>{msg.text}</code></b>")