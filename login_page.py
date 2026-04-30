from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # รอสูงสุด 10 วินาที
        
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_username(self, username):
        element = self.wait.until(EC.visibility_of_element_located(self.username_field))
        element.send_keys(username)

    def enter_password(self, password):
        element = self.wait.until(EC.visibility_of_element_located(self.password_field))
        element.send_keys(password)

    def click_login(self):
        element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        element.click()