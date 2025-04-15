from lbank_api import get_ohlcv
from technical_analysis import detect_support_resistance, detect_candlestick_patterns
from notifier import send_telegram_message

# لیست ارزها به فرمت lbank
symbols = [
    'btc_usdt', 'eth_usdt', 'bnb_usdt', 'xrp_usdt', 'ada_usdt',
    'sol_usdt', 'dot_usdt', 'link_usdt', 'ltc_usdt', 'doge_usdt',
    'trx_usdt', 'avax_usdt', 'matic_usdt', 'uni_usdt', 'atom_usdt'
]

def analyze_symbol(symbol, interval='1h', limit=150):
    print(f"\n----- Analyzing {symbol.upper()} -----")
    
    # دریافت داده‌های OHLCV از LBank
    df = get_ohlcv(symbol, interval, limit)

    # شناسایی سطوح حمایت و مقاومت
    supports, resistances = detect_support_resistance(df)
    
    # شناسایی الگوهای کندلی
    patterns = detect_candlestick_patterns(df)

    # چاپ سطوح حمایت و مقاومت
    print("Support Levels:")
    for t, s in supports[-3:]:  # نمایش آخرین 3 سطح حمایت
        print(f"{t} - {s:.2f}")

    print("Resistance Levels:")
    for t, r in resistances[-3:]:  # نمایش آخرین 3 سطح مقاومت
        print(f"{t} - {r:.2f}")

    # چاپ الگوهای کندلی
    print("Candlestick Patterns:")
    for t, p in patterns[-3:]:  # نمایش آخرین 3 الگوی کندلی
        print(f"{t} - {p}")

    # ارسال نتایج به تلگرام
    message = f"تحلیل ارز {symbol.upper()} در تایم‌فریم {interval}:\n\n"
    message += "Support Levels:\n"
    for t, s in supports[-3:]:
        message += f"{t} - {s:.2f}\n"
    message += "\nResistance Levels:\n"
    for t, r in resistances[-3:]:
        message += f"{t} - {r:.2f}\n"
    message += "\nCandlestick Patterns:\n"
    for t, p in patterns[-3:]:
        message += f"{t} - {p}\n"
    
    send_telegram_message(message)  # ارسال پیام به تلگرام

def main():
    for symbol in symbols:
        try:
            analyze_symbol(symbol)
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            send_telegram_message(f"خطا در تحلیل {symbol}: {e}")

if __name__ == "__main__":
    main()
