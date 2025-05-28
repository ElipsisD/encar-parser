import time
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def load_links(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
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


def main():
    links = load_links("links.txt")
    seen_ids = load_seen_ids("seen_ids.txt")

    while True:
        new_ids = set()
        for link in links:
            data = fetch_data(link)
            if data:
                for item in data.get("SearchResults", []):
                    item_id = item.get("Photo").split("/")[-1][:-1]
                    if item_id and item_id not in seen_ids:
                        try:
                            send_notification(item)
                            new_ids.add(item_id)
                        except requests.RequestException:
                            continue

        if new_ids:
            seen_ids.update(new_ids)
            save_seen_ids("seen_ids.txt", seen_ids)

        print("Go to sleep!")
        time.sleep(600)


if __name__ == "__main__":
    main()
