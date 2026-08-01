from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import import_cdp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import string
import random

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://the-internet.herokuapp.com/key_presses?")
time.sleep(2)
ite_vaule = 0
allString_List = []
All_strings = string.ascii_lowercase + string.ascii_uppercase + string.digits
allString_List.append(All_strings)

for string_list in allString_List:
    input_target = driver.find_element(By.ID, "target")
    input_target.send_keys(f"{string_list}")

    time.sleep(0.50)
    ite_vaule += 1
time.sleep(3)
driver.quit()
