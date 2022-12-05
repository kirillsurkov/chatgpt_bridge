import dotenv
import os

class Data:
    dotenv.load_dotenv()
    SELENIUM_TIMEOUT = int(os.environ.get("SELENIUM_TIMEOUT", 5))
    SELENIUM_CONVERSATION_TIMEOUT = int(os.environ.get("SELENIUM_CONVERSATION_TIMEOUT", 30))
    BATCH_SIZE = int(os.environ.get("BATCH_SIZE"))
    BRIDGE_ADDRESS = os.environ.get("BRIDGE_ADDRESS")