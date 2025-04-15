def generate_signal(df):
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

    # ATR - برای تحلیل حد ضرر یا نوسان‌سنجی استفاده می‌شه
    atr_value = last['atr']

    return signal, reason, atr_value
def is_strong_buy_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    conditions = [
        latest['RSI'] < 30,
        latest['MACD'] > latest['MACD_signal'] and prev['MACD'] <= prev['MACD_signal'],
        latest['close'] > latest['EMA_20'],
        latest['close'] < latest['resistance'] * 1.01,
        latest['candle_pattern'] in ['hammer', 'bullish_engulfing'],
    ]

    return sum(conditions) >= 3  # حداقل ۳ شرط برقرار باشه


def is_strong_sell_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    conditions = [
        latest['RSI'] > 70,
        latest['MACD'] < latest['MACD_signal'] and prev['MACD'] >= prev['MACD_signal'],
        latest['close'] < latest['EMA_20'],
        latest['close'] > latest['support']
