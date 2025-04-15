import requests
import datetime

def get_klines(symbol: str, interval: str = "15min", limit: int = 100):
    url = "https://api.lbank.info/v1/kline.do"
    params = {
        "symbol": symbol,
        "size": limit,
        "type": interval
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["result"]:
        klines = []
        for entry in data["data"]:
            klines.append({
                "timestamp": datetime.datetime.fromtimestamp(entry[0] / 1000),
                "open": float(entry[1]),
                "high": float(entry[2]),
                "low": float(entry[3]),
                "close": float(entry[4]),
                "volume": float(entry[5])
            })
        return klines
    else:
        return None
