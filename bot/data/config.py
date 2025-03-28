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
channel_id = read_config['settings']['channel_id'].strip().replace(" ", "")
pay_chat = read_config['settings']['pay_chat'].strip().replace(" ", "")
channel_url = read_config['settings']['channel_url'].strip().replace(" ", "")
cryptobot_token = read_config['settings']['crypto_bot_token']
# xrocket_token = read_config['settings']['xrocket_token']
path_database = "tgbot/data/database.db"  # Путь к Базе Данных
admin_chat = read_config['settings']['admin_chat']

game_slots = {
    'slots': 'game_slots',
    'coin': 'game_coin',
    'basketball': 'game_basketball',
    'football': 'game_football',
    'bowling': 'game_bowling',
    'dice': 'game_dice',
    'darts': 'game_darts'
}

#Не трогать, стикеры монетки
win_coin_sticker_id = 'CAACAgIAAxkBAAEMJ5NmTAHfILlZIWv31_PP5SRf5sPtwgAClhcAAsiE0Ui67wnmqzpt6TUE'
lose_coin_sticker_id = 'CAACAgIAAxkBAAEMJ5VmTAHkumw8jh7ZWMxTwxpiRCSVZAACpRcAAgaN0Egkmq4OpEO-oDUE'

#Фото для сообщений 
img_welcome = 'AgACAgIAAxkBAAIEd2aKgnQKJ8uHd8yauVXGgzD884HuAAIb5zEbvOVRSJK69zKnUkQHAQADAgADeQADNQQ'
img_support = 'AgACAgIAAxkBAAIEeWaKgprp0PXP_J9GKM9I48FDQ81RAAId5zEbvOVRSEOvzIUdkqy1AQADAgADeQADNQQ'
img_rules = 'AgACAgIAAxkBAAIEe2aKgrNBjFPLq2AbXWqLPGQXVuzHAAIf5zEbvOVRSLG1G99Hfj9uAQADAgADeQADNQQ'
img_profile = 'AgACAgIAAxkBAAIEfWaKgsRo-8xrHis8F9CVicpx9GcbAAIi5zEbvOVRSHrUliLT1KL0AQADAgADeQADNQQ'
img_games = 'AgACAgIAAxkBAAIEf2aKgtMdkNXgCddOqPziQ5x48qCCAAIj5zEbvOVRSLamqeabkhmZAQADAgADeQADNQQ'