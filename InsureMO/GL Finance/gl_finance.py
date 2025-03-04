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

    # Wait for and click the "GL Posting Query" item
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[@class="rb-sidemenu-item-content" and @title="GL Posting Query"]'))
    ).click()
    print("Clicked on GL Posting Query, opening new tab.")

    # Switch to the new tab
    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[-1])
    print("Switched to new tab.")

    # At this point, manually enter the Certificate No. in the input field and click the search button

    # Wait for 20 seconds to allow the table to load
    print("Waiting for 20 seconds to allow the table to load...")
    time.sleep(20)

    # Wait for the table to be present
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head'))
    )

    # Initialize a list to store all subdetails data
    all_subdetails_data = []


    # Function to extract data from the current subdetails page
    def extract_data_from_subdetails_page():
        # Wait for the subdetails table to be present
        sub_table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head'))
        )

        # Extract subdetails table data
        sub_rows = sub_table.find_elements(By.TAG_NAME, 'tr')

        for sub_row in sub_rows[1:]:  # Skip the header row in subdetails
            sub_cells = sub_row.find_elements(By.TAG_NAME, 'td') or sub_row.find_elements(By.TAG_NAME, 'th')
            sub_row_data = [cell.text.strip() for cell in sub_cells]
            all_subdetails_data.append(sub_row_data)


    # Function to handle pagination on the subdetails page
    def handle_subdetails_pagination():
        while True:
            extract_data_from_subdetails_page()

            # Re-locate the pagination element on the subdetails page
            try:
                sub_pagination = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'td.font_turnpage'))
                )

                # Find the current page number
                current_sub_page = sub_pagination.find_element(By.CLASS_NAME, 'font_pageon').text

                # Find all page links
                sub_page_links = sub_pagination.find_elements(By.TAG_NAME, 'a')

                # Find the next page link
                next_sub_page_link = None
                for link in sub_page_links:
                    if link.text > current_sub_page:
                        next_sub_page_link = link
                        break

                # If there's a next page, click it
                if next_sub_page_link:
                    next_sub_page_link.click()
                    WebDriverWait(driver, 20).until(
                        EC.staleness_of(sub_pagination))  # Wait for the pagination to refresh
                else:
                    break
            except TimeoutException:
                break  # No pagination found, exit the loop


    # Function to extract data from the current main page
    def extract_data_from_main_page():
        # Wait for the table to be present
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head'))
        )

        # Extract main table data
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, 'td')
            if columns:
                # Click on the link in the "Amount" column
                try:
                    amount_link = columns[3].find_element(By.TAG_NAME, 'a')
                    amount_link.click()

                    # Switch to the new tab
                    WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
                    driver.switch_to.window(driver.window_handles[-1])

                    # Handle pagination on the subdetails page
                    handle_subdetails_pagination()

                    # Close the new tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head')))
                except NoSuchElementException:
                    print("Link in the 'Amount' column not found.")


    # Extract data from the first main page
    extract_data_from_main_page()

    # Loop through each page link on the main page
    while True:
        # Re-locate the pagination element
        pagination = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'td.font_turnpage'))
        )

        # Find the current page number
        current_page = pagination.find_element(By.CLASS_NAME, 'font_pageon').text

        # Find all page links
        page_links = pagination.find_elements(By.TAG_NAME, 'a')

        # Find the next page link
        next_page_link = None
        for link in page_links:
            if link.text > current_page:
                next_page_link = link
                break

        # If there's a next page, click it and extract data
        if next_page_link:
            next_page_link.click()
            WebDriverWait(driver, 20).until(EC.staleness_of(pagination))  # Wait for the pagination to refresh
            extract_data_from_main_page()
        else:
            break

    # Convert all subdetails data to DataFrame
    df = pd.DataFrame(all_subdetails_data, columns=[
        'Posting ID', 'Fee ID', 'Posting Run Date', 'Transaction Date', 'Fee Type', 'Fee Status',
        'Disbursement Method', 'Reference Number', 'Grouping Level', 'Currency', 'Amount',
        'Certificate No.', 'Product Code', 'DR GL Account Code', 'CR GL Account Code'
    ])

    # Export to CSV
    df.to_csv('subdetails_output.csv', index=False)
    print("Subdetails data exported to subdetails_output.csv")

except TimeoutException as e:
    print("An element was not found within the time limit.")
    print(e)
finally:
    driver.quit()
