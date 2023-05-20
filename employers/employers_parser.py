import json
from transliterate import translit
import requests


class EmployersParser:
    """Парсинг компаний работодателя"""
    url = 'https://api.hh.ru/employers?only_with_vacancies=true'

    def get_employer_data(self, keyword):
        """
        Метод получает данные о 10 компаниях
        :param keyword: ключевое слово, которое используется для поиска в названии или описании компании
        :return: список словарей с информацией о компаниях
        """
        params = {'text': keyword.lower(),
                  'page': 1,
                  'per_page': 10,
                  'area': '113',
                  'only_with_salary': True}
        response = requests.get(self.url, params=params).json()['items']
        return response

    def get_employer_id(self, employers_data):
        """
        Метод получает id компании, необходим для дальнейшего поиска вакансий конкретной компании
        :param employers_data: список словарей с информацией о компаниях
        :return: список с id компаний
        """
        id_list = []
        for item in employers_data:
            id_list.append(item.get('id'))
        return id_list

    def get_json_employers(self, keyword):
        """
        Метод сохраняет информацию в json-файл
        :param keyword: кодовое слово для поиска компаний
        """
        data = self.get_employer_data(keyword)
        translit_filename = translit(keyword, language_code='ru', reversed=True)
        new_filename = f'{translit_filename}_employers.json'
        with open(new_filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=5)
            return f"Данные о работодателях по кодовому слову '{keyword}' выгружены в файл {new_filename}"
