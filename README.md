# chatgpt_bridge
Bridge to the ChatGPT via Selenium

# How to use
First of all you should create `.env` file. You can see required variables in `env.sample`

Then run the bridge with `uvicorn`. Example:
```console
cd bridge
uvicorn openai_bridge:fast_api --port 8001
```

After that you'll be able to open page `http://127.0.0.1/docs` and play with API. Currently there is 3 endpoints that you can use.

---

#### `/ask`

#### POST

Request format:
```json
{
        "question": "your question here"
}
```

Response format:
```json
"network answer here"
```

---

#### `/refresh_thread`

#### POST

Request body is empty.

Response body is empty.

---

#### `/is_thread_new`

#### GET

Request body is empty.

Response format:
```json
true
```

---

You can see example usage of this API in the `tg_bot` directory.


This project was made just for fun, so the code may not be perfect. Any suggestions are welcome!
