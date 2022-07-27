import sqlite3


class ProdBD:
    def __init__(self):
        self.connect = sqlite3.connect('my_bd.db', check_same_thread=False)
        self.cursor = self.connect.cursor()

    def goods(self):
        with self.connect:
            self.cursor.execute('ALTER TABLE new_t ADD COLUMN goods int NOT NULL DEFAULT(100) ')
            rows = self.cursor.fetchall()


    def get_prod_info(self, chat_id, art):
        new_n = ''
        res = self.cursor.execute('SELECT status FROM user_table WHERE chat_id=?', (chat_id,)).fetchall()
        for i in res:
            new_n = i[0]

        if new_n == '0':
            return self.cursor.execute(
                'SELECT name_product, product_type, brand, name_tm, high_price, USD_h, EUR_h  FROM new_t WHERE articul=?',
                (art,)).fetchall()

        if new_n == '1':
            return self.cursor.execute(
                'SELECT name_product, product_type, brand, name_tm, med_price, USD_m, EUR_m  FROM new_t WHERE articul=?',
                (art,)).fetchall()

        if new_n == '2':
            return self.cursor.execute(
                'SELECT name_product, product_type, brand, name_tm, low_price, USD_l, EUR_l FROM new_t WHERE articul=?',
                (art,)).fetchall()

        if new_n == '3':
            return self.cursor.execute(
                'SELECT name_product, product_type, brand, name_tm, site_price FROM new_t WHERE articul=?',
                (art,)).fetchall()

    def update_value_after_sale(self, art):
        our_goods = self.cursor.execute('SELECT goods FROM new_t WHERE articul=?', (art,)).fetchall()
        a = ''
        for elem in our_goods:
            a += str(elem[0])
        a = str(int(a) - 1)
        with self.connect:
            self.cursor.execute('UPDATE new_t SET goods=?  WHERE articul=?', (a, art,))



