import pandas as pd

def is_support(df, i):
    return df['low'][i] < df['low'][i-1] and df['low'][i] < df['low'][i+1] and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]

def is_resistance(df, i):
    return df['high'][i] > df['high'][i-1] and df['high'][i] > df['high'][i+1] and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2]

def get_levels(df):
    levels = []
    for i in range(2, len(df) - 2):
        if is_support(df, i):
            levels.append((i, df['low'][i]))
        elif is_resistance(df, i):
            levels.append((i, df['high'][i]))
    return levels
