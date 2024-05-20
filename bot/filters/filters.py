from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from bot.utils.utils_functions import get_admins
from bot.data.config import db
from bot.data import config
from bot.data.loader import bot

class IsAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return user_id in get_admins()
    
class IsBan(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = await db.get_user(user_id=message.from_user.id)
        if user['is_ban'] == True and not user['id'] in get_admins():
            return True
        else:
            return False
        
class IsSub(BoundFilter):
    async def check(self, message: Message):
        channel_id = config.channel_id
        if channel_id == "":
            return False
        else:
            user_status = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
            if user_status["status"] == 'left':
                return True
            else:
                return False