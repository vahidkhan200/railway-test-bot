import requests
import pandas as pd
import pandas_ta as ta
import asyncio
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ====== تنظیمات اولیه ======
TELEGRAM_TOKEN = '7808088088:AAGu9D1Vr5Iq6lrrE7P2jbMr32_-K6Y8wF4'
CHAT_ID = '392018191'
SYMBOLS = [
    'btc_usdt', 'eth_usdt', 'sol_usdt', 'xrp_usdt', 
    'not_usdt', 'xlm_usdt', 'grt_usdt', 'bnb_usdt'
]

# ====== تابع گرفتن دیتا از LBank ======
def get_klines(symbol):
    url = f"https://api.lbank.info/v1/kline.do?symbol={symbol}&size=50&type=hour1"
    res = requests.get(url).json()
    raw = res['data']
    df = pd.DataFrame(raw, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df

# ====== تابع تشخیص Hammer ======
def is_hammer(row):
    body = abs(row['close'] - row['open'])
    candle_length = row['high'] - row['low']
    lower_wick = min(row['open'], row['close']) - row['low']
    if candle_length == 0:
        return False
    return lower_wick > 2 * body

# ====== تحلیل تکنیکال و سیگنال ======
async def check_signals():
    bot = Bot(token=TELEGRAM_TOKEN)

    for symbol in SYMBOLS:
        try:
            df = get_klines(symbol)
            df.ta.rsi(length=14, append=True)
            df.ta.macd(append=True)

            rsi = df.iloc[-1]['RSI_14']
            macd = df.iloc[-1]['MACD_12_26_9']
            signal = df.iloc[-1]['MACDs_12_26_9']
            last_candle = df.iloc[-1]

            hammer = is_hammer(last_candle)
            macd_cross = macd > signal and df.iloc[-2]['MACD_12_26_9'] < df.iloc[-2]['MACDs_12_26_9']

            if rsi < 30 and macd_cross and hammer:
                price = last_candle['close']
                msg = f"""📈 سیگنال خرید - {symbol.upper()}
✅ شرایط ورود برقرار شد
🔹 قیمت فعلی: {price}
🔹 اندیکاتورها: RSI پایین، MACD صعودی، کندل Hammer
📊 استراتژی ترکیبی تکنیکال
"""
                await bot.send_message(chat_id=CHAT_ID, text=msg)
        except Exception as e:
            print(f"{symbol} خطا: {e}")

# ====== زمان‌بندی ربات ======
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_signals, 'interval', minutes=60)  # هر ۱ ساعت
    scheduler.start()

    print("ربات سیگنال‌دهنده فعال شد.")
    while True:
        await asyncio.sleep(60)

asyncio.run(main())
