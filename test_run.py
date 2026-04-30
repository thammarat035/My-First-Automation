import pytest
from selenium import webdriver
from login_page import LoginPage
import time
import os        # สำคัญมาก: ต้องมีบรรทัดนี้
import json
from dotenv import load_dotenv # สำหรับอ่านไฟล์ลับ .env

# โหลดค่าจากไฟล์ลับ .env
load_dotenv()
user_secret = os.getenv('SECRET_USER')
pass_secret = os.getenv('SECRET_PASS')

# ข้อมูลทดสอบ (ชุดแรกดึงจากไฟล์ลับ ส่วนชุดที่เหลือทดสอบกรณี Error)
test_data = [
    (user_secret, pass_secret, "Pass"),
    ("user_1", "pass_1", "Fail"),
    ("user_2", "pass_2", "Fail"),
    ("user_3", "pass_3", "Fail"),
    ("admin", "admin", "Fail"),
    ("guest", "guest", "Fail"),
    ("robot_tester", "bot123", "Fail"),
    ("testing_only", "999999", "Fail"),
    ("tomsmith", "wrongpassword", "Fail"), # แก้ให้ถูกตามความจริง
    ("tomsmith", "SuperSecretPassword!", "Pass") 
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login_process(username, password, expected):
    # 1. อ่าน Config
    with open('config.json') as f:
        config = json.load(f)

    # 2. เตรียมโฟลเดอร์รูป
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # 3. เปิด Browser
    driver = webdriver.Chrome()
    driver.implicitly_wait(config['timeout'])
    login = LoginPage(driver)
    
    try:
        driver.get(config['base_url'])
        
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()
        time.sleep(1)

        current_url = driver.current_url
        actual_result = "Pass" if "secure" in current_url else "Fail"

        # ถ้าผลลัพธ์ไม่ตรงกับที่คาดไว้ ให้ถ่ายรูป
        if actual_result != expected:
            screenshot_path = f"screenshots/fail_{username}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Captured: {screenshot_path}")

        assert actual_result == expected
            
    finally:
        driver.quit()