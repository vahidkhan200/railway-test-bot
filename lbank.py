import requests
import datetime

def get_klines(symbol: str, interval: str = "15min", limit: int = 100):
    """
    دریافت داده‌های OHLCV از API LBank
    
    :param symbol: جفت ارز برای درخواست (مثال: 'btc_usdt')
    :param interval: تایم‌فریم برای کاین‌ها (مثال: '15min', '1h')
    :param limit: تعداد داده‌های دریافت شده (پیش‌فرض 100)
    
    :return: لیستی از داده‌ها شامل timestamp, open, high, low, close, volume یا None در صورت خطا
    """
    url = "https://api.lbank.info/v1/kline.do"
    params = {
        "symbol": symbol,
        "size": limit,
        "type": interval
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # بررسی وضعیت درخواست
        data = response.json()

        # اگر داده‌ها موجود باشد، آنها را پردازش کرده و برمی‌گردانیم
        if data.get("result"):
            klines = []
            for entry in data["data"]:
                klines.append({
                    "timestamp": datetime.datetime.fromtimestamp(entry[0] / 1000),  # تبدیل تایم‌استمپ به datetime
                    "open": float(entry[1]),
                    "high": float(entry[2]),
                    "low": float(entry[3]),
                    "close": float(entry[4]),
                    "volume": float(entry[5])
                })
            return klines
        else:
            print(f"خطا: داده‌ای برای {symbol} در تایم‌فریم {interval} پیدا نشد.")
            return None

    except requests.exceptions.RequestException as e:
        # مدیریت خطاهای مربوط به درخواست (مشکلات شبکه یا API)
        print(f"خطا در درخواست به API: {e}")
        return None
