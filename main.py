import requests
from telegram.ext import Updater, CommandHandler

TOKEN = '7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4'

symbols = [
    'btc_usdt', 'eth_usdt', 'xrp_usdt', 'bnb_usdt',
    'hbar_usdt', 'xlm_usdt', 'xdc_usdt', 'not_usdt', 'dydx_usdt'
]

def get_prices():
    result = []
    for symbol in symbols:
        try:
            url = f"https://api.lbank.info/v2/ticker.do?symbol={symbol}"
            res = requests.get(url).json()
            price = res['data'][0]['ticker']['latest']
            result.append(f"{symbol.upper()}: {price}")
        except:
            result.append(f"{symbol.upper()}: خطا در دریافت")
    return "\n".join(result)

def start(update, context):
    update.message.reply_text("سلام! برای دریافت قیمت‌ها دستور /price رو بفرست.")

def price(update, context):
    prices = get_prices()
    update.message.reply_text(prices)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("price", price))

updater.start_polling()
updater.idle()
