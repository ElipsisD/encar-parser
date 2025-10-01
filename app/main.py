from sqlalchemy import select, text

from models import Link
from service import CarDataManager, send_notification
from utils import get_session, selenium_start, get_accident_data, fetch_data

import time

import requests


def main():
    driver = None and selenium_start()
    session = get_session()
    try:
        stmt = select(Link)
        links = session.execute(stmt)

        while True:
            for link_obj in links.scalars():
                link_obj: Link
                if data := fetch_data(link_obj.link):
                    for item in data.get("SearchResults", []):
                        try:
                            CarDataManager(item).process(driver=driver)
                            send_notification(item, link_obj.chat_id)
                        except requests.RequestException:
                            continue

            print("Go sleep!")
            return
            # time.sleep(600)
    finally:
        session.close()


if __name__ == "__main__":
    main()
