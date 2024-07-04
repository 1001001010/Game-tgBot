from aiogram.dispatcher.filters.state import State, StatesGroup


class admin_main_settings(StatesGroup):
    faq = State()
    
class Newsletter(StatesGroup):
    msg = State()
    
class Newsletter_photo(StatesGroup):
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
    here_check = State()
    
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
    
class АdminCheckSend(StatesGroup):
    user_id = State()
    check = State()

class AdminMail(StatesGroup):
    here_text_mail_text = State()
    here_text_mail_photo = State()
    here_photo_mail_photo = State()
    here_name_for_add_mail_button = State()
    here_new_name_for_mail_button = State()
    here_link_for_add_mail_button = State()
    here_category_for_open_mail = State()
    here_category_for_pod_open_mail = State()
    here_category_for_pos_open_mail = State()
    here_pod_category_for_pod_open_mail = State()
    
class AdminPrButtons(StatesGroup):
    here_name_pr_button_create = State()
    here_name_pr_button_delete = State()
    here_txt_pr_button_create = State()
    here_photo_pr_button_create = State()