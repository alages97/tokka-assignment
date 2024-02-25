from apscheduler.schedulers.background import BackgroundScheduler
from app.service.background_transaction_fetcher_service import fetch_and_store_transactions
from app.db.transaction_database import TransactionDatabase
from app.service.fee_price_calculator import FeePriceCalculator
from flask import Flask, jsonify,request
from flask_swagger_ui import get_swaggerui_blueprint
import datetime
import requests

#Scheduler to fetch and store transactions into DB
sched = BackgroundScheduler(daemon=True)
sched.add_job(fetch_and_store_transactions, 'interval', seconds=10, next_run_time=datetime.datetime.now())
sched.start()

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

db = TransactionDatabase("db/transaction_db.db")
fee_price_calculator = FeePriceCalculator()

@app.route('/getFee')
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) #TODO change the port to env variable