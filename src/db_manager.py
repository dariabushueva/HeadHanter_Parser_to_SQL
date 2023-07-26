import psycopg2


class DBManager:
    """ Класс для работы с БД Postgres"""

    def __init__(self, db_name: str, db_params: dict, filename: str):
        self.db_name = db_name
        self.db_params = db_params
        self.filename = filename

    def get_queries_sql(self):
        """ Получает данные из SQL-файла и создает словарь для дальнейшего использования """

        with open(self.filename, 'r', encoding='utf-8') as sql_file:
            clear_queries = " ".join(line.strip() for line in sql_file if not line.startswith("--"))
            queries = clear_queries.split(';')
        with open(self.filename, 'r', encoding='utf-8') as sql_file:
            clear_comments = " ".join(line.strip() for line in sql_file if line.startswith("--"))
            comments = clear_comments.split('.')

        queries_dict = {comments[i].strip(): queries[i] for i in range(len(comments))}
        return queries_dict

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    self.get_queries_sql()['-- Получает список всех компаний и количество вакансий у каждой компании']
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    self.get_queries_sql()['-- Получает список всех вакансий с указанием названия компании, '
                                           'названия вакансии и зарплаты и ссылки на вакансию']
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_avg_salary(self):
        """  Получает среднюю зарплату по вакансиям """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    self.get_queries_sql()['-- Получает среднюю зарплату по вакансиям']
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    self.get_queries_sql()['-- Получает список всех вакансий,'
                                           ' у которых зарплата выше средней по всем вакансиям']
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_vacancies_with_keyword(self, key_word: str):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python” """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    self.get_queries_sql()['-- Получает список всех вакансий,'
                                           ' в названии которых содержатся переданные в метод слова,'
                                           ' например “python”'], [f'%{key_word}%']
                    )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

