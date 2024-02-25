import sqlite3

class TransactionDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_hash TEXT PRIMARY KEY,
                time_ms INTEGER,
                fee DECIMAL,
                block_number INTEGER
            )
        ''')
        self.connection.commit()

    def get_transactions_by_time_range(self, start_time, end_time):
        query = "SELECT * FROM Transactions WHERE time_ms BETWEEN ? AND ?"
        self.cursor.execute(query, (start_time, end_time))
        return self.cursor.fetchall()

    def insert_transactions(self, transactions):
        try:
            for transaction in transactions:
                self.cursor.execute("INSERT OR IGNORE INTO Transactions (transaction_hash, time_ms, fee, block_number) VALUES (?, ?, ?, ?)",
                                    (transaction['transaction_hash'], transaction['time_ms'], transaction['fee'], transaction['block_number']))
            self.connection.commit()
            print("Transactions inserted into database successfully.")
        except Exception as e:
            print("Failed to insert transactions into database:", e)

    def fetch_largest_block_number(self):
        query = "SELECT MAX(block_number) FROM Transactions"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            return result[0]
        else:
            return 0  # Return 0 if no block number found in the database