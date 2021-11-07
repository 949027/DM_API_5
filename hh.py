import requests


def predict_rub_salary(vacancy):
    try:
        salary = vacancy['salary']
        from_salary, to_salary, currency = salary['from'], salary['to'], salary['currency']
        if currency != 'RUR':
            return None
        if from_salary and to_salary:
            avg_salary = (from_salary + to_salary) / 2
            return int(avg_salary)
        elif not from_salary and not to_salary:
            return None
        elif from_salary:
            return int(from_salary * 1.2)
        elif to_salary:
            return int(to_salary * 0.8)
    except:
        return None

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
            salary = predict_rub_salary(vacancy)
            found_vacancies += 1
            if salary:
                sum_salary += salary
                processed_vacancies +=1
        page += 1

    average_solary = sum_salary / processed_vacancies

    statistics = {
        'vacancies_found': found_vacancies,
        'vacancies_processed': processed_vacancies,
        'average_solary': average_solary,
    }
    return statistics


def main():
    total_statistics = {}
    languages = ['c#', 'c++', 'ruby', 'javaScript', 'python', 'php', 'java']

    for language in languages:
        total_statistics[language] = get_statictics_for_language(language)
        print(total_statistics)

    print(total_statistics)


if __name__ == '__main__':
    main()
