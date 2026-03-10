import requests
import os
from dotenv import load_dotenv

load_dotenv()

Courensy = "USD"
API_KEY = os.getenv("ExchangeRate_API_KEY")
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{Courensy}"

def get_exchange_rates():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success':
            print(data)


get_exchange_rates()