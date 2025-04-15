def generate_signal(df, patterns, levels):
    last = df.iloc[-1]
    previous = df.iloc[-2]

    signal = None
    reason = []

    # MACD سیگنال
    if previous['macd'] < previous['signal'] and last['macd'] > last['signal']:
        signal = 'buy'
        reason.append('MACD bullish crossover')
    elif previous['macd'] > previous['signal'] and last['macd'] < last['signal']:
        signal = 'sell'
        reason.append('MACD bearish crossover')

    # RSI سیگنال
    if last['rsi'] < 30:
        signal = 'buy'
        reason.append('RSI oversold')
    elif last['rsi'] > 70:
        signal = 'sell'
        reason.append('RSI overbought')

    # الگوهای کندلی
    if 'Bullish Engulfing' in patterns:
        signal = 'buy'
        reason.append('Bullish Engulfing pattern detected')
    elif 'Bearish Engulfing' in patterns:
        signal = 'sell'
        reason.append('Bearish Engulfing pattern detected')

    # بررسی سطح حمایت/مقاومت
    if signal == 'buy' and last['close'] > levels['support']:
        reason.append(f"Price is above support level ({levels['support']:.2f})")
    elif signal == 'sell' and last['close'] < levels['resistance']:
        reason.append(f"Price is below resistance level ({levels['resistance']:.2f})")

    # ATR - برای تحلیل حد ضرر یا نوسان‌سنجی
    atr_value = last['atr']

    # تعیین حد ضرر بر اساس ATR (حد ضرر = قیمت ورود - ATR)
    if signal == 'buy':
        stop_loss = last['close'] - atr_value
        targets = [last['close'] * 1.01, last['close'] * 1.02, last['close'] * 1.03]
    elif signal == 'sell':
        stop_loss = last['close'] + atr_value
        targets = [last['close'] * 0.99, last['close'] * 0.98, last['close'] * 0.97]
    else:
        stop_loss = None
        targets = []

    return {
        'signal': signal,
        'reason': reason,
        'stop_loss': stop_loss,
        'targets': targets,
        'atr_value': atr_value
    }
