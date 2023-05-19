# -*- coding: utf-8 -*-
import requests

API_TOKEN = '2050867b5d83e762932efeb84042c510fe9f5440'
ADDRESS = 'https://egk.okdesk.ru'


def get_roles(api_token):
    url = f"{ADDRESS}/api/v1/employees/roles?api_token={api_token}"

    response = requests.get(url)

    if response.status_code == 200:
        roles = response.json()
        print("Список ролей:")
        for role in roles:
            print(role)
        return roles
    else:
        print(f"Ошибка при получении ролей. Код ошибки: {response.status_code}")
        print(response.json())
        return None


def get_contacts(api_token, from_id='1',):
    url = f"{ADDRESS}/api/v1/contacts/list?api_token={api_token}&page[size]=100&page[from_id]={from_id}&page[direction]=forward"

    response = requests.get(url)

    if response.status_code == 200:
        roles = response.json()
        print("Список контактов:")
        for role in roles:
            print(role)
        return roles
    else:
        print(f"Ошибка при получении контактов. Код ошибки: {response.status_code}")
        print(response.json())
        return None


def get_companies(api_token):
    url = f"{ADDRESS}/api/v1/companies/list?api_token={api_token}"

    response = requests.get(url)

    if response.status_code == 200:
        roles = response.json()
        print("Список компаний:")
        for role in roles:
            print(role)
        return roles
    else:
        print(f"Ошибка при получении компаний. Код ошибки: {response.status_code}")
        print(response.json())
        return None


def create_employee(api_token, first_name, last_name, email, login, password, role_ids):
    url = f"{ADDRESS}/api/v1/employees/?api_token={api_token}"

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


def create_contact(api_token, first_name, last_name, company_id, department_name, **kwargs):
    url = f"{ADDRESS}/api/v1/contacts/?api_token={api_token}"

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


def archive_contact(api_token, contact_id):
    url = f"{ADDRESS}/api/v1/contacts/{contact_id}/activations?api_token={api_token}"

    data = {
        "active": False
    }

    response = requests.patch(url, json=data)

    if response.status_code == 200:
        print(f"Контакт с ID {contact_id} успешно архивирован.")
    else:
        print(f"Ошибка при архивации контакта с ID {contact_id}. Код ошибки: {response.status_code}")
        print(response.json())

def find_contacts(api_token, search_string):
    url = f"{ADDRESS}/api/v1/contacts/?api_token={api_token}&search_string={search_string}"

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

    roles = get_roles(api_token)
    contacts = get_contacts(api_token)
    companies = get_companies(api_token)

    contacts = find_contacts(api_token,"vadim")
    # create_employee(api_token, first_name, last_name, email, login, password, role_ids)

    # create_contact(api_token, first_name, last_name, email=email, company_id=company_id,
    #                department_name=department_name)

    contact_id = 598

    # for contact in range (contact_id,1000):
    #    archive_contact(api_token, contact)
