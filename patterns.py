import pandas as pd

def detect_patterns(df):
    df['pattern'] = ''

    # Engulfing
    cond_engulfing = (
        (df['close'].shift(1) > df['open'].shift(1)) &  # قبلی سبز
        (df['open'] > df['close']) &  # فعلی قرمز
        (df['open'] > df['close'].shift(1)) &
        (df['close'] < df['open'].shift(1))
    )
    df.loc[cond_engulfing, 'pattern'] = 'Bearish Engulfing'

    cond_engulfing_bull = (
        (df['close'].shift(1) < df['open'].shift(1)) &  # قبلی قرمز
        (df['close'] > df['open']) &  # فعلی سبز
        (df['close'] > df['open'].shift(1)) &
        (df['open'] < df['close'].shift(1))
    )
    df.loc[cond_engulfing_bull, 'pattern'] = 'Bullish Engulfing'

    # Hammer
    cond_hammer = (
        (df['high'] - df['low']) > 3 * (df['open'] - df['close']) &
        (df['close'] - df['low']) / (.001 + df['high'] - df['low']) > 0.6 &
        (df['open'] - df['low']) / (.001 + df['high'] - df['low']) > 0.6
    )
    df.loc[cond_hammer, 'pattern'] = 'Hammer'

    # Doji
    cond_doji = (abs(df['close'] - df['open']) / (df['high'] - df['low'])) < 0.1
    df.loc[cond_doji, 'pattern'] = 'Doji'

    return df
