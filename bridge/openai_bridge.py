import os
import sys
import traceback
from auth import AuthOpenAI
from conversation import Conversation
from fastapi import FastAPI
from pydantic import BaseModel
from selenium.webdriver.remote.webdriver import WebDriver

fast_api = FastAPI()

class Item(BaseModel):
    question: str

def create_api(conversation: Conversation, driver: WebDriver):
    global fast_api

    @fast_api.post("/ask")
    def ask(question: Item):
        try:
            return conversation.ask(question.question)
        except:
            print("Exception in /ask")
            traceback.print_exc()
        return ""

    @fast_api.post("/refresh_thread")
    def refresh_thread():
        try:
            conversation.refresh_thread()
        except:
            print("Exception in /refresh_thread")
            traceback.print_exc()
    
    @fast_api.get("/is_thread_new")
    def is_thread_new():
        try:
            return conversation.is_thread_new()
        except:
            print("Exception in /is_thread_new")
            traceback.print_exc()
        return False

try:
    auth = AuthOpenAI(os.environ.get("OPENAI_EMAIL"), os.environ.get("OPENAI_PASSWORD"))
    driver = auth.get_driver()
    try:
        auth.do_login()
        conversation = Conversation(driver)
        create_api(conversation, driver)
    except:
        print("Exception in main #2")
        traceback.print_exc()
        driver.quit()
        sys.exit(4)
except:
    print("Exception in main #1")
    traceback.print_exc()
    sys.exit(4)