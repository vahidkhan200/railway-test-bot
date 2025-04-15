import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# گرفتن توکن تلگرام و شناسه چت از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4")
CHAT_ID = os.getenv("392018191")
