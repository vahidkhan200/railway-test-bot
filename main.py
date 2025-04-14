import requests
import pandas as pd
import pandas_ta as ta
import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# توکن‌ها
TELEGRAM_TOKEN = "7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4"
TELEGRAM_CHAT_ID = "392018191"
CRYPTOCOMPARE_API_KEY = "374fba205ba3f9a14a3f1762fa77e4673763f990c63b5f934e4fd3e1cade5ca8"

# لیست ارزها
SYMBOLS = ["btc_usdt", "eth_usdt", "sol_usdt", "xrp_usdt", "not_usdt", "xlm_usdt", "xdc_usdt", "grs_usdt", "bnb_usdt"]

# گرفتن داده‌ها از LBank
def get_lbank_data(symbol):
    url = f"https://api.lbkex.com/v2/Kline?symbol={symbol}&period=60&size=100"
    response = requests.get(url)
    data = response.json()["data"]
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df

# گرفتن اخبار
def get_news_sentiment():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {"Authorization": f"Apikey {CRYPTOCOMPARE_API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        news = response.json()["Data"][:5]
        headlines = "\n".join(["- " + n["title"] for n in news])
        return "آخرین اخبار بازار:\n" + headlines
    return "دریافت اخبار ممکن نشد."

# بررسی سیگنال ورود
def check_signals(df):
    df["rsi"] = ta.rsi(df["close"])
    df["macd"] = ta.macd(df["close"])["MACD_12_26_9"]
    df["ema"] = ta.ema(df["close"], length=20)
    df["atr"] = ta.atr(df["high"], df["low"], df["close"])
    
    latest = df.iloc[-1]
    signal = ""

    if latest["rsi"] < 30 and latest["macd"] > 0 and latest["close"] > latest["ema"]:
        signal = "سیگنال ورود قوی (اشباع فروش + تایید مکدی و EMA)"
    elif latest["rsi"] > 70 and latest["macd"] < 0 and latest["close"] < latest["ema"]:
        signal = "احتمال ریزش (اشباع خرید و تایید خروج)"
    return signal

# ارسال پیام به تلگرام
def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# اجرای بررسی و ارسال سیگنال
def run(update=None, context=None):
    message = "وضعیت بازار:\n"
    for symbol in SYMBOLS:
        try:
            df = get_lbank_data(symbol)
            signal = check_signals(df)
            if signal:
                message += f"\n[{symbol.upper()}] → {signal}"
        except Exception as e:
            message += f"\n[{symbol.upper()}] → خطا در تحلیل"
    message += "\n\n" + get_news_sentiment()
    send_to_telegram(message)

# تلگرام
def start(update, context):
    run(update, context)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
