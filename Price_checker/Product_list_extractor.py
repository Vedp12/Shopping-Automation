from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os



Product = "laptop"

with open(f"Carts-{Product}.txt", "w", encoding="utf-8") as file:
        pass
def search_product_Amazon(product=Product):
    
    service = Service("/usr/bin/chromedriver")
    driverA = webdriver.Chrome(service=service)
    for pages in range(1, 2):
        driverA.get(f"https://www.amazon.in/s?k={product}&page={pages}")
        wait = WebDriverWait(driverA, 8)
        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal",
                )
            )
        )
        Product_Texts = driverA.find_elements(
            By.CSS_SELECTOR,
            ".a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal",
        )
        href_lists = []

        for product_href in Product_Texts:
            href = product_href.get_attribute("href")
            print("Amazon", href)
            if href and href is not None and href not in href_lists:
                href_lists.append(href)
        with open(f"Carts-{product}.txt", "a", encoding="utf-8") as file:
            for href_list in href_lists:
                file.write(f"{str(href_list)}\n")
        driverA.execute_script("window.scrollBy(0, 499);")
        sleep(0.15)
    sleep(5)
    driverA.quit()


def search_product_Flipkart(product=Product):
    
    service = Service("/usr/bin/chromedriver")
    driverF = webdriver.Chrome(service=service)
    for pages in range(1, 2):
        driverF.get(f"https://www.flipkart.com/search?q={product}&page={pages}")
        wait = WebDriverWait(driverF, 8)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "k7wcnx")))
        Product_Texts = driverF.find_elements(By.CLASS_NAME, "k7wcnx")
        href_lists = []

        for product_href in Product_Texts:
            href = product_href.get_attribute("href")
            print("Amazon", href)
            if href and href is not None and href not in href_lists:
                href_lists.append(href)
        with open(f"Carts-{product}.txt", "a", encoding="utf-8") as file:
            for href_list in href_lists:
                file.write(f"{str(href_list)}\n")
            driverF.execute_script("window.scrollBy(0, 499);")
        sleep(0.15)

    sleep(5)
    driverF.quit()


if __name__ == "__main__":
    search_product_Amazon()
    search_product_Flipkart()
