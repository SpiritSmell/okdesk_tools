import json_tools as jt
import getopt
import sys

JSON_FILE_NAME = 'issues.json'
EXCEL_FILE_NAME = "data.xlsx"
CONFIG_FILENAME = 'json_to_excel.cfg'


def print_help():
    print(
        "Usage: extract_issues.py -h|--help -e|--excel=<attribute name> ")
    print(" -j|--json <json file name>   ")
    print(" -c|--config <config file name>")
    print(
        ' Example: json_to_excel.py --excel="data.xlsx"  --json="issues.json" --config="json_to_excel.cfg"')
    print('Config file example:')
    print('["id", "title", {"parameters": {"search_name": "name", "search_value": "Характер задачи", '
          '"value": "value"}}, "created_at", "depart", {"assignee": "name"}, {"contact": "name"}, "observers", '
          '{"status": "name"}]')


def get_arguments():
    global EXCEL_FILE_NAME
    global JSON_FILE_NAME
    global CONFIG_FILENAME

    # options definition
    short_options = "he:j:c:"
    long_options = ["help", "excel=", "json=", "config="]

    # get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 3:
        print_help()
        sys.exit(2)
    # Обработка полученных параметров
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-e", "--excel"):
            EXCEL_FILE_NAME = current_value
            print("Attribute name:", EXCEL_FILE_NAME)
        elif current_argument in ("-j", "--json"):
            JSON_FILE_NAME = current_value
            print("JSON file name:", JSON_FILE_NAME)
        elif current_argument in ("-c", "--config"):
            CONFIG_FILENAME = current_value
            print("Config file name:", CONFIG_FILENAME)

    # Обработка оставшихся аргументов
    for value in values:
        print("Extra arguments:", value)


def main():
    EXPORT_FIELDS = jt.load_json_from_file(CONFIG_FILENAME)
    json_data = jt.load_json_from_file(JSON_FILE_NAME)
    rows = jt.fill_out_data(json_data, EXPORT_FIELDS)
    jt.save_data_to_excel(rows, EXCEL_FILE_NAME)


if __name__ == '__main__':
    get_arguments()

    main()
