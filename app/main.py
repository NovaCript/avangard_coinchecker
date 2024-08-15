import time
from coinmarket.coinmarketcap_api import get_latest_price
from coinmarket.models import CryptoCurrencyTracker


def main():
    tracker = CryptoCurrencyTracker()
    tracker.add_currency("LTC", 60, 50)

    while True:
        for symbol in tracker.currencies.keys():
            price = get_latest_price(symbol)
            if price is not None:
                tracker.currencies[symbol].update_price(price)
        notifications = tracker.check_thresholds()
        for notification in notifications:
            print(notification)
        time.sleep(60)  # update prices every 1 minute


if __name__ == "__main__":
    main()
