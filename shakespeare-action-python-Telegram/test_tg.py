from tg import send_text_message, test
params={
    # "http_proxy": "http://127.0.0.1:3128",
    "chatid": 1905796087,
    "text_message": "Hello!"
}
assets = {
    "bot_token": "5800150072:AAGpCCSYeG0piHJzYPV9nSHF3EV_0iGPKO4",
    "base_url": "https://api.telegram.org"
}
context_info = {}

print(send_text_message(params, assets, context_info))
print(test(params, assets, context_info))