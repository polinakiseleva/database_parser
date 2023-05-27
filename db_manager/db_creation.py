import json
import psycopg2


def create_database(db_name, params):
    connection = psycopg2.connect(dbname='postgres', **params)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f'База данных {db_name} успешно создана!')

    cursor.close()
    connection.close()


def create_tables(db_name, params):
    connection = psycopg2.connect(dbname=db_name, **params)

    with connection.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS employers (
                    employer_id serial PRIMARY KEY,
                    employer_name varchar(255) NOT NULL,
                    open_vacancies int,
                    employer_url text NOT NULL
                    )
                """)
        print('Таблица "employers" успешно создана!')

    with connection.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                    employer_id serial,
                    employer_name varchar(255) NOT NULL,
                    vacancy_name varchar(255) NOT NULL,
                    vacancy_url text NOT NULL,
                    salary_from int,
                    salary_to int)
                """)
        print('Таблица "vacancies" успешно создана!')
    connection.commit()
    connection.close()


def enter_data_into_emp_database(db_name, params):
    connection = psycopg2.connect(dbname=db_name, **params)
    with connection.cursor() as cur:
        with open('./employer.json', 'r', encoding='utf-8') as file:
            employer = json.load(file)
            for emp in employer:
                employer_name = emp['name']
                employer_url = emp['alternate_url']
                open_vacancies = emp['open_vacancies']
                cur.execute(
                    """
                    INSERT INTO employers (employer_name, employer_url, open_vacancies)
                    VALUES (%s, %s, %s)
                    """,
                    (employer_name, employer_url, open_vacancies)
                )
            print('Таблица "employers" успешно заполнена данными!')

    connection.commit()
    connection.close()


def enter_data_into_vac_database(db_name, params):
    connection = psycopg2.connect(dbname=db_name, **params)
    with connection.cursor() as cur:
        with open('./vacancy.json', encoding='utf-8') as file:
            vacancies = json.load(file)
            for vac in vacancies:
                employer_name = vac['employer_name']
                vacancy_name = vac['vacancy_title']
                vacancy_url = vac['vacancy_url']
                employer_id = vac['employer_id']
                salary_from = vac['salary_from']
                salary_to = vac['salary_to']
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, employer_name, vacancy_name, 
                    vacancy_url, salary_from, salary_to)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, employer_name, vacancy_name, vacancy_url, salary_from, salary_to)
                )
            print('Таблица "vacancies" успешно заполнена данными!')

        connection.commit()
        connection.close()
