# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from bot.middlewares.exists_user import ExistsUserMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware


# Подключение милдварей
def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(ExistsUserMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())