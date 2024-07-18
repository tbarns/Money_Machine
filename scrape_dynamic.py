import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_dynamic(url):
    service = Service(executable_path='C:/Users/tbarn/WebDriver/bin/chrome-win64/chromedriver-win64/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        print(f"Accessing the page {url}...")
        grants = []

        try:
            print("Waiting for grant items...")

            possible_selectors = [
                'div.grant-item', 'div.scholarship-item', 'div.listing-item', 'li.grant', 'li.scholarship',
                'article.grant', 'div.entry-content', 'div.article', 'div.list-item'
            ]

            grant_elements = []
            for selector in possible_selectors:
                try:
                    grant_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    if grant_elements:
                        break
                except TimeoutException:
                    continue

            if not grant_elements:
                print("Loading took too much time or elements not found!")
                return []

            print(f"Found {len(grant_elements)} grant items.")

            for element in grant_elements:
                grant_name = element.text
                grant_amount = "N/A"
                due_date = "N/A"
                link = "N/A"

                try:
                    link_element = element.find_element(By.TAG_NAME, 'a')
                    if link_element:
                        link = link_element.get_attribute('href')
                except NoSuchElementException:
                    pass

                grants.append([grant_name, grant_amount, due_date, link])

            print("Scraped data:", grants)
        except TimeoutException:
            print("Loading took too much time or elements not found!")
        finally:
            driver.quit()

        return grants
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return []
