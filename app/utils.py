import subprocess
from functools import lru_cache

import requests
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from models import Base


from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

from selenium import webdriver

engine = create_engine(f"sqlite:///{DATABASE_URL}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_session() -> Session:
    return session


def selenium_start() -> WebDriver:
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
        options.add_argument("--disable-blink-features=AutomationControlled")
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
    driver.implicitly_wait(5)
    print("Selenium ready!")
    return driver


@lru_cache
def get_chrome_version() -> str:
    return subprocess.run(
        "google-chrome --product-version", shell=True, capture_output=True, text=True
    ).stdout.strip()


def get_ua() -> str:
    chrome_version = get_chrome_version()
    return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"


def get_accident_data(driver: WebDriver, item_id: int) -> dict | None:
    try:
        driver.get(f"https://fem.encar.com/cars/detail/{item_id}")
        el = driver.find_element(By.CLASS_NAME, "DetailSummary_vehicle_num__jihW1")
        vehicle_no = el.text
        response = requests.get(
            f"https://api.encar.com/v1/readside/record/vehicle/{item_id}/open?vehicleNo={vehicle_no}"
        )
        return response.json()
    except Exception:
        return None


def fetch_data(url):
    headers = {"User-Agent": get_ua()}
    response = requests.get(url, headers=headers)
    if not response.ok:
        print(response.status_code)
        print(response.content)
    return response.json() if response.status_code == 200 else None
