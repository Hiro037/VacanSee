from src.models import Vacancy, BaseVacancy


def test_vacancy_inheritance():
    assert issubclass(Vacancy, BaseVacancy), "Vacancy должен наследовать BaseVacancy"


def test_vacancy_initialization():
    vacancy = Vacancy(
        title="Python Developer",
        salary=150000,
        url="http://example.com",
        employer="TechCorp",
        description="Разработка ПО"
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.salary == 150000
    assert vacancy.url == "http://example.com"
    assert vacancy.employer == "TechCorp"
    assert vacancy.description == "Разработка ПО"


def test_from_dict():
    data = {
        "title": "Data Scientist",
        "salary": 180000,
        "url": "http://ds.example.com",
        "employer": "DataCorp",
        "description": "Анализ данных"
    }

    vacancy = Vacancy.from_dict(data)

    assert vacancy.title == "Data Scientist"
    assert vacancy.salary == 180000
    assert vacancy.employer == "DataCorp"
    assert vacancy.description == "Анализ данных"


def test_from_dict_missing_fields():
    data = {"title": "Test"}
    vacancy = Vacancy.from_dict(data)

    assert vacancy.title == "Test"
    assert vacancy.salary == 0
    assert vacancy.url == ""
    assert vacancy.employer == "Неизвестно"
    assert vacancy.description == ""


def test_str_representation():
    vacancy = Vacancy("Java Developer", 120000, "", "BankCorp", "")
    assert str(vacancy) == "Java Developer — 120000 руб. / BankCorp"


def test_less_than_operator():
    v1 = Vacancy("A", 100000, "", "", "")
    v2 = Vacancy("B", 150000, "", "", "")

    assert v1 < v2
    assert not v2 < v1


def test_equal_operator():
    v1 = Vacancy("A", 100000, "", "", "")
    v2 = Vacancy("B", 100000, "", "", "")

    assert v1 == v2
    assert not (v1 != v2)


def test_zero_salary_representation():
    vacancy = Vacancy("Intern", 0, "", "", "")
    assert "0 руб." in str(vacancy)


def test_default_values():
    vacancy = Vacancy.from_dict({})

    assert vacancy.title == "Не указано"
    assert vacancy.salary == 0
    assert vacancy.employer == "Неизвестно"
    assert vacancy.description == ""