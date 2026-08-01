from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://monkeytype.com/")
try:
    cookie_button = driver.find_element(
        By.XPATH, "//button[text()='reject non-essential']"
    )
    cookie_button.click()
except Exception as e:
    print("No Cokkie button found")
#app_logo_button = driver.find_element(By.XPATH, "//a[@aria-label='Monkeytype Home']")
#app_logo_button.click()

wait = WebDriverWait(driver, 5)
wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".word.active"))
        )
while True:
    try:
        current_word = driver.find_element(By.CSS_SELECTOR, ".word.active")
        letters = current_word.find_elements(By.TAG_NAME, "letter")
        each_word = "".join(letter.text for letter in letters)
        print(each_word)
        if not each_word:
            each_word = current_word.text
        driver.switch_to.active_element.send_keys(each_word + Keys.SPACE)
        time.sleep(0.07)
    except Exception :
        print("Code execution finished")
        break
time.sleep(10)
driver.quit()
