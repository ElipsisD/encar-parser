import time

import requests
import os

from utils import get_accident_data

AUTO_TYPE_MAPPING = {
    "그래비티": "Gravity",
    "프레스티지": "Prestige",
    "시그니처": "Signature",
    "트렌디": "Trendy",
    "노블레스": "Noblesse",
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


class CarDataManager:
    def __init__(self, item):
        self.item = item

    def process(self, driver):
        item_id = self.item.get("Photo", "").split("/")[-1][:-1]
        accident_data = get_accident_data(driver, item_id)
        year = str(int(self.item["Year"]))
        price = int(self.item["Price"]) / 100
        item_id = self.item.get("Photo").split("/")[-1][:-1]
        accident_count = (
            f"\nСтраховых случаев: {len(accident_data['accidents'])}"
            if accident_data
            else ""
        )
        auto_type = AUTO_TYPE_MAPPING.get(self.item["BadgeDetail"])



class NotificationService:
    def __init__(self, item, accident_data, chat_id):
        self.item = item
        self.accident_data = accident_data
        self.chat_id = chat_id

    def send(self):
        pass

def send_notification(chat_id):
    auto_type_data = f"Комплектация: {auto_type}\n" if auto_type else ""
    message = (
        f"Цена: {price}\n"
        f"{auto_type_data}"
        f"Год: {year[:4]}/{year[4:]}\n"
        f"Пробег: {int(item['Mileage'])}"
        f"{accident_count}\n\n"
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
        payload = {"chat_id": chat_id, "media": media}
        response = requests.post(url, json=payload)
        if not response.ok:
            print(response.status_code)
            print(response.content)
            raise requests.RequestException
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        response = requests.post(url, json=payload)
        print(response)
        if not response.ok:
            print(response.status_code)
            print(response.content)
            raise requests.RequestException
    time.sleep(15)
