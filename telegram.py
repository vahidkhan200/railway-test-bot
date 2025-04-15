import requests
from config import TELEGRAM_TOKEN, CHAT_ID
import time

def send_message_to_telegram(message):
    """
    ارسال پیام به تلگرام
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)

        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            print(f"پیام با موفقیت ارسال شد: {message}")
            return response.json()
        else:
            print(f"خطا در ارسال پیام: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        # مدیریت خطاهای احتمالی شبکه یا API
        print(f"خطا در ارتباط با تلگرام: {e}")
        return None

def send_message_with_retry(message, retries=3, delay=5):
    """
    ارسال پیام با تلاش مجدد در صورت خطا
    """
    for attempt in range(retries):
        result = send_message_to_telegram(message)
        if result:
            return result
        else:
            print(f"تلاش {attempt + 1} برای ارسال پیام ناکام بود. در حال تلاش مجدد...")
            time.sleep(delay)

    print(f"ارسال پیام بعد از {retries} تلاش موفق نبود.")
    return None
