import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **params)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT employer_name, open_vacancies '
                        'FROM employers')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT employer_name, vacancy_name, vacancy_url'
                        'FROM employers'
                        'JOIN vacancies USING(employer_id))')
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT vacancy_name "
                        f"FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'")
            rows = cur.fetchall()
            for row in rows:
                print(row)
