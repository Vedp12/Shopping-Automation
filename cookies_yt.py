from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(4)
#    if driver.find_element(By.ID, "langSelectButton"):
WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
        )
input_language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")


input_language.click()
time.sleep(120)
driver.quit()
