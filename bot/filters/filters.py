from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from bot.utils.utils_functions import get_admins
from bot.data.config import db

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