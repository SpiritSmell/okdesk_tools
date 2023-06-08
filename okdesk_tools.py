# -*- coding: utf-8 -*-
import requests
import time
import json

API_TOKEN = '2050867b5d83e762932efeb84042c510fe9f5440'
ADDRESS = 'https://egk.okdesk.ru'
RETRY_ATTEMPTS = 5

JSON_FILE_NAME = 'issues.json'

FILTER_ATTRIBUTE_NAME = 'depart'
FILTER_ATTRIBUTE_VALUE = 'Отдел сервисного обслуживания'

def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

class OKDeskAPI:
    def __init__(self, api_token, address):
        self.api_token = api_token
        self.address = address
        self.issues_data = None
        self.roles_data = None
        self.contacts_data = None
        self.companies_data = None

    def fetch_roles(self):
        url = f"{self.address}/api/v1/employees/roles?api_token={self.api_token}"
        response = requests.get(url)

        if response.status_code == 200:
            roles = response.json()
            print("Список ролей:")
            for role in roles:
                print(role)
            self.roles_data = roles
            return roles
        else:
            print(f"Ошибка при получении ролей. Код ошибки: {response.status_code}")
            print(response.json())
            return None

    def get_roles(self):
        if not self.roles_data:
            self.fetch_roles()
        return self.roles_data

    @property
    def roles(self):
        return self.get_roles()

    def fetch_contacts(self, from_id='1'):

        from_id = 1
        STEP = 100
        first_request = True
        self.contacts_data = []

        while True:
            if first_request:
                # запрашиваем без значения from_if
                url = f"{self.address}/api/v1/contacts/list?api_token={self.api_token}&page[size]={STEP}"
                first_request = False
            else:
                url = f"{self.address}/api/v1/contacts/list?api_token={self.api_token}&page[size]={STEP}&page[from_id]={from_id}"
            response = requests.get(url)

            if response.status_code == 200:
                contacts = response.json()
                print("Список контактов:")
                for contact in contacts:
                    print(contact)

                # добавляем данные к внутренней переменной
                self.contacts_data += contacts

                # условие выхода из цикла
                if len(contacts) < STEP:
                    return self.contacts_data

                # получаем id последней записи, чтоб с нее продолжиь в следующий раз.
                from_id = contacts[-1]['id']
                # return contacts
            else:
                print(f"Ошибка при получении контактов. Код ошибки: {response.status_code}")
                print(response.json())
                return None

    def get_contacts(self):
        if not self.contacts_data:
            self.fetch_contacts()
        return self.contacts_data

    def find_contacts(self, search_string):
        url = f"{ADDRESS}/api/v1/contacts/?api_token={self.api_token}&search_string={search_string}"

        response = requests.get(url)

        if response.status_code == 200:
            results = response.json()
            print("Список ролей:")
            for result in results:
                print(result)
            return results
        else:
            print(f"Ошибка при получении ролей. Код ошибки: {response.status_code}")
            print(response.json())
            return None

    @property
    def contacts(self):
        return self.get_contacts()

    def fetch_companies(self):
        url = f"{self.address}/api/v1/companies/list?api_token={self.api_token}"
        response = requests.get(url)

        if response.status_code == 200:
            companies = response.json()
            print("Список компаний:")
            for company in companies:
                print(company)
            self.companies_data = companies
            return companies
        else:
            print(f"Ошибка при получении компаний. Код ошибки: {response.status_code}")
            print(response.json())
            return None

    def get_companies(self):
        if not self.companies_data:
            self.fetch_companies()
        return self.companies_data

    @property
    def companies(self):
        return self.get_companies()

    def fetch_issues_list_by_contaсt(self,authors=[460,461]):

        authors_url = ""
        for author in authors:
            authors_url +=f"&contact_ids[]={author}"

        url = f"{self.address}/api/v1/issues/count?api_token={self.api_token}{authors_url}"
        response = requests.get(url)

        if response.status_code == 200:
            issues = response.json()
            print("Список заявок:")
            for issue in issues:
                print(issue)
            self.issues_data = issues
            return issues
        else:
            print(f"Ошибка при получении заявок. Код ошибки: {response.status_code}")
            print(response.json())
            return None

    def fetch_issues_detaild_by_contact(self,authors=[460,461]):

        authors_url = ""
        for author in authors:
            authors_url +=f"&contact_ids[]={author}"

        url = f"{self.address}/api/v1/issues/list?api_token={self.api_token}{authors_url}"
        response = requests.get(url)

        if response.status_code == 200:
            issues = response.json()
            print("Список заявок:")
            for issue in issues:
                print(issue)
            self.issues_data = issues
            return issues
        else:
            print(f"Ошибка при получении заявок. Код ошибки: {response.status_code}")
            print(response.json())
            return None

    def fetch_issue_details_by_id(self, issue):

        url = f"{self.address}/api/v1/issues/{issue}?api_token={self.api_token}"
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = requests.get(url)
                # если все хорошо, то выходим из цикла
                break
            except requests.exceptions.RequestException as e:
                # если нет, то повторяем запрос
                print(f"Ошибка при выполнении запроса: {e}")

        if response.status_code == 200:
            issue = response.json()
            print(f"Заявка: {issue}")
            return issue
        else:
            print(f"Ошибка при получении заявок. Код ошибки: {response.status_code}")
            print(response.json())
            return None
    def fetch_issues_by_ids(self,issues):

        result = []
        for issue in issues:
            result.append(self.fetch_issue_details_by_id(issue))
            #time.sleep(1)
        return result


    def get_issues(self, issues_ids):
        return self.fetch_issues_by_ids(issues_ids)

    def get_contacts_by_custom_attribute(self, attribute, value):

        result = []
        if not self.contacts_data:
            self.get_contacts()

        for contact in self.contacts_data:
            for parameter in contact['parameters']:
                if not parameter['code'] == attribute:
                    continue
                if not (parameter['value'] == value):
                    continue
                result.append(contact)

        return result

    def create_employee(self, first_name, last_name, email, login, password, role_ids):
        url = f"{self.address}/api/v1/employees/?api_token={self.api_token}"

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "login": login,
            "password": password,
            "role_ids": role_ids
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Сотрудник успешно создан.")
        else:
            print(f"Ошибка при создании сотрудника. Код ошибки: {response.status_code}")
            print(response.json())

    def create_contact(self, first_name, last_name, company_id, department_name, **kwargs):
        url = f"{self.address}/api/v1/contacts/?api_token={self.api_token}"

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "company_id": company_id,
            "custom_parameters": {'depart': department_name},
            **kwargs
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            contact_id = response.json()["id"]
            print(f"Контакт успешно создан. ID контакта: {contact_id}")
            return contact_id
        else:
            print(f"Ошибка при создании контакта. Код ошибки: {response.status_code}")
            print(response.json())
            return None

def add_attribute(json_data,attribute_name, attribute_value):
    for item in json_data:
        item[attribute_name]=attribute_value
    return json_data

if __name__ == '__main__':
    api_token = API_TOKEN
    first_name = "John"
    last_name = "Doe Department"
    email = "john.doe@example.com"
    login = "johndoe"
    password = "secretpassword"
    role_ids = [68158]
    company_id = 3
    department_name = 'Отдел сервисного обслуживания'

    okdesk_api = OKDeskAPI(api_token, ADDRESS)

    # roles = okdesk_api.get_roles()
    # contacts = okdesk_api.get_contacts()
    # companies = okdesk_api.get_companies

    #print(okdesk_api.roles)
    #print(okdesk_api.contacts)
    #print(okdesk_api.companies)

    contacts = okdesk_api.find_contacts("vadim")
    # okdesk_api.create_employee(first_name, last_name, email, login, password, role_ids)

    # okdesk_api.create_contact(first_name, last_name, email=email, company_id=company_id,
    #                          department_name=department_name)

    contact_id = 598

    # for contact in range (contact_id,1000):
    #    archive_contact(api_token, contact)

    # issues = get_issues(api_token,[555,533])

    # okdesk_api.get_department_members()

    authors = okdesk_api.get_contacts_by_custom_attribute(attribute='depart', value='Отдел сервисного обслуживания')

    authors_list = []
    for author in authors:
        authors_list.append(author['id'])


    issues_ids = okdesk_api.fetch_issues_list_by_contaсt(authors_list)

    #for result in results:
    #    print(result)

    results = okdesk_api.get_issues(issues_ids)

    # добавляем параметр FILTER_ATTRIBUTE_NAME равный FILTER_ATTRIBUTE_VALUE

    add_attribute(json_data=results,attribute_name=FILTER_ATTRIBUTE_NAME,attribute_value=FILTER_ATTRIBUTE_VALUE)

    save_json_to_file(results,JSON_FILE_NAME)


