class Texts:
##########################################################################
################################## Buttons ###############################
##########################################################################
    reply_kb1 = 'Games 🎮'
    reply_kb2 = 'Profile 👨‍💻'
    reply_kb3 = 'FAQ 📖'
    reply_kb4 = 'Support 🛎'
    reply_admin = "👩‍💻Admin Panel"
    back = "🔙 To main menu"
    back_to_adm_m = "🔙 Back"
    back = "⬅ Back"
    support_inl = "⚙️ Support"
    test_balance = "Получить демо баланс"
    change_language = "Язык"
    promo = "Ввести промокод"
    new_promo = "💎 Создать промокод"   
    del_promo = "🎲 Удалить промокод"

##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 New user {name} has been registered" # {name} - username of the user
    welcome = "Welcome 👋"
    admin_menu = "welcome to the Administrator menu 👋"
    def open_profile(self, user_id, user_name, balance, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance):
        msg = f"""🆔 Your ID: {user_id}
                🤖 @Username: {user_name}
                
                💰 Your balance: {balance}   
                Демо баланс: {test_balance}
                💸 Displayed by: {balance_vivod}
                
                👥 Users invited: {referals}
                🍬 Income from referrals: {referals_sum} | Level: {refer_lvl}
                🔗 Referral link: {refer_link}"""
        return msg
    admin_settings = "⚙️ Settings Menu"
    admin_edit_faq = "✍ Enter new text for FAQ"
    faq_success = "✅ FAQ Changed successfully"
    admin_mail = "❗ Select mailing type"
    mail_only_text = "💎 Just text"
    mail_with_photo = "🖼Text with picture"
    admin_text_send = "🖊️ Enter your newsletter text"
    admin_newsletter = "✍ Send a message for newsletter"
    admin_photo_send = "🖼️ Send a photo for mailing"
    no_support = "<b>⚙️ The owner of the bot did not leave a link to support!</b>"
    yes_support = "<b>📩 To contact Support press the bottom button:</b>"
    yes_demo = "Демо баланс успешно выдан"
    no_demo = "Вы уже получали демо баланс"
    promo_menu = "Выберите действие"