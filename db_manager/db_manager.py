import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **params)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT employer_name, open_vacancies '
                        'FROM employers '
                        'ORDER BY employer_name DESC')
            rows = cur.fetchall()
            for row in rows:
                print(f'Компания "{row[0]}", {row[1]} вак.')

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT employer_name, vacancy_name, vacancy_url '
                        'FROM vacancies '
                        'ORDER BY employer_name DESC')
            rows = cur.fetchall()
            for row in rows:
                print(f'Компания "{row[0]}", должность - {row[1]}, ссылка на вакансию: {row[2]}')

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT (AVG(salary_from)+AVG(salary_to))/2 '
                        'AS salary_avg '
                        'FROM vacancies')
            rows = cur.fetchall()
            for row in rows:
                print(f'Средняя зарплата по вакансиям составляет {row[0]}')

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT vacancy_name, salary_from, vacancy_url '
                        'FROM vacancies '
                        'WHERE salary_from > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies) '
                        'ORDER BY salary_from DESC')
            rows = cur.fetchall()
            for row in rows:
                print(f'Должность - {row[0]}, начальная зарплата: {row[1]}, ссылка на вакансию: {row[2]}')

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT employer_name, vacancy_name, vacancy_url "
                        f"FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'"
                        f"ORDER BY employer_name DESC")
            rows = cur.fetchall()
            for row in rows:
                print(f'Компания "{row[0]}", должность - {row[1]}, ссылка на вакансию: {row[2]}')
