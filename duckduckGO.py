from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep


def Search_zone(query):
    service = Service("/usr/bin/chromedriver")
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.duckduckgo.com")

        driver.switch_to.active_element.send_keys(
            query
            + " site:geeksforgeeks.org OR site:Python.org OR site:wikipedia.org OR github.com OR"
        )
        driver.switch_to.active_element.send_keys(Keys.ENTER)

        sleep(120)
        driver.quit()

    except Exception as e:
        print(str(e))
    finally:
        print("Code completly")


query = str(input("Search your queries: "))
Search_zone(query)
