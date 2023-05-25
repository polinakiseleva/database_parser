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

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT employer_name, vacancy_name, vacancy_url "
                        f"FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'"
                        f"ORDER BY employer_name DESC")
            rows = cur.fetchall()
            for row in rows:
                print(f'Компания "{row[0]}", должность - {row[1]}, ссылка на вакансию: {row[2]}')
