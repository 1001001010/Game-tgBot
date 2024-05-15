class Texts:
################################################## #########################
################################## Buttons ############### ################
################################################## #########################
    reply_kb1 = 'Games 🎮'
    reply_kb2 = 'Profile 👨‍💻'
    reply_kb3 = 'FAQ 📖'
    reply_kb4 = 'Support 🛎'
    reply_admin = "👩‍💻Admin Panel"
    back = "🔙 To main menu"
    back_to_adm_m = "🔙 Back"
    back = "⬅Back"
    support_inl = "⚙️ Tech. Support"
    test_balance = "🏦 Get demo balance"
    change_language = "🎌 Change Language"
    promo = "🎫 Enter promo code"
    new_promo = "💎 Create a promotional code"
    del_promo = "🎲 Remove promo code"
    ####GAMES####
    game_slots = "🎰 Slots"
    game_dice = "🎲 Dice"
    game_basketball = "🏀 Basketball"
    game_bowling = "🎳 Bowling"
    game_football = "⚽ Football"
    game_coin = "🪙 Coin" 

################################################## #########################
################################## Messages ############### ################
################################################## #########################
    reg_user = "💎 New user {name} has been registered" # {name} - username of the user
    welcome = "Welcome 👋"
    admin_menu = "welcome to the Administrator menu 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance):
        msg = f"""🆔 Your ID: {user_id}
                🤖 Username: {user_name}
            
                💰 Your balance: {balance} 🪙
                🏦 Demo balance: {test_balance}
                💸 Displayed by: {balance_vivod}
            
                👥 Users invited: {referals}
                🍬 Income from referrals: {referals_sum} | Level: {refer_lvl}
                🔗 Referral link: {refer_link}"""
        return msg
    admin_settings = "⚙️ Settings menu"
    admin_edit_faq = "✍ Enter new text for FAQ"
    faq_success = "✅ FAQ Changed successfully"
    admin_mail = "❗ Select mailing type"
    mail_only_text = "💎 Just text"
    mail_with_photo = "🖼Text with picture"
    admin_text_send = "🖊️ Enter your newsletter text"
    admin_newsletter = "✍ Send a message for newsletter"
    admin_photo_send = "🖼️ Send a photo for mailing"
    no_support = "<b>⚙️ The owner of the bot did not leave a link to Technical Support!</b>"
    yes_support = "<b>📩 To contact Technical Support, click on the button below:</b>"
    yes_demo = "✅ Demo balance issued successfully"
    no_demo = "❌ You have already received demo balance"
    promo_menu = "👇 Select an action"
    promo_act = "<b>📩 To activate a promo code, write its name</b>\n" \
                "<b>⚙️ Example: promo2023</b>"
    no_coupon = "<b>❌ Promo code <code>{coupon}</code> does not exist!</b>"
    no_uses_coupon = "<b>❌ You did not have time to activate the promotional code!</b>"
    yes_coupon = "<b>✅ You have successfully activated the promotional code and received <code>{summa}</code>!</b>"
    yes_uses_coupon = "<b>❌ You have already activated this promotional code!</b>"
    is_ban_text = "<b>❌ You have been banned from the bot!</b>\nReason for Ban: {ban_msg}"
    game_menu = "<b>Select game mode 🕹</b>"
    adm_user_ban = "⛔ Block"
    adm_user_unban = "🟢 Unban"
    adm_user_revork_bal = "💰 Change balance"
    adm_user_give_bal = "💰 Give balance"
    adm_user_revork_demo = "🏦 Edit Demo"
    adm_user_give_demo = "🏦 Give Demo"
    why_ban = "❗Specify the reason for blocking"