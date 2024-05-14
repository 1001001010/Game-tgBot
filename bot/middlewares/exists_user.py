# - *- coding: utf- 8 - *-
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from bot.data.config import db
from bot.utils.utils_functions import send_admins
from bot.data.loader import bot
from loguru import logger
from bot.data.config import lang_ru as texts
from bot.keyboards.inline import choose_languages_kb


class ExistsUserMiddleware(BaseMiddleware):

    def __init__(self):
        super(ExistsUserMiddleware, self).__init__()

    async def on_process_update(self, update: Update, data: dict):
        user = update
        if "message" in update:
            user = update.message.from_user
            logger.info(f"{user.full_name} - {update.message.text}")
        elif "callback_query" in update:
            user = update.callback_query.from_user
            logger.info(f"{user.full_name} - {update.callback_query.data} (Callback)")
        try:
            if user is not None:
                if not user.is_bot:
                    self.id = user.id
                    self.user_name = user.username
                    self.first_name = user.first_name
                    self.bot = await bot.get_me()
                    if self.user_name is None:
                        self.user_name = ""
                    if await db.get_user(user_id=self.id) is None:
                        await db.register_user(user_id=self.id, user_name=self.user_name, first_name=self.first_name)
                        name = f"@{self.user_name}"
                        if self.user_name == "":
                            us = await bot.get_chat(self.id)
                            name = us.get_mention(as_html=True)
                        await bot.send_message(chat_id=self.id, text="<b>Выберите язык / Select language</b>",
                                                   reply_markup=await choose_languages_kb())
                        await send_admins(f"<b>{texts.reg_user.format(name=name)}</b>", False)
                    else:
                        self.user = await db.get_user(user_id=self.id)
                        if self.user['user_name'] != self.user_name:
                            await db.update_user(self.id, user_name=self.user_name)
                        if self.user['first_name'] != self.first_name:
                            await db.update_user(self.id, first_name=self.first_name)

                        if len(self.user_name) >= 1:
                            if self.user_name != self.user['user_name']:
                                await db.update_user(self.id, user_name=self.user_name)
                        else:
                            await db.update_user(self.id, user_name="")
        except:
            pass