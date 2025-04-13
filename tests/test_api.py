import pytest
from unittest.mock import Mock, patch
from src.api import HeadHunterAPI, VacancyAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI(pages=2, per_page=5)


@pytest.fixture
def mock_response(hh_api):
    response = Mock()
    response.status_code = 200
    items = [
        {
            "name": f"Python Developer {i}",
            "salary": {"from": 100000 + i, "currency": "RUR"},
            "area": {"name": "Москва"},
            "alternate_url": f"http://example.com/{i}",
            "employer": {"name": "TechCorp"},
            "snippet": {
                "requirement": "Опыт работы с Python",
                "responsibility": "Разработка ПО"
            }
        } for i in range(hh_api.per_page)
    ]
    response.json.return_value = {"items": items}
    return response


@pytest.fixture
def mock_error_response():
    response = Mock()
    response.status_code = 500
    return response


def test_hh_api_inheritance():
    assert issubclass(HeadHunterAPI, VacancyAPI)


def test_get_vacancies_success(hh_api, mock_response):
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = hh_api.get_vacancies("Python")
        expected_count = hh_api.pages * hh_api.per_page
        assert len(result) == expected_count
        assert mock_get.call_count == hh_api.pages
        assert hh_api.vacancies == result


def test_get_vacancies_error_handling(hh_api, mock_error_response):
    with patch('requests.get', return_value=mock_error_response):
        result = hh_api.get_vacancies("Python")
        assert len(result) == 0


def test_format_vacancy_data():
    test_data = {
        "name": "DevOps Engineer",
        "salary": None,
        "area": {"name": ""},
        "alternate_url": "",
        "employer": {},
        "snippet": {"requirement": None, "responsibility": ""}
    }

    formatted = HeadHunterAPI.format_vacancy_data(test_data)

    assert formatted["title"] == "DevOps Engineer"
    assert formatted["salary"] == 0
    assert formatted["city"] == ""
    assert formatted["url"] == ""
    assert formatted["employer"] is None
    assert formatted["requirements"] is None
    assert formatted["responsibilities"] == ""


def test_fetch_and_format(hh_api):
    with patch.object(hh_api, 'get_vacancies') as mock_get:
        mock_get.return_value = [{"name": "Test Job"}]
        result = hh_api.fetch_and_format("Python")
        assert len(result) == 1
        assert result[0]["title"] == "Test Job"
        mock_get.assert_called_once_with("Python")


def test_pagination_params():
    api = HeadHunterAPI(pages=3, per_page=10)
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": []}

        api.get_vacancies("Python")

        assert mock_get.call_count == 3
        calls = [call.kwargs['params'] for call in mock_get.call_args_list]
        assert [c["page"] for c in calls] == [0, 1, 2]
        assert all(c["per_page"] == 10 for c in calls)