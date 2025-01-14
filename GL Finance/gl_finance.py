from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import pandas as pd

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

    # Wait for the table to be present
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head'))
    )

    # Extract table data
    rows = table.find_elements(By.TAG_NAME, 'tr')
    data = []

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        if columns:
            # Print the text of each column for debugging
            column_texts = [col.text for col in columns]
            print("Row data:", column_texts)

            try:
                # Check if the "Amount" column has a link
                if len(columns) > 3:
                    amount_link = columns[3].find_element(By.TAG_NAME, 'a')
                    amount_link.click()

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[-1])

                    # Wait for the new page to load
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'detail_table')))
                    detail_data = driver.find_element(By.ID, 'detail_table').text

                    # Append data to list
                    data.append({
                        'Posting ID': columns[0].text,
                        'Posting Run Date': columns[1].text,
                        'Currency': columns[2].text,
                        'Amount': columns[3].text,
                        'Pay Currency': columns[4].text,
                        'Pay Amount': columns[5].text,
                        'Detail': detail_data
                    })

                    # Close the new tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    # Wait for the main table page to be ready again
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_head')))
            except NoSuchElementException:
                print("Link in the 'Amount' column not found.")

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Export to Excel
    df.to_excel('output.xlsx', index=False)
    print("Data exported to output.xlsx")

except TimeoutException as e:
    print("An element was not found within the time limit.")
    print(e)
finally:
    driver.quit()
