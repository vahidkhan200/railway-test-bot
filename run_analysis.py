from lbank_api import get_ohlcv
from technical_analysis import detect_support_resistance, detect_candlestick_patterns

# لیست ارزها به فرمت lbank
symbols = [
    'btc_usdt', 'eth_usdt', 'bnb_usdt', 'xrp_usdt', 'ada_usdt',
    'sol_usdt', 'dot_usdt', 'link_usdt', 'ltc_usdt', 'doge_usdt',
    'trx_usdt', 'avax_usdt', 'matic_usdt', 'uni_usdt', 'atom_usdt'
]

def analyze_symbol(symbol):
    print(f"\n----- Analyzing {symbol.upper()} -----")
    df = get_ohlcv(symbol, '1h', 150)

    supports, resistances = detect_support_resistance(df)
    patterns = detect_candlestick_patterns(df)

    print("Support Levels:")
    for t, s in supports[-3:]:
        print(f"{t} - {s:.2f}")

    print("Resistance Levels:")
    for t, r in resistances[-3:]:
        print(f"{t} - {r:.2f}")

    print("Candlestick Patterns:")
    for t, p in patterns[-3:]:
        print(f"{t} - {p}")

def main():
    for symbol in symbols:
        try:
            analyze_symbol(symbol)
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")

if __name__ == "__main__":
    main()
