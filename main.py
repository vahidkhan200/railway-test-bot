import requests

symbols = [
    'btc_usdt', 'eth_usdt', 'xrp_usdt', 'bnb_usdt',
    'hbar_usdt', 'xlm_usdt', 'xdc_usdt', 'not_usdt', 'dydx_usdt'
]

for symbol in symbols:
    url = f"https://api.lbank.info/v2/ticker.do?symbol={symbol}"
    response = requests.get(url)
    data = response.json()

    try:
        price = data['data'][0]['ticker']['latest']
        print(f"{symbol.upper()}: {price}")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
