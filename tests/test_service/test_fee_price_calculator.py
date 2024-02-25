import unittest
from unittest.mock import MagicMock
from app.service.fee_price_calculator import FeePriceCalculator

class TestFeePriceCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = FeePriceCalculator()

    def test_get_price_from_binance_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [[0, '100'], [1, '200']]  # Sample kline data

        with unittest.mock.patch('requests.get', return_value=mock_response):
            price = self.calculator.get_price_from_binance(0)
            self.assertEqual(price, 200.0)  # Expected price is the last element of the kline data

    def test_get_price_from_binance_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulate a failed request

        with unittest.mock.patch('requests.get', return_value=mock_response):
            price = self.calculator.get_price_from_binance(0)
            self.assertIsNone(price)  # Expecting None when request fails

    def test_get_latest_price_from_binance_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'price': '500'}  # Sample ticker data

        with unittest.mock.patch('requests.get', return_value=mock_response):
            price = self.calculator.get_latest_price_from_binance()
            self.assertEqual(price, 500.0)  # Expected price is the value from ticker data

    def test_get_latest_price_from_binance_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulate a failed request

        with unittest.mock.patch('requests.get', return_value=mock_response):
            price = self.calculator.get_latest_price_from_binance()
            self.assertIsNone(price)  # Expecting None when request fails

    def test_get_fee_in_usdt(self):
        # Mocking methods to return specific values
        self.calculator.get_price_from_binance = MagicMock(return_value=1000.0)
        self.calculator.get_latest_price_from_binance = MagicMock(return_value=2000.0)

        wei_price = 1000000000000000000  # 1 ETH in Wei
        time_ms = 0  # Example time
        expected_fee = 1000.0  # Calculated expected fee

        fee = self.calculator.get_fee_in_usdt(wei_price, time_ms)
        self.assertEqual(fee, expected_fee)

if __name__ == '__main__':
    unittest.main()