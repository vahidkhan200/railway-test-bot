import pandas as pd
import ta

def analyze(ohlcv, symbol):
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # محاسبه اندیکاتورها
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # شرط ساده برای سیگنال خرید
    if last['rsi'] < 30 and last['macd'] > last['macd_signal'] and prev['macd'] < prev['macd_signal']:
        return f"""
📈 سیگنال خرید ({symbol})
تایم‌فریم: 1H
نقطه ورود: {last['close']:.2f}
حد سود: {last['close'] * 1.05:.2f}
حد ضرر: {last['close'] * 0.97:.2f}
لوریج: اختیاری

تحلیل بر اساس: RSI و MACD
        """
    return None
