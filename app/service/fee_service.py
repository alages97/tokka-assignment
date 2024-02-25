class FeeService:
    def __init__(self, db, fee_price_calculator):
        self.db = db
        self.fee_price_calculator = fee_price_calculator

    def get_fee(self, transaction_hash):
        """Get fee for a transaction"""
        if not transaction_hash:
            return {'error': 'Transaction hash is required'}, 400

        res = self.db.get_fee_and_time_by_transaction_hash(transaction_hash)

        if res is None:
            return {'error': 'Transaction not found'}, 404

        fee_in_wei = res[-1][0]
        time_ms = res[-1][1] * 1000

        fee_in_usdt = self.fee_price_calculator.get_fee_in_usdt(fee_in_wei, time_ms)

        if fee_in_usdt is None:
            return {'error': 'Unable to calculate price'}, 404
        
        return {'fee': fee_in_usdt}, 200