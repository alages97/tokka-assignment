import requests

class UniswapTransactionFetcher:
    def __init__(self, address):
        self.address = address

    def fetch_transactions(self, start_block, end_block):
        print("start block: {}, end block: {}".format(start_block, end_block))
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={self.address}&startblock={start_block}&endblock={end_block}&sort=desc"
        response = requests.get(url)
        
        print(response)
        if response.status_code == 200:
            transactions = response.json().get('result', [])
            return self.process_transactions(transactions)
        else:
            print("Failed to fetch transactions:", response.status_code)
            return []

    def process_transactions(self, transactions):
        processed_transactions = []
        for tx in transactions:
            try: 
                transaction_hash = tx.get('hash')
                time_ms = tx.get('timeStamp')
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