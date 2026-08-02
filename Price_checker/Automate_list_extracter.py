from os.path import exists

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os

if not os.path.exists("Products/amazon"):
    os.makedirs("Products/amazon",exist_ok=True)
def search_product(product):
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    for pages in range(1,16):
        driver.get(f"https://www.amazon.in/s?k={product}e&page={pages}")
        
        #* It extract data like: 
        #- Image
        #- name (with link)
        #- review
        #- Price
        
        for no,_ in enumerate(range(9)):
                try:
                    Product_Image  = driver.find_element(By.CSS_SELECTOR,".a-section.aok-relative.s-image-fixed-height")
                    Product_Text   = driver.find_element(By.CSS_SELECTOR,".a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal")
                    Product_Review = driver.find_element(By.XPATH,"//i[@data-cy='reviews-ratings-slot']")
                    Product_Price  = driver.find_element(By.XPATH,"//div[@data-cy='price-recipe']")
                    """
                    print("Image",Product_Image)            
                    print("Text",Product_Text)            
                    print("Review",Product_Review)
                    print("Price",Product_Price)
                    """
                    #for image,text,review,price in zip(Product_Image, Product_Text, Product_Review, Product_Price):
                    I = Product_Image.get_attribute("outerHTML")
                    T = Product_Text.get_attribute("outerHTML") 
                    R = Product_Review.get_attribute("outerHTML") 
                    P = Product_Price.get_attribute("outerHTML") 
                    print(I,T,R,P)           
                    driver.execute_script("window.scrollBy(0, 200);")
                    sleep(0.5)
                    with open(f"Products/amazon/{product}-{no}.txt","w",encoding="utf-8") as file:
                          file.write(f"{I}\n\n{T}\n\n{R}\n\n{P}")


                except Exception as e:
                    print(str(e))
sleep(10)
product = (input("Enter a product name: "))
search_product(product)
