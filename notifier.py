import requests

TOKEN = '7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4'
CHAT_ID = '392018191'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)
