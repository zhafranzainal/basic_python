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

    # Extract main table data
    rows = table.find_elements(By.TAG_NAME, 'tr')
    main_data = []

    for row in rows[1:]:  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, 'td')
        if columns:
            # Extract text from each cell in the row
            row_data = [col.text.strip() for col in columns]

            # Click on the link in the "Amount" column
            try:
                amount_link = columns[3].find_element(By.TAG_NAME, 'a')
                amount_link.click()

                # Switch to the new tab
                WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
                driver.switch_to.window(driver.window_handles[-1])

                # Wait for the subdetails table to be present
                sub_table = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head'))
                )

                # Extract subdetails table data
                sub_rows = sub_table.find_elements(By.TAG_NAME, 'tr')
                sub_data = []

                for sub_row in sub_rows:
                    sub_cells = sub_row.find_elements(By.TAG_NAME, 'td') or sub_row.find_elements(By.TAG_NAME, 'th')
                    sub_row_data = [cell.text.strip() for cell in sub_cells]
                    sub_data.append(sub_row_data)

                # Append subdetails to row data
                row_data.append(sub_data)

                # Close the new tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head')))
            except NoSuchElementException:
                print("Link in the 'Amount' column not found.")
                row_data.append("No details found")

            # Append row data to list
            main_data.append(row_data)

    # Convert data to DataFrame
    df = pd.DataFrame(main_data,
                      columns=['Posting ID', 'Posting Run Date', 'Currency', 'Amount', 'Pay Currency', 'Pay Amount',
                               'Detail'])

    # Export to CSV
    df.to_csv('output_with_details.csv', index=False)
    print("Data exported to output_with_details.csv")

except TimeoutException as e:
    print("An element was not found within the time limit.")
    print(e)
finally:
    driver.quit()
