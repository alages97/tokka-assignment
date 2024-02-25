class FeeService:
    """Service that fetches fee details"""
    
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
        time_ms = res[-1][1]

        fee_in_usdt = self.fee_price_calculator.get_fee_in_usdt(fee_in_wei, time_ms)

        if fee_in_usdt is None:
            return {'error': 'Unable to calculate price'}, 404
        
        return {'fee': fee_in_usdt}, 200
    
    def get_fee_statistics(self, start_time_ms, end_time_ms):
        """Get fee statistics (max, min, avg) within a time range"""
        max_fee, min_fee, avg_fee = self.db.get_fee_stats_by_time_range(start_time_ms, end_time_ms)
        if max_fee is None or min_fee is None or avg_fee is None:
            return {'error' : 'Unable to fetch fee statistics'}, 404
        statistics = self.fee_price_calculator.get_fee_statistics_in_usdt(max_fee, min_fee, avg_fee)
        if statistics is None:
            return {'error' : 'Unable to fetch fee statistics'}, 404
        return {'max_fee_usdt': statistics[0], 'min_fee_usdt': statistics[1], 'avg_fee_usdt': statistics[2]}

