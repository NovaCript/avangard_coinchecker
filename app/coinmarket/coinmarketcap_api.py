import requests
from app.config import COINMARKETCAP_API_URL, API_KEY


def get_latest_price(symbol):
    params = {"symbol": symbol, "convert": "USD"}
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    response = requests.get(COINMARKETCAP_API_URL, params=params, headers=headers)
    data = response.json()
    try:
        price = data["data"][symbol]["quote"]["USD"]["price"]
    except KeyError as e:
        print(f"Error: {e}")
        print(f"Response data: {data}")
        return None
    return price
