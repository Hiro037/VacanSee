from abc import ABC, abstractmethod
from typing import Any


# Абстрактный базовый класс
class BaseVacancy(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """Человеко-понятное отображение вакансии"""
        pass

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """Сравнение вакансий по зарплате"""
        pass


# Конкретный класс вакансии
class Vacancy(BaseVacancy):
    def __init__(self, title: str, salary: int, url: str, employer: str, description: str):
        self.title = title
        self.salary = salary
        self.url = url
        self.employer = employer
        self.description = description

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        return cls(
            title=data.get("title", "Не указано"),
            salary=data.get("salary", 0),
            url=data.get("url", ""),
            employer=data.get("employer", "Неизвестно"),
            description=data.get("description", "")
        )

    def __str__(self) -> str:
        return f"{self.title} — {self.salary} руб. / {self.employer}"

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary
