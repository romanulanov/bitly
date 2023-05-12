from urllib.parse import urlparse
import requests
import os
import argparse
from dotenv import load_dotenv


URL = "https://api-ssl.bitly.com/v4/"


def is_bitlink(token, url):
    response = requests.get(
        "{}{}{}".format(URL, "bitlinks/", url), headers={"Authorization": token})
    return response.ok


def shorten_link(token, url):
    response = requests.post("{}{}".format(URL, "shorten"), headers={"Authorization": token}, json={'long_url': url})
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token, url):
    total_clicks = requests.get("{}{}{}{}".format(URL, "bitlinks/", url, "/clicks/summary"), headers={"Authorization": token})
    total_clicks.raise_for_status()
    return total_clicks.json()['total_clicks']


def main():
    load_dotenv()
    token = "Bearer " + os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    namespace = parser.parse_args()
    full_url = urlparse(namespace.name).strip()
    url = "{}{}".format(full_url.netloc, full_url.path)
    if is_bitlink(token, url):
        try:
            total_clicks = count_clicks(token, url)
            print("Количество кликов: {}".format(total_clicks))
        except requests.exceptions.HTTPError:
            print("Ошибка при вводе битлинка!")
    else:
        try:
            bitlink = shorten_link(token, full_url.geturl())
            print("Битлинк: {}".format(bitlink))
        except requests.exceptions.HTTPError:
            print("Ошибка при вводе ссылки!")


main()
