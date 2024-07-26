import requests
import pandas as pd

def fetch_btc_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '30',  # Fetch the last 30 days of data
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data