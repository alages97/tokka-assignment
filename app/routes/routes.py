from flask import jsonify, Blueprint, request

from ..service.fee_service import FeeService
from ..db.transaction_database import TransactionDatabase
from ..service.fee_price_calculator import FeePriceCalculator

# Create a Blueprint object for defining routes
fee_routes = Blueprint('fee_routes', __name__)

# Create instances of services
db = TransactionDatabase("db/transaction_db.db")
fee_price_calculator = FeePriceCalculator()
fee_service = FeeService(db, fee_price_calculator)

@fee_routes.route('/getFee')
def get_fee():
    """Get rest method to get fee for a transaction"""
    # Get transaction_hash from the request arguments
    transaction_hash = request.args.get('transaction_hash')

    # Call the get_fee method of FeeService
    return fee_service.get_fee(transaction_hash)

@fee_routes.route('/getStatistics')
def get_fee_statistics():
    """Get rest method to get fee for a transaction"""
    # Get transaction_hash from the request arguments
    start_time_ms = request.args.get('start_time')
    end_time_ms = request.args.get('end_time')

    # Call the get_fee method of FeeService
    return fee_service.get_fee_statistics(start_time_ms, end_time_ms)