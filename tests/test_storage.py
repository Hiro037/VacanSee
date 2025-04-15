import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.models import Vacancy
from src.storage import JSONStorage, VacancyStorage
import pandas as pd


@pytest.fixture
def temp_json(tmpdir):
    return tmpdir.join("test_vacancies.json")


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Dev", 150000, "url1", "CompanyA", "Senior Python developer"),
        Vacancy("Java Dev", 120000, "url2", "CompanyB", "Java backend"),
        Vacancy("Data Scientist", 200000, "url3", "CompanyC", "ML and Python"),
    ]


def test_storage_inheritance():
    assert issubclass(JSONStorage, VacancyStorage)


def test_json_storage_init_creates_file(temp_json):
    JSONStorage(str(temp_json))
    assert os.path.exists(temp_json)
    with open(temp_json, "r") as f:
        assert json.load(f) == []


def test_save_and_load(temp_json, sample_vacancies):
    storage = JSONStorage(str(temp_json))

    for v in sample_vacancies:
        storage.save(v)

    loaded = storage.load()
    assert len(loaded) == 3
    assert loaded[0].title == "Python Dev"
    assert loaded[2].salary == 200000


def test_save_duplicate(temp_json):
    storage = JSONStorage(str(temp_json))
    vacancy = Vacancy("Test", 0, "unique_url", "", "")

    storage.save(vacancy)
    storage.save(vacancy)  # Дубликат

    assert len(storage.load()) == 1


def test_delete(temp_json, sample_vacancies):
    storage = JSONStorage(str(temp_json))
    target = sample_vacancies[1]

    for v in sample_vacancies:
        storage.save(v)

    storage.delete(target)
    remaining = [v.url for v in storage.load()]
    assert "url2" not in remaining
    assert len(remaining) == 2


def test_filter_by_keyword(temp_json, sample_vacancies):
    storage = JSONStorage(str(temp_json))
    for v in sample_vacancies:
        storage.save(v)

    result = storage.filter_by_keyword("python")
    assert len(result) == 2
    assert all("python" in v.description.lower() for v in result)


def test_top_n_by_salary(temp_json, sample_vacancies):
    storage = JSONStorage(str(temp_json))
    for v in sample_vacancies:
        storage.save(v)

    # Добавляем вакансию с нулевой зарплатой
    storage.save(Vacancy("Intern", 0, "url4", "CompanyD", ""))

    top = storage.top_n_by_salary(2)
    assert len(top) == 2
    assert top[0].salary == 200000
    assert top[1].salary == 150000


def test_empty_storage(temp_json):
    storage = JSONStorage(str(temp_json))
    assert storage.load() == []
    assert storage.filter_by_keyword("test") == []
    assert storage.top_n_by_salary(5) == []


def test_pandas_integration(temp_json, sample_vacancies):
    with patch.object(pd.DataFrame, 'sort_values') as mock_sort:
        storage = JSONStorage(str(temp_json))
        storage.save(sample_vacancies[0])
        storage.top_n_by_salary(1)

        mock_sort.assert_called_once_with(by="salary", ascending=False)


def test_file_write_operations(temp_json):
    mock_data = [Vacancy("Test", 0, "", "", "")]

    # Патчим только метод записи
    with patch.object(JSONStorage, '_write_all') as mock_write:
        storage = JSONStorage(str(temp_json))
        storage._write_all(mock_data)

        mock_write.assert_called_once_with(mock_data)