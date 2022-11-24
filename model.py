import sqlite3
from datetime import date

from service import Analizer


class DB:
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    @classmethod
    def create_new_db(cls):
        cls.cur.execute('''
        CREATE TABLE IF NOT EXISTS statistic(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_word TEXT NOT NULL,
        experience TEXT NOT NULL,
        quantity_vac INTEGER NOT NULL,
        avarage_salary INTEGER NOT NULL,
        number_of_vacancies_for_avarage_salary INTEGER NOT NULL,
        remote_vac INTEGER NOT NULL,
        created_at DATE NOT NULL);
        ''')
        cls.con.commit()
        cls.con.close()

    @staticmethod
    def save_to_db(df):
        con = sqlite3.connect('db.sqlite')
        df.to_sql('statistic', con, schema='main', if_exists='append', index=False)
        print('Вакансии загружены в БД')

    @staticmethod
    def data_for_view(word: str = '') -> list:
        con = sqlite3.connect('db.sqlite')
        cur = con.cursor()
        data = []
        if word == '':
            cur.execute('''SELECT * FROM statistic ORDER BY id DESC LIMIT 4''')
        else:
            expression = f"SELECT * FROM statistic WHERE statistic.search_word = '{word}' ORDER BY id DESC LIMIT 4"
            cur.execute(expression)
            for line in cur:
                data.insert(0, line)
            if not data:  # or (str(date.today()) == data[0][7])
                print('слова нет в бд')
                DB.save_to_db(Analizer.create_table(word))
                cur.execute(expression)
        for line in cur:
            data.insert(0, line)
        return data


if __name__ == '__main__':
    DB.create_new_db()
