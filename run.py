from apscheduler.schedulers.background import BackgroundScheduler
from app.service import fetch_and_store_transactions
from flask import Flask
from app.routes import transaction_routes
import datetime

def sensor():
    print("Test")

sched = BackgroundScheduler(daemon=True)
sched.add_job(fetch_and_store_transactions, 'interval', seconds=10, next_run_time=datetime.datetime.now())
sched.start()

app = Flask(__name__)
app.register_blueprint(transaction_routes)

if __name__ == "__main__":
    app.run()