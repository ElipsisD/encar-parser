import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time


def get_chrome_version() -> str:
    return subprocess.run(
        "google-chrome --product-version", shell=True, capture_output=True, text=True
    ).stdout.strip()


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
# options.add_argument(
#     f"--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{get_chrome_version()} Safari/537.36"
# )
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless=new")

driver = uc.Chrome(options=options, headless=False)
driver.get("https://www.encar.com/index.do")

print("Открыта страница:", driver.title)
time.sleep(180)
driver.quit()
