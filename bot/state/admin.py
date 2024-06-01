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
    here_count_lvl_ref = State()
    here_ref_percent = State()

class AdminCoupons(StatesGroup):    
    here_name_promo = State()
    here_uses_promo = State()
    here_discount_promo = State()
    here_name_for_delete_promo = State()
    
class AdminFind(StatesGroup):
    here_user = State()
    
class AdminBanCause(StatesGroup):
    cause = State()
    user_id = State()

class AdminGame_edit(StatesGroup):
    game = State()
    param = State()
    value = State()
    
class AdminRevorkPrice(StatesGroup):
    type = State()
    user_id = State()
    summa = State()
    
class AdminPlusPrice(StatesGroup):
    type = State()
    user_id = State()
    summa = State()

class АdminMethod(StatesGroup):
    percent = State()
    method = State()
    
class АdminVivoCheack(StatesGroup):
    percent = State()
    