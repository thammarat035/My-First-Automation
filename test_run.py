import pytest
from selenium import webdriver
from login_page import LoginPage
import time

# ข้อมูลทดสอบ 10 ชุดเหมือนเดิม
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
    ("tomsmith", "wrongpassword", "Fail")
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login_process(username, password, expected):
    driver = webdriver.Chrome()
    login = LoginPage(driver)
    
    try:
        driver.get("https://the-internet.herokuapp.com/login")
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()
        time.sleep(1)

        current_url = driver.current_url
        if "secure" in current_url:
            assert expected == "Pass", f"ควรจะ Login พังแต่ดันผ่านสำหรับ user: {username}"
        else:
            assert expected == "Fail", f"ควรจะ Login ผ่านแต่ดันพังสำหรับ user: {username}"
            
    finally:
        driver.quit()