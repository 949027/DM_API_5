import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        avg_salary = (salary_from + salary_to) / 2
        return avg_salary

    elif salary_from:
        return salary_from * 1.2

    elif salary_to:
        return salary_to * 0.8

    return None


def predict_rub_salary_hh(language):
    page_number = 0
    pages_amount = 1
    processed_vacancies = 0
    sum_salary = 0
    publish_period = 1
    city_id = 1

    while page_number < pages_amount:
        url = 'https://api.hh.ru/vacancies/'
        payload = {
            'text': language,
            'period': publish_period,
            'area': city_id,
            'page': page_number
        }
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()

        page = page_response.json()
        pages_amount = page['pages']
        vacancies = page['items']
        found_vacancies = page['found']

        for vacancy in vacancies:
            salary = vacancy['salary']
            if salary and salary['currency'] == 'RUR':
                salary = predict_salary(salary['from'], salary['to'])
                sum_salary += salary
                processed_vacancies += 1
        page_number += 1

    average_salary = int(sum_salary / processed_vacancies)

    statistics = {
        'found_vacancies': found_vacancies,
        'processed_vacancies': processed_vacancies,
        'average_salary': average_salary,
    }
    return statistics


def predict_rub_salary_sj(language, token):
    results_more = True
    page_number = 0
    sum_salary = 0
    processed_vacancies = 0
    city_id = 4
    publish_period = 0

    while results_more:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {'X-Api-App-Id': token}
        payload = {
            't': city_id,
            'keyword': language,
            'page': page_number,
            'count': 100,
            'period': publish_period,
        }

        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        page = page_response.json()
        vacancies = page['objects']
        results_more = page['more']
        found_vacancies = page['total']

        for vacancy in vacancies:
            if vacancy['currency'] == 'rub':
                salary = predict_salary(
                    vacancy['payment_from'],
                    vacancy['payment_to'],
                )
                if salary:
                    sum_salary += salary
                    processed_vacancies += 1

        page_number += 1

    average_salary = int(sum_salary / processed_vacancies)

    statistics = {
        'found_vacancies': found_vacancies,
        'processed_vacancies': processed_vacancies,
        'average_salary': average_salary,
    }

    return statistics


def create_table(statistics, title):
    table = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]]
    for language, calculations in statistics.items():
        line = [language, *calculations.values()]
        table.append(line)

    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[2] = 'right'

    return table_instance.table


def main():
    hh_statistics = {}
    sj_statistics = {}
    languages = ['c#', 'c++', 'ruby', 'javaScript', 'python', 'php', 'java']
    load_dotenv()
    sj_token = os.getenv('SJ_TOKEN')

    for language in languages:
        hh_statistics[language] = predict_rub_salary_hh(language)
        sj_statistics[language] = predict_rub_salary_sj(language, sj_token)

    hh_table = create_table(sj_statistics, 'SuperJob Moscow')
    sj_table = create_table(hh_statistics, 'HeadHunter Moscow')

    print(hh_table)
    print(sj_table)


if __name__ == '__main__':
    main()
