import okdesk_tools as od
import getopt
import sys


def main():
    okdesk_api = od.OKDeskAPI(API_TOKEN, ADDRESS)
    authors = okdesk_api.get_contacts_by_custom_attribute(attribute='depart', value='Отдел сервисного обслуживания')

    # extract authors only
    authors_list = []
    for author in authors:
        authors_list.append(author['id'])

    # get issues ids for these authors
    issues_ids = okdesk_api.fetch_issues_list_by_contaсt(authors_list)

    # get issues for these IDs
    issues = okdesk_api.get_issues(issues_ids)

    # добавляем параметр FILTER_ATTRIBUTE_NAME равный FILTER_ATTRIBUTE_VALUE

    od.add_attribute(json_data=issues, attribute_name=FILTER_ATTRIBUTE_NAME, attribute_value=FILTER_ATTRIBUTE_VALUE)

    od.save_json_to_file(issues, JSON_FILE_NAME)


def print_help():
    print(
        "Usage: extract_issues.py -h|--help -an|--attribute_name=<attribute name> -av|--attribute_value <attribute "
        "value>")
    print(" -j|--json <json file name>  -k|--key <API key> ")
    print(" -a|--address <okdesk domain address>")
    print(
        'Example: extract_issues.py --attribute_name="depart"  --attribute_value="Отдел сервисного обслуживания" '
        '--key="2050867b5d83e762932efeb84042c510fe9f" --address="https://egk.okdesk.ru"')


if __name__ == '__main__':

    # options definition
    short_options = "han:av:j:k:a:"
    long_options = ["help", "attribute_name=", "attribute_value=", "json=",
                    "key=", "address="]

    # get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 4:
        print_help()
        sys.exit(2)
    # Обработка полученных параметров
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-an", "--attribute_name"):
            FILTER_ATTRIBUTE_NAME = current_value
            print("Attribute name:", FILTER_ATTRIBUTE_NAME)
        elif current_argument in ("-av", "--attribute_value"):
            FILTER_ATTRIBUTE_VALUE = current_value
            print("Attribute value:", FILTER_ATTRIBUTE_VALUE)
        elif current_argument in ("-j", "--json"):
            JSON_FILE_NAME = current_value
            print("JSON file name:", JSON_FILE_NAME)
        elif current_argument in ("-k", "--key"):
            API_TOKEN = current_value
            print("Destination book name:", API_TOKEN)
        elif current_argument in ("-a", "--address"):
            ADDRESS = current_value
            print("Address:", ADDRESS)

    # Обработка оставшихся аргументов
    for value in values:
        print("Extra arguments:", value)

    main()
