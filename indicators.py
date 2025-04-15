import pandas as pd

def calculate_macd(df):
    """
    محاسبه اندیکاتور MACD و سیگنال آن
    """
    # محاسبه EMA12 و EMA26
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()

    # محاسبه MACD و سیگنال آن
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # مدیریت NaN
    df['macd'].fillna(0, inplace=True)
    df['signal'].fillna(0, inplace=True)

    return df

def calculate_rsi(df, period=14):
    """
    محاسبه اندیکاتور RSI با استفاده از قیمت بسته شدن
    """
    # محاسبه تغییرات قیمت
    delta = df['close'].diff()
    gain = delta.clip(lower=0)  # تغییرات مثبت
    loss = -1 * delta.clip(upper=0)  # تغییرات منفی

    # محاسبه میانگین سود و زیان
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # جلوگیری از تقسیم بر صفر
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # مدیریت NaN
    df['rsi'].fillna(50, inplace=True)

    return df

def calculate_atr(df, period=14):
    """
    محاسبه اندیکاتور ATR (میانگین دامنه واقعی)
    """
    # محاسبه دامنه واقعی
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift())
    df['L-PC'] = abs(df['low'] - df['close'].shift())
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    # محاسبه ATR
    df['atr'] = df['TR'].rolling(window=period).mean()

    # مدیریت NaN
    df['atr'].fillna(0, inplace=True)

    return df
