from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_tenant_dashboard_and_rent():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # Open dashboard directly
    driver.get("http://127.0.0.1:5000/TenantDashboard")

    # 🔥 Use text instead of href (bulletproof)
    rent_button = wait.until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, "Rent")
        )
    )

    rent_button.click()

    # Wait for Rent page
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    driver.quit()