from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from Product_list_extractor import Product
import os
import re



def read_file_by_line(filename):
    no_of_lines = 0
    with open(filename, "r") as f:
        
        for line in f:
            
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service)

            print(line)
            sleep(0.15)
            no_of_lines+=1
            if "amazon" in line:
                print("amazon")
                driver.get(line)
                wait = WebDriverWait(driver,2)
                wait.until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,".a-dynamic-image.a-stretch-vertical.media-block-image-tag"
                    )))
                displayed_image = driver.find_element(By.CSS_SELECTOR,".a-dynamic-image.a-stretch-vertical.media-block-image-tag")
                get_image = displayed_image.get_attribute("src")
             
                print("----------------------------------------------------------")
                get_title = driver.find_element(By.CSS_SELECTOR,".a-size-large.product-title-word-break")
                get_price = driver.find_element(By.CSS_SELECTOR,".a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay.apex-pricetopay-value")
                get_about = driver.find_element(By.ID,"feature-bullets")
                print(get_image)
                print(get_title.text)
                print(get_price.text)
                print(get_about.text)
                safe_title = re.sub(r'[\\/*?:"<>|]', "_", get_title.text)

# Save to file
                os.makedirs(f"Products/amazon/{Product}", exist_ok=True)
                with open(f"Products/amazon/{Product}/{safe_title}.txt", "w", encoding="utf-8") as file:
                    file.write("Title: " + get_title.text + "\n")
                    file.write("Price: " + get_price.text + "\n")
                    file.write("About: " + get_about.text + "\n")
                    file.write("URL: "   + line + "\n")
                driver.quit()

            elif "flipkart" in line:
                print("flipkart")

read_file_by_line("Carts-laptop.txt")
#if __name__ == "__main__":

