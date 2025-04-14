import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
            result.append(f"{symbol.upper()}: خطا")
    return "\n".join(result)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! دستور /price رو بزن تا قیمت‌ها رو ببینی.")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_prices()
    await update.message.reply_text(prices)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    app.run_polling()
