import json
import pandas as pd

JSON_FILE_NAME = 'issues.json'

EXCEL_FILE_NAME = "data.xlsx"
# {'parameters': [{0: 'value'}]}

#EXPORT_FIELDS = ['id', 'title', {'parameters': {'search_name': 'name', 'search_value': 'Характер задачи', 'value': 'value'}}, 'created_at','depart', {'assignee': 'name'}, {'contact': 'name'}, 'observers', {'status': 'name'}]


# возвращает True если переменная является словарем
def is_dict(variable):
    return isinstance(variable, dict)


# возвращает True если переменная является списком
def is_list(variable):
    return isinstance(variable, list)


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


def fill_out_data(json_data,export_fields):
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
            # for subfield in field:
            #    try:
            #        # вытаскиваем ветвь
            #        field_value = item[subfield]
            #        # если поле пустое
            #        if not field_value:
            #            row[subfield] = ''
            #            continue
            #        # иначе - добавляем вложенное поле
            #        row[subfield] = field_value[field[subfield]]
            #    except Exception as e:
            #        print("Exception")
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
        json.dump(data, file, indent = 4, ensure_ascii=False)

if __name__ == '__main__':
    EXPORT_FIELDS = load_json_from_file('json_to_excel.cfg')
    json_data = load_json_from_file(JSON_FILE_NAME)

    rows = fill_out_data(json_data, EXPORT_FIELDS)
    df = pd.DataFrame(rows)
    save_data_to_excel(rows, EXCEL_FILE_NAME)


