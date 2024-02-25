import sqlite3

class TransactionDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id TEXT PRIMARY KEY,
                timeMs INTEGER,
                fee DECIMAL
            )
        ''')
        self.connection.commit()

    def get_transactions_by_time_range(self, start_time, end_time):
        query = "SELECT * FROM Transactions WHERE timeMs BETWEEN ? AND ?"
        self.cursor.execute(query, (start_time, end_time))
        return self.cursor.fetchall()

    def insert_transactions(self, transactions):
        try:
            for transaction in transactions:
                print(transaction)
                self.cursor.execute("INSERT INTO Transactions (transaction_id, timeMs, fee) VALUES (?, ?, ?)",
                                    (transaction['transaction_id'], transaction['timeMs'], transaction['fee']))
            self.connection.commit()
            print("Transactions inserted into database successfully.")
        except Exception as e:
            print("Failed to insert transactions into database:", e)