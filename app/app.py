import subprocess
import time
from functools import lru_cache

import requests
import os

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

from selenium import webdriver

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def load_links(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def fetch_data(url):
    headers = {"User-Agent": get_ua()}
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(response.status_code)
        print(response.content)
    return response.json() if response.status_code == 200 else None


def send_notification(item):
    year = str(int(item["Year"]))
    price = int(item["Price"]) / 100
    item_id = item.get("Photo").split("/")[-1][:-1]
    message = (
        f"Цена: {price}\n"
        f"Год: {year[:4]}/{year[4:]}\n"
        f"Пробег: {int(item['Mileage'])}\n\n"
        f"https://fem.encar.com/cars/detail/{item_id}"
    )
    if item.get("Photos"):
        media = []
        for index, image in enumerate(item.get("Photos")):
            image_url = f"https://ci.encar.com/carpicture{image.get('location')}"  # URL изображения
            if index == 0:
                # Для первой фотографии добавляем подпись
                media.append(
                    {
                        "type": "photo",
                        "media": image_url,
                        "caption": message,
                    }
                )
            else:
                media.append({"type": "photo", "media": image_url})

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMediaGroup"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "media": media}
        response = requests.post(url, json=payload)
        if not response.ok:
            print(response.status_code)
            print(response.content)
            raise requests.RequestException
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, json=payload)
        if not response.ok:
            print(response.status_code)
            print(response.content)
            raise requests.RequestException
    time.sleep(15)


def load_seen_ids(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return set(line.strip() for line in f.readlines())
    return set()


def save_seen_ids(file_path, seen_ids):
    with open(file_path, "w") as f:
        for item_id in seen_ids:
            f.write(f"{item_id}\n")


def selenium_start():
    get_chrome_version()

    def _initialize_webdriver() -> WebDriver:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = Service("/usr/bin/chromedriver")
        return webdriver.Chrome(service=service, options=options)

    driver = _initialize_webdriver()
    stealth(
        driver=driver,
        user_agent=get_ua(),
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
          """
        },
    )
    driver.get(
        "http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.Year.range(..202206)._.Mileage.range(..30000)._.(C.CarType.Y._.(C.Manufacturer.%ED%98%84%EB%8C%80._.(C.ModelGroup.%ED%88%AC%EC%8B%BC._.(C.Model.%ED%88%AC%EC%8B%BC%20(NX4_)._.BadgeGroup.%EA%B0%80%EC%86%94%EB%A6%B0%201600cc.)))))%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A%2250%22%2C%22searchKey%22%3A%22%22%2C%22loginCheck%22%3Afalse%7D"
    )
    print("Selenium wait!")
    driver.implicitly_wait(10)
    print("Selenium ready!")


@lru_cache
def get_chrome_version() -> str:
    return subprocess.run(
        "google-chrome --product-version", shell=True, capture_output=True, text=True
    ).stdout.strip()


def get_ua() -> str:
    chrome_version = get_chrome_version()
    return f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"


def main():
    selenium_start()
    links = load_links("links.txt")
    seen_ids = load_seen_ids("seen_ids.txt")

    while True:
        for link in links:
            data = fetch_data(link)
            if data:
                for item in data.get("SearchResults", []):
                    item_id = item.get("Photo").split("/")[-1][:-1]
                    if item_id and item_id not in seen_ids:
                        try:
                            send_notification(item)
                            seen_ids.add(item_id)
                        except requests.RequestException:
                            continue

        save_seen_ids("seen_ids.txt", seen_ids)
        print("Go sleep!")
        time.sleep(600)


if __name__ == "__main__":
    main()
