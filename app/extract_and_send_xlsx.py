import sys
import getopt
import json
import os
import extract_issues as ei
import json_to_excel as je
import send_to_email as se

class IssueExtractor:
    def __init__(self):
        self.CONFIG_PATH = None
        self.settings = None

    @staticmethod
    def print_help():
        """
        Prints the help message with usage instructions.
        """
        print("Usage: extract_and_send_xlsx.py -h|--help -c|--config=<filename>")
        print("")
        print("Options:")
        print("-h, --help                   Show help message and exit")
        print("-c, --config <filename>      Path to the configuration file")
        print("")
        print("Example:")
        print("extract_and_send_xlsx.py -c /path/to/extract_and_send_xlsx.cfg")

    def get_arguments_from_env(self):
        # Read the value from the environment variable
        value = os.getenv("config")
        if value:
            self.CONFIG_PATH = value.strip('"').strip("'")

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
                self.CONFIG_PATH = current_value
                print("Config path:", self.CONFIG_PATH)

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

    def configure_module_settings(self, module, settings):
        """
        Loads the provided settings into the specified module.
        """
        for item in settings:
            setattr(module, item, settings[item])

    def load_settings_from_file(self):
        if not self.CONFIG_PATH:
            print("Error: Config path is not found")
            self.print_help()
            sys.exit(2)

        self.settings = self.load_json_from_file(self.CONFIG_PATH)

    def main(self):
        """
        Main function to extract issues, convert to Excel, and send the email with attachments using the provided settings.
        """

        # Load settings into extract_issues.py
        self.configure_module_settings(ei, self.settings.get('extract_issues', {}))
        ei.main()

        # Load settings into json_to_excel.py
        self.configure_module_settings(je, self.settings.get('json_to_excel', {}))
        je.main()

        # Load settings into send_to_email.py
        self.configure_module_settings(se, self.settings.get('send_to_email', {}))
        se.main()


if __name__ == '__main__':
    extractor = IssueExtractor()
    extractor.get_arguments_from_env()
    extractor.get_arguments()
    extractor.load_settings_from_file()
    extractor.main()
