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
    async def get_user(self, **kwargs):
        queryy = "SELECT * FROM users"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
        return await row.fetchone()
    
    # Получение пользователя из БД
    async def get_settings(self, **kwargs):
        queryy = "SELECT * FROM settings"
        queryy, params = query_args(queryy, kwargs)
        row = await self.con.execute(queryy, params)
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
    
    # Регистрация пользователя в БД
    async def register_user(self, user_id, user_name, first_name):
        await self.con.execute("INSERT INTO users("
                                "user_id, user_name, first_name, balance, reg_date_unix, test_balance, request_test)"
                                "VALUES (?,?,?,?,?,?,?)",
                                [user_id, user_name, first_name, 0, get_unix(), 0, 0])
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

    #Проверка на существование бд и ее создание
    async def create_db(self):
        users_info = await self.con.execute("PRAGMA table_info(users)")
        if len(await users_info.fetchall()) == 9:
            print("database was found (Users | 1/3)")
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
                                   "balance INTEGER)")
            print("database was not found (Users | 1/3), creating...")
            await self.con.commit()
            
        settings = await self.con.execute("PRAGMA table_info(settings)")
        if len(await settings.fetchall()) == 5:
            print("database was found (Settings | 2/18)")
        else:
            await self.con.execute("CREATE TABLE settings("
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                    "profit_day INTEGER,"
                                    "profit_week INTEGER,"
                                    "FAQ TEXT,"
                                    "support TEXT)")

            print("database was not found (Settings | 2/3), creating...")
            await self.con.execute("INSERT INTO settings("
                                            "FAQ, support, profit_day, profit_week) "
                                            "VALUES (?, ?, ?, ?)", ['FAQ', '-', f'{get_unix()}', f'{get_unix()}'])
            await self.con.commit()
            
        langs = await self.con.execute("PRAGMA table_info(languages)")
        if len(await langs.fetchall()) == 3:
            print("database was found (Languages | 12/18)")
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

            print("database was not found (Languages | 3/3), creating...")

            await self.con.commit()

        # Промокоды
        promos = await self.con.execute("PRAGMA table_info(coupons)")
        if len(await promos.fetchall()) == 3:
            print("database was found (Promocodes| 9/18)")
        else:
            await self.con.execute('CREATE TABLE coupons('
                                   'coupon TEXT,'
                                   'uses INTEGER,'
                                   'summa_promo INTEGER);')
            print("database was not found (Promocodes | 9/18), creating...")
            await self.con.commit()

        # Активные промокоды
        ac_prs = await self.con.execute("PRAGMA table_info(activ_coupons)")
        if len(await ac_prs.fetchall()) == 2:
            print("database was found (Active Promocodes | 10/18)")
        else:
            await self.con.execute('CREATE TABLE activ_coupons('
                                   'coupon_name TEXT,'
                                   'user_id INTEGER);')
            print("database was not found (Active Promocodes | 10/18), creating...")
            await self.con.commit()