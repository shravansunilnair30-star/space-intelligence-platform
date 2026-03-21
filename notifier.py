import requests

BOT_TOKEN = "8590818153:AAHpfnkfwR_2Tr77W8z2duThGFKqvnjM1Zs"
CHAT_ID = "5654707501"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Telegram response:", response.text)