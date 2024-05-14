class Texts:
##########################################################################
################################## Buttons ###############################
##########################################################################
    reply_kb1 = 'Games 🎮'
    reply_kb2 = 'Profile 👨‍💻'
    reply_kb3 = 'FAQ 📖'
    reply_kb4 = 'Support 🛎'
    reply_admin = "👩‍💻Admin Panel"


##########################################################################
################################## Messages ##############################
##########################################################################
    reg_user = "💎 New user {name} has been registered" # {name} - username of the user
    welcome = "Welcome 👋"
    def open_profile(self, user_id, user_name, balance, referals, referals_sum, refer_lvl, balance_vivod, refer_link):
        msg = f"""🆔 Your ID: {user_id}
                🤖 @Username: {user_name}
                
                💰 Your balance: {balance}   
                💸 Displayed by: {balance_vivod}
                
                👥 Users invited: {referals}
                🍬 Income from referrals: {referals_sum} | Level: {refer_lvl}
                🔗 Referral link: {refer_link}"""
        return msg