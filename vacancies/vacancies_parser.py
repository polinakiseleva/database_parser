import json
import requests
from transliterate import translit


class VacanciesParser:
    """Парсинг вакансий работодателя"""

    url = 'https://api.hh.ru/vacancies'

    def get_employers_vacancies(self, indexes):
        """
        Метод получает данные о вакансиях компаний
        :param indexes: список из id компаний, результат работы метода get_employer_id
        :return: список словарей с информацией о вакансиях
        """
        params = {'employer_id': indexes,
                  'per_page': 100,
                  }
        response = requests.get(self.url, params=params).json()['items']
        return response

    def get_json_vacancies(self, filename, data):
        """
        Метод сохраняет информацию в json-файл
        :param filename: название файла, в который будет сохраняться информация о конкретных вакансиях
        :param data: список словарей с информацией о вакансиях, результат работы метода get_employers_vacancies
        """
        vacancy_list = []
        with open('./vacancy.json', 'w', encoding='utf-8') as file:
            for item in data:
                employer_id = int(item.get('employer').get('id'))
                employer_name = str(item.get('employer').get('name'))
                vacancy_title = str(item.get('name'))
                vacancy_url = str(item.get('alternate_url'))
                new_data = {
                    'employer_id': employer_id,
                    'employer_name': employer_name,
                    'vacancy_title': vacancy_title,
                    'vacancy_url': vacancy_url
                }
                vacancy_list.append(new_data)
            json.dump(vacancy_list, file, ensure_ascii=False, indent=5)
            return f"Данные о вакансиях по кодовому слову '{filename}' выгружены в файл 'vacancy.json'"
