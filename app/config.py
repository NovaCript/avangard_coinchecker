import os
from dotenv import load_dotenv, dotenv_values

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

config = dotenv_values(dotenv_path)

class Config:
    def __init__(self):
        self.COINMARKETCAP_API_URL = os.getenv('COINMARKETCAP_API_URL')
        self.API_KEY = os.getenv('API_KEY')
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        if not self.TELEGRAM_TOKEN:
            raise ValueError('TELEGRAM_TOKEN не задан в файле .env')
        if not self.API_KEY:
            raise ValueError('API_KEY не задан в файле .env')
        if not self.COINMARKETCAP_API_URL:
            raise ValueError('COINMARKETCAP_API_URL не задан в файле .env')

settings = Config()