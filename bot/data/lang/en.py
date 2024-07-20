class Texts:
################################################## #########################
################################## Buttons ############### ################
################################################## #########################
    reply_kb1 = '🕹Games'
    reply_kb2 = '👨‍💻 Profile'
    reply_kb3 = '📖 Rules'
    reply_kb4 = '🚑 Support'
    reply_admin = "👩‍💻Admin Panel"
    back = "🔙 To main menu"
    back_to_adm_m = "🔙 Back"
    back = "⬅Back"
    conclusion = "💸 Withdraw balance"
    refill = "💳 Refill balance"
    groups_list = "Groups 📰"
    support_inl = "🌟Support"
    test_balance = "🏦 Get demo balance"
    change_language = "🇷🇺 Change Language"
    promo = "🎫 Promo code"
    new_promo = "💎 Create a promotional code"
    del_promo = "🎲 Remove promo code"
    ####GAMES####
    game_slots = "🎰 Slots"
    game_dice = "🎲 Dice"
    game_darts = "🎯 Darts"
    game_basketball = "🏀 Basketball"
    game_bowling = "🎳 Bowling"
    game_football = "⚽ Football"
    game_coin = "🪙 Coin"
    adm_edit_factor = "📊 Factor: X{factor}"
    min_bet = "Min. Bet: {min_bet} 🪙"
    real_chance = "💸 Chance of winning: {real_chance}%"
    demo_chance = "🏦 Demo chance: {demo_chance}%"
    use_demo = "💰 Use Demo balance"
    use_real = "💎 Use balance"
    adm_user_revork_bal = "💰 Change balance"
    adm_user_give_bal = "💰 Give balance"
    adm_user_revork_demo = "🏦 Edit Demo"
    adm_user_give_demo = "🏦 Give Demo"
    adm_user_ban = "⛔ Block"
    adm_user_unban = "🟢 Unban"
    go_next = "Play more 🔃"
    pay_link = "💸 Pay"
    pay_id = "🎆 Check payment"
    edit_network = "Edit network"
    back_vivod_to_method = "⬅️ Change method"

    
################################################## #########################
################################## Messages ################ ################
################################################## #########################
    reg_user = "💎 New user {name} has been registered" # {name} - username of the user
    welcome = """👋 <b>Welcome to the best gaming bot</b> 🎲\n\n🤖 Our bot has many games for your entertainment\n\n📰Follow the news in the channel!\nPostonic <code> 🎁 draws</code> and <code>🎫 promotional codes</code>\nIf you need help, our <code>🚑 support</code>\n\n<b>💚 3-level referral system</code>\n b> to make playing with friends more fun\n\n<b>🧠 You can read the rules by going to the 📖Rules</b>""" 
    admin_menu = "welcome to the Administrator menu 👋"
    def open_profile(self, user_id, balance, user_name, referals, referals_sum, refer_lvl, balance_vivod, refer_link, test_balance, reffer):
        msg = f"""🆔 Your ID: <code>{user_id}</code>
        👑 Username: <code>{user_name}</code>

        💰 Your balance: ₽ <code>{balance}</code>
        🏦 Demo balance: ₽ <code>{test_balance}</code>
        💸 Withdrawn: ₽ <code>{balance_vivod}</code>

        👥 Users invited: <code>{referals}</code>
        🌃 Income from referrals: ₽ <code>{referals_sum}</code> | Level: <code>{refer_lvl}</code>
        ⭐ You were invited by: {reffer}
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
    yes_support = "<b>🚑 Need help? Contact our support\nReply time up to 12h</b>"
    yes_demo = "✅ Demo balance issued successfully"
    no_demo = "❌ You have already received demo balance"
    promo_menu = "👇 Select an action"
    promo_act = "<b>📩 Enter promo code</b>\n"
    no_coupon = "<b>❌ Promo code <code>{coupon}</code> does not exist!</b>"
    no_uses_coupon = "<b>❌ You did not have time to activate the promotional code!</b>"
    yes_coupon = "<b>✅ You have successfully activated the promotional code and received <code>{summa}</code>!</b>"
    yes_uses_coupon = "<b>❌ You have already activated this promotional code!</b>"
    is_ban_text = "<b>❌ You have been blocked from the bot!</b>\nReason for Blocking: {ban_msg}"
    game_menu = "<b>🎮 Select game</b>"
    why_ban = "❗Specify the reason for blocking"
    incorrect_amount = "Enter an amount from ₽ <code>1</code> to <code>1000</code>"
    is_work_text = f"<b>❌ The bot is at technical work!</b>"
    is_work_text = f"<b>❌ The bot is on those. works!</b>"
    def bet_msg(self, game_name_text, min_bet, user_balance):
        msg = f"""<b>Game:</b> {game_name_text}

        <b>📉 Minimum bet:</b> ₽ <code>{min_bet}</code>
        <b>💰 Your balance:</b> ₽ <code>{user_balance}</code>

        <b>✍ Specify the bet amount:</b> """
        return msg
    def bet_msg_demo(self, game_name_text, min_bet, demo_balance):
        msg = f"""<b>Game:</b> {game_name_text}

        <b>📉 Minimum bet:</b> ₽ <code>{min_bet}</code>
        <b>🏦 Your Demo balance:</b> ₽ <code>{demo_balance}</code>

        <b>✍ Specify the bet amount:</b> """
        return msg
    vibor_game_to_edit = "<b>Select a game to edit 🕹</b>"
    adm_edit_game_menu = "🃏 Game: <code>{game_name}</code>\n<b>Select settings to change</b>"
    admin_edit_real_chance = "📈 Choose a new chance to win\n<b>(For real money)</b>"
    admin_edit_demo_chance = "📉 Choose a new chance to win\n<b>(On demo balance)</b>"
    admin_edit_min_bet = "🌟 Enter a new <b>minimum bet</b>"
    admin_edit_factor = "🧮 Enter a new <b>factor</b>"
    admin_open_profile ="""<b>👤 Profile:
    💎 User: {name}
    🆔 ID: <code>{user_id}</code>
    📅 Registration date: <code>{total_refill}</code>

    💰 Balance: ₽ <code>{balance}</code>
    🏦 Demo balance: ₽ <code>{demo_balance}</code>

    ⚙️ Bot language: <code>{lang}</code>
    💵 Topped up: ₽ <code>{tr}</code>
    💵 Withdrawn: ₽ <code>{vivod}</code>

    🎱Total games: <code>{amount_all_games}</code>
    🎰 Slots: <code>{amount_slots}</code>
    🎲 Dice: <code>{amount_dice}</code>
    🏀 Basketball: <code>{amount_basketball}</code>
    🎳 Bowling: <code>{amount_bowling}</code>
    ⚽ Football: <code>{amount_football}</code>
    🪙 Coin: <code>{amount_coin}</code>
    🎯 Darts: <code>{amount_darts}</code>

    🔗 Ban status: <code>{ban_status}</code>
    {cause_ban}
    👥 Referrals: <code>{count_refers} people</code>
    💎 Earned from referrals: ₽ <code>{referalst_summa}</code>
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
    def lose_game(self, summ, balance):
        msg = f"""<b>😞 Loss</b>

        You lost: ₽ <code>-{summ}</code>

        🏦 Your balance: ₽ <code>{balance}</code>"""
        return msg
    def win_game(self, summ, balance, kef):
        msg = f"""<b>🎉 Winning</b>

        Coefficient: X<code>{kef}</code>
        Your winnings: ₽ <code>{summ}</code>

        🏦 Your balance: ₽ <code>{balance}</code>"""
        return msg
    refil_sposob = "💎 Select a replenishment method"
    choose_coin = "Choose coin side 🪙"
    Eagle = "🦅 Eagle"
    Tails = "1️⃣ Tails"
    need_summa_cryptobot = "Enter the amount in <b>₽</b>"
    payment_link = "💠 Pay using the link below and click check payment"
    not_pay = "❌ Payment not found"
    yes_pay = "✅ Paid successfully"
    success_pay = "💰 Balance successfully replenished"
    ref_plus_balance = "💚 Your referral has replenished the balance, your percentage: {percent}"
    your_cube = "Your cube ⬇️"
    enemy_cube = "Enemy Cube ⬇️"
    bank_money = "Draw!\nMoney returned to balance"
    vibor_crypto = "💎 Select the desired cryptocurrency for payment"
    summa_vivoda = "💰 Your balance: <code>{balance}</code>\n\nEnter the amount to withdraw: "
    need_Crypto = "<b>📤 Withdrawal</b>\n\nSelect a withdrawal method: "
    need_adress = "📭 Enter your withdrawal address"
    need_network = "<b>🌏 Select a network to send USDT balance to</b>"
    succes_msg = "Your application has been sent successfully, please wait for confirmation"
    need_balance = "Not enough balance"
    otklon_vivod = "Canceled"
    vivod_mimo = "Your withdrawal request was rejected by the administrator\nThe money has been returned to your balance"
    vivod_success_msg = "Your withdrawal request has been approved!\nWait for funds to arrive ⏳"
    vivod_success_msg_check = "Your withdrawal request has been approved!\n\nThe administrator will write to you and give you your check\n\nWait ⏳"
    Confirmation_msg = """
    <b>👮 Check and confirmation</b>

    <b>🌏 Network:</b> <code>{network}</code>
    <b>📭Address:</b> <code>{adress}</code>

    <b>💠 Output:</b> <code>{amount_vivod}</code>
    <b>💚 Commission:</b> <code>{comma_vivod}</code>

    <b>💎 Summary:</b> <code>{full_summa}</code>

    <b>📤 Are you sure you want to withdraw this amount?</b>
    """
    need_real_adress = "📮 Incorrect address. Send the correct wallet address, which is located in the {crypto} network."
    Confirmation_msg_chek = """
    <b>👮 Check and confirmation</b>

    <b>💠 Output:</b> <code>{amount_vivod}</code>
    <b>💚 Commission:</b> <code>{comma_vivod}</code>

    <b>💎 Summary:</b> <code>{full_summa}</code>

    <b>📤 Are you sure you want to withdraw this amount?</b>
    """