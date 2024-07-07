class Texts:
##########################################################################
################################## Buttons ###############################
##########################################################################
    reply_kb1 = '🕹 Игры'
    reply_kb2 = '👨‍💻 Профиль'
    reply_kb3 = '📖 Правила'
    reply_kb4 = '🚑 Поддержка'
    reply_admin = "👩‍💻 Панель администратора"
    back = "🔙 В главное меню"
    back_to_adm_m = "🔙 Назад"
    back = "⬅ Вернуться"
    conclusion = "💸 Вывести баланс"
    refill = "💳 Пополнить баланс"
    groups_list = "Группы 📰"
    support_inl = "🌟 Саппорт"
    test_balance = "🏦 Получить демо баланс"
    change_language = "🇷🇺 Изменить Язык"
    promo = "🎫 Промокод"
    new_promo = "💎 Создать промокод"
    del_promo = "🎲 Удалить промокод"
    ####GAMES####
    game_slots = "🎰 Слоты"
    game_dice = "🎲 Кости"
    game_darts = "🎯 Дартс"
    game_basketball = "🏀 Баскетбол"
    game_bowling = "🎳 Боулинг"
    game_football = "⚽ Футбол"
    game_coin = "🪙 Монетка" 
    adm_edit_factor = "📊 Коэффициент: X{factor}"
    min_bet = "Мин. Ставка: {min_bet} 🪙"
    real_chance = "💸 Шанс победы: {real_chance}%"
    demo_chance = "🏦 Демо шанс: {demo_chance}%"
    use_demo = "💰 Использовать Демо баланс"
    use_real = "💎 Использовать баланс"
    adm_user_revork_bal = "💰 Изменить баланс"
    adm_user_give_bal = "💰 Выдать баланс"
    adm_user_revork_demo = "🏦 Изменить Демо"
    adm_user_give_demo = "🏦 Выдать Демо"
    adm_user_ban = "⛔ Заблокировать"
    adm_user_unban = "🟢 Разблокировать"
    go_next = "Играть еще 🔃"
    pay_link = "💸 Оплатить"
    pay_id = "🎆 Проверить оплату"
    edit_network = "Изменить сеть"
    back_vivod_to_method = "⬅️ Изменить способ"
     

##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 Зарегистрирован новый пользователь {name}" # {name} - username пользователя 
    welcome = """👋 <b>Добро пожаловать в лучшего игрового бота</b> 🎲\n\n🤖 В нашем боте есть множество игр для вашего развлечения\n\n📰Следи за новостями в канале!\nПостонные <code>🎁 розыгрыши</code> и <code>🎫 промокоды</code>\nЕсли необходима помощь, вам всегда поможет наш <code>🚑 саппорт</code>\n\n<b>💚 3 Уровневая реферальная система</b>, чтобы играть с друзьями было веселее\n\n<b>🧠 Ознакомиться с правилами вы можете перейдя в раздел 📖Правила</b>"""
    admin_menu = "добро пожаловать в меню Администратора 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance, reffer):
        msg = f"""🆔 Ваш ID: <code>{user_id}</code>
                👑 Username: <code>{user_name}</code>
                
                💰 Ваш баланс: ₽ <code>{balance}</code>
                🏦 Демо баланс: ₽ <code>{test_balance}</code>
                💸 Выведено: ₽ <code>{balance_vivod}</code>
                
                👥 Приглашено пользователей: <code>{referals}</code> 
                🌃 Доход с рефералов: ₽ <code>{referals_sum}</code> | Уровень: <code>{refer_lvl}</code> 
                ⭐ Вас пригласил: {reffer}
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
    yes_support = "<b>🚑 Нужна помощь? Обращайся к нашему саппорту\nВрем ответа до 12ч</b>"
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
    game_menu = "<b>🎮 Выберите игру</b>"
    why_ban = "❗Укажите причину блокировки"
    incorrect_amount = "Введите сумму от ₽ <code>1</code> до <code>1000</code>"
    is_work_text = f"<b>❌ Бот находиться на тех. работах!</b>"
    is_work_text = f"<b>❌ The bot is on those. works!</b>"
    def bet_msg(self, game_name_text, min_bet, user_balance):
        msg = f"""<b>Игра:</b> {game_name_text}
        
                <b>📉 Минимальная ставка:</b> ₽ <code>{min_bet}</code>
                <b>💰 Ваш баланс:</b> ₽ <code>{user_balance}</code>
                
                <b>✍ Укажите сумму ставки:</b> """
        return msg
    def bet_msg_demo(self, game_name_text, min_bet, demo_balance):
        msg = f"""<b>Игра:</b> {game_name_text}
        
                <b>📉 Минимальная ставка:</b> ₽ <code>{min_bet}</code> 
                <b>🏦 Ваш Демо баланс:</b> ₽ <code>{demo_balance}</code>
                
                <b>✍ Укажите сумму ставки:</b> """
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
                
                💰 Баланс: ₽ <code>{balance}</code>
                🏦 Демо баланс: ₽ <code>{demo_balance}</code>
                
                ⚙️ Язык бота: <code>{lang}</code>
                💵 Пополнено: ₽ <code>{tr}</code>
                💵 Выведено: ₽ <code>{vivod}</code>
                
                🎱Всего игр: <code>{amount_all_games}</code>
                🎰 Слоты: <code>{amount_slots}</code>
                🎲 Кости: <code>{amount_dice}</code>
                🏀 Баскетбол: <code>{amount_basketball}</code>
                🎳 Боулинг: <code>{amount_bowling}</code>
                ⚽ Футбол: <code>{amount_football}</code>
                🪙 Монетка: <code>{amount_coin}</code>
                🎯 Дартс: <code>{amount_darts}</code>
                
                🔗 Статус блокировки: <code>{ban_status}</code>
                {cause_ban}
                👥 Рефералов: <code>{count_refers} чел</code>
                💎 Заработано с рефералов: ₽ <code>{referalst_summa}</code>
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
        msg = f"""<b>😞 Проигрыш</b>
                    
                    Вы проиграли: ₽ <code>-{summ}</code>
                    
                    🏦 Ваш баланс: ₽ <code>{balance}</code>"""
        return msg
    def win_game(self, summ, balance, kef):
        msg = f"""<b>🎉 Выйгрыш</b>
                    
                    Коэффициент: X<code>{kef}</code>
                    Ваш выйгрыш: ₽ <code>{summ}</code>
                    
                    🏦 Ваш баланс: ₽ <code>{balance}</code>"""
        return msg
    refil_sposob = "💎 Выберите способ пополнения"
    choose_coin = "Выберите сторону монетки 🪙"
    Eagle = "🦅 Орел"
    Tails = "1️⃣ Решка"
    need_summa_cryptobot = "Введите сумму в <b>₽</b>"
    payment_link = "💠 Оплатите по ссылке ниже и нажимите проверить оплату"
    not_pay = "❌ Платёж не найден"
    yes_pay = "✅ Успешно оплачено"
    success_pay = "💰 Баланс успешно пополнен"
    ref_plus_balance = "💚 Ваш реферал пополнил баланс, ваш процент: {percent}"
    your_cube = "Ваш кубик ⬇️"
    enemy_cube = "Кубик противника ⬇️"
    bank_money = "Ничья!\nДеньги возвращены на баланс"
    vibor_crypto = "💎 Выберите желаемую криптовалюту для оплаты"
    summa_vivoda = "💰 Ваш баланс: <code>{balance}</code>\n\nВведите сумму для вывода: "
    need_Crypto = "<b>📤 Вывод</b>\nВыберите способ для вывода: "
    need_adress = "Введите адресс для вывода"
    need_network = "<b>Выберите сеть для отправки баланса USDT</b>"
    succes_msg = "Ваша заявка успешно отправлена, ожидайте ее подтверждения"
    need_balance = "Недостаточно баланса"
    otklon_vivod = "Отмененно"
    vivod_mimo = "Ваша заявка на вывод была отклонена администратором\nДеньги возвращены на баланс"
    vivod_success_msg = "Ваша заявка на вывод была одобрена!\nОжидайте поступления средств ⏳"
    vivod_success_msg_check = "Ваша заявка на вывод была одобрена!\n\nВам напишет администратор и выдаст ваш чек\n\nОжидайте ⏳"
    Confirmation_msg = """
        <b>Проверка и подтверждение</b>
        
        <b>Сеть:</b> <code>{network}</code>
        <b>Адрес:</b> <code>{adress}</code>
        
        <b>Выводите:</b> <code>{amount_vivod}</code>
        <b>Комиссия:</b> <code>{comma_vivod}</code>
        
        <b>Итог:</b> <code>{full_summa}</code>
        
        <b>Вы уверены что хотите вывести эту сумму?</b>     
        """
    need_real_adress = "😞 Некорректный адрес. Пришлите верный адрес кошелька, который нахоится в сети {crypto}."
    Confirmation_msg_chek = """
        <b>Проверка и подтверждение</b>
        
        <b>Выводите:</b> <code>{amount_vivod}</code>
        <b>Комиссия:</b> <code>{comma_vivod}</code>
        
        <b>Итог:</b> <code>{full_summa}</code>
        
        <b>Вы уверены что хотите вывести эту сумму?</b>     
        """