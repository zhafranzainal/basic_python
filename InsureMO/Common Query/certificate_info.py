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


def login():
    """Logs in to the website."""

    driver.get('https://stbdpreprod-sandbox-sg.insuremo.com/ui/admin/#/')

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('abc')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys('123')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'submitEbao'))).click()
        print("Login successful.")

        # Navigate to "Common Query"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@class="rb-sidemenu-item-content" and @title="Common Query"]'))
        ).click()
        print("Navigated to Common Query.")

        # Switch to the new tab
        WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to new tab.")

    except TimeoutException:
        print("Login failed due to timeout.")
        driver.quit()
        exit()


def search_certificate(cert_no):
    """Searches for a given certificate number."""

    try:
        input_element = driver.find_element(By.NAME, "policyCode_text")
        input_element.click()
        input_element.clear()
        input_element.send_keys(cert_no)

        search_button = driver.find_element(By.XPATH, "//input[@value='Search']")
        search_button.click()

        print(f"\nSearched for certificate: {cert_no}")
        time.sleep(1)  # Allow time for the table to load

    except NoSuchElementException:
        print(f"\nSearch input field not found for certificate: {cert_no}")


def extract_certificate_data(cert_no):
    """Extracts proposal date and commencement date for the given certificate."""

    try:
        tables = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.table_data'))
        )

        if len(tables) < 2:
            print(f"Error: Second table not found for certificate {cert_no}!")
            return [cert_no, "N/A", "N/A"]

        second_table = tables[1]

        # Extract proposal date
        proposal_date = WebDriverWait(second_table, 1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    './/td[@class="list_td"]/div[@class="label"]/label[contains(text(),"Proposal Date")]/../../div[@class="input"]'
                )
            )
        ).text

        # Extract risk start date
        risk_start_date = WebDriverWait(second_table, 1).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    './/td[@class="list_td"]/div[@class="label"]/label[contains(text(),"Risk Start Date")]/../../div[@class="input"]'
                )
            )
        ).text

        print(f"Certificate No: {cert_no} | Proposal Date: {proposal_date} | Risk Start Date: {risk_start_date}")
        return [cert_no, proposal_date, risk_start_date]

    except (TimeoutException, NoSuchElementException):
        print(f"Error: No records found for certificate {cert_no}.")
        return [cert_no, "N/A", "N/A"]


def click_back_to_search():
    """Navigate to search homepage."""
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@value="Back to Search Homepage"]'))
        ).click()
        print("Clicked 'Back to Search Homepage' button.")

    except TimeoutException:
        print("Error: 'Back to Search Homepage' button not found or not clickable.")


def main():
    """Main function to execute the copy-pasting workflow."""

    login()

    # Load certificate numbers from CSV
    certificates_df = pd.read_csv('certificate_no.csv')

    if 'Certificate No.' not in certificates_df.columns:
        print("Error: 'Certificate No.' column not found in certificate_no.csv.")
        driver.quit()
        return

    certificate_numbers = certificates_df['Certificate No.'].tolist()
    certificates_list = []

    for certificate_number in certificate_numbers:
        # Format certificate number with leading zeros (10 digits)
        formatted_cert_no = f"{certificate_number:010d}"

        search_certificate(formatted_cert_no)
        certificate_data = extract_certificate_data(formatted_cert_no)
        certificates_list.append(certificate_data)
        click_back_to_search()

    # Save extracted data to CSV
    df = pd.DataFrame(certificates_list, columns=['Certificate No.', 'Proposal Date', 'Risk Start Date'])
    df.to_csv('certificates_output.csv', index=False)
    print("\nData exported to certificates_output.csv")

    driver.quit()


if __name__ == "__main__":
    main()
