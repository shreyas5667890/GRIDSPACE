from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def test_tenant_login_and_rent():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")   # Required for Jenkins
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ Use Selenium Manager (automatic driver handling)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")

    # Step 1 – Click Sign In dropdown
    driver.find_element(By.CLASS_NAME, "signin").click()
    time.sleep(1)

    # Step 2 – Click Tenant
    driver.find_element(By.LINK_TEXT, "Tenant").click()
    time.sleep(2)

    # Step 3 – Enter Email
    driver.find_element(By.NAME, "username").send_keys("shreyasdkharat@gmail.com")

    # Step 4 – Enter Password
    driver.find_element(By.NAME, "pswd1").send_keys("Asdf@1234")

    # Step 5 – Click Sign In button
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)

    # Step 6 – Click Rent Apartments
    driver.find_element(By.LINK_TEXT, "RentApartment").click()
    time.sleep(2)

    # Step 7 – Assertion
    assert "Available Apartments" in driver.page_source

    driver.quit()