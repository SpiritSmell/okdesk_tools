import sys
import getopt
import json
import os
import okdesk_tools
from pathlib import Path

data = {"key": "value", "some_unicode_char": "\u049b"}

CONFIG_ENTRY_TEMPLATE= \
    {
        "API_TOKEN": "2050867b5d83e762932efeb84042c510fe9f5440",
        "ADDRESS": "https://egk.okdesk.ru",
        "ROLES_FILE_NAME": "..\\data\\roles.json",
        "CONTACTS_FILE_NAME": "..\\data\\contacts.json",
        "COMPANIES_FILE_NAME": "..\\data\\companies.json",
        "ISSUES_FILE_NAME": "..\\data\\issues.json",
        "receiver_emails": [
                    "darkhan.rakhimov@eurasia.kz"
                ]
    }

def file_exist(file_name):

    # Получаем полный путь к текущей рабочей директории
    current_directory = os.getcwd()

    # Соединяем путь к файлу
    file_path = os.path.abspath(file_name)

    # Проверка существования файла
    if Path(file_path).is_file():
        print("File exists.")
        return True
    else:
        print("File does not exist.")
        return False

class ItemsExtractor:
    def __init__(self):
        self.CONFIG = None
        self.settings = None

    @staticmethod
    def print_help():
        """
        Prints the help message with usage instructions.
        """
        print("Usage: extract_items.py -h|--help -c|--config=<filename>")
        print("")
        print("Options:")
        print("-h, --help                   Show help message and exit")
        print("-c, --config <filename>      Path to the configuration file")
        print("")
        print("Example:")
        print("extract_items.py -c /path/to/extract_items.cfg")

    def get_arguments_from_env(self):
        # Read the value from the environment variable
        value = os.getenv("config")
        if value:
            self.CONFIG = value.strip('"').strip("'")

    def get_arguments(self):
        """
        Retrieves and processes the command-line arguments.
        """
        # Define parameters
        short_options = "hc:"
        long_options = ["help", "config="]

        # Get command line arguments
        arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

        # Process command line parameters
        for current_argument, current_value in arguments:
            if current_argument in ("-h", "--help"):
                self.print_help()
            elif current_argument in ("-c", "--config"):
                self.CONFIG = current_value
                print("Config path:", self.CONFIG)


        # Process remaining arguments
        for value in values:
            print("Extra arguments:", value)

    @staticmethod
    def save_json_to_file(data, filename):
        """
        Saves JSON data to a file.
        """
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_json_from_file(filename):
        """
        Loads JSON data from a file.
        """
        with open(filename, 'r', encoding='cp1251') as file:
            data = json.load(file)
        return data

    def load_settings_from_file(self):
        if not self.CONFIG:
            print("Error: Config path is not found")
            self.print_help()
            sys.exit(2)

        self.settings = self.load_json_from_file(self.CONFIG)

    def main(self):
        """
        Main function to extract issues, convert to Excel, and send the email with attachments using the provided settings.
        """

        # Загрузка данных из файла Excel в DataFrame
        if not file_exist(self.CONFIG):
            print("Error: Config file is not found")
            self.print_help()
            sys.exit(2)

        okdesk_api = okdesk_tools.OKDeskAPI(self.settings["API_TOKEN"], self.settings["ADDRESS"])

        self.save_json_to_file(okdesk_api.roles,self.settings["ROLES_FILE_NAME"])
        self.save_json_to_file(okdesk_api.contacts, self.settings["CONTACTS_FILE_NAME"])
        self.save_json_to_file(okdesk_api.companies, self.settings["COMPANIES_FILE_NAME"])
        issues = okdesk_api.get_issues(okdesk_api.fetch_all_issues())
        self.save_json_to_file(issues, self.settings["ISSUES_FILE_NAME"])


if __name__ == '__main__':
    ie = ItemsExtractor()
    ie.get_arguments_from_env()
    ie.get_arguments()
    ie.save_json_to_file(CONFIG_ENTRY_TEMPLATE,ie.CONFIG)
    ie.load_settings_from_file()
    ie.main()
