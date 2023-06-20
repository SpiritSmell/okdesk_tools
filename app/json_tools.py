import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import pandas as pd
import re

JSON_FILE_NAME = '../issues.json'
EXCEL_FILE_NAME = "../data.xlsx"


def is_dict(variable):
    """
    Checks if a variable is a dictionary.

    Args:
        variable: The variable to be checked.

    Returns:
        bool: True if the variable is a dictionary, False otherwise.
    """
    return isinstance(variable, dict)


def is_list(variable):
    """
    Checks if a variable is a list.

    Args:
        variable: The variable to be checked.

    Returns:
        bool: True if the variable is a list, False otherwise.
    """
    return isinstance(variable, list)


def is_tuple(variable):
    """
    Checks if a variable is a tuple.

    Args:
        variable: The variable to be checked.

    Returns:
        bool: True if the variable is a tuple, False otherwise.
    """
    return isinstance(variable, tuple)


def is_dict_subset(source, destination):
    """
    Checks if a dictionary is a subset of another dictionary.

    Args:
        source (dict): The dictionary to check if it is a subset.
        destination (dict): The dictionary to check against.

    Returns:
        bool: True if the source dictionary is a subset of the destination dictionary, False otherwise.
    """
    return all(item in destination.items() for item in source.items())


def extract_dict(item, field, row):
    """
    Extracts values from a nested dictionary and assigns them to corresponding keys in the row dictionary.

    Args:
        item (dict): The dictionary to extract values from.
        field (dict): The dictionary specifying the nested fields to extract.
        row (dict): The dictionary to assign the extracted values to.

    Returns:
        None.
    """
    for subfield in field:
        try:
            field_value = item[subfield]
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
            row[subfield] = field_value[field[subfield]]
        except Exception as e:
            print(f"Exception {e}")


def load_json_from_file(filename):
    """
    Loads JSON data from a file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        dict: The loaded JSON data.
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def fill_out_data(json_data, export_fields):
    """
    Fills out data from JSON based on the export fields configuration.

    Args:
        json_data (dict): The JSON data to extract values from.
        export_fields (list): The list of export field configurations.

    Returns:
        list: The filled out data rows.
    """
    rows = []
    for item in json_data:
        row = {}
        for field in export_fields:
            if not is_dict(field):
                try:
                    row[field] = item[field]
                except Exception as e:
                    print(f"Поле {e} не найдено. Проверьте настройки выгрузки.")
                continue
            extract_dict(item, field, row)
        rows.append(row)
    return rows


def merge_tuples(data):
    """
    Merges tuples into a single string.

    Args:
        data (list): The list of data to merge.

    Returns:
        list: The merged data list.
    """
    if not data:
        return None
    result = []
    for item in data:
        if is_tuple(item):
            item = "".join(item)
        result.append(item)
    return result


def extract_data(json_data, filter_fields):
    """
    Extracts data from JSON based on the filter fields configuration.

    Args:
        json_data (dict): The JSON data to extract values from.
        filter_fields (list): The list of filter field configurations.

    Returns:
        list: The extracted data rows.
    """
    rows = []
    for item in json_data:
        row = {}
        for filter_field in filter_fields:
            do_not_save_record = False
            jsonpath_expression = parse(filter_field['filter'])
            match = ''
            for match_1 in jsonpath_expression.find(item):
                match += json.dumps(match_1.value, ensure_ascii=False)
            if match == '':
                match = '""'
            if 'regexp_filter' in filter_field:
                pattern = filter_field['regexp_filter']
                try:
                    regexp_matches = re.findall(pattern, match)
                except Exception as e:
                    print(f"Error processing regexps {e} . Check config settings.")
                if not regexp_matches:
                    do_not_save_record = True
                    break
                regexp_matches = merge_tuples(regexp_matches)
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


def save_data_to_excel(data, filename, append=False):
    """
    Saves data to an Excel file.

    Args:
        data (list): The data to be saved.
        filename (str): The name of the Excel file.

    Returns:
        None.
    """
    try:
        df = pd.DataFrame(data)
        if append:
            with pd.ExcelWriter(filename, mode='a') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
        else:
            df.to_excel(filename, index=False)
        print("Excel files saved successfully:", filename)
    except Exception as e:
        print("Error saving data (is the file opened elsewhere?):", e)


def save_json_to_file(data, filename):
    """
    Saves JSON data to a file.

    Args:
        data (dict): The JSON data to be saved.
        filename (str): The name of the file.

    Returns:
        None.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    EXPORT_FIELDS = load_json_from_file('../data/json_to_excel.cfg')
    json_data = load_json_from_file(JSON_FILE_NAME)
    rows = extract_data(json_data, EXPORT_FIELDS)
    save_data_to_excel(rows, EXCEL_FILE_NAME)
