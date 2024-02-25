from flask import Blueprint, jsonify, request
from .transaction_database import TransactionDatabase

# Define a Blueprint for routes
transaction_routes = Blueprint('transaction_routes', __name__)

# Create an instance of TransactionDatabase
db = TransactionDatabase("db/transaction_db.db")

@transaction_routes.route('/getFee', methods=['GET'])
def get_fee():
    # Get transaction_hash from the request arguments
    transaction_hash = request.args.get('transaction_hash')

    # Check if transaction_hash is provided
    if not transaction_hash:
        return jsonify({'error': 'Transaction hash is required'}), 400

    # Query the database for the fee of the given transaction_hash
    fee = db.get_fee_by_transaction_hash(transaction_hash)

    print(fee)

    if fee is None:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify({'fee': fee}), 200