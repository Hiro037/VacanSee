from src.api import HeadHunterAPI
from src.models import Vacancy
from src.storage import JSONStorage
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies


def user_interaction():
    print("\n🔍 Добро пожаловать в VacanSee!\n")

    # Получение поискового запроса
    keyword = input("Введите поисковый запрос (например, Python): ").strip()

    # Получение данных с hh.ru
    print(f"\n📡 Загружаем вакансии по запросу: {keyword} ...")
    api = HeadHunterAPI()
    vacancies_data = api.fetch_and_format(keyword)
    vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

    # Сохранение вакансий в файл
    storage = JSONStorage()
    for v in vacancies:
        storage.save(v)

    print(f"✅ Загружено и сохранено {len(vacancies)} вакансий.\n")

    # Получение топ-N вакансий
    try:
        top_n = int(input("Введите количество вакансий для вывода (например, 10): ").strip())
    except ValueError:
        print("⚠️ Некорректный ввод. Выведем топ-5.")
        top_n = 5

    # Фильтрация по ключевым словам
    filter_input = input("Введите ключевые слова для фильтрации (через пробел): ").strip()
    filter_keywords = filter_input.split() if filter_input else []

    # Применение фильтров
    filtered = vacancies
    for word in filter_keywords:
        filtered = filter_vacancies(filtered, word)

    if not filtered:
        print("\n❌ Вакансии по заданным фильтрам не найдены.")
        return

    # Сортировка и топ
    sorted_vacancies = sort_vacancies(filtered)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод
    print(f"\n📋 Топ-{top_n} вакансий:\n")
    for vacancy in top_vacancies:
        print(vacancy)

    print("\n✅ Завершено!")
