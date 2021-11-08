import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        avg_salary = (salary_from + salary_to) / 2
        return avg_salary

    elif not salary_from and not salary_to:
        return None

    elif salary_from:
        return salary_from * 1.2

    elif salary_to:
        return salary_to * 0.8


def predict_rub_salary_hh(language):
    page = 0
    pages_amount = 1
    found_vacancies = 0
    processed_vacancies = 0
    sum_salary = 0

    while page < pages_amount:
        url = 'https://api.hh.ru/vacancies/'
        payload = {'text': language, 'period': '1', 'area': '1', 'page': page}
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()

        page_data = page_response.json()
        pages_amount = page_data['pages']
        vacancies = page_data['items']

        for vacancy in vacancies:
            found_vacancies += 1
            salary = vacancy['salary']
            if salary and salary['currency'] == 'RUR':
                salary = predict_salary(salary['from'], salary['to'])
                sum_salary += salary
                processed_vacancies += 1
        page += 1

    average_solary = int(sum_salary / processed_vacancies)

    statistics = {
        'found_vacancies': found_vacancies,
        'processed_vacancies': processed_vacancies,
        'average_solary': average_solary,
    }
    return statistics


def predict_rub_salary_sj(language, token):
    results_more = True
    page = 0
    found_vacancies = 0
    sum_salary = 0
    processed_vacancies = 0

    while results_more:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {'X-Api-App-Id': token}
        payload = {
            't': '4',
            'keyword': language,
            'page': page,
            'count': 100,
            'period': 0,
        }

        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        vacancies = page_response.json()['objects']
        results_more = page_response.json()['more']

        for vacancy in vacancies:
            found_vacancies += 1
            if vacancy['currency'] == 'rub':
                salary = predict_salary(
                    vacancy['payment_from'],
                    vacancy['payment_to'],
                )
                if salary:
                    sum_salary += salary
                    processed_vacancies += 1

        page += 1

    average_solary = int(sum_salary / processed_vacancies)

    statistics = {
        'found_vacancies': found_vacancies,
        'processed_vacancies': processed_vacancies,
        'average_solary': average_solary,
    }

    return statistics


def create_table(statistics, languages, title):
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for language in languages:
        line = [language]
        for value in statistics[language].values():
            line.append(value)
        table_data.append(line)

    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)


def main():
    hh_statistics = {}
    sj_statistics = {}
    languages = ['c#', 'c++', 'ruby', 'javaScript', 'python', 'php', 'java']
    load_dotenv()
    sj_token = os.getenv('SJ_TOKEN')

    for language in languages:
        hh_statistics[language] = predict_rub_salary_hh(language)
        sj_statistics[language] = predict_rub_salary_sj(language, sj_token)

    create_table(sj_statistics, languages, 'SuperJob Moscow')
    create_table(hh_statistics, languages, 'HeadHunter Moscow')


if __name__ == '__main__':
    main()
