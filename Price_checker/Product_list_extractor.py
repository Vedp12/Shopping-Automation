import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Product = "laptop"


def get_optimized_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Fast execution without opening UI window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Speed up loading by disabling image rendering on listing pages
    options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )

    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)


def search_product_Amazon(driver, product=Product, max_pages=1):
    links = set()
    for page in range(1, max_pages + 1):
        driver.get(f"https://www.amazon.in/s?k={product}&page={page}")
        wait = WebDriverWait(driver, 8)

        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
                )
            )
            elements = driver.find_elements(
                By.CSS_SELECTOR, "a.a-link-normal.s-no-hover, h2 a.a-link-normal"
            )
            for elem in elements:
                href = elem.get_attribute("href")
                if href and "/dp/" in href:  # Ensure it is a valid product detail page
                    links.add(href)
        except Exception as e:
            print(f"Error scraping Amazon page {page}: {e}")

    return links


def search_product_Flipkart(driver, product=Product, max_pages=1):
    links = set()
    for page in range(1, max_pages + 1):
        driver.get(f"https://www.flipkart.com/search?q={product}&page={page}")
        wait = WebDriverWait(driver, 8)

        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div._1AtVbE, div.CGtarget")
                )
            )
            elements = driver.find_elements(
                By.CSS_SELECTOR, "a._1fQO21, a.CGtarget, a[href*='/p/']"
            )
            for elem in elements:
                href = elem.get_attribute("href")
                if href:
                    links.add(href)
        except Exception as e:
            print(f"Error scraping Flipkart page {page}: {e}")

    return links


if __name__ == "__main__":
    file_path = f"Carts-{Product}.txt"

    # Clean/Reset link file
    with open(file_path, "w", encoding="utf-8") as file:
        pass

    driver = get_optimized_driver()
    try:
        amazon_urls = search_product_Amazon(driver, Product, max_pages=1)
        flipkart_urls = search_product_Flipkart(driver, Product, max_pages=1)

        all_urls = amazon_urls.union(flipkart_urls)

        with open(file_path, "a", encoding="utf-8") as file:
            for url in all_urls:
                file.write(f"{url}\n")
        print(f"Saved {len(all_urls)} URLs to {file_path}")
    finally:
        driver.quit()
