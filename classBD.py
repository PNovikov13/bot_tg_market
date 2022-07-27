import sqlite3


class DB:
    def __init__(self):
        self.connect = sqlite3.connect('my_bd.db', check_same_thread=False)
        self.cursor = self.connect.cursor()

    def create_tablet(self):
        self.cursor.execute(
            ' CREATE TABLE IF NOT EXISTS `user_table` (name ,chat_id UNIQUE, status, status_of_purchaise) ')

    def add(self, x, y):
        with self.connect:
            self.cursor.execute(
                'INSERT OR IGNORE  INTO  `user_table`  (name, chat_id, status, status_of_purchaise ) VALUES  (?, ?, ?, ?) ',
                (y, x, '0', None))

    def admin_change_status(self, status, name):
        with self.connect:
            self.cursor.execute('UPDATE `user_table` SET status=? WHERE name=?', (status, name))

    def get_status(self, nick):
        res = self.cursor.execute('SELECT `status` FROM `user_table` WHERE name=?', (nick,)).fetchall()
        return res

    def count_goods(self):
        self.cursor.execute('ALTER TABLE user_table ADD COLUMN goods int NOT NULL DEFAULT(0)')
        self.cursor.execute('ALTER TABLE user_table ADD COLUMN  status_of_purchaise ')

    def insert_chat_id(self, id):
        with self.connect:
            self.cursor.execute('INSERT OR IGNORE INTO user_id_admin  VALUES (?)', (str(id),))

    def create_tablet_adm(self):
        self.cursor.execute('CREATE TABLE user_id_admin (chat_id UNIQUE)')

    def get_admin_id(self):
        return self.cursor.execute('SELECT * FROM  user_id_admin').fetchall()

    def create_cart(self):
        with self.connect:
            self.cursor.execute('CREATE TABLE cart_prod (chat_id , articul_prod)')

    def add_to_cart(self, user, prod):
        with self.connect:
            self.cursor.execute('INSERT INTO cart_prod  (chat_id, articul_prod) VALUES (?,?) ', (str(user), str(prod)))

    def get_from_card(self, user):
        return self.cursor.execute('SELECT articul_prod FROM cart_prod  WHERE chat_id=?', (user,)).fetchall()

    def delete_from_cart(self, user, art):
        with self.connect:
            self.cursor.execute('DELETE  FROM cart_prod WHERE chat_id=? AND articul_prod=?', (user, art))

    def delete_after_pay(self, user):
        with self.connect:
            self.cursor.execute('DELETE FROM cart_prod WHERE chat_id=?', (user,))
