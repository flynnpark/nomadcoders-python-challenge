import os
import requests
from requests import ConnectionError
from multiprocessing import Process
from typing import List


def check_down(urls: List[str]) -> None:
    processes = [Process(target=check_url, args=(url,)) for url in urls]
    for process in processes:
        process.start()
    for process in processes:
        process.join()


def check_url(url: str) -> None:
    if not "." in url:
        print(f"{url} is not a valid url.")
        return

    url = url.replace(" ", "").lower()
    if not url.startswith("http://"):
        url = f"http://{url}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} is up!")

        else:
            print(f"{url} is down!")

    except ConnectionError:
        print(f"{url} is down!")


def clear() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    while True:
        print("Welcome to IsItDown.py!")
        print("Please write a URL or URLs you want to check. (separated by comma)")
        input_value = input()
        urls = input_value.split(",")

        check_down(urls)

        while True:
            is_over = input("Do you want to start over? (y/n) ")
            if is_over in ["y", "n"]:
                if is_over == "n":
                    exit(0)
                clear()
                break
