import requests

url = "https://api.lbank.info/v2/ticker.do?symbol=btc_usdt"
response = requests.get(url)

print("Status Code:", response.status_code)

try:
    data = response.json()
    print("Raw JSON:", data)
except Exception as e:
    print("JSON parsing error:", e)
    print("Raw text:", response.text)
