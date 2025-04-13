import json
import os
from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from src.models import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для хранения вакансий."""

    @abstractmethod
    def save(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def filter_by_keyword(self, keyword: str) -> List[Vacancy]:
        pass

    @abstractmethod
    def top_n_by_salary(self, n: int) -> List[Vacancy]:
        pass


class JSONStorage(VacancyStorage):
    """Хранение вакансий в JSON-файле."""

    def __init__(self, file_path: str = "data/vacancies.json"):
        self._file_path = file_path
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save(self, vacancy: Vacancy) -> None:
        vacancies = self.load()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._write_all(vacancies)

    def load(self) -> List[Vacancy]:
        with open(self._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Vacancy.from_dict(v) for v in data]

    def delete(self, vacancy: Vacancy) -> None:
        vacancies = self.load()
        updated = [v for v in vacancies if v.url != vacancy.url]
        self._write_all(updated)

    def filter_by_keyword(self, keyword: str) -> List[Vacancy]:
        vacancies = self.load()
        return [v for v in vacancies if keyword.lower() in v.description.lower()]

    def top_n_by_salary(self, n: int) -> List[Vacancy]:
        vacancies = self.load()

        # Обработка пустого списка
        if not vacancies:
            return []

        # Создаем DataFrame с гарантированным наличием salary
        df = pd.DataFrame([{
            "title": v.title,
            "salary": v.salary if v.salary is not None else 0,
            "url": v.url,
            "employer": v.employer,
            "description": v.description
        } for v in vacancies])

        # Фильтрация только если есть данные
        if not df.empty:
            df = df[df["salary"] > 0].sort_values(by="salary", ascending=False)
            top_df = df.head(n)
        else:
            top_df = pd.DataFrame()

        return [Vacancy.from_dict(row.to_dict()) for _, row in top_df.iterrows()]

    def _write_all(self, vacancies: List[Vacancy]) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump([v.__dict__ for v in vacancies], f, ensure_ascii=False, indent=2)
