class Texts:
##########################################################################
################################## Buttons ###############################
##########################################################################
    reply_kb1 = 'Игры 🎮'
    reply_kb2 = 'Профиль 👨‍💻'
    reply_kb3 = 'FAQ 📖'
    reply_kb4 = 'Поддержка 🛎'
    reply_admin = "👩‍💻 Панель администратора"


##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 Зарегистрирован новый пользователь {name}" # {name} - username пользователя 
    welcome = "Добро пожаловать 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link):
        msg = f"""🆔 Ваш ID: {user_id}
                🤖 @Username: {user_name}
                
                💰 Ваш баланс: {balance} 🪙
                💸 Выведено: {balance_vivod}
                
                👥 Приглашено пользователей: {referals} 
                🍬 Доход с рефералов: {referals_sum} | Уровень: {refer_lvl} 
                🔗 Реферальная ссылка: {refer_link}"""
        return msg
        
                