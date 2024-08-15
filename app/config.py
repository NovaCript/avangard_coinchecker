from dotenv import dotenv_values

config = dotenv_values(".env")

API_KEY = config["API_KEY"]
COINMARKETCAP_API_URL = config["COINMARKETCAP_API_URL"]
