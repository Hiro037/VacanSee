from typing import List
from src.models import Vacancy

def filter_vacancies(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """Фильтрует вакансии по ключевому слову (в заголовке или описании)"""
    keyword = keyword.lower()
    return [
        vacancy for vacancy in vacancies
        if keyword in vacancy.title.lower() or keyword in vacancy.description.lower()
    ]

def sort_vacancies(vacancies: List[Vacancy], reverse: bool = True) -> List[Vacancy]:
    """Сортирует вакансии по зарплате, обрабатывая None как 0"""
    return sorted(vacancies, key=lambda x: x.salary if x.salary is not None else 0, reverse=reverse)

def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """Возвращает топ-N вакансий по зарплате"""
    return sort_vacancies(vacancies)[:n]