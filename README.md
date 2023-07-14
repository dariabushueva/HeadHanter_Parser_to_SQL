# SQL “Парсер HeadHanter вакансий заранее определенных работодателей и заполнение таблиц базы данных”

## Задание

Получение данных через API HeadHanter (hh.ru) и создание базы данных, в которой будет храниться информация о работодателях
и вакансиях. В коде используются библиотеки requests, datetime, psycopg2.

## Запуск

1. Добавьте свой файл database.ini с конфигурацией по БД, содержащий секцию [postgresql]
2. Запустите скрипт.

## Использование

1. При запуске скрипт получит данные о работодателях и их вакансиях по API.
2. Данные по работодателям и вакансиям будут сохранены в БД PostgreSQL.
3. Скрипт предложит пользователю меню для работы с вакансиями.
4. Пользователь может выбрать пункт меню или выйти из программы.

## Изменение настроек

Вы можете изменить работодателей, для которых загружаются вакансии, изменив значение переменной employer_ids в файле main.py. 
ID работодателей можно получить на сайте HeadHanter путем извлечения цифровой части URL на странице работодателя