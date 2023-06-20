import okdesk_tools as od  # Importing the 'okdesk_tools' module
import getopt  # Importing the 'getopt' module for command-line argument parsing
import sys  # Importing the 'sys' module for system-specific parameters and functions
import pandas as pd
import json_tools as jt
from datetime import datetime, timedelta  # Importing the 'datetime' module for date and time manipulation

FILE_NAME = None
COPY_FIELDS=[
                            {
                                "name": "ID",
                                "filter": "$.id"
                            },
                            {
                                "name": "Имя",
                                "filter": "$.first_name",
                                "regexp_filter": "\"([^\"]*)\"",
                                "comment": "Regexp фильтр убирает кавычки"
                            },
                            {
                                "name": "Фамилия",
                                "filter": "$.last_name",
                                "regexp_filter": "\"([^\"]*)\"",
                                "comment": "Regexp фильтр убирает кавычки"
                            },
                            {
                                "name": "e-mail",
                                "filter": "$.email",
                                "regexp_filter": "\"([^\"]*)\"",
                                "comment": "Regexp фильтр убирает кавычки"
                            },
{
                                "name": "Мобильный",
                                "filter": "$.mobile_phone"
                            },
{
                                "name": "ID_компании",
                                "filter": "$.company_id"

                            },
                            {
                                "name": "Отдел",
                                "filter": "$.parameters[?(@.code==\"depart\")].value",
                                "regexp_filter": "\"([^\"]*)\"",
                                "comment": "filter фильтр выбирает параметр в разделе parameters у которого поле .code равно A. Regexp фильтр убирает кавычки"
                            },
                            {
                                "name": "Active",
                                "filter": "$.active"
                            }
            ]

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


def main():

    # Creating an instance of the OKDeskAPI class from 'okdesk_tools' module

    okdesk_api = od.OKDeskAPI(API_TOKEN, ADDRESS)
    contacts = okdesk_api.contacts

    #print(contacts)
    items = []
 #   for contact in contacts:
 #       item = {}
 ##       for field in COPY_FIELDS:
 #           item[field] = contact[field]

 #       items.append(item)

    items = jt.extract_data(contacts, COPY_FIELDS)

    save_data_to_excel(items,FILE_NAME)
    #od.save_json_to_file(issues, JSON_FILE_NAME)  # Saving the issues data to a JSON file


def print_help():
    print(
        "Usage: get_contacts.py -h|--help  ")
    print(" -f|--filename <export file name>  -k|--key <API key> ")
    print(" -a|--address <okdesk domain address>")
    print(
        'Example: get_contacts.py  '
        '--key="2050867b5d83e762932efeb84042c510fe" --address="https://egk.okdesk.ru" --filename="result.csv" ')


def get_arguments():
    global FILE_NAME
    global API_TOKEN
    global ADDRESS


    # Options definition
    short_options = "hf:k:a:"
    long_options = ["help", "filename=", "key=", "address="]

    # Get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 3:
        print_help()
        sys.exit(2)
    # Handling the received parameters
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-f", "--filename"):
            FILE_NAME = current_value
            print("File name:", FILE_NAME)
        elif current_argument in ("-k", "--key"):
            API_TOKEN = current_value
            print("Destination book name:", API_TOKEN)
        elif current_argument in ("-a", "--address"):
            ADDRESS = current_value
            print("Address:", ADDRESS)


    # Handling remaining arguments
    for value in values:
        print("Extra arguments:", value)


if __name__ == '__main__':
    get_arguments()

    main()
