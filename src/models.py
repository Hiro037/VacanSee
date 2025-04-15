from abc import ABC, abstractmethod
from typing import Any, Optional


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
    __slots__ = ["title", "salary", "url", "employer", "description"]

    def __init__(self, title: str, salary: int, url: str, employer: str, description: str):
        self.title = self.__validate_str(title)
        self.salary = self.__validate_salary(salary)
        self.url = url
        self.employer = employer
        self.description = description

    def __validate_str(self, value: str) -> str:
        return value if value else "Не указано"

    def __validate_salary(self, value: Optional[int]) -> int:
        return value if isinstance(value, int) and value > 0 else 0

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        return cls(
            title=data.get("title", "Не указано"),
            salary=data.get("salary", 0),
            url=data.get("url", ""),
            employer=data.get("employer", "Неизвестно"),
            description=data.get("description", "")
        )

    def to_dict(self) -> dict:
        return {attr: getattr(self, attr) for attr in self.__slots__}

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
