from urllib.parse import urlparse
import requests
import os
import argparse
from dotenv import load_dotenv


URL = "https://api-ssl.bitly.com/v4/"


def is_bitlink(header, url):
    response = requests.get(
        "{}{}{}".format(URL, "bitlinks/", url), headers=header)
    return response.ok


def shorten_link(header, url):
    response = requests.post("{}{}".format(URL, "shorten"), headers=header, json={'long_url': url})
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(header, url):
    total_clicks = requests.get("{}{}{}{}".format(URL, "bitlinks/", url, "/clicks/summary"), headers=header)
    total_clicks.raise_for_status()
    return total_clicks.json()['total_clicks']


def main():
    load_dotenv()
    token = os.environ["BITLY_TOKEN"]
    header = {"Authorization": token}
    parser = argparse.ArgumentParser()
    parser.add_argument ('url', nargs='?')
    args = parser.parse_args()
    full_url = urlparse(args.url.strip())
    url = "{}{}".format(full_url.netloc, full_url.path)
    if is_bitlink(header, url):
        try:
            total_clicks = count_clicks(header, url)
            print("Количество кликов: {}".format(total_clicks))
        except requests.exceptions.HTTPError:
            print("Ошибка при вводе битлинка!")
    else:
        try:
            bitlink = shorten_link(header, full_url.geturl())
            print("Битлинк: {}".format(bitlink))
        except requests.exceptions.HTTPError:
            print("Ошибка при вводе ссылки!")


if __name__ == '__main__':
    main()
