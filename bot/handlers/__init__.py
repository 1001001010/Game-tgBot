# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from .errors import dp
from .main_start import dp
from .admin import dp
from .user import dp

__all__ = ['dp']