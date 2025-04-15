import pandas as pd

def is_support(df, i):
    """بررسی اینکه آیا نقطه i یک سطح حمایت است."""
    return df['low'][i] < df['low'][i-1] and df['low'][i] < df['low'][i+1] and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]

def is_resistance(df, i):
    """بررسی اینکه آیا نقطه i یک سطح مقاومت است."""
    return df['high'][i] > df['high'][i-1] and df['high'][i] > df['high'][i+1] and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2]

def get_levels(df):
    """شناسایی سطوح حمایت و مقاومت در داده‌ها."""
    levels = []
    for i in range(2, len(df) - 2):
        if is_support(df, i):
            levels.append(('support', i, df['low'][i]))  # افزودن نوع سطح به همراه شاخص و قیمت
        elif is_resistance(df, i):
            levels.append(('resistance', i, df['high'][i]))  # افزودن نوع سطح به همراه شاخص و قیمت
    return levels

def get_support_resistance_levels(df):
    """
    شناسایی سطوح حمایت و مقاومت و برگشت قیمت از آنها.
    این تابع سطوح حمایت و مقاومت را می‌شناسد و ممکن است آنها را برای تحلیل
    بعدی مورد استفاده قرار دهد.
    """
    levels = get_levels(df)
    
    # نمایش سطوح برای بررسی دقیق‌تر
    supports = [(index, price) for level, index, price in levels if level == 'support']
    resistances = [(index, price) for level, index, price in levels if level == 'resistance']

    return supports, resistances
