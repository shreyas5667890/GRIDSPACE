import requests
import time

def test_flask_server_running():

    # Give Flask a few seconds to start
    time.sleep(5)

    # Try accessing dashboard
    response = requests.get("http://127.0.0.1:5000/TenantDashboard")

    assert response.status_code == 200

    print("Login Successful - Dashboard Loaded")