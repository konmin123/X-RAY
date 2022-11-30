import sqlite3

from service import Analizer
from settings import app, db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_word = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    quantity_vac = db.Column(db.Integer)
    avarage_salary = db.Column(db.Integer)
    number_of_vacancies_for_avarage_salary = db.Column(db.Integer)
    remote_vac = db.Column(db.Integer)
    created_at = db.Column(db.Date)

    @staticmethod
    def create_db():
        app.app_context().push()
        db.create_all()

    @staticmethod
    def save_to_db(df):
        con = sqlite3.connect("instance///bd.db")
        df.to_sql("data", con, schema="main", if_exists="append", index=False)
        print("Вакансии загружены в БД")

    @staticmethod
    def data_for_view(word: str = "") -> list:
        data = []
        if word == "":
            cur = Data.query.order_by(Data.id.desc()).limit(4).all()
        else:
            cur = (
                Data.query.filter_by(search_word=word)
                .order_by(Data.id.desc())
                .limit(4)
                .all()
            )
            if not cur:
                Data.save_to_db(Analizer.create_table(word))
                cur = Data.query.order_by(Data.id.desc()).limit(4).all()
        for line in cur:
            data.insert(0, line)
        return data
