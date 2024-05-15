from aiogram.dispatcher.filters.state import State, StatesGroup


class admin_main_settings(StatesGroup):
    faq = State()
    
class Newsletter(StatesGroup): #State на рассылку
    msg = State()
    
class Newsletter_photo(StatesGroup): #State на рассылку с офто
    msg = State()
    photo = State()

class AdminSettingsEdit(StatesGroup):
    here_support = State()

class AdminCoupons(StatesGroup):    
    here_name_promo = State()
    here_uses_promo = State()
    here_discount_promo = State()
    here_name_for_delete_promo = State()