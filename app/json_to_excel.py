import json_tools as jt
import getopt
import sys
import shutil

JSON_FILE_NAME = None
EXCEL_FILE_NAME = None
CONFIG_FILENAME = None
EXCEL_TEMPLATE_NAME = None


def print_help():
    """
    Prints the help message with usage instructions.
    """
    print("Usage: extract_issues.py -h|--help -e|--excel=<attribute name> ")
    print(" -j|--json <json file name>   ")
    print(" -c|--config <config file name>")
    print(' Example: json_to_excel.py --excel="data.xlsx"  --json="issues.json" --config="json_to_excel.cfg"')
    print('Config file example:')
    print('["id", "title", {"parameters": {"search_name": "name", "search_value": "Характер задачи", '
          '"value": "value"}}, "created_at", "depart", {"assignee": "name"}, {"contact": "name"}, "observers", '
          '{"status": "name"}]')


def get_arguments():
    """
    Retrieves and processes the command-line arguments.
    """
    global EXCEL_FILE_NAME
    global JSON_FILE_NAME
    global CONFIG_FILENAME
    global EXCEL_TEMPLATE_NAME

    # Options definition
    short_options = "he:j:c:t:"
    long_options = ["help", "excel=", "json=", "config=","template="]

    # Get command line arguments
    try:
        arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as e:
        print(e)
        print_help()
        sys.exit(2)

    if len(arguments) < 3:
        print_help()
        sys.exit()

    # Process the obtained parameters
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
        elif current_argument in ("-t", "--template"):
            EXCEL_TEMPLATE_NAME = current_value
            print("Config file name:", EXCEL_TEMPLATE_NAME)

    # Process remaining arguments
    for value in values:
        print("Extra arguments:", value)


def main():
    """
    Main function to extract data from JSON and save it to Excel.
    """
    print("Export to Excel has started")
    try:
        json_data = jt.load_json_from_file(JSON_FILE_NAME)
        rows = jt.extract_data(json_data, EXPORT_FIELDS)
        if EXCEL_TEMPLATE_NAME:
            # Копирование файла
            shutil.copy(EXCEL_TEMPLATE_NAME, EXCEL_FILE_NAME)
        jt.save_data_to_excel(rows, EXCEL_FILE_NAME, append=(EXCEL_TEMPLATE_NAME is not None))
        print("Export to Excel completed successfully.")
    except Exception as e:
        print("An error occurred during export:", e)


if __name__ == '__main__':

    JSON_FILE_NAME = '../issues.json'
    EXCEL_FILE_NAME = '../data.xlsx'
    CONFIG_FILENAME = '../data/json_to_excel.cfg'
    EXCEL_TEMPLATE_NAME = '../data/template.xlsx'
    get_arguments()
    try:
        EXPORT_FIELDS = jt.load_json_from_file(CONFIG_FILENAME)
        main()
    except Exception as e:
        print("An error occurred:", e)
