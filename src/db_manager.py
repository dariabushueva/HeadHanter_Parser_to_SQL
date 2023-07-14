import psycopg2


class DBManager:
    """ Класс для работы с БД Postgres"""

    def __init__(self, db_name: str, db_params: dict):
        self.db_name = db_name
        self.db_params = db_params

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT title, open_vacancies FROM employers')
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
                    """
                    SELECT employers.title, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url
                    FROM employers
                    JOIN vacancies USING (employer_id)
                    ORDER BY employers.title
                    """
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
                    """
                    SELECT ROUND(AVG((salary_from + salary_to)/2))
                    FROM vacancies
                    WHERE salary_from IS NOT NULL
                    AND salary_to IS NOT NULL
                    """
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
                    """
                    SELECT title, salary_from, salary_to
                    FROM vacancies
                    WHERE salary_to > (
                    	SELECT AVG((salary_from + salary_to)/2)
                    	FROM vacancies
                    	WHERE salary_from IS NOT NULL
                    	AND salary_to IS NOT NULL
                    	)
                    """
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_vacancies_with_keyword(self, key_word):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python” """

        with psycopg2.connect(dbname=self.db_name, **self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT *
                    FROM vacancies
                    WHERE title LIKE '%{key_word}%'
                    """
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

