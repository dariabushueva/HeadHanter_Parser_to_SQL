from config import config
from src.utils import get_hh_employers, get_hh_vacancies, create_database, save_data_to_database


def main():

    employer_ids = ['677539',  # Издательство МАНН, ИВАНОВ и ФЕРБЕР
              #      '1993194',  # YADRO
              #      '1057',     # Лаборатория Касперского
              #      '2838290',  # Евромобайл
              #      '3935621',  # АО Север Телеком
              #      '1102601',  # Самолет
              #      '205152',   # Mindbox
              #      '2324020',  # Точка
              #      '99993',    # Модульбанк
                    '3536900']  # Платформа ОФД

    params = config()

    employer_data = get_hh_employers(employer_ids)
    vacancies_data = get_hh_vacancies(employer_ids)
    create_database('headhanter', params)
    save_data_to_database(employer_data, vacancies_data, 'headhanter', params)


if __name__ == '__main__':
    main()

 # select * from employers
 # select * from vacancies