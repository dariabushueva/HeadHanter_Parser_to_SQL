-- Получает список всех компаний и количество вакансий у каждой компании

SELECT title, open_vacancies FROM employers

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию

SELECT employers.title, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url
FROM employers
JOIN vacancies USING (employer_id)
ORDER BY employers.title

-- Получает среднюю зарплату по вакансиям

SELECT ROUND(AVG((salary_from + salary_to)/2))
FROM vacancies
WHERE salary_from IS NOT NULL
	AND salary_to IS NOT NULL

-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

SELECT title, salary_from, salary_to
FROM vacancies
WHERE salary_to > (
	SELECT AVG((salary_from + salary_to)/2)
	FROM vacancies
	WHERE salary_from IS NOT NULL
	AND salary_to IS NOT NULL)

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”

SELECT *
FROM vacancies
WHERE title LIKE '%{key_word}%'