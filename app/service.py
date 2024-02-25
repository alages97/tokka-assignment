from .uniswap_transaction_fetcher import UniswapTransactionFetcher
from .transaction_database import TransactionDatabase

def fetch_and_store_transactions():
    db = TransactionDatabase("db/test_db.db")
    fetcher = UniswapTransactionFetcher(address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")
    
    # Fetch the maximum block number from the database
    max_block_number = db.fetch_largest_block_number()
    print("Max block number: {}".format(max_block_number))
    
    # Fetch transactions from Uniswap using the maximum block number
    transactions = fetcher.fetch_transactions(start_block=max_block_number + 1, end_block= 99999999)
    
    # Store transactions into the database
    db.insert_transactions(transactions)

    transactions = db.get_transactions_by_time_range(0,999999999999)
    print(len(transactions))