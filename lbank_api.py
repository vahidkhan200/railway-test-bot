import requests
import pandas as pd

def get_ohlcv(symbol='btc_usdt', interval='1h', limit=100):
    url = f"https://api.lbank.info/v1/kline.do"
    params = {
        'symbol': symbol,
        'size': limit,
        'type': interval  # '15min', '1h', '1day'
    }

    response = requests.get(url, params=params)
    data = response.json()['data']

    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df.astype({
        'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'float'
    })

    return df
