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
                    employer_id int PRIMARY KEY,
                    employer_name varchar(255) NOT NULL,
                    open_vacancies int,
                    employer_url text NOT NULL
                    )
                """)
        print('Таблица "employers" успешно создана!')

    with connection.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS vacancies (
                    employer_id int,
                    employer_name varchar(255) NOT NULL,
                    vacancy_name varchar(255) NOT NULL,
                    vacancy_url text NOT NULL,
                    FOREIGN KEY (employer_id) REFERENCES employers(employer_id)
                    )
                """)
        print('Таблица "vacancies" успешно создана!')
    connection.commit()
    connection.close()


def enter_data_into_emp_database(db_name, params, emp_data):
    connection = psycopg2.connect(dbname=db_name, **params)
    with connection.cursor() as cur:
        with open(emp_data, encoding='utf-8') as file:
            employer = json.load(file)
            for emp in employer:
                employer_name = emp['name']
                employer_url = emp['alternate_url']
                open_vacancies = emp['open_vacancies']
                cur.executemany(
                    'INSERT INTO employers VALUES (%s, %s, %s)',
                    [(employer_name, employer_url, open_vacancies)])
            print('Таблица "employers" успешно заполнена данными!')

    connection.commit()
    connection.close()


def enter_data_into_vac_database(db_name, params, vac_data):
    connection = psycopg2.connect(dbname=db_name, **params)
    with connection.cursor() as cur:
        with open(vac_data, encoding='utf-8') as file:
            vacancies = json.load(file)
            for vac in vacancies:
                employer_name = vac['employer']['name']
                vacancy_name = vac['name']
                employer_id = vac['employer_id']
                vacancy_url = vac['alternate_url']
                cur.executemany(
                    'INSERT INTO vacancies VALUES (%s, %s, %s, %s)',
                    [(employer_name, vacancy_name, employer_id, vacancy_url)])
            print('Таблица "vacancies" успешно заполнена данными!')

        connection.commit()
        connection.close()
