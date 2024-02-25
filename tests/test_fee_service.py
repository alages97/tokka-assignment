import unittest
from unittest.mock import MagicMock
from app.service.fee_service import FeeService

class TestFeeService(unittest.TestCase):
    def setUp(self):
        # Create mock objects for db and fee_price_calculator
        self.mock_db = MagicMock()
        self.mock_fee_price_calculator = MagicMock()
        self.fee_service = FeeService(self.mock_db, self.mock_fee_price_calculator)

    def test_get_fee_transaction_not_found(self):
        # Mock the behavior of db.get_fee_and_time_by_transaction_hash to return None (transaction not found)
        self.mock_db.get_fee_and_time_by_transaction_hash.return_value = None
        
        # Call the get_fee method with a non-existent transaction hash
        response = self.fee_service.get_fee('nonexistent_hash')
        
        # Assert that the response contains the expected error message and status code
        self.assertEqual(response, ({'error': 'Transaction not found'}, 404))

    def test_get_fee_unable_to_calculate_price(self):
        # Mock the behavior of db.get_fee_and_time_by_transaction_hash to return a transaction tuple
        self.mock_db.get_fee_and_time_by_transaction_hash.return_value = [(100, 123)]
        
        # Mock the behavior of fee_price_calculator.get_fee_in_usdt to return None (unable to calculate price)
        self.mock_fee_price_calculator.get_fee_in_usdt.return_value = None
        
        # Call the get_fee method with a valid transaction hash
        response = self.fee_service.get_fee('valid_hash')
        
        # Assert that the response contains the expected error message and status code
        self.assertEqual(response, ({'error': 'Unable to calculate price'}, 404))

    def test_get_fee_success(self):
        # Mock the behavior of db.get_fee_and_time_by_transaction_hash to return a transaction tuple
        self.mock_db.get_fee_and_time_by_transaction_hash.return_value = [(100, 123)]
        
        # Mock the behavior of fee_price_calculator.get_fee_in_usdt to return a fee value
        self.mock_fee_price_calculator.get_fee_in_usdt.return_value = 50
        
        # Call the get_fee method with a valid transaction hash
        response = self.fee_service.get_fee('valid_hash')
        
        # Assert that the response contains the expected fee value and status code
        self.assertEqual(response, ({'fee': 50}, 200))

if __name__ == '__main__':
    unittest.main()