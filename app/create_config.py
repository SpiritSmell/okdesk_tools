import sys
import getopt
import json
import os
import pandas as pd
import copy
from pathlib import Path


CONFIG_ENTRY_TEMPLATE= \
    {
        "extract_and_send_xlsx":
        {
            "send_to_email": {
                "sender_email": "noreply@eurasia.kz",
                "receiver_emails": [
                    "vladimir.muzychenko@eurasia.kz",
                    "vladimir.muzychenko@eurasia.kz"
                ]
            },

            "extract_issues": {
                "FILTER_ATTRIBUTE_NAME": "depart",
                "FILTER_ATTRIBUTE_VALUE": "Отдел продаж запасных частей"
            }
        },
        "CONFIG_FILE_NAME": "..\\data\\extract_and_send_xlsx.cfg"
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

class ConfigCreator:
    def __init__(self):
        self.INPUT_XLSX = None
        self.OUTPUT_CFG = None
        self.settings = None

    @staticmethod
    def print_help():
        """
        Prints the help message with usage instructions.
        """
        print("Usage: config_creator.py -h|--help -c|--config=<filename>")
        print("")
        print("Options:")
        print("-h, --help                   Show help message and exit")
        print("-c, --config <filename>      Path to the configuration file")
        print("")
        print("Example:")
        print("config_creator.py -c /path/to/batch_send.cfg")

    def get_arguments_from_env(self):
        # Read the value from the environment variable
        value = os.getenv("input")
        if value:
            self.INPUT_XLSX = value.strip('"').strip("'")
        output = os.getenv("output")
        if value:
            self.INPUT_XLSX = value.strip('"').strip("'")

    def get_arguments(self):
        """
        Retrieves and processes the command-line arguments.
        """
        # Define parameters
        short_options = "hi:o:"
        long_options = ["help", "input=", "output="]

        # Get command line arguments
        arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

        # Process command line parameters
        for current_argument, current_value in arguments:
            if current_argument in ("-h", "--help"):
                self.print_help()
            elif current_argument in ("-i", "--input"):
                self.INPUT_XLSX = current_value
                print("Config path:", self.INPUT_XLSX)
            elif current_argument in ("-o", "--output"):
                self.OUTPUT_CFG = current_value
                print("Config path:", self.OUTPUT_CFG)

        # Process remaining arguments
        for value in values:
            print("Extra arguments:", value)

    @staticmethod
    def save_json_to_file(data, filename):
        """
        Saves JSON data to a file.
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_json_from_file(filename):
        """
        Loads JSON data from a file.
        """
        with open(filename, 'r', encoding='cp1251') as file:
            data = json.load(file)
        return data

    def main(self):
        """
        Main function to extract issues, convert to Excel, and send the email with attachments using the provided settings.
        """

        if not self.INPUT_XLSX:
            print("Error: Config path is not found")
            self.print_help()
            sys.exit(2)


        # Загрузка данных из файла Excel в DataFrame
        if not file_exist(self.INPUT_XLSX):
            print("Error: Config file is not found")
            self.print_help()
            sys.exit(2)

        df = pd.read_excel(self.INPUT_XLSX)

        config_data = []

        # Вывод первых нескольких строк DataFrame
        for item in range(len(df)):
            department = df.at[item, 'Department']
            email = df.at[item, 'e-mail']
            data_item = copy.deepcopy(CONFIG_ENTRY_TEMPLATE)
            data_item['extract_and_send_xlsx']['extract_issues']['FILTER_ATTRIBUTE_VALUE'] = department
            data_item['extract_and_send_xlsx']['send_to_email']['receiver_emails']=[email]
            config_data.append(data_item)
        self.save_json_to_file(config_data,self.OUTPUT_CFG)



if __name__ == '__main__':
    cc = ConfigCreator()
    cc.get_arguments_from_env()
    cc.get_arguments()
    cc.main()
