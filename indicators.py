import pandas as pd
import ta

def add_indicators(klines):
    df = pd.DataFrame(klines)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # EMA
    df['EMA_20'] = ta.trend.ema_indicator(df['close'], window=20).ema_indicator()

    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(df['close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # ATR
    df['ATR'] = ta.volatility.AverageTrueRange(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    ).average_true_range()

    return df
