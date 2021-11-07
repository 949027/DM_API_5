from terminaltables import AsciiTable, DoubleTable, SingleTable



statistics = {'python': {'vacancies_found': 32, 'vacancies_processed': 25, 'average_solary': 121256}, 'java': {'vacancies_found': 17, 'vacancies_processed': 15, 'average_solary': 222000}}

table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
title = 'статистика с sj'

print(statistics.values())



table_instance = SingleTable(table_data, title)
table_instance.justify_columns[2] = 'right'
print(table_instance.table)
print()
