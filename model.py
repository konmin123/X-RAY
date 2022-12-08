import sqlite3

import pandas

from service import Analizer
from settings import app, db


class Data(db.Model):
    """Класс создающий базу данных и описывающий взаимодействие с ней,
    имеет следующие публичные методы:\n
    create_db() - создаёт базу данных sqlite3.\n
    save_to_db() - сохраняет датафрейм(pandas) с данными в базу данных.\n
    data_for_view() - создаёт список данных для рендеренга страницы. На вход
    плучает строку для поискового запроса. Проверяет наличие в базе данных
    соответсвующих запросу данных. В случае наличия, возвращает данные из базы,
    иначе обращается к методу create_table класса Analizer для получения этих
    данных.
    """
    id = db.Column(db.Integer, primary_key=True)
    search_word = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    quantity_vac = db.Column(db.Integer)
    avarage_salary = db.Column(db.Integer)
    number_of_vacancies_for_avarage_salary = db.Column(db.Integer)
    remote_vac = db.Column(db.Integer)
    created_at = db.Column(db.Date)

    @staticmethod
    def create_db() -> None:
        """Метод создаёт базу данных sqlite3."""
        app.app_context().push()
        db.create_all()

    @staticmethod
    def save_to_db(df: pandas.DataFrame) -> None:
        """Метод сохраняет датафрейм(pandas) с данными в базу данных."""
        con = sqlite3.connect("instance///bd.db")
        df.to_sql("data", con, schema="main", if_exists="append", index=False)

    @staticmethod
    def data_for_view(word: str = "") -> list:
        """Метод создаёт список данных для рендеренга страницы. На вход
    плучает строку для поискового запроса. Проверяет наличие в базе данных
    соответсвующих запросу данных. В случае наличия, возвращает данные из базы,
    иначе обращается к методу create_table класса Analizer для создания этих
    данных."""
        data: list = []
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
