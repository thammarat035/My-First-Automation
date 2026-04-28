import pytest
from selenium import webdriver
from login_page import LoginPage
import time
import os

test_data = [
    ("tomsmith", "SuperSecretPassword!", "Pass"),
    ("user_1", "pass_1", "Fail"),
    ("user_2", "pass_2", "Fail"),
    ("user_3", "pass_3", "Fail"),
    ("tomsmith", "SuperSecretPassword!", "Pass"),
    ("admin", "admin", "Fail"),
    ("guest", "guest", "Fail"),
    ("robot_tester", "bot123", "Fail"),
    ("testing_only", "999999", "Fail"),
    ("tomsmith", "wrongpassword", "Pass") # แกล้งให้พังตรงนี้ (รหัสผิดแต่บอกว่า Pass)
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login_process(username, password, expected):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    driver = webdriver.Chrome()
    login = LoginPage(driver)
    
    try:
        driver.get("https://the-internet.herokuapp.com/login")
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()
        time.sleep(1)

        current_url = driver.current_url
        actual_result = "Pass" if "secure" in current_url else "Fail"

        # ถ้าผลไม่ตรงตามคาด ให้ถ่ายรูป
        if actual_result != expected:
            screenshot_path = f"screenshots/fail_{username}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Captured: {screenshot_path}")

        # เช็ค Assert เพื่อให้ Pytest รู้ว่าเคสนี้พัง
        assert actual_result == expected, f"Expected {expected} but got {actual_result}"
            
    finally:
        driver.quit()