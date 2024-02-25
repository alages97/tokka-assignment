import requests

class UniswapTransactionFetcher:
    """Class that exposes method to fetch Uniswap transactions"""
    def __init__(self, address):
        self.address = address

    def fetch_transactions(self, start_block, end_block):
        """Fetches transactions from Uniswap"""

        print("start block: {}, end block: {}".format(start_block, end_block))
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={self.address}&startblock={start_block}&endblock={end_block}&sort=desc"
        response = requests.get(url)
        
        if response.status_code == 200:
            transactions = response.json().get('result', [])
            return self.process_transactions(transactions)
        else:
            print("Failed to fetch transactions:", response.status_code)
            return []

    def process_transactions(self, transactions):
        """Processes the transactions fetched from uniswap and converts them into transaction data"""
        print("Number of new transactions fetched {}".format(len(transactions)))
        processed_transactions = []
        for tx in transactions:
            try: 
                transaction_hash = tx.get('hash')
                time_ms = int(tx.get('timeStamp')) * 1000 #we receive time in seconds, convert to milliseconds before insert into DB
                block_number = tx.get('blockNumber')
                gas_used = int(tx.get('gasUsed', 0))
                gas_price = int(tx.get('gasPrice', 0))
                fee = gas_used * gas_price
                
                processed_transactions.append({
                    'transaction_hash': transaction_hash,
                    'fee': fee,
                    'time_ms' : time_ms,
                    'block_number': block_number
                })
            except Exception:
                print("Skipping transaction due to error processing fields")
        
        return processed_transactions