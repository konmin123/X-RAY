import datetime
import json
import threading
from typing import Union

import pandas
import requests


class RequestHH:
    """
    Класс получающий данные через "https://api.hh.ru/vacancies".\n
    Класс имеет следующие атрибуты:\n
    data - словарь в который в процессе загрузки данных добавляются списки
    содержащие параметры запроса и json объект с полученными данными.\n
    __search_word - список содержащий строку для дальнейшего запроса данных
    через "https://api.hh.ru/vacancies".\n
    __exp - список кортежей хранящий уровни опыта, необходим для дальнейшего
    запроса данных через "https://api.hh.ru/vacancies".\n
    Класс имеет следующие методы:\n
    get_page() - метод непосредственно осуществляющий запрос на
    "https://api.hh.ru/vacancies". Принимает: слово для поиска,
    уровень опыта требуемый в вакансии, номер страницы данных.
    Добавляет список из json объекта и параметров запроса в RequestHH.data.\n
    threading_request() - метод осуществляющий множественные вызовы метода
    get_page в многопоточном режиме для увеличения скорости работы программы.\n
    set_search_words() - метод 'сеттер' для установки значения в атрибут
    RequestHH.__search_word.\n
    clear_data() - метод для отчистки данных в атрибуте RequestHH.data.
    """

    data: dict[str, list] = {
        "noExperience": [],
        "between1And3": [],
        "between3And6": [],
        "moreThan6": []
    }

    __search_word: list[str] = [""]

    __exp: list[tuple[str]] = [
        ("без опыта", "noExperience"),
        ("с опытом от года до трёх лет", "between1And3"),
        ("с опытом от трёх до шести лет", "between3And6"),
        ("с опытом больше шести лет", "moreThan6"),
    ]

    @classmethod
    def get_page(cls, word: str, exp: tuple, page: int = 0) -> None:
        """
        Метод непосредственно осуществляющий запрос на
        "https://api.hh.ru/vacancies". Принимает: слово для поиска,
        уровень опыта требуемый в вакансии, номер страницы данных.
        Добавляет список из json объекта и параметров запроса в RequestHH.data.
        """
        params: dict[str, Union[str, int]] = {
            "text": "Name:" + word,
            "area": 113,
            "page": page,
            "experience": exp[1],
            "per_page": 100,
            "search_word": word,
            "experience_level": exp[0],
        }

        req = requests.get("https://api.hh.ru/vacancies", params)
        data = req.content.decode()
        req.close()
        obj = json.loads(data)
        cls.data[exp[1]].append([obj, params])

    @classmethod
    def threading_request(cls) -> None:
        """
        Метод осуществляющий множественные вызовы метода
        get_page в многопоточном режиме для увеличения скорости работы
        программы.
        """
        threading_count = len(threading.enumerate())
        RequestHH.clear_data()
        for exp in cls.__exp:
            for page in range(0, 20):
                th = threading.Thread(
                    target=cls.get_page, args=(cls.__search_word[0], exp, page)
                )
                th.start()
            while True:
                if len(threading.enumerate()) == threading_count:
                    break

    @classmethod
    def set_search_words(cls, word: str) -> None:
        """
        Метод 'сеттер' для установки значения в атрибут
        RequestHH.__search_word.
        """
        cls.__search_word: list = []
        cls.__search_word.append(word)

    @classmethod
    def clear_data(cls) -> None:
        """
        Метод для отчистки данных в атрибуте RequestHH.data.
        """
        cls.data: dict[str, list] = {
            "noExperience": [],
            "between1And3": [],
            "between3And6": [],
            "moreThan6": [],
        }


class CurrencyConverter:
    """
    Класс отвечающий за получение актуального курса валюты. \n
    Имеет атрибут:\n
    __data - содержит json объект полученный в результате запроса на url
    'https://www.cbr-xml-daily.ru/daily_json.js'.\n
    Имеет метод:\n
    exchange_rate() - метод принимает строку(str, абривиатуру валюты в формате:
    'USD', 'EUR'), возвращает мультипликатор для перевода валюты в рубли.
    """

    __data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()

    @classmethod
    def exchange_rate(cls, currency: str) -> float:
        """
        Метод принимает строку (абривиатуру валюты в формате: 'USD', 'EUR'),
        возвращает мультипликатор
        для перевода валюты в рубли.
        """
        if currency == "RUR":
            return 1
        data = CurrencyConverter.__data
        return data["Valute"][currency]["Value"]


class Analizer:
    raw_data = {
        "count_vac": 0,
        "count_vac_for_salary": 0,
        "sum_min_salary": 0,
        "count_min_salary": 0,
        "sum_max_salary": 0,
        "count_max_salary": 0,
        "remote": 0,
    }
    data = {
        "language_db": [],
        "experience_db": [],
        "count_vac_db": [],
        "ave_salary_db": [],
        "count_for_ave_sal_db": [],
        "remote_db": [],
        "date_db": [],
    }

    @classmethod
    def slicer(cls):
        count = 0
        for item in RequestHH.data.values():
            for object_ in item:
                count += 1
                try:
                    for vac in object_[0]["items"]:
                        cls.squeezer(vac)
                    if count == 20:
                        cls.data["language_db"].append(object_[1]
                                                       ["search_word"])
                        cls.data["experience_db"].append(object_[1]
                                                         ["experience_level"])
                        cls.data_transfer()
                        count = 0
                except KeyError:
                    continue

    @classmethod
    def data_transfer(cls):
        raw = cls.raw_data
        data = cls.data
        if raw["count_min_salary"] > 0 and raw["count_max_salary"] > 0:
            ave_min_salary = raw["sum_min_salary"] / raw["count_min_salary"]
            ave_max_salary = raw["sum_max_salary"] / raw["count_max_salary"]
            ave_salary = int((ave_min_salary + ave_max_salary) / 2)

            cls.data["ave_salary_db"].append(ave_salary)
        else:
            cls.data["ave_salary_db"].append(0)

        data["count_vac_db"].append(raw["count_vac"])
        data["count_for_ave_sal_db"].append(raw["count_vac_for_salary"])
        data["remote_db"].append(raw["remote"])
        data["date_db"].append(datetime.date.today())

        cls.clear_raw_data()

    @classmethod
    def squeezer(cls, vac):
        raw = cls.raw_data
        raw["count_vac"] += 1
        if vac["schedule"]["id"] == "remote":
            raw["remote"] += 1
        if vac["salary"]:
            if vac["salary"]["currency"] in ["RUR", "USD", "EUR"]:
                cur = vac["salary"]["currency"]
                raw["count_vac_for_salary"] += 1
                if vac["salary"]["from"]:
                    raw["sum_min_salary"] += vac["salary"][
                        "from"
                    ] * CurrencyConverter.exchange_rate(cur)
                    raw["count_min_salary"] += 1
                if vac["salary"]["to"]:
                    raw["sum_max_salary"] += vac["salary"][
                        "to"
                    ] * CurrencyConverter.exchange_rate(cur)
                    raw["count_max_salary"] += 1

    @classmethod
    def clear_raw_data(cls):
        for name_item in cls.raw_data:
            cls.raw_data[name_item] = 0

    @classmethod
    def clear_date(cls):
        for name_item in cls.data:
            cls.data[name_item] = []

    @classmethod
    def create_table(cls, word):
        Analizer.clear_date()
        Analizer.clear_raw_data()
        RequestHH.set_search_words(word)
        RequestHH.threading_request()
        Analizer.slicer()
        df = pandas.DataFrame(
            {
                "search_word": cls.data["language_db"],
                "experience": cls.data["experience_db"],
                "quantity_vac": cls.data["count_vac_db"],
                "avarage_salary": cls.data["ave_salary_db"],
                "number_of_vacancies_for_avarage_salary": cls.data[
                    "count_for_ave_sal_db"
                ],
                "remote_vac": cls.data["remote_db"],
                "created_at": cls.data["date_db"],
            }
        )
        Analizer.clear_date()
        Analizer.clear_raw_data()
        return df
