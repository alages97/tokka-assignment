from flask import Blueprint, jsonify, request
from ..db.transaction_database import TransactionDatabase
from ..service.fee_price_calculator import FeePriceCalculator

# Define a Blueprint for routes
transaction_routes = Blueprint('transaction_routes', __name__)

# Create an instance of TransactionDatabase
db = TransactionDatabase("db/transaction_db.db")
fee_price_calculator = FeePriceCalculator()

@transaction_routes.route('/getFee', methods=['GET'])
def get_fee():
    # Get transaction_hash from the request arguments
    transaction_hash = request.args.get('transaction_hash')

    # Check if transaction_hash is provided
    if not transaction_hash:
        return jsonify({'error': 'Transaction hash is required'}), 400

    # Query the database for the fee of the given transaction_hash
    res = db.get_fee_and_time_by_transaction_hash(transaction_hash)

    if res is None:
        return jsonify({'error': 'Transaction not found'}), 404

    fee_in_wei = res[-1][0]
    time_ms = res[-1][1] * 1000

    fee_in_usdt = fee_price_calculator.get_fee_in_usdt(fee_in_wei, time_ms)

    if fee_in_usdt is None:
        return jsonify({'error': 'Unable to calculate price'}), 404
    
    return jsonify({'fee': fee_in_usdt}), 200