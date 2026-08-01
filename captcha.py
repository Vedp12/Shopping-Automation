import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

CHROME_PROFILE_DIR = "/tmp/selenium_profile"  # choose a path you control
COOKIES_FILE = "cookies.json"
LOCAL_STORAGE_FILE = "local_storage.json"

def start_browser_with_profile(chromedriver_path="/usr/bin/chromedriver"):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    # Run visible browser so a human can solve challenges
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def save_cookies_and_local_storage(driver, cookies_path=COOKIES_FILE, local_storage_path=LOCAL_STORAGE_FILE):
    cookies = driver.get_cookies()
    with open(cookies_path, "w") as f:
        json.dump(cookies, f)
    # local storage
    local_storage = driver.execute_script(
        "var items = {}; for (var i=0; i<localStorage.length; i++){ var k = localStorage.key(i); items[k]=localStorage.getItem(k);} return items;"
    )
    with open(local_storage_path, "w") as f:
        json.dump(local_storage, f)

def load_cookies_and_local_storage(driver, cookies_path=COOKIES_FILE, local_storage_path=LOCAL_STORAGE_FILE):
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            cookies = json.load(f)
        driver.delete_all_cookies()
        for c in cookies:
            # remove domain attribute if it causes issues
            c.pop("sameSite", None)
            try:
                driver.add_cookie(c)
            except Exception:
                pass
    if os.path.exists(local_storage_path):
        with open(local_storage_path, "r") as f:
            local_storage = json.load(f)
        for k, v in local_storage.items():
            driver.execute_script(f"localStorage.setItem(arguments[0], arguments[1]);", k, v)

def human_validate_and_save(url="https://orteil.dashnet.org/cookieclicker/"):
    driver = start_browser_with_profile()
    driver.get(url)
    print("Browser opened. Please complete any Cloudflare challenge manually in the visible window.")
    # Wait for human to solve challenge and for the site to be usable
    # This is a simple heuristic: wait until a known element is present or user presses Enter in console
    try:
        # Give the user up to 5 minutes to solve
        timeout = 300
        poll = 0
        while poll < timeout:
            time.sleep(1)
            poll += 1
            # Replace this check with a reliable element that indicates the page is loaded
            if "Cookie Clicker" in driver.title or driver.execute_script("return document.readyState") == "complete":
                # small extra wait for scripts to finish
                time.sleep(2)
                break
        save_cookies_and_local_storage(driver)
        print("Saved cookies and local storage for later reuse.")
    finally:
        driver.quit()

# Example: run once manually to create saved session
if __name__ == "__main__":
    human_validate_and_save()

