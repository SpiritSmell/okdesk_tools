import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import pandas as pd
import re

JSON_FILE_NAME = 'issues.json'

EXCEL_FILE_NAME = "data.xlsx"
#        "regexp_filter": "Отложена|Решена|В очереди|Ожидание ответа от пользователя"
EXPORT_FIELDS = [{'name': '№ заявки', 'filter': '$.id'},
                 {'name': 'Тема', 'filter': '$.title'},
                 {'name': 'Характер задачи', 'filter': '$.parameters[?(@.code=="A")].value'},
                 {'name': 'Дата регистрации', 'filter': '$.created_at'},
                 {'name': 'Отдел', 'filter': '$.depart'},
                 {'name': 'Ответственный сотрудник', 'filter': '$.assignee.name'},
                 {'name': 'Контактное лицо', 'filter': '$.contact.name'},
                 {'name': 'Наблюдатели', 'filter': '$.observers'},
                 {'name': 'Статус', 'filter': '$.status.name'}
                 ]


# {'parameters': [{0: 'value'}]}
#regexp_filter": "name\": \"([^\"]*)"
# EXPORT_FIELDS = ['id', 'title', {'parameters': {'search_name': 'name', 'search_value': 'Характер задачи',
# 'value': 'value'}}, 'created_at','depart', {'assignee': 'name'}, {'contact': 'name'}, 'observers', {'status':
# 'name'}]


# возвращает True если переменная является словарем
def is_dict(variable):
    return isinstance(variable, dict)


# возвращает True если переменная является списком
def is_list(variable):
    return isinstance(variable, list)

def is_tuple(variable):
    return isinstance(variable, tuple)


def is_dict_subset(source, destination):
    return all(item in destination.items() for item in source.items())


def extract_dict(item, field, row):
    # иначе разбираем что там внутри
    for subfield in field:
        try:
            # вытаскиваем ветвь
            field_value = item[subfield]
            # если поле пустое
            if not field_value:
                row[subfield] = ''
                continue
            if is_dict(field[subfield]):
                search_name = field[subfield]['search_name']
                search_value = field[subfield]['search_value']
                search_dict = {search_name: search_value}
                value_field = field[subfield]['value']
                for field_value_item in field_value:
                    if is_dict_subset(search_dict, field_value_item):
                        row[subfield] = field_value_item[value_field]
                        continue
                continue
            # иначе - добавляем вложенное поле
            row[subfield] = field_value[field[subfield]]
        except Exception as e:
            print(f"Exception {e}")


def load_json_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def fill_out_data(json_data, export_fields):
    # вытаскиваем данные из JSON и помещаем в матрицу
    rows = []
    for item in json_data:
        row = {}
        for field in export_fields:
            # если поле не является словарем, то присваиваем и идем дальше
            if not is_dict(field):
                try:
                    row[field] = item[field]
                except Exception as e:
                    print(f"Поле {e} не найдено. Проверьте настройки выгрузки.")
                continue
            # иначе разбираем что там внутри
            extract_dict(item, field, row)
        rows.append(row)
    return rows

def merge_tuples(data):
    if not data:
        return None
    result = []
    for item in data:
        if is_tuple(item):
            item ="".join(item)
        result.append(item)
    return result


def extract_data(json_data, filter_fields):
    # вытаскиваем данные из JSON и помещаем в матрицу
    rows = []
    for item in json_data:
        row = {}
        for filter_field in filter_fields:
            do_not_save_record = False
            jsonpath_expression = parse(filter_field['filter'])

            #matches = [match.value for match in jsonpath_expression.find(item)]
            ## выбираем только первый элемент
            #if matches:
            #    match = matches[0]

            match = ''

            for match_1 in jsonpath_expression.find(item):
                match += json.dumps(match_1.value, ensure_ascii=False)

            # на случай если значение было пустое
            if match == '':
                match = '""'
            # дополнительный regexp фильтр
            if 'regexp_filter' in filter_field:
                pattern = filter_field['regexp_filter']

                try:
                    regexp_matches = re.findall(pattern, match)
                except Exception as e:
                    print(f"Error processing regexps {e} . Check config settings.")
                # если не подошло по regexp фильтру - выходим из цикла и устанавливаем флаг чтоб не записывать.
                if not regexp_matches:
                    do_not_save_record = True
                    break
                # если в результате выполнения фильтра regexp получилось несколько групп, объединяем их в одну
                regexp_matches = merge_tuples(regexp_matches)
                # объединяем элементы в одну строку
                try:
                    match = " ".join(regexp_matches)
                except Exception as e:
                    print(f"Error joining regexps {e} . Check config settings.")
            try:
                row[filter_field['name']] = match
            except Exception as e:
                print(f"Fiels {e} is not found. Check config settings.")
            continue
        if not do_not_save_record:
            rows.append(row)
    return rows


def save_data_to_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print("Data saved successfully:", filename)
    except Exception as e:
        print("Error saving data (is file opened elsewhere?):", e)


def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    EXPORT_FIELDS = load_json_from_file('json_to_excel.cfg')
    # save_json_to_file(EXPORT_CONFIG,'json_to_excel.cfg')
    json_data = load_json_from_file(JSON_FILE_NAME)

    # rows = fill_out_data(json_data, EXPORT_FIELDS)

    rows = extract_data(json_data, EXPORT_FIELDS)
    #  df = pd.DataFrame(rows)
    save_data_to_excel(rows, EXCEL_FILE_NAME)
