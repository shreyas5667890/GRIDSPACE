from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_tenant_login_and_rent():

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # IMPORTANT for Jenkins
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")

    # Step 2 – Click Sign In dropdown
    driver.find_element(By.CLASS_NAME, "signin").click()
    time.sleep(1)

    # Step 3 – Click Tenant
    driver.find_element(By.LINK_TEXT, "Tenant").click()
    time.sleep(2)

    # Step 4 – Enter Email
    driver.find_element(By.NAME, "username").send_keys("shreyasdkharat@gmail.com")

    # Step 5 – Enter Password
    driver.find_element(By.NAME, "pswd1").send_keys("Asdf@1234")

    # Step 6 – Click Sign In button
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)

    # Step 7 – Click Rent Apartments
    driver.find_element(By.LINK_TEXT, "RentApartment").click()
    time.sleep(2)

    # Step 8 – Assertion (VERY IMPORTANT)
    assert "Available Apartments" in driver.page_source

    driver.quit()