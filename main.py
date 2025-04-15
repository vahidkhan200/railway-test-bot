import time
import ccxt
import telebot
from analysis import analyze
from config import TELEGRAM_TOKEN, CHAT_ID

# تنظیم ربات تلگرام
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# اتصال به صرافی LBANK
exchange = ccxt.lbank({
    'enableRateLimit': True
})

# لیست ارزهایی که بررسی می‌کنیم
symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']

def send_signal(message):
    bot.send_message(CHAT_ID, message)

def run_bot():
    for symbol in symbols:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
            signal = analyze(ohlcv, symbol)
            if signal:
                send_signal(signal)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

# اجرای هر ۳۰ دقیقه یک بار
while True:
    run_bot()
    time.sleep(1800)
