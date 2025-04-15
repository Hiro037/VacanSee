from abc import ABC, abstractmethod
from typing import List, Dict
import requests


class VacancyAPI(ABC):
    """Абстрактный класс для подключения к API платформ с вакансиями"""

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """Метод для получения вакансий по ключевому слову"""
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API hh.ru"""

    __BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self, pages: int = 5, per_page: int = 20):
        self.pages = pages
        self.per_page = per_page
        self.vacancies: List[Dict] = []

    @property
    def base_url(self) -> str:
        return self.__BASE_URL

    def get_vacancies(self, keyword: str) -> List[Dict]:
        all_vacancies = []

        for page in range(self.pages):
            params = {"text": keyword, "page": page, "per_page": self.per_page}
            response = requests.get(self.__BASE_URL, params=params)

            if response.status_code != 200:
                print(f"Ошибка запроса: {response.status_code}")
                continue

            items = response.json().get("items", [])
            all_vacancies.extend(items)

        self.vacancies = all_vacancies
        return all_vacancies

    @staticmethod
    def format_vacancy_data(vacancy: Dict) -> Dict:
        return {
            "title": vacancy.get("name"),
            "salary": vacancy.get("salary", {}).get("from") if vacancy.get("salary") else 0,
            "city": vacancy.get("area", {}).get("name"),
            "url": vacancy.get("alternate_url"),
            "employer": vacancy.get("employer", {}).get("name"),
            "requirements": vacancy.get("snippet", {}).get("requirement"),
            "responsibilities": vacancy.get("snippet", {}).get("responsibility")
        }

    def fetch_and_format(self, keyword: str) -> List[Dict]:
        raw_vacancies = self.get_vacancies(keyword)
        return [self.format_vacancy_data(v) for v in raw_vacancies]
