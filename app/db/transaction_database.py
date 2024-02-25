"""Module provides methods for sqlite"""
import sqlite3

class TransactionDatabase:
    """Database that stores the information about WETH transactions in Uniswap"""

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Creates DB table if does not exist"""

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
        """Gets transactions by time range"""

        query = "SELECT * FROM Transactions WHERE time_ms BETWEEN ? AND ?"
        self.cursor.execute(query, (start_time, end_time))
        return self.cursor.fetchall()
    
    def get_fee_and_time_by_transaction_hash(self, transaction_hash):
        """Gets fee and time given a transaction hash"""

        query = "SELECT fee, time_ms FROM Transactions WHERE transaction_hash = ?"
        self.cursor.execute(query, (transaction_hash,))
        return self.cursor.fetchall()

    def insert_transactions(self, transactions):
        """Inserts transactions into the DB"""
        try:
            for transaction in transactions:
                self.cursor.execute("INSERT OR IGNORE INTO Transactions (transaction_hash, time_ms, fee, block_number) VALUES (?, ?, ?, ?)",
                                    (transaction['transaction_hash'], transaction['time_ms'], transaction['fee'], transaction['block_number']))
            self.connection.commit()
            print("Transactions inserted into database successfully.")
        except Exception as e:
            print("Failed to insert transactions into database:", e)

    def check_db_size(self):
        """Monitor size of DB, could do periodic cleanups of DB if size gets too large"""
        query = "SELECT count(*) FROM Transactions"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print("Current number of transactions stored in DB: {}".format(result[0]))

    def fetch_largest_block_number(self):
        """Fetches current largest block number, so that we don't have to process these blocks again"""
        query = "SELECT MAX(block_number) FROM Transactions"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result and result[0]:
            return result[0]
        else:
            return 0  # Return 0 if no block number found in the database
    
    def get_fee_stats_by_time_range(self, start_time_ms, end_time_ms):
        """Get maximum, minimum, and average fee within a time range"""
        query = """
            SELECT 
                MAX(fee) AS max_fee, 
                MIN(fee) AS min_fee, 
                AVG(fee) AS avg_fee 
            FROM Transactions 
            WHERE time_ms BETWEEN ? AND ?
        """
        self.cursor.execute(query, (start_time_ms, end_time_ms))
        result = self.cursor.fetchone()

        max_fee = result[0]
        min_fee = result[1]
        avg_fee = result[2]
        print("Max fee: {}, min fee: {}, avg fee: {}".format(max_fee, min_fee, avg_fee))

        return max_fee, min_fee, avg_fee