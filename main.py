import requests

url = "https://api.lbank.info/v2/ticker.do?symbol=btc_usdt"
response = requests.get(url)
data = response.json()

price = data['data'][0]['ticker']['latest']
print("BTC/USDT:", price)
