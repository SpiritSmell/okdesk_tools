import sys
import getopt
import json
import extract_issues as ei
import json_to_excel as je
import send_to_email as se

SETTINGS = {
    'send_to_email':
        {
            'smtp_server': 'eurasia-kz.mail.protection.outlook.com',
            'smtp_port': 25,
            'sender_email': 'vladimir.muzychenko@eurasia.kz',
            'receiver_emails': ['receiver1@example.com', 'receiver2@example.com', 'receiver3@example.com'],
            'subject': 'Тестовое письмо с вложением',
            'message_text': 'Привет, это тестовое письмо.',
            'attachment_path': 'data.xlsx'
        },
    'json_to_excel':
        {
            'JSON_FILE_NAME': 'issues.json',
            'EXCEL_FILE_NAME': 'data.xlsx',
            'CONFIG_FILENAME': 'json_to_excel.cfg'
        },
    'extract_issues':
        {
            'API_TOKEN': "2050867b5d83e762932efeb84042c510fe9f5440",
            'ADDRESS': "https://egk.okdesk.ru",
            'JSON_FILE_NAME': "issues.json",
            'FILTER_ATTRIBUTE_NAME': "depart",
            'FILTER_ATTRIBUTE_VALUE': "Отдел сервисного обслуживания",
            'SINCE': '04-04-2023',
            'UNTIL': '06-06-2023'
        }
}


def print_help():
    print("Usage: your_script.py -h|--help -s|--server=<SMTP server> -r|--sender=<sender email> "
          "-f|--receivers=<receiver emails> -t|--subject=<subject> -a|--text=<message text> "
          "--attachment=<attachment path>")
    print("")
    print("Options:")
    print("-h, --help                   Show help message and exit")
    print("-c --config <filename>")
    print("")
    print("Example:")
    print("extract_and_send_xlsx.py -c /path/to/config.cfg ")


def get_arguments():
    global config_path

    # define parameters
    short_options = "hc:"
    long_options = ["help", "config="]

    # get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 1:
        print_help()
        sys.exit(2)

    # process command line parameters
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-c", "--config"):
            config_path = current_value
            print("Config path:", config_path)

    # process remaining arguments
    for value in values:
        print("Extra arguments:", value)


def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent = 4, ensure_ascii=False)

def load_json_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def main():
    global config_path
    #save_json_to_file(SETTINGS, 'config.cfg')
    SETTINGS = load_json_from_file(config_path)

    # load settings into extract_issues.py
    for item in SETTINGS['extract_issues']:
        setattr(ei, item, SETTINGS['extract_issues'][item])

    ei.main()

    # load settings into json_to_excel.py
    for item in SETTINGS['json_to_excel']:
        setattr(je, item,SETTINGS['json_to_excel'][item])

    je.main()

    # load settings into send_to_email.py
    for item in SETTINGS['send_to_email']:
        setattr(se, item, SETTINGS['send_to_email'][item])

    se.main()
    #print(SETTINGS)

if __name__ == '__main__':
    get_arguments()
    main()
