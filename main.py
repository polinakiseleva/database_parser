from config import config
from employers.employers_parser import EmployersParser
from vacancies.vacancies_parser import VacanciesParser
from db_manager.db_creation import create_tables, create_database, enter_data_into_emp_database, \
    enter_data_into_vac_database
from db_manager.db_manager import DBManager


def main():

    print('Мы рады приветствовать вас!\n'
          'Эта программа предназначена для получения информации о работодателях\n'
          'и их вакансиях, а также для создания базы данных, которую можно будет\n'
          'использовать для получения нужной информации.\n')

    params = config()

    employer_kw = input('Введите ключевое слово, по которому будет осуществляться\n'
                        'поиск работодателя: ')
    exp_emp = EmployersParser()
    employers_data = exp_emp.get_employer_data(employer_kw)
    employers_indexes = exp_emp.get_employer_id(employers_data)

    print('Ищем информацию о работодателях и их вакансиях...\n')

    exp_emp.get_json_employers(employer_kw)

    exp_vac = VacanciesParser()
    vacancies_data = exp_vac.get_employers_vacancies(employers_indexes)
    exp_vac.get_json_vacancies(employer_kw, vacancies_data)

    db_name = input('Для продолжения работы введите название базы данных: ').strip().replace(' ', '_')
    print(f'Создаем базу данных с названием {db_name}...')
    print(f'Загружаем данные о работодателях и вакансиях в базу данных {db_name}...\n')

    create_database(db_name, params)
    create_tables(db_name, params)
    enter_data_into_emp_database(db_name, params)
    enter_data_into_vac_database(db_name, params)

    while True:
        db_manager = DBManager(db_name, config())
        user_input = input("\nДля продолжения работы выберите команду из списка:\n"
                           "1: Получение списка всех компаний и количества вакансий у каждой компании\n"
                           "2: Получение списка всех вакансий с указанием названия компании, "
                           "названия вакансии и ссылки на вакансию\n"
                           "3: Получение списка всех вакансий по ключевому слову\n"
                           "4: Получение средней зарплаты по вакансиям\n"
                           "5: Получение списка вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                           "6: Выход из программы\n"
                           "   Введите цифру нужной команды: ").strip()

        if user_input == '1':
            db_manager.get_companies_and_vacancies_count()

        elif user_input == '2':
            db_manager.get_all_vacancies()

        elif user_input == '3':
            vacancy_kw = input('   Введите ключевое слово: ').strip()
            db_manager.get_vacancies_with_keyword(vacancy_kw)

        elif user_input == '4':
            db_manager.get_avg_salary()

        elif user_input == '5':
            db_manager.get_vacancies_with_higher_salary()

        elif user_input not in ('1', '2', '3', '4', '5', '6'):
            print('Такой команды нет в списке. Пожалуйста, повторите ввод')
            user_input = input('Введите команду из списка: ').strip()

        elif user_input == '6':
            print('\nБлагодарим за использование программы! До новых встреч!')
            break


if __name__ == "__main__":
    main()
