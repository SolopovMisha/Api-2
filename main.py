import requests
import os
from urllib.parse import urlparse


def shorten_link(telegram_token, long_url):
    url = 'https://api.vk.ru/method/utils.getShortLink'
    
    params = {
        "v": 5.199, 
        "url": long_url
    }
    headers = {
        "Authorization": f"Bearer {telegram_token}"
    }
    
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()["response"]["short_url"]


def count_clicks(telegram_token, short_link):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    
    params = {
        "v": 5.236,
        "interval": "forever",
        "key": short_link,
        "extended": 0
    }
    headers = {"Authorization": f"Bearer {telegram_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()["response"]["stats"]


def main():
    telegram_token = os.environ['TELEGRAM_TOKEN']
    
    user_url = input("Введите ссылку: ")
    parsed_url = urlparse(user_url)
    
    try:
        if parsed_url.netloc == "vk.cc":
            print("Количество кликов по ссылке:",
                  count_clicks(telegram_token, parsed_url.path[1:])[0]['views'])
        else:
            print("Сокращёная ссылка:", shorten_link(telegram_token, user_url))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")


if __name__ == "__main__":
    main()
