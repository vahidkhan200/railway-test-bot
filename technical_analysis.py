import pandas as pd
import ta

def detect_support_resistance(df, window=5):
    """
    شناسایی سطوح حمایت و مقاومت با استفاده از پنجره مشخص.
    """
    support = []
    resistance = []

    for i in range(window, len(df) - window):
        low_range = df['low'][i - window:i + window]
        high_range = df['high'][i - window:i + window]

        current_low = df['low'][i]
        current_high = df['high'][i]

        # شناسایی سطح حمایت
        if current_low == low_range.min():
            support.append((df['time'][i], current_low))

        # شناسایی سطح مقاومت
        if current_high == high_range.max():
            resistance.append((df['time'][i], current_high))

    return support, resistance

def detect_candlestick_patterns(df):
    """
    شناسایی الگوهای کندلی از جمله Bullish Engulfing و Bearish Engulfing.
    """
    patterns = []

    for i in range(1, len(df)):
        o1, h1, l1, c1 = df.loc[i-1, ['open', 'high', 'low', 'close']]
        o2, h2, l2, c2 = df.loc[i, ['open', 'high', 'low', 'close']]

        # الگوی پوشای صعودی
        if c1 < o1 and c2 > o2 and c2 > o1 and o2 < c1:
            patterns.append((df['time'][i], 'Bullish Engulfing'))

        # الگوی پوشای نزولی
        elif c1 > o1 and c2 < o2 and c2 < o1 and o2 > c1:
            patterns.append((df['time'][i], 'Bearish Engulfing'))

        # الگوی دوجی (Doji)
        elif abs(c2 - o2) < (h2 - l2) * 0.1:
            patterns.append((df['time'][i], 'Doji'))

        # الگوی چکش (Hammer)
        elif (h2 - l2) > 2 * (o2 - c2) and (c2 - l2) / (h2 - l2) > 0.6 and (o2 - l2) / (h2 - l2) > 0.6:
            patterns.append((df['time'][i], 'Hammer'))

    return patterns
