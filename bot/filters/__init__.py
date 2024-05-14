from .filters import IsAdmin
from bot.data.loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)