if 'ticker' in data:
    price = data['ticker']['latest']
    print("BTC/USDT:", price)
else:
    print("No ticker found. Full response:")
    print(data)
