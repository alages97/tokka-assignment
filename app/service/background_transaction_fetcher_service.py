"""Background transaction fetcher service to pull and update DB"""

from ..db.transaction_database import TransactionDatabase
from .uniswap_transaction_fetcher import UniswapTransactionFetcher


def fetch_and_store_transactions():
    """Fetches uniswap transactions and stores into the DB"""

    db = TransactionDatabase("db/transaction_db.db")
    fetcher = UniswapTransactionFetcher(address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")

    #check db size
    db.check_db_size()

    # Fetch the latest block number from the database
    latest_block_number = db.fetch_largest_block_number()
    print(f"Latest processed block number: {latest_block_number}")

    # Fetch transactions from Uniswap using the latest block number+1 as start block
    transactions = fetcher.fetch_transactions(start_block=latest_block_number + 1, 
                                              end_block= 99999999)

    # Store transactions into the database
    db.insert_transactions(transactions)
