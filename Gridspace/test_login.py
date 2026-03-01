from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_tenant_login_and_rent():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.CLASS_NAME, "signin").click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Tenant"))).click()

    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("shreyasdkharat@gmail.com")
    driver.find_element(By.NAME, "pswd1").send_keys("Asdf@1234")

    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Rent Apartment")))

    # Click Rent Apartment
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Rent Apartment"))).click()

    # Final assertion
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "Available Apartments" in driver.page_source

    driver.quit()