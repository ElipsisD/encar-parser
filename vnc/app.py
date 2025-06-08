from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.get("https://www.encar.com/index.do")

print("Открыта страница:", driver.title)
time.sleep(180)
driver.quit()
