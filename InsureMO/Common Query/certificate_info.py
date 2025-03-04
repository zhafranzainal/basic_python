from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pandas as pd
import time

# Specify the path to your ChromeDriver
service = Service('D:/Installation/chromedriver-win64/chromedriver.exe')

# Set up Selenium WebDriver with the Service
driver = webdriver.Chrome(service=service)

# Load certificate numbers from the CSV file
certificates_df = pd.read_csv('certificate_no.csv')

# Check if the CSV has a column named 'Certificate No.'
if 'Certificate No.' not in certificates_df.columns:
    print("Error: 'Certificate No.' column not found in certificate_no.csv.")
    driver.quit()
else:
    certificate_numbers = certificates_df['Certificate No.'].tolist()

# Format certificate number with leading zeros (10 digits)
formatted_cert_no = f"{certificate_numbers[0]:010d}"

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

    # Wait for and click the "Common Query" item
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[@class="rb-sidemenu-item-content" and @title="Common Query"]'))
    ).click()
    print("Clicked on Common Query, opening new tab.")

    # Switch to the new tab
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])
    print("Switched to new tab.")

    # At this point, manually enter the Certificate No. in the input field and click the search button

    input_element = driver.find_element(By.NAME, "policyCode_text")
    input_element.click()
    input_element.send_keys(formatted_cert_no)

    search_button = driver.find_element(By.XPATH, "//input[@value='Search']")
    search_button.click()

    # Wait until the tables are fully loaded
    time.sleep(5)
    tables = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.table_data'))
    )

    # Initialize a list to store data
    certificates_data = []

    if len(tables) < 2:
        print("Error: Second table not found!")
    else:
        # Select the second table
        second_table = tables[1]

        # Extract proposal date
        proposal_date = WebDriverWait(second_table, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    './/td[@class="list_td"]/div[@class="label"]/label[contains(text(),"Proposal Date")]/../../div[@class="input"]'
                )
            )
        ).text

        # Extract risk start date
        risk_start_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    './/td[@class="list_td"]/div[@class="label"]/label[contains(text(),"Risk Start Date")]/../../div[@class="input"]'
                )
            )
        ).text

        certificates_data.append([formatted_cert_no, proposal_date, risk_start_date])

        # Convert data to DataFrame
        df = pd.DataFrame(certificates_data, columns=['Certificate No.', 'Proposal Date', 'Risk Start Date'])

        # Export to CSV
        df.to_csv('certificates_output.csv', index=False)
        print("Data exported to certificates_output.csv")

except TimeoutException as e:
    print("An element was not found within the time limit.")
    print(e)
finally:
    driver.quit()
