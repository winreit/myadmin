import requests
from bs4 import BeautifulSoup
import re

# Конфигурационные данные
phpmyadmin_url = "http://185.244.219.162/phpmyadmin/"
login = "test"
password = "JHFBdsyf2eg8*"
db_name = "testDB"
table_name = "users"

# Создаем сессию для сохранения cookies между запросами
session = requests.Session()


def login_to_phpmyadmin():
    """Функция для авторизации в phpMyAdmin"""
    try:
        response = session.get(phpmyadmin_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        login_token = soup.find('input', {'name': 'token'}).get('value')

        login_data = {
            'pma_username': login,
            'pma_password': password,
            'server': '1',
            'token': login_token
        }

        login_response = session.post(phpmyadmin_url, data=login_data)

        if "name=\"login_form\"" not in login_response.text:
            print("Успешная авторизация в phpMyAdmin")
            return True
        else:
            print("Ошибка авторизации")
            return False
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        return False


def get_table_data():
    """Функция для получения данных из таблицы users"""
    try:
        sql_url = f"{phpmyadmin_url}?db={db_name}&table={table_name}&sql_query=SELECT+*+FROM+`{table_name}`"
        response = session.get(sql_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'id': 'table_results'}) or \
                soup.find('table', {'class': 'table_results'}) or \
                soup.find('table', {'class': 'data'}) or \
                soup.find('table', {'id': 'result_table'})

        if table:
            print(f"\nДанные из таблицы {table_name}:\n")
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            print(" | ".join(headers))
            rows = table.find_all('tr')[1:]
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    print(" | ".join([cell.get_text(strip=True) for cell in cells]))
        else:
            print("Таблица найдена, но не удалось распарсить данные")
            with open("debug_page.html", "w") as f:
                f.write(response.text)
            print("Сохранена HTML-страница для отладки: debug_page.html")

    except Exception as e:
        print(f"Ошибка при получении данных таблицы: {e}")


if __name__ == "__main__":
    if login_to_phpmyadmin():
        get_table_data()