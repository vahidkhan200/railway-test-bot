import requests

url = "https://api.lbank.info/v2/ticker.do?symbol=btc_usdt"
res = requests.get(url)
data = res.json()

print("Raw response:", data)
