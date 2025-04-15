def detect_candle_patterns(df):
    df = df.copy()

    # Engulfing - Bullish
    df['bullish_engulfing'] = (
        (df['close'].shift(1) < df['open'].shift(1)) &
        (df['close'] > df['open']) &
        (df['open'] < df['close'].shift(1)) &
        (df['close'] > df['open'].shift(1))
    )

    # Engulfing - Bearish
    df['bearish_engulfing'] = (
        (df['close'].shift(1) > df['open'].shift(1)) &
        (df['close'] < df['open']) &
        (df['open'] > df['close'].shift(1)) &
        (df['close'] < df['open'].shift(1))
    )

    # Doji
    df['doji'] = abs(df['close'] - df['open']) / (df['high'] - df['low'] + 1e-10) < 0.1

    return df
