import pytest
from selenium import webdriver
from login_page import LoginPage
import time
import os
import json # เพิ่มการอ่านไฟล์ JSON

# ข้อมูลทดสอบ 10 ชุด
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
    ("tomsmith", "wrongpassword", "Pass") # แกล้งให้พัง 1 เคสเพื่อดูรูป
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login_process(username, password, expected):
    # 1. อ่านค่าการตั้งค่าจากไฟล์ config.json
    with open('config.json') as f:
        config = json.load(f)

    # 2. เตรียมโฟลเดอร์เก็บรูป
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # 3. เลือก Browser ตามที่ระบุใน Config
    if config['browser'] == "chrome":
        driver = webdriver.Chrome()
    else:
        # ถ้าในอนาคตอยากเพิ่ม Edge หรือ Firefox ก็มาใส่ตรงนี้ได้
        driver = webdriver.Chrome() 

    login = LoginPage(driver)
    
    try:
        # 4. ดึง URL จาก Config
        driver.get(config['base_url'])
        driver.implicitly_wait(config['timeout'])
        
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()
        time.sleep(1)

        current_url = driver.current_url
        actual_result = "Pass" if "secure" in current_url else "Fail"

        # 5. ถ้าเทสพัง ให้ถ่ายรูป
        if actual_result != expected:
            screenshot_path = f"screenshots/fail_{username}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Captured: {screenshot_path}")

        assert actual_result == expected
            
    finally:
        driver.quit()