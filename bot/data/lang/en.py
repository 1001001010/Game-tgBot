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
    refill = "💰 Refill balance"
    groups_list = "Groups 📰"
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
    adm_edit_factor = "📊 Factor: X{factor}"
    min_bet = "Min. Bet: {min_bet} 🪙"
    real_chance = "💸 Chance of winning: {real_chance}%"
    demo_chance = "🏦 Demo chance: {demo_chance}%"
    use_demo = "💰 Use Demo balance"
    use_real = "💰 Use balance"
    adm_user_revork_bal = "💰 Change balance"
    adm_user_give_bal = "💰 Give balance"
    adm_user_revork_demo = "🏦 Edit Demo"
    adm_user_give_demo = "🏦 Give Demo"
    adm_user_ban = "⛔ Block"
    adm_user_unban = "🟢 Unban"
    
    
################################################## #########################
################################## Messages ############### ################
################################################## #########################
    reg_user = "💎 New user {name} has been registered" # {name} - username of the user
    welcome = "Welcome 👋"
    admin_menu = "welcome to the Administrator menu 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance, reffer):
        msg = f"""🆔 Your ID: <code>{user_id}</code>
                🤖 Username: <code>{user_name}</code>
            
                💰 Your balance: <code>{balance}</code> 🪙
                🏦 Demo balance: <code>{test_balance}</code>
                💸 Output: <code>{balance_vivod}</code>
            
                👥 Users invited: <code>{referals}</code>
                🍬 Income from referrals: <code>{referals_sum}</code> | Level: <code>{refer_lvl}</code>
                ⚙️ You were invited by: {reffer}
                🔗 Referral link:
                <code>{refer_link}</code>"""
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
    why_ban = "❗Specify the reason for blocking"
    def bet_msg(self, game_name_text, min_bet, user_balance):
        msg = f"""Game: {game_name_text}
    
                💰 Minimum bet: <code>{min_bet}</code>
                🏦 Your balance: <code>{user_balance}</code> 🪙
                <b>❗ Enter the bet amount:</b> """
        return msg
    def bet_msg_demo(self, game_name_text, min_bet, demo_balance):
        msg = f"""Game: {game_name_text}
    
                💰 Minimum bet: <code>{min_bet}</code>
                🏦 Your Demo balance: <code>{demo_balance}</code> 🪙
                <b>❗ Enter the bet amount:</b> """
        return msg
    vibor_game_to_edit = "<b>Select a game to edit 🕹</b>"
    adm_edit_game_menu = "🃏Game: <code>{game_name}</code>\n<b>Select settings to change</b>"
    admin_edit_real_chance = "📈 Choose a new chance to win\n<b>(For real money)</b>"
    admin_edit_demo_chance = "📉 Choose a new chance to win\n<b>(On demo balance)</b>"
    admin_edit_min_bet = "🌟 Enter a new <b>minimum bet</b>"
    admin_edit_factor = "🧮 Enter a new <b>factor</b>"
    admin_open_profile ="""<b>👤 Profile:
                💎 User: {name}
                🆔 ID: <code>{user_id}</code>
                📅 Registration date: <code>{total_refill}</code>
            
                💰 Balance: <code>{balance}</code>
                🏦 Demo balance: <code>{demo_balance}</code>
            
                ⚙️ Bot language: <code>{lang}</code>
                💵 Total replenished: <code>{tr}</code>
                💵 Output: <code>{vivod}</code>
            
                🎱Total games: <code>{amount_all_games}</code>
                🎰 Slots: <code>{amount_slots}</code>
                🎲 Dice: <code>{amount_dice}</code>
                🏀 Basketball: <code>{amount_basketball}</code>
                🎳 Bowling: <code>{amount_bowling}</code>
                ⚽ Football: <code>{amount_football}</code>
                🪙 Coin: <code>{amount_coin}</code>
            
                🔗 Ban status: <code>{ban_status}</code>
                {cause_ban}
                👥 Referrals: <code>{count_refers} people</code>
                💎 Earned from referrals: <code>{referalst_summa}</code>
                📜 List of referrals:\n</b>"""
    need_number = "<b>You need to enter a number!</b>"
    wright_summ = "<b>Enter sum:</b>"
    invite_yourself = "<b>❗You cannot invite yourself</b>"
    yes_reffer = f"<b>❗ You already have a referr!</b>"
    new_refferal = "<b>💎 You have a new referral! @{user_name} \n" \
                "⚙️ You now have <code>{user_ref_count}</code> {convert_ref}!</b>"
    ref_s = ['referral', 'referral', 'referrals'] # leave parentheses intact
    new_ref_lvl = "<b>💚 You have a new referral level, {new_lvl}! There are {remain_refs} {convert_ref} left to {next_lvl} level</b>"
    max_ref_lvl = f"<b>💚 You have a new referral level, 3! Maximum level!</b>"
    cur_max_lvl = f"💚You have the maximum level!</b>"
    next_lvl_remain = "💚 Only <code>{remain_refs} people left to invite to the next level</code></b>"
    nobody = "<code>Nobody</code>"
    no_money = "Insufficient balance!"
    no_sub = "<b>❗ Error!\nYou have not subscribed to the channel.</b>"