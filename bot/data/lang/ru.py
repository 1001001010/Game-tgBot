class Texts:
##########################################################################
################################## Buttons ###############################
##########################################################################
    reply_kb1 = 'Игры 🎮'
    reply_kb2 = 'Профиль 👨‍💻'
    reply_kb3 = 'FAQ 📖'
    reply_kb4 = 'Поддержка 🛎'
    reply_admin = "👩‍💻 Панель администратора"
    back = "🔙 В главное меню"
    back_to_adm_m = "🔙 Назад"
    back = "⬅ Вернуться"
    support_inl = "⚙️ Тех. Поддержка"
    test_balance = "🏦 Получить демо баланс"
    change_language = "🎌 Смменить Язык"
    promo = "🎫 Ввести промокод"
    new_promo = "💎 Создать промокод"
    del_promo = "🎲 Удалить промокод"
    ####GAMES####
    game_slots = "🎰 Слоты"
    game_dice = "🎲 Кости"
    game_basketball = "🏀 Баскетбол"
    game_bowling = "🎳 Боулинг"
    game_football = "⚽ Футбол"
    game_coin = "🪙 Монетка"
    adm_edit_factor = "Коэффициент: X{factor}"
    min_bet = "Мин. Ставка: {min_bet} 🪙"
    real_chance = "Реальный шанс: {real_chance}%"
    demo_chance = "Демо шанс: {demo_chance}%"
    

##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 Зарегистрирован новый пользователь {name}" # {name} - username пользователя 
    welcome = "Добро пожаловать 👋"
    admin_menu = "добро пожаловать в меню Администратора 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance):
        msg = f"""🆔 Ваш ID: <code>{user_id}</code>
                🤖 Username: <code>{user_name}</code>
                
                💰 Ваш баланс: <code>{balance}</code> 🪙
                🏦 Демо баланс: <code>{test_balance}</code>
                💸 Выведено: <code>{balance_vivod}</code>
                
                👥 Приглашено пользователей: <code>{referals}</code> 
                🍬 Доход с рефералов: <code>{referals_sum}</code> | Уровень: <code>{refer_lvl}</code> 
                🔗 Реферальная ссылка: 
                <code>{refer_link}</code>"""
        return msg
    admin_settings = "⚙️ Меню настроек"
    admin_edit_faq = "✍ Введите новый текст для FAQ"   
    faq_success = "✅ FAQ Успешно измененно"
    admin_mail = "❗ Выберите тип рассылки" 
    mail_only_text = "💎 Просто текст"
    mail_with_photo = "🖼 Текст с картинкой"
    admin_text_send = "🖊️ Введите текст рассылки"
    admin_newsletter = "✍ Отправьте сообщение для рассылки"
    admin_photo_send = "🖼️ Отправьте фото для рассылки"
    no_support = "<b>⚙️ Владелец бота не оставил ссылку на Тех. Поддержку!</b>"
    yes_support = "<b>📩 Чтобы обратиться в Тех. Поддержку нажмите на кнопку снизу:</b>"
    yes_demo = "✅ Демо баланс успешно выдан"
    no_demo = "❌ Вы уже получали демо баланс"
    promo_menu = "👇 Выберите действие"
    promo_act = "<b>📩 Для активации промокода напишите его название</b>\n" \
                "<b>⚙️ Пример: promo2023</b>"
    no_coupon = "<b>❌ Промокода <code>{coupon}</code> не существует!</b>"
    no_uses_coupon = "<b>❌ Вы не успели активировать промокод!</b>"
    yes_coupon = "<b>✅ Вы успешно активировали промокод и получили <code>{summa}</code>!</b>"
    yes_uses_coupon = "<b>❌ Вы уже активировали данный промокод!</b>"
    is_ban_text = "<b>❌ Вы были заблокированы в боте!</b>\nПричина Блокировки: {ban_msg}"
    game_menu = "<b>Выберите режим игры 🕹</b>"
    adm_user_ban = "⛔ Заблокировать"
    adm_user_unban = "🟢 Разблокировать"
    adm_user_revork_bal = "💰 Изменить баланс"
    adm_user_give_bal = "💰 Выдать баланс"
    adm_user_revork_demo = "🏦 Изменить Демо"
    adm_user_give_demo = "🏦 Выдать Демо"
    why_ban = "❗Укажите причину блокировки"
    def bet_msg(self, game_name_text, min_bet, user_balance):
        msg = f"""Игра: {game_name_text}
        
                💰 Минимальная ставка: {min_bet} 
                🏦 Ваш баланс: {user_balance}
                ❗ Укажите сумму ставки: """
        return msg
    vibor_game_to_edit = "<b>Выберите игру для редактирования 🕹</b>"
    adm_edit_game_menu = "Игра {game_name}\nВыберите настройку для изменения"
    admin_edit_real_chance = "Выберите новый шанс победы (На реальные деньги)"
    admin_edit_demo_chance = "Выберите новый шанс победы (На демо баланс)"