# chatgpt_bridge
Bridge to the ChatGPT via Selenium

# How to use
First of all you should create `.env` file. You can see required variables in `env.sample`

Then run the bridge with `uvicorn`. Example:
```console
cd bridge
uvicorn openai_bridge:fast_api --port 8001
```

After that you'll be able to open page `http://127.0.0.1/docs` and play with API. Currently there is only 1 endpoint `/ask` that you can use.


You can see example usage of this API in the `tg_bot` directory.


This project was made just for fun, so the code may not be perfect. Any suggestions are welcome!
