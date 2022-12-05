import sys
sys.path.insert(0, "..")

import time
from data import Data
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

class Conversation:
    def __init__(self, driver: WebDriver):
        wait = WebDriverWait(driver, Data.SELENIUM_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "form textarea"))
        self.prompt = wait.until(cond)
        parent = self.prompt.find_element(By.XPATH, "./..")
        self.send = parent.find_element(By.TAG_NAME, "button")
        self.refresh = driver.find_element(By.CSS_SELECTOR, "nav a")
        self.driver = driver

    def ask(self, question: str):
        self.driver.execute_script("arguments[0].value = arguments[1]", self.prompt, question)
        self.driver.execute_script("arguments[0].click()", self.send)
        wait = WebDriverWait(self.driver, Data.SELENIUM_CONVERSATION_TIMEOUT)
        cond = expected_conditions.element_to_be_clickable((By.CLASS_NAME, "result-streaming"))
        answer = wait.until(cond)
        while True:
            if "result-streaming" not in answer.get_attribute("class").split():
                break
            time.sleep(0.1)
        if "text-red-500" in answer.get_attribute("class").split():
            self.refresh.click()
            raise ValueError("Remote error")
        return answer.get_attribute("innerText")