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
    conclusion = "💸 Вывести баланс"
    refill = "💰 Пополнить баланс"
    groups_list = "Группы 📰"
    support_inl = "⚙️ Тех. Поддержка"
    test_balance = "🏦 Получить демо баланс"
    change_language = "🇷🇺 Изменить Язык"
    promo = "🎫 Промокод"
    new_promo = "💎 Создать промокод"
    del_promo = "🎲 Удалить промокод"
    ####GAMES####
    game_slots = "🎰 Слоты"
    game_dice = "🎲 Кости"
    game_basketball = "🏀 Баскетбол"
    game_bowling = "🎳 Боулинг"
    game_football = "⚽ Футбол"
    game_coin = "🪙 Монетка" 
    adm_edit_factor = "📊 Коэффициент: X{factor}"
    min_bet = "Мин. Ставка: {min_bet} 🪙"
    real_chance = "💸 Шанс победы: {real_chance}%"
    demo_chance = "🏦 Демо шанс: {demo_chance}%"
    use_demo = "💰 Использовать Демо баланс"
    use_real = "💰 Использовать баланс"
    adm_user_revork_bal = "💰 Изменить баланс"
    adm_user_give_bal = "💰 Выдать баланс"
    adm_user_revork_demo = "🏦 Изменить Демо"
    adm_user_give_demo = "🏦 Выдать Демо"
    adm_user_ban = "⛔ Заблокировать"
    adm_user_unban = "🟢 Разблокировать"
    go_next = "Играть еще 🔃"
    

##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 Зарегистрирован новый пользователь {name}" # {name} - username пользователя 
    welcome = "Добро пожаловать 👋"
    admin_menu = "добро пожаловать в меню Администратора 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance, reffer):
        msg = f"""🆔 Ваш ID: <code>{user_id}</code>
                🤖 Username: <code>{user_name}</code>
                
                💰 Ваш баланс: <code>{balance}</code> 🪙
                🏦 Демо баланс: <code>{test_balance}</code>
                💸 Выведено: <code>{balance_vivod}</code>
                
                👥 Приглашено пользователей: <code>{referals}</code> 
                🍬 Доход с рефералов: <code>{referals_sum}</code> | Уровень: <code>{refer_lvl}</code> 
                ⚙️ Вас пригласил: {reffer}
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
    why_ban = "❗Укажите причину блокировки"
    def bet_msg(self, game_name_text, min_bet, user_balance):
        msg = f"""Игра: {game_name_text}
        
                💰 Минимальная ставка: <code>{min_bet}</code> 
                🏦 Ваш баланс: <code>{user_balance}</code> 🪙
                <b>❗ Укажите сумму ставки:</b> """
        return msg
    def bet_msg_demo(self, game_name_text, min_bet, demo_balance):
        msg = f"""Игра: {game_name_text}
        
                💰 Минимальная ставка: <code>{min_bet}</code> 
                
                🏦 Ваш Демо баланс: <code>{demo_balance}</code> 🪙
                <b>❗ Укажите сумму ставки:</b> """
        return msg
    vibor_game_to_edit = "<b>Выберите игру для редактирования 🕹</b>"
    adm_edit_game_menu = "🃏 Игра: <code>{game_name}</code>\n<b>Выберите настройки для изменения</b>"
    admin_edit_real_chance = "📈 Выберите новый шанс победу\n<b>(На реальные деньги)</b>"
    admin_edit_demo_chance = "📉 Выберите новый шанс победу\n<b>(На демо баланс)</b>"
    admin_edit_min_bet = "🌟 Введите новую <b>минимальную ставку</b>"
    admin_edit_factor = "🧮 Введите новый <b>коэффициент</b>"
    admin_open_profile ="""<b>👤 Профиль:
                💎 Юзер: {name} 
                🆔 ID: <code>{user_id}</code>
                📅 Дата регистрации: <code>{total_refill}</code>
                
                💰 Баланс: <code>{balance}</code>
                🏦 Демо баланс: <code>{demo_balance}</code>
                
                ⚙️ Язык бота: <code>{lang}</code>
                💵 Всего пополнено: <code>{tr}</code>
                💵 Выведено: <code>{vivod}</code>
                
                🎱Всего игр: <code>{amount_all_games}</code>
                🎰 Слоты: <code>{amount_slots}</code>
                🎲 Кости: <code>{amount_dice}</code>
                🏀 Баскетбол: <code>{amount_basketball}</code>
                🎳 Боулинг: <code>{amount_bowling}</code>
                ⚽ Футбол: <code>{amount_football}</code>
                🪙 Монетка: <code>{amount_coin}</code>
                
                🔗 Статус блокировки: <code>{ban_status}</code>
                {cause_ban}
                👥 Рефералов: <code>{count_refers} чел</code>
                💎 Заработано с рефералов: <code>{referalst_summa}</code>
                📜 Список рефералов: \n</b>"""
    need_number = "<b>Нужно ввести число!</b>"
    wright_summ = "<b>Введите сумму:</b>"
    invite_yourself = "<b>❗ Вы не можете пригласить себя</b>"
    yes_reffer = f"<b>❗ У вас уже есть рефер!</b>"
    new_refferal = "<b>💎 У вас новый реферал! @{user_name} \n" \
                "⚙️ Теперь у вас <code>{user_ref_count}</code> {convert_ref}!</b>"
    ref_s = ['реферал', 'реферала', 'рефералов']  # не трогать скобки
    new_ref_lvl = "<b>💚 У вас новый реферальный уровень, {new_lvl}! До {next_lvl} уровня осталось {remain_refs} {convert_ref}</b>"
    max_ref_lvl = f"<b>💚 У вас новый реферальный уровень, 3! Максимальный уровень!</b>"
    cur_max_lvl = f"💚 У вас максимальный уровень!</b>"
    next_lvl_remain = "💚 До следующего уровня осталось пригласить <code>{remain_refs} чел</code></b>"
    nobody = "<code>Никто</code>"
    no_money = "Недостаточно баланса!"
    no_sub = "<b>❗ Ошибка!\nВы не подписались на канал.</b>"
    def lose_game(self, summ, balance):
        msg = f"""<b>Увы, вы проиграли 🥴</b>
                    
                    Ваш проигрыш: -{summ} 🪙
                    
                    Ваш баланс: {balance} 🪙"""
        return msg
    def win_game(self, summ, balance, kef):
        msg = f"""<b>Ура, вы выйграли 🤩</b>
                    
                    Коэффициент: X{kef}
                    Ваш выйгрыш: {summ} 🪙
                    
                    Ваш баланс: {balance} 🪙"""
        return msg
    refil_sposob = "💳 Выберите способ пополнения"
    choose_coin = "Выберите сторону монетки 🪙"
    Eagle = "🦅 Орел"
    Tails = "1️⃣ Решка"