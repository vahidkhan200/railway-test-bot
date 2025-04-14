import requests import pandas as pd import pandas_ta as ta from telegram import Bot from telegram.ext import Updater, CommandHandler import datetime

Telegram Bot Token

TELEGRAM_TOKEN = '7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4' CHAT_ID = '392018191'

CryptoCompare API Key

NEWS_API_KEY = '374fba205ba3f9a14a3f1762fa77e4673763f990c63b5f934e4fd3e1cade5ca8'

List of symbols to track

SYMBOLS = ['btc_usdt', 'eth_usdt', 'sol_usdt', 'xrp_usdt', 'not_usdt', 'xlm_usdt', 'xdc_usdt', 'grs_usdt', 'bnb_usdt']

bot = Bot(token=7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4)

def fetch_lbank_data(symbol): url = f"https://api.lbkex.com/v2/ticker/24hr.do?symbol={symbol}" response = requests.get(url) data = response.json()['ticker'] return float(data['latest'])

def fetch_news(): url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN" headers = {"Authorization": f"Apikey {NEWS_API_KEY}"} response = requests.get(url, headers=headers) articles = response.json().get("Data", [])[:3]  # limit to 3 latest articles news_text = "\n\nاخبار مهم:\n" for article in articles: news_text += f"- {article['title']}\nلینک: {article['url']}\n" return news_text

def analyze_and_send(): messages = [] for symbol in SYMBOLS: price = fetch_lbank_data(symbol) # نمونه داده فرضی برای تحلیل data = pd.DataFrame({"close": [price] * 100})  # جایگزین با داده واقعی OHLC در صورت وجود data['rsi'] = ta.rsi(data['close']) data['macd'] = ta.macd(data['close'])['MACD_12_26_9'] data['ema'] = ta.ema(data['close'])

latest = data.iloc[-1]
    if latest['rsi'] < 30 and latest['macd'] > 0 and price > latest['ema']:
        messages.append(f"رمزارز {symbol.upper()} در ناحیه ورود احتمالی قرار دارد.\nقیمت: {price}")

if messages:
    final_message = '\n\n'.join(messages) + '\n' + fetch_news()
    bot.send_message(chat_id=CHAT_ID, text=final_message)
else:
    bot.send_message(chat_id=CHAT_ID, text="هیچ سیگنال معتبری یافت نشد.")

def start(update, context): update.message.reply_text("ربات فعال است. در حال تحلیل...") analyze_and_send()

def main(): updater = Updater(TELEGRAM_TOKEN, use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) updater.start_polling() updater.idle()

if name == 'main': main()
