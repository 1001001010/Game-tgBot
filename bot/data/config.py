# - *- coding: utf- 8 - *-
import configparser
import asyncio
from datetime import datetime, timedelta
from bot.data.lang import ru, en
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.aaio import AsyncAaio

from bot.data.db import DB

# Создание экземпляра бд 
async def main_db():
    db = await DB()

    return db

lang_ru = ru.Texts()
lang_en = en.Texts()

loop = asyncio.get_event_loop()
task = loop.create_task(main_db())
db = loop.run_until_complete(task)

BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота

# Чтение конфига
read_config = configparser.ConfigParser()
read_config.read("settings.ini")

bot_token = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
path_database = "tgbot/data/database.db"  # Путь к Базе Данных

# CryptoBot
cryptoBot = AsyncCryptoBot(read_config['settings']['crypto_bot_token'].strip().replace(" ", ""))

xrocket = read_config['settings']['crypto_bot_token'].strip().replace(" ", "")

game_slots = {
    'slots': 'game_slots',
    'coin': 'game_coin',
    'basketball': 'game_basketball',
    'football': 'game_football',
    'bowling': 'game_bowling',
    'dice': 'game_dice'
}