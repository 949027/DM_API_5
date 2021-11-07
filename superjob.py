import requests
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        avg_salary = (salary_from + salary_to) / 2
        return int(avg_salary)

    elif not salary_from and not salary_to:
        return None

    elif salary_from:
        return int(salary_from * 1.2)

    elif salary_to:
        return int(salary_to * 0.8)


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
            if salary:
                if salary['currency'] == 'RUR':
                    salary = predict_salary(salary['from'], salary['to'])
                    sum_salary += salary
                    processed_vacancies +=1
        page += 1

    average_solary = int(sum_salary / processed_vacancies)

    statistics = {
        'vacancies_found': found_vacancies,
        'vacancies_processed': processed_vacancies,
        'average_solary': average_solary,
    }
    return statistics


def predict_rub_salary_sj(language):
    result_more = True
    page = 0
    found_vacancies = 0
    sum_salary = 0
    processed_vacancies = 0
    while result_more:
        page += 1
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': 'v3.r.135478234.45de286f7bd7826e6a6d84180f47cb92aa81497f.f60797102d049007d32304a50b1d38f44c56b102'
        }
        payload = {
            't': '4',
            'keyword': language,
            'page': page,
            'count': 50,
            'period': 0,
        }

        page_response = requests.get(url, headers=headers, params=payload)
        page_response.raise_for_status()
        vacancies = page_response.json()['objects']
        result_more = page_response.json()['more']

        for vacancy in vacancies:
            found_vacancies += 1
            if vacancy['currency'] == 'rub':
                salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
                if salary:
                    sum_salary += salary
                    processed_vacancies += 1

    average_solary = int(sum_salary / processed_vacancies)

    statistics = {
        'vacancies_found': found_vacancies,
        'vacancies_processed': processed_vacancies,
        'average_solary': average_solary,
    }
    return statistics


# def create_table(statistics):
#     table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
#     table_data.append([statistics.keys(), list(statistics['python'].values())])
#     print(table_data)
#     table = AsciiTable(table_data)
#     print(table.table)



def main():
    total_hh_statistics = {}
    total_sj_statistics = {}
    languages = ['python', 'java']

    for language in languages:
        #total_hh_statistics[language] = predict_rub_salary_hh(language)
        total_sj_statistics[language] = predict_rub_salary_sj(language)
        #create_table(total_sj_statistics)



    #print(total_hh_statistics)
    print(total_sj_statistics)




if __name__ == '__main__':
    main()