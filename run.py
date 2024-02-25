import datetime
import requests

from flask import Flask, jsonify,request
from flask_swagger_ui import get_swaggerui_blueprint
from apscheduler.schedulers.background import BackgroundScheduler

import config
from app.db.transaction_database import TransactionDatabase
from app.service.background_transaction_fetcher_service import fetch_and_store_transactions
from app.service.fee_price_calculator import FeePriceCalculator
from app.service.fee_service import FeeService


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
fee_service = FeeService(db, fee_price_calculator)

@app.route('/getFee')
def get_fee():
    """Get rest method to get fee for a transaction"""
    # Get transaction_hash from the request arguments
    transaction_hash = request.args.get('transaction_hash')
    msg,code = fee_service.get_fee(transaction_hash)
    return jsonify(msg), code
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.port)