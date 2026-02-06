import requests
import os

TELEGRAM_TOKEN = os.environ['BTC_TELEGRAM_API_KEY']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
COINDESK_API_KEY = os.environ['COINDESK_API_KEY']

params = {
    'fsym': 'BTC',
    'tsyms': 'USD',
     }

headers = {
    'User-Agent': 'btc-bot/1.0',
    'authorization': f'Apikey {COINDESK_API_KEY}'
}


btc_price_url = 'https://min-api.cryptocompare.com/data/price'
response = requests.get(btc_price_url, params=params, timeout=20, headers=headers)
response.raise_for_status()
price_data = response.json()

todays_price = round(float(price_data['USD']))

params = {
    'fsym': 'BTC',
    'tsym': 'USD',
    'limit': 1,
     }

btc_history_url = 'https://min-api.cryptocompare.com/data/v2/histoday'
history_response = requests.get(btc_history_url, params=params, timeout=20, headers=headers)
history_response.raise_for_status()
history_data = history_response.json()['Data']['Data']

yesterdays_price = round(float(history_data[0]['close']), 1)
price_change_percent = round(((todays_price - yesterdays_price) / yesterdays_price * 100), 1)

if price_change_percent > 0:
    direction = 'Went up'
    emoji_direction = '% 📈'
elif price_change_percent < 0:
    direction = 'Went down'
    emoji_direction = '% 📉'
else:
    direction = 'Didnt change.'
    emoji_direction = ''


text = f'Hey daddy, BTC is at ${todays_price:,} USD.\n{direction} {price_change_percent:g}{emoji_direction}'

telegram_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
params = {
    'chat_id': CHAT_ID,
    'text': text,
}

response = requests.post(telegram_url, json=params, timeout=20)
response.raise_for_status()
