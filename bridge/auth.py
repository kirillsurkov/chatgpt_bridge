import sys
sys.path.insert(0, "..")

import abc
import undetected_chromedriver as uc
from data import Data
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Auth(abc.ABC):
    @abc.abstractmethod
    def do_login(self):
        print("loading login page")
        self._driver.get("https://chat.openai.com/auth/login")

        print("proceed to auth")
        buttons = self._driver.find_elements(By.CLASS_NAME, "btn")
        if len(buttons) != 2:
            raise ValueError("Something wrong with OpenAI website")
        button = buttons[0]
        button.click()

    def get_driver(self) -> WebDriver :
        return self._driver

class AuthOpenAI(Auth):
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password
        self._driver = uc.Chrome(headless=True)
    
    def do_login(self):
        super().do_login()

        print("logging in: email")
        wait = WebDriverWait(self._driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.ID, "username"))
        text_field = wait.until(cond)
        text_field.send_keys(self._email)
        text_field.send_keys(Keys.RETURN)

        print("logging in: password")
        wait = WebDriverWait(self._driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.ID, "password"))
        text_field = wait.until(cond)
        text_field.send_keys(self._password)
        text_field.send_keys(Keys.RETURN)

        print("Logged in!")
        print()

# Does not work in headless mode
class AuthGoogle(Auth):
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password
        self._driver = uc.Chrome(headless=False)

    def do_login(self):
        super().do_login()

        print("choose auth method")
        wait = WebDriverWait(self._driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "[data-provider='google']"))
        button = wait.until(cond)
        button.click()

        print("logging in: email")
        wait = WebDriverWait(self._driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "[type='email']"))
        text_field = wait.until(cond)
        text_field.send_keys(self._email)
        button = self._driver.find_element(By.ID, "identifierNext").find_element(By.TAG_NAME, "button")
        button.click()

        print("logging in: password")
        wait = WebDriverWait(self._driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "[type='password']"))
        text_field = wait.until(cond)
        text_field.send_keys(self._password)
        button = self._driver.find_element(By.ID, "passwordNext").find_element(By.TAG_NAME, "button")
        button.click()

        print("Logged in!")
        print()