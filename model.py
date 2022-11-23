import sqlite3


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


if __name__ == '__main__':
    DB.create_new_db()
