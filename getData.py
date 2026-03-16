import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_exchange_rates(base_currency="USD"):
    API_KEY = os.getenv("ExchangeRate_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rates']
    except Exception as e:
        print(f"Error fetching rates: {e}")
    return None

if __name__ == "__main__":
    # Test call
    rates = get_exchange_rates()
    if rates:
        print(f"USD to EUR: {rates.get('EUR')}")
