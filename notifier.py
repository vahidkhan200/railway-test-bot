import requests

# توکن ربات تلگرام و شناسه چت
TOKEN = '7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4'
CHAT_ID = '392018191'

def send_telegram_message(message):
    """
    ارسال پیام به تلگرام با استفاده از API ربات تلگرام
    
    :param message: پیامی که قرار است ارسال شود.
    :return: None
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }

    try:
        # ارسال درخواست POST به تلگرام
        response = requests.post(url, data=payload)
        
        # بررسی وضعیت پاسخ
        response.raise_for_status()  # اگر کد وضعیت غیر از 2xx بود خطا پرتاب می‌شود
        
        # بررسی اینکه آیا ارسال پیام موفق بوده است
        response_data = response.json()
        if response_data.get("ok"):
            print("پیام با موفقیت ارسال شد.")
        else:
            print("ارسال پیام با خطا مواجه شد.")
            print(response_data)
    
    except requests.exceptions.RequestException as e:
        # مدیریت خطاهای احتمالی در ارتباط با تلگرام
        print(f"خطا در ارسال پیام به تلگرام: {e}")
