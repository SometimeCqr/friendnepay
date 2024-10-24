import sqlite3
import array
import os

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS users("
                     "id INTEGER PRIMARY KEY,"
                     "telegram_id INTEGER,"
                     "pricing INTEGER DEFAULT 0,"
                     "balance INTEGER DEFAULT 0,"
                     "polite INTEGER DEFAULT 0,"
                     "referer INTEGER DEFAULT 0,"
                     "referer_amount INTEGER DEFAULT 0,"
                     "attempts INTEGER DEFAULT 0,"
                     "timesub INTEGER DEFAULT 0,"
                     "is_admin INTEGER DEFAULT 0,"
                     "number_of_admin_withdraws INTEGER DEFAULT 0,"
                     "sum_of_admin_withdraws INTEGER DEFAULT 0,"
                     "number_of_referers_today INTEGER DEFAULT 0);"
                     "CREATE TABLE IF NOT EXISTS consts("
                     "id INTEGER PRIMARY KEY,"
                     "number_of_withdraws INTEGER DEFAULT 0,"
                     "today INTEGER DEFAULT 0);"
                     "CREATE TABLE IF NOT EXISTS admins("
                     "id INTEGER PRIMARY KEY,"
                     "telegram_id INTEGER,"
                     "is_online INTEGER DEFAULT 0);")
            self.cursor.executescript(query)
            self.connection.commit()

        except sqlite3.Error as Error:
            print('Ошибка при создании:', Error)

    def add_user(self, telegram_id):
        self.cursor.execute(f"INSERT INTO users(telegram_id,pricing) VALUES (?,?)", (telegram_id,0))
        self.connection.commit()

    def pricing_edit(self,user_id, pricing):
        self.cursor.execute(f"UPDATE 'users' SET 'pricing' = ? WHERE telegram_id = ?",
                            (pricing,user_id))
        self.connection.commit()

    def number_of_admin_withdraws_edit(self,user_id, number_of_admin_withdraws):
        self.cursor.execute(f"UPDATE 'users' SET 'number_of_admin_withdraws' = ? WHERE telegram_id = ?",
                            (number_of_admin_withdraws, user_id))
        self.connection.commit()

    def sum_of_admin_withdraws_edit(self,user_id, sum_of_admin_withdraws):
        self.cursor.execute(f"UPDATE 'users' SET 'sum_of_admin_withdraws' = ? WHERE telegram_id = ?",
                            (sum_of_admin_withdraws, user_id))
        self.connection.commit()

    def numbers_of_withdraws_edit(self, number_of_withdraws, id):
        self.cursor.execute(f"UPDATE 'consts' SET 'number_of_withdraws' = ? WHERE id = ?",
                            (number_of_withdraws, id))
        self.connection.commit()

    def todays_const_edit(self, today, id):
        self.cursor.execute(f"UPDATE 'consts' SET 'today' = ? WHERE id = ?",
                            (today,id))
        self.connection.commit()


    def get_online_admins_id(self):
        online_admins_id=(self.cursor.execute(f"SELECT * FROM admins WHERE is_online = 1").fetchall())  # Попробовать поменять чтобы SELECT брал не все значения а сразу только idшники
        length = len(online_admins_id)
        for i in range(length):
            online_admins_id[i] = online_admins_id[i][1]
        if(online_admins_id == []):
            return 0
        else:
            return online_admins_id

    def down_to_zero_all_number_referers(self):
        users = (self.cursor.execute(f"SELECT * FROM users WHERE polite = 1").fetchall())
        length = len(users)
        for i in range(length):
            self.cursor.execute(f"UPDATE 'users' SET 'number_of_referers_today' = ? WHERE telegram_id = ?",(0, users[i][1]))
        self.connection.commit()


    def is_online_edit(self,telegram_id, is_online):
        self.cursor.execute(f"UPDATE 'admins' SET 'is_online' = ? WHERE telegram_id = ?",
                            (is_online, telegram_id))
        self.connection.commit()

    def select_user_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def select_admin_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM admins WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def select_number_of_withdraws(self):
        users = self.cursor.execute("SELECT * FROM consts WHERE id = 1")
        return users.fetchone()[1]

    def get_today_const(self):
        users = self.cursor.execute("SELECT * FROM consts WHERE id = 1")
        return int(users.fetchone()[2])

    def select_user_pricing(self, pricing):
        users = self.cursor.execute("SELECT * FROM users WHERE pricing = ?", (pricing,))
        return users.fetchone()

    def select_user_balance(self, balance):
        users = self.cursor.execute("SELECT * FROM users WHERE balance = ?", (balance,))
        return users.fetchone()

    def select_user_polite(self, polite):
        users = self.cursor.execute("SELECT * FROM users WHERE polite = ?", (polite,))
        return users.fetchone()

    def polite_edit(self, user_id, polite):
        self.cursor.execute(f"UPDATE 'users' SET 'polite' = ? WHERE telegram_id = ?",
                            (polite, user_id))
        self.connection.commit()

    def referer_amount_edit(self, user_id, referer_amount):
        self.cursor.execute(f"UPDATE 'users' SET 'referer_amount' = ? WHERE telegram_id = ?",
                            (referer_amount, user_id))
        self.connection.commit()

    def number_of_referers_today_edit(self, user_id, number_of_referers_today):
        self.cursor.execute(f"UPDATE 'users' SET 'number_of_referers_today' = ? WHERE telegram_id = ?",
                            (number_of_referers_today, user_id))
        self.connection.commit()
    def balance_edit(self, user_id, balance):
        self.cursor.execute(f"UPDATE 'users' SET 'balance' = ? WHERE telegram_id = ?",
                            (balance, user_id))
        self.connection.commit()

    def referer_edit(self, user_id, referer):
        self.cursor.execute(f"UPDATE 'users' SET 'referer' = ? WHERE telegram_id = ?",
                            (referer, user_id))
        self.connection.commit()

    def attempts_edit(self, user_id, attempts):
        self.cursor.execute(f"UPDATE 'users' SET 'attempts' = ? WHERE telegram_id = ?",
                            (attempts, user_id))
        self.connection.commit()

    def timesub_edit(self,user_id, timesub):
        self.cursor.execute(f"UPDATE 'users' SET 'timesub' = ? WHERE telegram_id = ?",
                            (timesub, user_id))
        self.connection.commit()

    def get_online_admins_id(self):
        online_admins_id=(self.cursor.execute(f"SELECT * FROM admins WHERE is_online = 1").fetchall())
        length = len(online_admins_id)
        for i in range(length):
            online_admins_id[i] = online_admins_id[i][1]
        if(online_admins_id == []):
            return 0
        else:
            return online_admins_id
    def get_balances_sum(self):
        all_balances = self.cursor.execute(f"SELECT balance FROM users").fetchall()
        balances_sum = 0
        length = len(all_balances)
        for i in range(length):
            balances_sum = balances_sum + all_balances[i][0]
        return balances_sum


    def __def__(self):
        self.cursor.close()
        self.connection.close()

