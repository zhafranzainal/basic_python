from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd
import time

# Specify the path to your ChromeDriver
service = Service('D:/Installation/chromedriver-win64/chromedriver.exe')

# Set up Selenium WebDriver with the Service
driver = webdriver.Chrome(service=service)

# Log in to the website
driver.get('https://stbdpreprod-sandbox-sg.insuremo.com/ui/admin/#/')

try:
    # Wait for the username field to be present and enter the username
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('abc')
    print("Username field found and filled.")

    # Wait for the password field to be present and enter the password
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys('123')
    print("Password field found and filled.")

    # Wait for the login button to be clickable and click it
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'submitEbao'))).click()
    print("Login button clicked.")

    # Wait for and click the "New Business Query" item
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[@class="rb-sidemenu-item-content" and @title="Query"]'))
    ).click()
    print("Clicked on New Business Query, opening new tab.")

    # Switch to iframe as Selenium cannot see it prior to switching
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "micro-app-iframe")))

    # List to store extracted certificate numbers
    certificate_data = []

    while True:
        # Wait for all table rows to load on the current page
        rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody.rb-table-tbody tr.rb-table-row'))
        )

        # Extract certificate numbers for this page
        for row in rows:
            try:
                cols = row.find_elements(By.CSS_SELECTOR, 'td')

                cert_no = cols[1].get_attribute("title").strip()
                product_main = cols[3].get_attribute("title").strip()

                certificate_data.append([cert_no, product_main])
                print(f"Certificate No: {cert_no} | Main Product: {product_main}")

            except Exception as e:
                print("Error extracting certificate", e)

        # Check if the "Next" button is present (the right arrow)
        try:

            # Check if the "Next" button is not inactive
            next_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'li.rb-pagination-btn:not(.not) span.rainbow.SingleArrowRight16-1')
                )
            )
            next_button.click()
            print("Moved to the next page.\n")

            # Wait for the next page to load
            time.sleep(1)

        except TimeoutException:
            print("No more pages. Exiting the loop.")
            break

    # Export to CSV
    df = pd.DataFrame(certificate_data, columns=['Certificate No.', 'Main Product'])
    df.to_csv('certificate_no.csv', index=False)
    print("\nData exported to certificate_no.csv")

except TimeoutException as e:
    print("An element was not found within the time limit.")
    print(e)
finally:
    driver.quit()
