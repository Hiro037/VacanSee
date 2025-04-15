import pytest
from src.models import Vacancy
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Developer", 150000, "", "CompanyA", "Senior Python developer needed"),
        Vacancy("Java Engineer", None, "", "CompanyB", "Java backend development"),
        Vacancy("Data Scientist", 200000, "", "CompanyC", "Python and ML experience"),
        Vacancy("DevOps Engineer", 120000, "", "CompanyD", "Cloud infrastructure"),
        Vacancy("Junior Python", 80000, "", "CompanyE", "Learn Python programming"),
    ]

def test_filter_vacancies_keyword_title(sample_vacancies):
    result = filter_vacancies(sample_vacancies, "python")
    assert len(result) == 3
    assert all("python" in v.title.lower() or "python" in v.description.lower() for v in result)

def test_filter_vacancies_keyword_description(sample_vacancies):
    result = filter_vacancies(sample_vacancies, "cloud")
    assert len(result) == 1
    assert "DevOps" in result[0].title

def test_filter_vacancies_case_insensitive(sample_vacancies):
    result = filter_vacancies(sample_vacancies, "JAVA")
    assert len(result) == 1
    assert result[0].title == "Java Engineer"

def test_filter_vacancies_no_matches(sample_vacancies):
    result = filter_vacancies(sample_vacancies, "ruby")
    assert len(result) == 0

def test_sort_vacancies_descending(sample_vacancies):
    sorted_list = sort_vacancies(sample_vacancies)
    salaries = [v.salary if v.salary is not None else 0 for v in sorted_list]
    assert salaries == [200000, 150000, 120000, 80000, 0]

def test_sort_vacancies_ascending(sample_vacancies):
    sorted_list = sort_vacancies(sample_vacancies, reverse=False)
    salaries = [v.salary if v.salary is not None else 0 for v in sorted_list]
    assert salaries == [0, 80000, 120000, 150000, 200000]

def test_sort_vacancies_with_none():
    vacancies = [
        Vacancy("A", 0, "", "", ""),
        Vacancy("B", 100, "", "", ""),
        Vacancy("C", 50, "", "", "")
    ]
    sorted_list = sort_vacancies(vacancies)
    assert sorted_list[0].salary == 100
    assert sorted_list[1].salary == 50
    assert sorted_list[2].salary == 0

def test_get_top_vacancies(sample_vacancies):
    top = get_top_vacancies(sample_vacancies, 3)
    assert len(top) == 3
    assert top[0].salary == 200000
    assert top[1].salary == 150000
    assert top[2].salary == 120000

def test_get_top_more_than_exists(sample_vacancies):
    top = get_top_vacancies(sample_vacancies, 10)
    assert len(top) == 5

def test_get_top_zero_or_negative(sample_vacancies):
    assert len(get_top_vacancies(sample_vacancies, 0)) == 0
    assert len(get_top_vacancies(sample_vacancies, -5)) == 0

def test_empty_inputs():
    assert filter_vacancies([], "test") == []
    assert sort_vacancies([]) == []
    assert get_top_vacancies([], 5) == []