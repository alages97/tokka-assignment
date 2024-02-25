import datetime

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from apscheduler.schedulers.background import BackgroundScheduler

from app.service.background_transaction_fetcher_service import fetch_and_store_transactions
from app.routes.routes import fee_routes


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
app.register_blueprint(fee_routes)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)