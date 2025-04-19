import base64
import logging
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait

load_dotenv()
logger = logging.getLogger("scraper")


def login_to_sop(driver: WebDriver) -> WebDriver:
    SOP_URL = os.getenv("SOP_URL")
    SOP_USERNAME = os.getenv("SOP_USERNAME")
    SOP_PASSWORD = os.getenv("SOP_PASSWORD")
    driver.get(SOP_URL)
    logging.info(driver.title)
    logging.info(driver.current_url)

    username_input = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "username"))
    )
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(SOP_USERNAME)
    password_input.send_keys(SOP_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input.formButton[value='Login']").click()
    logging.info(driver.title)
    logging.info(driver.current_url)
    return driver


def get_payslips_selector(driver: WebDriver) -> WebDriver:
    payslip_link = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.LINK_TEXT, "View my Payslip")
        )
    )
    payslip_link.click()
    select_element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.NAME, "assId"))
    )
    select = Select(select_element)
    return driver, select


def save_pdf_for_month(driver: WebDriver, option_text: str) -> WebDriver:
    pdf = driver.execute_cdp_cmd(
        "Page.printToPDF", {"printBackground": True, "landscape": False}
    )
    filename = f"downloads/{option_text}_payslip.pdf"
    # Save the base64 PDF to a file
    with open(filename, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))
    return driver


def save_all_payslips(driver: WebDriver, select: list) -> WebDriver:
    options = [option.text for option in select.options]
    for index, text in enumerate(options):
        logger.info(f"Selecting option {index}: {text}")
        # Have to re-wrap with Select each time
        select_element = driver.find_element(By.NAME, "assId")
        select = Select(select_element)
        select.select_by_visible_text(text)
        driver.find_element(By.CSS_SELECTOR, 'input[type="image"]').click()
        time.sleep(2)
        save_pdf_for_month(driver, text)
    return driver


def main():
    driver = webdriver.Chrome()
    login_to_sop(driver)
    _, select = get_payslips_selector(driver)
    save_all_payslips(driver, select)
    driver.quit()


if __name__ == "__main__":
    main()
