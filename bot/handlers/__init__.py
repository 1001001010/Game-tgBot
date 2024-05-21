# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from .errors import dp
from .main_start import dp
from .admin import dp
from .user import dp
from .game import dp
from .payment import dp

__all__ = ['dp']