from app.transaction_database import TransactionDatabase

transactions_db = TransactionDatabase("db/trans_db.db")
test_transactions = [{"transaction_id" : "test", "timeMs" : 123, "fee": 20}]
transactions_db.insert_transactions(transactions=test_transactions)