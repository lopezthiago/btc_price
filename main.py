import requests
import os

TELEGRAM_TOKEN = os.environ["BTC_TELEGRAM_API_KEY"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

btc_url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'
response = requests.get(btc_url, timeout=20)
response.raise_for_status()
data = response.json()

btc_price = round(float(data['lastPrice']))
price_change = round(float(data['priceChangePercent']), 1)

if price_change > 0:
    direction = 'Went up'
    emoji_direction = '% 📈'
elif price_change < 0:
    direction = 'Went down'
    emoji_direction = '% 📉'
else:
    direction = 'Didnt change.'
    emoji_direction = ''


text = f'Hey daddy, BTC is at ${btc_price:,} USD.\n{direction} {price_change:g}{emoji_direction}'

telegram_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
params = {
    'chat_id': CHAT_ID,
    'text': text,
}

response = requests.post(telegram_url, json=params, timeout=20)
response.raise_for_status()
