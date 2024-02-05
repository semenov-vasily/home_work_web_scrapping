import json
from pprint import pprint
import bs4
import requests
import fake_headers
import lxml


# Функция создания ссылки url
def url_create(query):
    query_ready = "+".join([i for i in query.split(',')])
    url = f'https://spb.hh.ru/search/vacancy?text={query_ready}&area=1&area=2'
    return url

# Функция парсинга страницы headhunter по url и создания итогового файла vacancies.json
def json_file(url):
    vacancies = []
    headers = fake_headers.Headers(os="win", browser="chrome")
    headers = headers.generate()
    response = requests.get(url, headers=headers)
    main_html = response.text
    soup = bs4.BeautifulSoup(main_html, "lxml")
    vacancies_list_tag = soup.find("div", id="a11y-main-content")
    vacancy_tags = vacancies_list_tag.find_all("div", class_="vacancy-serp-item-body")
    for tag in vacancy_tags:
        # название вакансии
        name_vacancy = tag.find("span", class_="serp-item__title").text
        # ссылка на вакансию
        link_vacancy = tag.find("a")["href"]
        # вилка зарплаты
        salary_vacancy = tag.find("span", class_="bloko-header-section-2")
        salary = (" ".join(salary_vacancy.text.split('\u202f')) if salary_vacancy else "не указана")
        # название компании
        company_vacancy = tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
        company = " ".join(company_vacancy.text.split('\xa0'))
        # город
        city_vacancy = tag.find_all("div", class_="bloko-text")
        city = (" ".join(city_vacancy[1].text.split('\xa0'))).split(',')[0]
        # Словарь по данным вакансии
        dict_vacancies = {"name_vacancy": name_vacancy,
                          "link_vacancy": link_vacancy,
                          "salary": salary,
                          "company": company,
                          "city": city}
        # Записываем словарь итоговый список
        vacancies.append(dict_vacancies)
    with open("vacancies.json", "w", encoding="utf-8") as file:
        json.dump(vacancies, file, indent=3, ensure_ascii=False)
    return vacancies


# Строка запроса
query = 'Python,Django,Flask'
pprint(json_file(url_create(query)))
