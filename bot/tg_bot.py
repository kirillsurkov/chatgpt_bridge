import sys
sys.path.insert(0, "..")

import os
import json
import requests
import telebot
from data import Data

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))
print(bot)
SELF_ID = int(os.environ.get("BOT_ID"))
SELF_ALIAS = os.environ.get("BOT_ALIAS")
#PROMPT="Продолжи диалог от своего лица"
PROMPT = "Продолжи диалог одним сообщением"
batch = []
is_busy = False

def get_answer(chat_id, question: str) -> str:
    global is_busy
    if is_busy:
        return "Я сейчас занят"
    bot.send_chat_action(chat_id, "typing")
    res = ""
    is_busy = True
    try:
        print(Data.BRIDGE_ADDRESS + "/ask")
        req = requests.post(Data.BRIDGE_ADDRESS + "/ask", json={"question": question}, timeout=Data.SELENIUM_CONVERSATION_TIMEOUT)
        res = json.loads(req.text)
    except Exception as e:
        res = "Ошибка"
        print(e)
    is_busy = False
    return ": ".join(res.split("\n")[0].split(": ")[1:])

def make_question(message: telebot.types.Message):
    name = (message.from_user.first_name or "") + " " + (message.from_user.last_name or "")
    text = message.text
    return name + ": " + text + "."

# Frequent crashes when enabled
def mentions_filter(message: telebot.types.Message):
    return False
    if message.reply_to_message and message.reply_to_message.from_user.id == SELF_ID:
        return True
    if message.entities:
        for e in message.entities:
            if e.type == 'mention' and message.text[e.offset:e.offset+e.length] == SELF_ALIAS:
                return True
    return False
    
@bot.message_handler(func=mentions_filter)
def on_mention(message: telebot.types.Message):
    bot.reply_to(message, get_answer(message.chat.id, make_question(message)))

@bot.message_handler(func=lambda message: message.chat.type != "private")
def on_message(message: telebot.types.Message):
    global batch
    batch += [message]
    print("Batch size:", len(batch))
    if len(batch) >= Data.BATCH_SIZE:
        question = [make_question(msg) for msg in batch]
        bot.send_message(message.chat.id, get_answer(message.chat.id, f"{PROMPT}\n" + "\n".join(question)))
        batch = []

bot.infinity_polling()