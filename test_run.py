import pytest
from selenium import webdriver
from login_page import LoginPage
import time
import os
import json
import logging
from dotenv import load_dotenv

# ลบของเก่าออก แล้ววางชุดนี้แทนครับ
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_log.log", mode='w', encoding='utf-8'), # บังคับสร้างไฟล์ที่นี่
        logging.StreamHandler() # ให้โชว์ใน Terminal ด้วย
    ]
)

# 2. โหลดความลับจาก .env
load_dotenv()
user_secret = os.getenv('SECRET_USER')
pass_secret = os.getenv('SECRET_PASS')

# 3. ข้อมูลทดสอบ (10 เคส)
test_data = [
    (user_secret, pass_secret, "Pass"),
    ("wrong_user_1", "pass_1", "Fail"),
    ("wrong_user_2", "pass_2", "Fail"),
    ("wrong_user_3", "pass_3", "Fail"),
    ("admin", "admin", "Fail"),
    ("guest", "guest", "Fail"),
    ("test_bot", "123456", "Fail"),
    ("staff_01", "password", "Fail"),
    ("tomsmith", "wrong_pass", "Fail"),
    ("tomsmith", "SuperSecretPassword!", "Pass")
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login_process(username, password, expected):
    logging.info(f"--- เริ่มทดสอบ User: {username} ---")
    
    # อ่าน Config
    with open('config.json') as f:
        config = json.load(f)

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    driver = webdriver.Chrome()
    driver.implicitly_wait(config['timeout'])
    login = LoginPage(driver)
    
    try:
        logging.info(f"เปิด Browser ไปที่: {config['base_url']}")
        driver.get(config['base_url'])
        
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()
        time.sleep(1) # รอหน้าเว็บเปลี่ยนนิดนึง

        current_url = driver.current_url
        actual_result = "Pass" if "secure" in current_url else "Fail"

        if actual_result != expected:
            screenshot_path = f"screenshots/fail_{username}.png"
            driver.save_screenshot(screenshot_path)
            logging.error(f"❌ ผลไม่ตรงคาดหวัง! ถ่ายรูปไว้ที่: {screenshot_path}")
        else:
            logging.info(f"✅ ผลการทดสอบถูกต้องตามคาด ({actual_result})")

        assert actual_result == expected
            
    except Exception as e:
        logging.critical(f"😱 บัคตำตา!: {str(e)}")
        raise e
    finally:
        driver.quit()