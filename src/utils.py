import requests
import time
from typing import Any
import psycopg2


def get_hh_employers(employer_ids: list[str]) -> list[dict[str, Any]]:
    """ Получение данных о работодателях с помощью API """

    employers = []
    for employer_id in employer_ids:

        response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        if response.status_code != 200:
            raise Exception(f"Ошибка получения данных {response.status_code}")
        employer_data = response.json()
        employers.append(employer_data)
        time.sleep(0.25)
        print(f"Загружаю информацию о работодателе с ID {employer_id}")

    return employers


def get_hh_vacancies(employer_ids: list[str], page=0) -> list[dict[str, Any]]:
    """ Получение данных о вакансиях с помощью API """

    vacancies = []
    vacancies.clear()
    for page in range(0, 20):

        params = {
            'employer_id': employer_ids,  # Идентификатор работодателя
            'page': page,  # Номер страницы
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'archived': False  # Не включать архивные вакансии
        }

        response = requests.get('https://api.hh.ru/vacancies', params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения данных {response.status_code}")
        vacancies_data = response.json()
        vacancies.extend(vacancies_data["items"])
        print(f"Загружаю {page + 1} страницу с вакансиями")
        if (vacancies_data['pages'] - page) <= 1:  # Проверка на последнюю страницу, если вакансий меньше 2000
            break
        time.sleep(0.25)

    return vacancies


def create_database(db_name: str, db_params: dict) -> None:
    """ Создает базу данных для сохранения полученных данных о работодателях и вакансиях """

    conn = psycopg2.connect(dbname='postgres', **db_params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')
    print(f'База данных {db_name} успешно создана')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **db_params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    open_vacancies INTEGER,
                    site_url TEXT,
                    hh_url TEXT NOT NULL
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    city VARCHAR(50),
                    address TEXT,
                    publish_date DATE,
                    vacancy_url TEXT NOT NULL,
                    requirement TEXT
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(employers_data: list[dict[str, Any]],
                          vacancies_data: list[dict[str, Any]],
                          db_name: str,
                          db_params: dict) -> None:
    """Сохраняет данные о канале и видео в базу данных"""

    conn = psycopg2.connect(dbname=db_name, **db_params)
    with conn.cursor() as cur:

        for employer in employers_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, title, open_vacancies, site_url, hh_url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    employer['id'],
                    employer['name'],
                    employer['open_vacancies'],
                    employer['site_url'],
                    employer['alternate_url']
                )
            )

        for vacancy in vacancies_data:

            address = vacancy['address']
            if address is not None:
                full_address = address['raw']
            else:
                full_address = None

            salary = vacancy['salary']
            if salary:
                salary_from = salary['from']
                salary_to = salary['to']
            else:
                salary_from = None
                salary_to = None

            cur.execute(
                """
                INSERT INTO vacancies (employer_id, title, salary_from, salary_to, city, 
                                        address, publish_date, vacancy_url, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    vacancy['employer']['id'],
                    vacancy['name'],
                    salary_from,
                    salary_to,
                    vacancy['area']['name'],
                    full_address,
                    vacancy['published_at'],
                    vacancy['alternate_url'],
                    vacancy['snippet']['requirement']
                )
            )
    conn.commit()
    conn.close()




