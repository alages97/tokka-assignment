import requests

class FeePriceCalculator:
    """Fetches ETH-USDT price and converts fee to USDT form"""

    def __init__(self):
        self.base_kline_url = "https://www.binance.com/api/v3/klines"
        self.base_ticker_price_url = "https://www.binance.com/api/v3/ticker/price"
        self.symbol = "ETHUSDT"
        self.interval = '1m'

    def get_price_from_binance(self, time_ms):
        """Fetches ETH-USDT price from binance during a given time"""

        start_time = time_ms
        end_time = time_ms + 60000  # Adding 60,000 milliseconds (1 minute)

        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'startTime': start_time,
            'endTime': end_time
        }

        response = requests.get(self.base_kline_url, params=params)

        if response.status_code == 200:
            kline_data = response.json()
            print(kline_data)
            # Assuming the price is available
            if kline_data and len(kline_data) > 0:
                price = float(kline_data[-1][1])  # Closing price is at index 4
                return price
            else:
                return None
        else:
            print("Failed to fetch price:", response.status_code)
            return None
    
    def get_latest_price_from_binance(self):
        """Fetches latest ETH-USDT price from Binance"""

        params = {
            'symbol': self.symbol
        }
        response = requests.get(self.base_ticker_price_url, params=params)
        if response.status_code == 200:
            ticker_data = response.json()
            if ticker_data and len(ticker_data) > 0:
                print(ticker_data)
                price = float(ticker_data['price'])
                return price
            else:
                return None
        else:
            print("Failed to fetch latest price:", response.status_code)
            return None

    def get_fee_in_usdt(self, wei_price, time_ms):
        """Converts fee from wei to USDT"""
        
        price = self.get_price_from_binance(time_ms)
        if price is None:
            print("Unable to fetch price at transaction time from Binance, defaulting to fetch latest price from Binance")
            price = self.get_latest_price_from_binance()
            if price is None:
                print("Unable to fetch latest price from Binance")
                return None
        return wei_price * pow(10, -18) * price