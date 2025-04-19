import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select

import base64

load_dotenv()


SOP_URL = os.getenv("SOP_URL")
SOP_USERNAME = os.getenv("SOP_USERNAME")
SOP_PASSWORD = os.getenv("SOP_PASSWORD")

print("hi")

driver = webdriver.Chrome()
driver.get(SOP_URL)
print(driver.title)
print(driver.current_url)  # Shows the final URL
print(driver.title)  

# username_input = driver.find_element(By.NAME, "username")
username_input = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.ID, "username"))
)
password_input = driver.find_element(By.ID, "password")
username_input.send_keys(SOP_USERNAME)
password_input.send_keys(SOP_PASSWORD)
driver.find_element(By.CSS_SELECTOR, "input.formButton[value='Login']").click()

print(driver.current_url) 

payslip_link = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.LINK_TEXT, "View my Payslip")))
payslip_link.click()


select_element = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.NAME, "assId")))

select = Select(select_element)
options = select.options

for option in options:
    print(option.text)


pdf = driver.execute_cdp_cmd("Page.printToPDF", {
    "printBackground": True,
    "landscape": False
})

filename = f"downloads/output.pdf"
# Save the base64 PDF to a file
with open(filename, "wb") as f:
    f.write(base64.b64decode(pdf['data']))

print("PDF saved as output.pdf")

driver.quit()



def main():

    print("Hello from payslips-scraping!")





if __name__ == "__main__":
    main()
