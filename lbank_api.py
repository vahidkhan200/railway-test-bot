import requests
import pandas as pd

def get_ohlcv(symbol='btc_usdt', interval='1h', limit=100):
    """
    دریافت داده‌های OHLCV از API LBank و تبدیل آن به یک DataFrame
    
    :param symbol: جفت ارز برای دریافت داده‌ها (مثال: 'btc_usdt')
    :param interval: تایم‌فریم برای دریافت داده‌ها (مثال: '15min', '1h', '1day')
    :param limit: تعداد داده‌های دریافت شده (پیش‌فرض 100)
    
    :return: DataFrame شامل زمان، قیمت باز، بالا، پایین، بسته و حجم
    """
    url = f"https://api.lbank.info/v1/kline.do"
    params = {
        'symbol': symbol,
        'size': limit,
        'type': interval  # '15min', '1h', '1day'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # بررسی وضعیت درخواست

        data = response.json().get('data', [])
        
        if not data:
            print(f"هیچ داده‌ای برای {symbol} در تایم‌فریم {interval} موجود نیست.")
            return None
        
        # تبدیل داده‌ها به DataFrame
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        
        # تبدیل زمان از میلی‌ثانیه به datetime
        df['time'] = pd.to_datetime(df['time'], unit='ms')

        # تبدیل مقادیر قیمت‌ها و حجم به نوع float
        df = df.astype({
            'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'float'
        })

        return df

    except requests.exceptions.RequestException as e:
        # مدیریت خطاهای مربوط به درخواست (مشکلات شبکه یا API)
        print(f"خطا در درخواست به API: {e}")
        return None
