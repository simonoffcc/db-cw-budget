class BalanceService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_balances(self):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, expense_sum, income_sum, net_profit, balance_date FROM balances")
            balances = cursor.fetchall()
            return [{'id': row[0], 'expense_sum': row[1], 'income_sum': row[2], 'net_profit': row[3],
                     'balance_date': row[4]} for row in balances]

    def generate_balances(self):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT generate_balances_without_triggers()")
            self.db_manager.conn.commit()

    def unbalance_balances(self):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT unbalance_operations()")
            self.db_manager.conn.commit()