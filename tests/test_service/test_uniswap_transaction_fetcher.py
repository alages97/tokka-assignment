import unittest
from unittest.mock import MagicMock
from app.service.uniswap_transaction_fetcher import UniswapTransactionFetcher

class TestUniswapTransactionFetcher(unittest.TestCase):
    def setUp(self):
        self.address = "your_address"
        self.fetcher = UniswapTransactionFetcher(self.address)

    def test_fetch_transactions_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_transactions = [
            {
                "hash": "tx_hash_1",
                "timeStamp": "1234567890",
                "blockNumber": "1000",
                "gasUsed": "100000",
                "gasPrice": "50000000000"
            },
            {
                "hash": "tx_hash_2",
                "timeStamp": "1234567891",
                "blockNumber": "1001",
                "gasUsed": "200000",
                "gasPrice": "60000000000"
            }
        ]
        mock_response.json.return_value = {"result": mock_transactions}

        with unittest.mock.patch('requests.get', return_value=mock_response):
            transactions = self.fetcher.fetch_transactions(0, 1000)
            self.assertEqual(len(transactions), 2)
            self.assertEqual(transactions[0]['transaction_hash'], 'tx_hash_1')
            self.assertEqual(transactions[0]['fee'], 50000000000 * 100000)

    def test_fetch_transactions_failure(self):
        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulate a failed request

        with unittest.mock.patch('requests.get', return_value=mock_response):
            transactions = self.fetcher.fetch_transactions(0, 1000)
            self.assertEqual(len(transactions), 0)

if __name__ == '__main__':
    unittest.main()