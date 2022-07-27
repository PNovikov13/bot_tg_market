import pandas as pd
import bisect
import pycbrf
import sqlite3


class FromExelToSql:
    def __init__(self):
        self.rates = pycbrf.ExchangeRates('2022-06-21')
        self.gl = pd.read_excel('new.xlsx')
        self.connect = sqlite3.connect('my_bd.db')
        self.cursor = self.connect.cursor()

    def new_price_low(self, numm):
        input_list = [20, 30, 40, 60, 80, 110, 160, 220, 310, 440, 630, 880, 1300, 1800, 2500, 3500, 5000, 7100, 10000,
                      14100, 20000, 28300, 40000, 56600, 80000, 113000, 160000, 226000, 320000, 453000, 640000, 905000,
                      128000000, 1810000, 2560000, 3620000, 5120000, 7240000, 10240000, 14480000, 20480000, 28960000,
                      40960000, 57930000, 81920000]
        res = bisect.bisect_right(input_list, numm)
        return input_list[res]

    def new_price_med(self, numm):
        input_list = [630, 1800, 5000, 10000, 20000, 40000]
        res = bisect.bisect_right(input_list, numm)
        return input_list[res]

    def new_price_high(self, numm):
        input_list = [2500, 5000, 14100, 40000, 80000, 160000, 453000]
        res = bisect.bisect_right(input_list, numm)
        return input_list[res]

    def usd(self, num):
        return int(num / float(self.rates['USD'].value))

    def eur(self, num):
        return int(num / float(self.rates['EUR'].value))

    def pandas_file(self):
        self.gl.dropna(subset=['site_price_current', 'articul'], inplace=True)
        self.gl['low_price'] = self.gl['site_price_current'].apply(self.new_price_low)
        self.gl['med_price'] = self.gl['site_price_current'].apply(self.new_price_med)
        self.gl['high_price'] = self.gl['site_price_current'].apply(self.new_price_high)


    def to_sql(self):
        self.pandas_file()
        self.money_usd()
        with self.connect:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS `new_t` {} '.format(tuple(self.gl.columns)))
            self.gl.to_sql('new_t', self.connect, if_exists='replace', index=False)

    def money_usd(self):
        self.gl['USD_l'] = self.gl['low_price'].apply(self.usd)
        self.gl['USD_m'] = self.gl['med_price'].apply(self.usd)
        self.gl['USD_h'] = self.gl['high_price'].apply(self.usd)
        self.gl['EUR_l'] = self.gl['low_price'].apply(self.eur)
        self.gl['EUR_m'] = self.gl['med_price'].apply(self.eur)
        self.gl['EUR_h'] = self.gl['high_price'].apply(self.eur)



