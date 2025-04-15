import pandas as pd

def detect_patterns(df):
    """
    تشخیص الگوهای کندلی در دیتافریم و علامت‌گذاری آن‌ها.
    
    :param df: دیتافریم با قیمت‌های OHLCV (open, high, low, close)
    :return: دیتافریم با ستون 'pattern' که الگوی شناسایی‌شده را در خود دارد.
    """
    # ستون جدید برای نگهداری الگوها
    df['pattern'] = ''

    # Bearish Engulfing
    cond_engulfing = (
        (df['close'].shift(1) > df['open'].shift(1)) &  # قبلی سبز
        (df['open'] > df['close']) &  # فعلی قرمز
        (df['open'] > df['close'].shift(1)) &
        (df['close'] < df['open'].shift(1))
    )
    df.loc[cond_engulfing, 'pattern'] = 'Bearish Engulfing'

    # Bullish Engulfing
    cond_engulfing_bull = (
        (df['close'].shift(1) < df['open'].shift(1)) &  # قبلی قرمز
        (df['close'] > df['open']) &  # فعلی سبز
        (df['close'] > df['open'].shift(1)) &
        (df['open'] < df['close'].shift(1))
    )
    df.loc[cond_engulfing_bull, 'pattern'] = 'Bullish Engulfing'

    # Hammer
    cond_hammer = (
        (df['high'] - df['low']) > 3 * (df['open'] - df['close']) &  # بدنه کوچیک
        (df['close'] - df['low']) / (0.001 + df['high'] - df['low']) > 0.6 &  # دقت به موقعیت
        (df['open'] - df['low']) / (0.001 + df['high'] - df['low']) > 0.6
    )
    df.loc[cond_hammer, 'pattern'] = 'Hammer'

    # Doji
    cond_doji = (abs(df['close'] - df['open']) / (df['high'] - df['low'])) < 0.1
    df.loc[cond_doji, 'pattern'] = 'Doji'

    # اضافه کردن الگوهای دیگر (اگر نیاز باشد، به راحتی می‌توان الگوهای بیشتر را اضافه کرد)
    # مثال:
    # # Shooting Star
    # cond_shooting_star = (
    #     (df['high'] - df['low']) > 2 * (df['open'] - df['close']) &
    #     (df['close'] - df['low']) / (df['high'] - df['low']) < 0.4
    # )
    # df.loc[cond_shooting_star, 'pattern'] = 'Shooting Star'

    return df
