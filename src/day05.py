import os
import requests
from typing import List, Dict, Union
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"


CURRENCY_LIST: List[Dict[str, Union[str, int]]] = []


def init_data() -> None:
    global CURRENCY_LIST
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table table-bordered downloads tablesorter")
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        columns = row.find_all("td")
        country_name = columns[0].text.strip().capitalize()
        currency_name = columns[1].text.strip()
        currency_code = columns[2].text.strip()

        if currency_code:
            CURRENCY_LIST.append(
                {"name": country_name, "currency": currency_name, "code": currency_code}
            )


def get_input_value() -> int:
    while True:
        try:
            input_value = int(input("#: "))

            if not input_value in range(1, len(CURRENCY_LIST) + 1):
                print("Choose a number from the list")
                continue

            return input_value

        except ValueError:
            print("That wasn't a number.")


if __name__ == "__main__":
    init_data()
    print("Hello! Please choose select a country by number:")
    for index, data in enumerate(CURRENCY_LIST):
        print(f"# {index + 1} {data['name']}")

    input_value = get_input_value()
    country_info = CURRENCY_LIST[input_value - 1]
    print(f"You choose {country_info['name']}")
    print(f"The currency code is {country_info['code']}")
