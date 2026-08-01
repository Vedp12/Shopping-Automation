#!/usr/bin/env python3
"""
cookieclicker_human_session.py

Workflow:
1. If saved session exists, reuse it.
2. If not, open a visible Chrome window for a human to complete Cloudflare.
3. Save cookies and localStorage after validation.
4. Reuse saved session to automate language selection and cookie clicks.
"""

import os
import json
import time
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- Configuration ----------
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"   # change if needed
CHROME_PROFILE_DIR = "/tmp/selenium_profile_cookieclicker"  # optional persistent profile
COOKIES_FILE = "cookies_cookieclicker.json"
LOCAL_STORAGE_FILE = "local_storage_cookieclicker.json"
PAGE_URL = "https://orteil.dashnet.org/cookieclicker/"
HUMAN_TIMEOUT_SECONDS = 300  # time allowed for human to solve challenge
CLICK_COUNT = 2000
CLICK_INTERVAL = 0.01  # seconds between clicks

# ---------- Browser helpers ----------
def start_browser(chromedriver_path: str = CHROMEDRIVER_PATH, user_data_dir: Optional[str] = None, headless: bool = False):
    options = webdriver.ChromeOptions()
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def save_cookies_and_local_storage(driver, cookies_path: str = COOKIES_FILE, local_storage_path: str = LOCAL_STORAGE_FILE):
    cookies = driver.get_cookies()
    with open(cookies_path, "w") as f:
        json.dump(cookies, f)
    local_storage = driver.execute_script(
        "var items = {}; for (var i=0; i<localStorage.length; i++){ var k = localStorage.key(i); items[k]=localStorage.getItem(k);} return items;"
    )
    with open(local_storage_path, "w") as f:
        json.dump(local_storage, f)

def load_cookies_and_local_storage(driver, cookies_path: str = COOKIES_FILE, local_storage_path: str = LOCAL_STORAGE_FILE):
    if os.path.exists(cookies_path):
        with open(cookies_path, "r") as f:
            cookies = json.load(f)
        driver.delete_all_cookies()
        for c in cookies:
            c.pop("sameSite", None)
            try:
                driver.add_cookie(c)
            except Exception:
                pass
    if os.path.exists(local_storage_path):
        with open(local_storage_path, "r") as f:
            local_storage = json.load(f)
        for k, v in local_storage.items():
            driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", k, v)

# ---------- Human validation ----------
def human_validate_and_save(url: str = PAGE_URL, timeout_seconds: int = HUMAN_TIMEOUT_SECONDS):
    print("Opening visible browser. Please complete any Cloudflare challenge in the opened window.")
    driver = start_browser(user_data_dir=CHROME_PROFILE_DIR, headless=False)
    try:
        driver.get(url)
        waited = 0
        while waited < timeout_seconds:
            time.sleep(1)
            waited += 1
            try:
                ready = driver.execute_script("return document.readyState")
            except Exception:
                ready = ""
            title = driver.title or ""
            if ready == "complete" and ("Cookie Clicker" in title or "cookie clicker" in title.lower()):
                time.sleep(2)
                break
        save_cookies_and_local_storage(driver)
        print(f"Saved cookies to {COOKIES_FILE} and local storage to {LOCAL_STORAGE_FILE}.")
    finally:
        driver.quit()

# ---------- Cookie Clicker automation ----------
def run_cookieclicker_bot(use_saved_session: bool = True, clicks: int = CLICK_COUNT, click_interval: float = CLICK_INTERVAL):
    driver = start_browser(user_data_dir=CHROME_PROFILE_DIR, headless=False)
    try:
        driver.get(PAGE_URL)
        if use_saved_session:
            load_cookies_and_local_storage(driver)
            driver.get(PAGE_URL)

        wait = WebDriverWait(driver, 15)

        try:
            if driver.find_elements(By.ID, "promptContentChangeLanguage"):
                en_btn = wait.until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
                try:
                    en_btn.click()
                except Exception:
                    en_btn.send_keys(Keys.ENTER)
                time.sleep(2)
        except Exception as e:
            print("Language selection skipped or failed:", e)

        try:
            big_cookie = wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
        except Exception as e:
            print("bigCookie not found:", e)
            return

        print(f"Clicking cookie {clicks} times.")
        for i in range(clicks):
            try:
                big_cookie.click()
            except Exception:
                try:
                    big_cookie = driver.find_element(By.ID, "bigCookie")
                    big_cookie.click()
                except Exception:
                    pass
            time.sleep(click_interval)

        print("Done clicking. Browser will remain open for 10 seconds for inspection.")
        time.sleep(10)
    finally:
        driver.quit()

# ---------- Session expiry detection ----------
def saved_session_valid() -> bool:
    if not (os.path.exists(COOKIES_FILE) and os.path.exists(LOCAL_STORAGE_FILE)):
        return False
    # quick heuristic: try loading saved cookies into a short-lived browser and check page title
    driver = start_browser(user_data_dir=None, headless=False)
    try:
        driver.get(PAGE_URL)
        load_cookies_and_local_storage(driver)
        driver.get(PAGE_URL)
        time.sleep(3)
        title = driver.title or ""
        return "Cookie Clicker" in title or "cookie clicker" in title.lower()
    except Exception:
        return False
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# ---------- Orchestration ----------
def main():
    if not saved_session_valid():
        print("No valid saved session found. Launching human validation.")
        human_validate_and_save(PAGE_URL)
    else:
        print("Valid saved session found. Reusing it.")

    run_cookieclicker_bot(use_saved_session=True, clicks=2000, click_interval=0.01)

if __name__ == "__main__":
    main()

