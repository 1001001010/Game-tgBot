from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputFile 
import asyncio

from bot.data.config import lang_ru, lang_en
from bot.data.loader import dp, bot
from bot.data.config import db
from bot.utils.utils_functions import get_language, ded, send_admins
from bot.filters.filters import IsAdmin
from bot.state.admin import admin_main_settings, Newsletter, Newsletter_photo, AdminSettingsEdit
from bot.keyboards.inline import admin_menu, admin_settings, back_to_adm_m, mail_types, opr_mail_text, opr_mail_photo

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
    
@dp.message_handler(state=Newsletter_photo.msg)
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
    
@dp.message_handler(state=Newsletter.msg)
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