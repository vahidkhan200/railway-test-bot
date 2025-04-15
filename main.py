import time
import ccxt
import telebot
import logging
from analysis import analyze
from config import TELEGRAM_TOKEN, CHAT_ID

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# تنظیم ربات تلگرام
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# اتصال به صرافی LBANK
exchange = ccxt.lbank({
    'enableRateLimit': True
})

# لیست ارزهایی که بررسی می‌کنیم
symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']

def send_signal(message):
    try:
        bot.send_message(CHAT_ID, message)
        logger.info(f"سیگنال برای {CHAT_ID} ارسال شد.")
    except Exception as e:
        logger.error(f"خطا در ارسال پیام به تلگرام: {e}")

def run_bot():
    for symbol in symbols:
        try:
            # دریافت داده OHLCV
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
            # آنالیز داده‌ها
            signal = analyze(ohlcv, symbol)
            if signal:
                send_signal(signal)
            else:
                logger.info(f"برای {symbol} سیگنالی پیدا نشد.")
        except ccxt.NetworkError as e:
            logger.error(f"خطا در اتصال به صرافی برای {symbol}: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"خطا در دریافت داده‌ها از صرافی برای {symbol}: {e}")
        except Exception as e:
            logger.error(f"خطای غیرمنتظره در پردازش {symbol}: {e}")

def main():
    while True:
        run_bot()
        logger.info("انتظار برای 30 دقیقه...")
        time.sleep(1800)  # اجرا هر ۳۰ دقیقه یک بار

if __name__ == "__main__":
    main()
