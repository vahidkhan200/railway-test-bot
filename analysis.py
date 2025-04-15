import pandas as pd
import ta

def analyze(ohlcv, symbol, timeframe='1H'):
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # محاسبه اندیکاتورها
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    
    # محاسبه ATR برای حد ضرر و حد سود داینامیک
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # شرط سیگنال خرید
    if last['rsi'] < 30 and last['macd'] > last['macd_signal'] and prev['macd'] < prev['macd_signal']:
        stop_loss = last['close'] - last['atr'] * 1.5  # استفاده از ATR برای حد ضرر
        take_profit = last['close'] + last['atr'] * 2.5  # استفاده از ATR برای حد سود
        return f"""
📈 سیگنال خرید ({symbol})
تایم‌فریم: {timeframe}
نقطه ورود: {last['close']:.2f}
حد سود: {take_profit:.2f}
حد ضرر: {stop_loss:.2f}
لوریج: اختیاری

تحلیل بر اساس: RSI و MACD
        """
    
    # شرط سیگنال فروش
    elif last['rsi'] > 70 and last['macd'] < last['macd_signal'] and prev['macd'] > prev['macd_signal']:
        stop_loss = last['close'] + last['atr'] * 1.5  # استفاده از ATR برای حد ضرر
        take_profit = last['close'] - last['atr'] * 2.5  # استفاده از ATR برای حد سود
        return f"""
📉 سیگنال فروش ({symbol})
تایم‌فریم: {timeframe}
نقطه ورود: {last['close']:.2f}
حد سود: {take_profit:.2f}
حد ضرر: {stop_loss:.2f}
لوریج: اختیاری

تحلیل بر اساس: RSI و MACD
        """
    
    return None
