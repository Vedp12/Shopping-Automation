import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Product = "laptop"  # Match Product target


def get_optimized_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)


def extract_safe_text(driver, selector, by=By.CSS_SELECTOR, default="N/A"):
    try:
        return driver.find_element(by, selector).text.strip()
    except Exception:
        return default


def process_urls(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    driver = get_optimized_driver()
    wait = WebDriverWait(driver, 5)

    try:
        for url in urls:
            print(f"Processing: {url}")
            driver.get(url)

            if "amazon" in url:
                try:
                    wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
                    title = extract_safe_text(driver, "#productTitle")
                    price_css_selector = driver.find_element(
                        By.CSS_SELECTOR, ".a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay.apex-pricetopay-value"
                    )
                    price = price_css_selector.find_element(By.CLASS_NAME,"a-price-whole").text
                    about = extract_safe_text(driver, "#feature-bullets")

                    # Fetch image
                    try:
                        img_elem = driver.find_element(
                            By.CSS_SELECTOR, "#landingImage, #imgBlkFront"
                        )
                        image_url = img_elem.get_attribute("src")
                    except Exception:
                        image_url = "N/A"

                    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)[
                        :50
                    ]  # Limit length for valid filename
                    out_dir = f"Products/amazon/{Product}"
                    os.makedirs(out_dir, exist_ok=True)

                    with open(
                        f"{out_dir}/{safe_title}.txt", "w", encoding="utf-8"
                    ) as out_file:
                        out_file.write(
                            f"Title: {title}\nPrice: {price}\nImage: {image_url}\nAbout: {about}\nURL: {url}\n"
                        )

                except Exception as e:
                    print(f"Failed to parse Amazon URL: {url} | Error: {e}")

            elif "flipkart" in url:
                pass

    finally:
        driver.quit()


if __name__ == "__main__":
    process_urls(f"Carts-{Product}.txt")
