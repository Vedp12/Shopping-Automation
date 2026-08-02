from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time


def google_search(query, max_results=5):
    """
    Perform a Google search in headless mode and return top results.
    :param query: Search query string
    :param max_results: Number of results to return
    :return: List of (title, link) tuples
    """
    results = []

    # Configure Chrome to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        # Open Google
        driver.get("https://www.duckduckgo.com")

        # Accept cookies if prompted (optional)
        try:
            consent_button = driver.find_element(
                By.XPATH, "//button[contains(., 'Accept')]"
            )
            consent_button.click()
        except NoSuchElementException:
            pass  # No consent popup

        # Find search box and enter query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # Wait for results to load

        # Extract search results
        search_items = driver.find_elements(
            By.XPATH, "//div[@class='tF2Cxc']"
        )  # Each result block
        for item in search_items[:max_results]:
            try:
                title = item.find_element(By.TAG_NAME, "h3").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                results.append((title, link))
            except NoSuchElementException:
                continue

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    finally:
        driver.quit()

    return results


if __name__ == "__main__":
    query = "Python Selenium headless search"
    search_results = google_search(query, max_results=5)

    print("\nTop Google Search Results:")
    for idx, (title, link) in enumerate(search_results, start=1):
        print(f"{idx}. {title}\n   {link}")
