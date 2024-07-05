import aiosqlite
from async_class import AsyncClass
import time

path_db = 'bot/data/database.db'

# Получение текущего unix времени
def get_unix(full=False):
    if full:
        return time.time_ns()
    else:
        return int(time.time())

#Преобразование результата в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

# Форматирование запроса без аргументов
def query(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def query_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

#Проверка и создание бд
class DB(AsyncClass):
    async def __ainit__(self):
        self.con = await aiosqlite.connect(path_db)
        self.con.row_factory = dict_factory

    # Получение всех пользователей из БД
    async def all_users(self):
        row = await self.con.execute("SELECT * FROM users")

        return await row.fetchall()

    # Получение пользователя из БД
    async def get_game_settings(self, **kwargs):
        queryy = "SELECT * FROM game_settings"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()

    # Получение пользователя из БД
    async def get_user(self, **kwargs):
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    async def get_userAll(self, **kwargs):
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchall()
    
    # Получение настроек из БД
    async def get_settings(self, **kwargs):
        queryy = "SELECT * FROM settings"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    async def get_language(self, name=None, lang_id=None):
        row = None
        if name:
            row = await self.con.execute("SELECT * FROM languages WHERE language = ?", (name,))
        if lang_id:
            row = await self.con.execute("SELECT * FROM languages WHERE id = ?", (lang_id,))

        return await row.fetchone()
    
    # Получение настроек
    async def get_only_settings(self):
        row = await self.con.execute("SELECT * FROM settings")
        return await row.fetchone()
    
    # Редактирование пользователя
    async def update_user(self, id, **kwargs):
        queryy = f"UPDATE users SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE user_id = ?", params)
        await self.con.commit()
    
    async def update_vivod(self, id, **kwargs):
        queryy = f"UPDATE conclusion SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE id = ?", params)
        await self.con.commit()
    
    async def get_vivod(self, **kwargs):
        sql = "SELECT * FROM conclusion"
        sql, parameters = query_args(sql, kwargs)
        row = await self.con.execute(sql, parameters)

        return await row.fetchone()
    
    async def all_deposit(self):
        row = await self.con.execute("SELECT total_pay FROM users")
        return await row.fetchall()
    
    # Регистрация пользователя в БД
    async def register_user(self, user_id, user_name, first_name):
        await self.con.execute("INSERT INTO users("
                                "user_id, user_name, first_name, balance, reg_date_unix, test_balance, request_test, is_ban, vivod)"
                                "VALUES (?,?,?,?,?,?,?,?,?)",
                                [user_id, user_name, first_name, 0, get_unix(), 0, 0, False, 0])
        await self.con.commit()
        
    # Создание чека
    async def add_check(self, unix, user_id, transaction_type, conclusion_id, summa):
        await self.con.execute("INSERT INTO [check]("
                                "unix, user_id, transaction_type, conclusion_id, summa)"
                                "VALUES (?,?,?,?,?)",
                                [unix, user_id, transaction_type, conclusion_id, summa])
        await self.con.commit()
    
    #Получение списка всех языков
    async def get_all_languages(self):
        row = await self.con.execute("SELECT * FROM languages")
        return await row.fetchall()

    async def update_settings(self, **kwargs):
        queryy = "UPDATE settings SET"
        queryy, parameters = query(queryy, kwargs)
        await self.con.execute(queryy, parameters)
        await self.con.commit()

    # Создание промокода
    async def create_coupon(self, coupon, uses, summa_promo):
        await self.con.execute("INSERT INTO coupons "
                               "(coupon, uses, summa_promo) "
                               "VALUES (?, ?, ?)",
                               [coupon, uses, summa_promo])
        await self.con.commit()

    # Получение Промокода
    async def get_promo(self, **kwargs):
        queryy = "SELECT * FROM coupons"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()

    # Удаление промокода
    async def delete_coupon(self, coupon):
        await self.con.execute("DELETE FROM coupons WHERE coupon = ?", (coupon,))
        await self.con.execute("DELETE FROM activ_coupons WHERE coupon_name = ?", (coupon,))
        await self.con.commit()

    # Получение промокода
    async def get_coupon_search(self, **kwargs):
        sql = "SELECT * FROM coupons"
        sql, parameters = query_args(sql, kwargs)
        row = await self.con.execute(sql, parameters)

        return await row.fetchone()
    
    # Получение Чека
    async def get_check(self, **kwargs):
        sql = "SELECT * FROM [check]"
        sql, parameters = query_args(sql, kwargs)
        row = await self.con.execute(sql, parameters)
        
        return await row.fetchone()
    
    # Получение активироного промокода
    async def get_activate_coupon(self, **kwargs):
        sql = "SELECT * FROM activ_coupons"
        sql, parameters = query_args(sql, kwargs)
        row = await self.con.execute(sql, parameters)

        return await row.fetchone()

    # Активировать промокод
    async def activate_coupon(self, user_id, coupon):
        await self.con.execute('''UPDATE activ_coupons SET coupon_name = ? WHERE user_id = ?''', (coupon, user_id,))
        await self.con.commit() 

    # Добавить id юзера который ввел промокод
    async def add_activ_coupon(self, user_id):
        await self.con.execute(f"INSERT INTO activ_coupons(user_id) VALUES (?)", (user_id,))
        await self.con.commit()

    async def add_vivod(self, user_id, summa, network, status, adress, data):
        await self.con.execute('''INSERT INTO conclusion (user_id, summa, network, status, adress, data) VALUES (?, ?, ?, ?, ?, ?)''', (user_id, summa, network, status, adress, data))
        await self.con.commit()

    # Редактирование промокода
    async def update_coupon(self, coupon, **kwargs):
        sql = f"UPDATE coupons SET"
        sql, parameters = query(sql, kwargs)
        parameters.append(coupon)
        await self.con.execute(sql + "WHERE coupon = ?", parameters)
        await self.con.commit()

    # Редактирование промокода
    async def update_game_settings(self, name, **kwargs):
        sql = f"UPDATE game_settings SET"
        sql, parameters = query(sql, kwargs)
        parameters.append(name)
        await self.con.execute(sql + "WHERE name = ?", parameters)
        await self.con.commit()

    # Удаление промокода
    async def delete_coupon(self, coupon):
        await self.con.execute("DELETE FROM coupons WHERE coupon = ?", (coupon,))
        await self.con.execute("DELETE FROM activ_coupons WHERE coupon_name = ?", (coupon,))
        await self.con.commit()

    async def create_mail_button(self, name: str, typ: str):
        await self.con.execute('INSERT INTO mail_buttons(name, type) VALUES (?,?)', (name, typ))
        await self.con.commit()

    async def delete_mail_button(self, id: str):
        await self.con.execute('DELETE FROM mail_buttons WHERE id = ?', (id,))

    async def get_mail_button(self, id: int):
        row = await self.con.execute('SELECT * FROM mail_buttons WHERE id = ?', (id,))
        return await row.fetchone()

    async def get_all_mail_buttons(self):
        row = await self.con.execute('SELECT * FROM mail_buttons')
        return await row.fetchall()

    async def update_mail_button(self, id, **kwargs):
        queryy = f"UPDATE mail_buttons SET"
        queryy, params = query(queryy, kwargs)
        params.append(id)
        await self.con.execute(queryy + "WHERE id = ?", params)
        await self.con.commit()

    ##############################################################################################
    ######################               Рекламные кнопки             ############################
    ##############################################################################################

    # Получение всех кнопок
    async def get_all_pr_buttons(self):
        row = await self.con.execute(f'SELECT * FROM pr_buttons')

        return await row.fetchall()

    # Получение кнопки
    async def get_pr_button(self, btn_id):
        row = await self.con.execute(f'SELECT * FROM pr_buttons WHERE id = ?', (btn_id,))

        return await row.fetchone()

    # Создание кнопки
    async def create_pr_button(self, name, txt, photo):
        values = [name, txt, photo]
        await self.con.execute('INSERT INTO pr_buttons(name, txt, photo) VALUES (?, ?, ?)', values)
        await self.con.commit()

    # Удаление кнопки
    async def delete_pr_button(self, name):
        await self.con.execute('DELETE FROM pr_buttons WHERE name = ?', (name,))
        await self.con.commit()

    #Проверка на существование бд и ее создание
    async def create_db(self):
        users_info = await self.con.execute("PRAGMA table_info(users)")
        if len(await users_info.fetchall()) == 26:
            print("database was found (Users | 1/10)")
        else:
            await self.con.execute("CREATE TABLE users ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "user_id INTEGER,"
                                   "user_name TEXT,"
                                   "first_name TEXT,"
                                   "reg_date_unix INTEGER,"
                                   "language TEXT DEFAULT 'ru',"
                                   "test_balance INTEGER,"
                                   "request_test INTEGER,"
                                   "total_refill INTEGER DEFAULT 0,"
                                   "total_pay INTEGER DEFAULT 0,"
                                   "ref_count INTEGER DEFAULT 0,"
                                   "ref_lvl INTEGER DEFAULT 1,"
                                   "ref_id INTEGER,"
                                   "ref_user_name TEXT,"
                                   "ref_first_name TEXT,"
                                   "is_ban INTEGER,"
                                   "ban_cause TEXT,"
                                   "amount_all_games INTEGER DEFAULT 0,"
                                   "amount_slots INTEGER DEFAULT 0,"
                                   "amount_dice INTEGER DEFAULT 0,"
                                   "amount_basketball INTEGER DEFAULT 0,"
                                   "amount_bowling INTEGER DEFAULT 0,"
                                   "amount_football INTEGER DEFAULT 0,"
                                   "amount_coin INTEGER DEFAULT 0,"
                                   "vivod INTEGER,"
                                   "balance INTEGER)")
            print("database was not found (Users | 1/10), creating...")
            await self.con.commit()
            
        settings = await self.con.execute("PRAGMA table_info(settings)")
        if len(await settings.fetchall()) == 18:
            print("database was found (Settings | 2/10)")
        else:
            await self.con.execute("CREATE TABLE settings("
                                   "is_work TEXT,"
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                    "profit_day INTEGER,"
                                    "profit_week INTEGER,"
                                    "ref_percent_1 INTEGER DEFAULT 0,"
                                    "ref_percent_2 INTEGER DEFAULT 0,"
                                    "ref_percent_3 INTEGER DEFAULT 0,"
                                    "ref_lvl_1 INTEGER DEFAULT 0,"
                                    "ref_lvl_2 INTEGER DEFAULT 0,"
                                    "ref_lvl_3 INTEGER DEFAULT 0,"
                                    "FAQ TEXT,"
                                    "Commission_TON INTEGER DEFAULT 0,"
                                    "Commission_TRC20 INTEGER DEFAULT 0,"
                                    "Commission_ERC20 INTEGER DEFAULT 0,"
                                    "CommissionBER20 INTEGER DEFAULT 0,"
                                    "Commission_check INTEGER DEFAULT 0,"
                                    "Minimum_check INTEGER DEFAULT 0,"
                                    "support TEXT)")

            print("database was not found (Settings | 2/10), creating...")
            await self.con.execute("INSERT INTO settings("
                                            "is_work, FAQ, support, profit_day, profit_week) "
                                            "VALUES (?, ?, ?, ?, ?)", ['True', 'FAQ', '-', f'{get_unix()}', f'{get_unix()}'])
            await self.con.commit()
            
        langs = await self.con.execute("PRAGMA table_info(languages)")
        if len(await langs.fetchall()) == 3:
            print("database was found (Languages | 3/10)")
        else:
            await self.con.execute("CREATE TABLE languages("
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                    "language TEXT,"
                                    "name TEXT)")

            await self.con.execute("INSERT INTO languages("
                                "language, name) "
                                "VALUES (?, ?)", ['ru', '🇷🇺 Русский'])
            await self.con.execute("INSERT INTO languages("
                                "language, name) "
                                "VALUES (?, ?)", ['en', '🇺🇸 English'])

            print("database was not found (Languages | 3/10), creating...")

            await self.con.commit()

        # Промокоды
        promos = await self.con.execute("PRAGMA table_info(coupons)")
        if len(await promos.fetchall()) == 3:
            print("database was found (Promocodes| 4/10)")
        else:
            await self.con.execute('CREATE TABLE coupons('
                                   'coupon TEXT,'
                                   'uses INTEGER,'
                                   'summa_promo INTEGER);')
            print("database was not found (Promocodes | 4/10), creating...")
            await self.con.commit()

        # Активные промокоды
        ac_prs = await self.con.execute("PRAGMA table_info(activ_coupons)")
        if len(await ac_prs.fetchall()) == 2:
            print("database was found (Active Promocodes | 5/10)")
        else:
            await self.con.execute('CREATE TABLE activ_coupons('
                                   'coupon_name TEXT,'
                                   'user_id INTEGER);')
            print("database was not found (Active Promocodes | 5/10), creating...")
            await self.con.commit()

        conclusion = await self.con.execute("PRAGMA table_info(conclusion)")
        if len(await conclusion.fetchall()) == 7:
            print("database was found (Conclusion | 6/10)")
        else:
            await self.con.execute("CREATE TABLE conclusion("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "user_id INTEGER,"
                                   "summa INTEGER,"
                                   "network TEXT,"
                                   "status TEXT,"
                                   "adress TEXT,"
                                   "data TEXT);")
            print("database was not found (Active Promocodes | 6/10), creating...")
            await self.con.commit()

        game_stats = await self.con.execute("PRAGMA table_info(game_settings)")
        if len(await game_stats.fetchall()) == 6:
            print("database was found (Languages | 7/10)")
        else:
            await self.con.execute("""
                CREATE TABLE game_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    factor INTEGER,
                    min_bet INTEGER,
                    chance_real INTEGER,
                    chance_demo INTEGER
                )
            """)

            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['slots', 1, 1, 0, 1])
            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['coin', 1, 1, 0, 1])
            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['basketball', 1, 1, 0, 1])
            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['football', 1, 1, 0, 1])
            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['bowling', 1, 1, 0, 1])
            await self.con.execute("""INSERT INTO game_settings (
                                    name, factor, min_bet, chance_real, chance_demo) VALUES (?, ?, ?, ?, ?)""", 
                                    ['dice', 1, 1, 0, 1])


            print("database was not found (Languages | 7/10), creating...")
            await self.con.commit()
            
        check_ = await self.con.execute("PRAGMA table_info([check])")
        if len(await check_.fetchall()) == 6:
            print("database was found (Check | 8/10)")
        else:
            await self.con.execute("CREATE TABLE [check]("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "unix INTEGER,"
                                "user_id INTEGER,"
                                "transaction_type TEXT CHECK(transaction_type IN ('deposit', 'withdrawal')),"
                                "summa INTEGER,"
                                "conclusion_id INTEGER);")
            print("database was not found (Check | 8/10), creating...")
            await self.con.commit()
            
        # Кнопки в рассылках
        mail_buttons = await self.con.execute("PRAGMA table_info(mail_buttons)")
        if len(await mail_buttons.fetchall()) == 3:
            print("database was found (Mail Buttons | 9/10)")
        else:
            await self.con.execute("CREATE TABLE mail_buttons("
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "name TEXT,"
                                       "type TEXT)")

            print("database was not found (Mail Buttons | 9/10), creating...")

            await self.con.commit()
            
        # Рекламные кнопки
        pr_buttons = await self.con.execute("PRAGMA table_info(pr_buttons)")
        if len(await pr_buttons.fetchall()) == 4:
            print("database was found (AD Buttons | 10/10)")
        else:
            await self.con.execute("CREATE TABLE pr_buttons("
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "name TEXT,"
                                       "txt TEXT,"
                                       "photo TEXT)")

            print("database was not found (AD Buttons | 10/10), creating...")

            await self.con.commit()