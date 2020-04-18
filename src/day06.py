import os
import requests
from typing import List, Dict, Union, cast
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
currency_info_url = "https://www.iban.com/currency-codes"
currency_convery_url = (
    "https://transferwise.com/gb/currency-converter/{}-to-{}-rate?amount={}"
)

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

COUNTRY_LIST: List[Dict[str, Union[str, int]]] = []


def soup_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def init_data() -> None:
    global COUNTRY_LIST
    soup = soup_page(currency_info_url)

    table = soup.find("table", class_="table table-bordered downloads tablesorter")
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        columns = row.find_all("td")
        country_name = columns[0].text.strip().capitalize()
        currency_name = columns[1].text.strip()
        currency_code = columns[2].text.strip()

        if currency_code:
            COUNTRY_LIST.append(
                {"name": country_name, "currency": currency_name, "code": currency_code}
            )


def get_country_index_input(question: str, retry_question: str) -> int:
    while True:
        try:
            print(question)
            input_value = int(input("#: "))

            if not input_value in range(1, len(COUNTRY_LIST) + 1):
                print(f"{retry_question}\n")
                continue

            return input_value

        except ValueError:
            print("That wasn't a number.\n")


def get_money_input(question) -> int:
    while True:
        try:
            print(question)
            input_value = int(input())
            return input_value

        except ValueError:
            print("That wasn't a number.\n")


def get_country_info(index: int) -> Dict[str, Union[str, int]]:
    return COUNTRY_LIST[index - 1]


def convery_currency(
    from_country_code: str, to_country_code: str, from_money: float
) -> float:
    soup = soup_page(
        currency_convery_url.format(from_country_code, to_country_code, from_money)
    )
    to_money = soup.find("input", id="cc-amount-to")
    return float(to_money.get("value"))


def print_result(
    from_country_code: str, to_country_code: str, from_money: float, to_money: float
) -> None:
    formatted_from_money = format_currency(
        from_money, from_country_code, locale="ko_KR"
    )
    formatted_to_money = format_currency(to_money, to_country_code, locale="ko_KR")
    print(f"{formatted_from_money} is {formatted_to_money}")


if __name__ == "__main__":
    init_data()

    print("Welcome to CurrencyConvert PRO 2000")
    for index, data in enumerate(COUNTRY_LIST):
        print(f"# {index + 1} {data['name']}")

    print("\n")
    from_index = get_country_index_input(
        "Where are you from? Choose a country by number.",
        "Choose a number from the list",
    )
    from_country = get_country_info(from_index)
    print(f'{from_country["name"]}\n\n')

    to_index = get_country_index_input(
        "Now choose another country.", "Choose a number from the list"
    )
    to_country = get_country_info(to_index)
    print(f'{to_country["name"]}\n\n')

    from_money = get_money_input(
        f'How many {from_country["code"]} do you want to convert to {to_country["code"]}?'
    )
    from_country_code = cast(str, from_country["code"])
    to_country_code = cast(str, to_country["code"])

    to_money = convery_currency(from_country_code, to_country_code, from_money)
    print_result(from_country_code, to_country_code, from_money, to_money)
