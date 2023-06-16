import okdesk_tools as od  # Importing the 'okdesk_tools' module
import getopt  # Importing the 'getopt' module for command-line argument parsing
import sys  # Importing the 'sys' module for system-specific parameters and functions
import re  # Importing the 're' module for regular expression operations
from datetime import datetime, timedelta  # Importing the 'datetime' module for date and time manipulation

SINCE = None  # Variable to store the start date
UNTIL = None  # Variable to store the end date


def process_date(date):
    pattern = r"now\s+([-+]?\d+(\.\d+)?)"

    matches = re.search(pattern, date)  # Searching for a pattern in the provided date string
    if matches:
        extracted_number = matches.group(1)
        print(extracted_number)  # Output: "+25.5"
        number_of_days = float(extracted_number)  # Extracting the number of days from the pattern match
        new_date = datetime.now() + timedelta(
            days=number_of_days)  # Calculating the new date by adding the number of days to the current date
        formatted_date = new_date.strftime("%d-%m-%Y")  # Formatting the new date
        print(f'new date is {formatted_date}')  # Printing the new date
        return formatted_date
    else:
        print("No match found.")
        return date


def main():
    global SINCE
    global UNTIL

    okdesk_api = od.OKDeskAPI(API_TOKEN,
                              ADDRESS)  # Creating an instance of the OKDeskAPI class from 'okdesk_tools' module
    authors = okdesk_api.get_contacts_by_custom_attribute(attribute=FILTER_ATTRIBUTE_NAME,
                                                          value=FILTER_ATTRIBUTE_VALUE)  # Getting contacts by a
    # custom attribute

    # Extracting authors only
    authors_list = []
    for author in authors:
        authors_list.append(author['id'])

    SINCE = process_date(SINCE)  # Processing the start date
    UNTIL = process_date(UNTIL)  # Processing the end date

    # Getting issue IDs for these authors
    issues_ids = okdesk_api.fetch_issues_list_by_contaсt(authors_list, SINCE, UNTIL)

    # Getting issues for these IDs
    issues = okdesk_api.get_issues(issues_ids)

    # Adding the FILTER_ATTRIBUTE_NAME parameter equal to FILTER_ATTRIBUTE_VALUE
    od.add_attribute(json_data=issues, attribute_name=FILTER_ATTRIBUTE_NAME, attribute_value=FILTER_ATTRIBUTE_VALUE)

    od.save_json_to_file(issues, JSON_FILE_NAME)  # Saving the issues data to a JSON file


def print_help():
    print(
        "Usage: extract_issues.py -h|--help -an|--attribute_name=<attribute name> -av|--attribute_value <attribute "
        "value>")
    print(" -j|--json <json file name>  -k|--key <API key> ")
    print(" -a|--address <okdesk domain address>")
    print(" -s|--since <since date>")
    print(" -u|--until <until date>")
    print(
        'Example: extract_issues.py --attribute_name="depart"  --attribute_value="Отдел бухгалтерского учета" '
        '--key="2050867b5d83e762932efeb84042c510fe9f" --address="https://egk.okdesk.ru" --since="01-02-2023" '
        '--until="now -7"')


def get_arguments():
    global FILTER_ATTRIBUTE_NAME
    global FILTER_ATTRIBUTE_VALUE
    global JSON_FILE_NAME
    global API_TOKEN
    global ADDRESS
    global SINCE
    global UNTIL

    FILTER_ATTRIBUTE_NAME = None
    FILTER_ATTRIBUTE_VALUE = None

    SINCE = None
    UNTIL = None

    # Options definition
    short_options = "han:av:j:k:a:s:u:"
    long_options = ["help", "attribute_name=", "attribute_value=", "json=",
                    "key=", "address=", "since=", "until="]

    # Get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 3:
        print_help()
        sys.exit(2)
    # Handling the received parameters
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
        elif current_argument in ("-s", "--since"):
            SINCE = current_value
            print("Since:", SINCE)
        elif current_argument in ("-u", "--until"):
            UNTIL = current_value
            print("Until:", UNTIL)

    # Handling remaining arguments
    for value in values:
        print("Extra arguments:", value)


if __name__ == '__main__':
    get_arguments()

    main()
