class OperationService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_operations(self):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, expense_amount, income_amount, operation_date, article_id, balance_id FROM operations")
            operations = cursor.fetchall()
            return [{'id': row[0], 'expense_amount': row[1], 'income_amount': row[2], 'operation_date': row[3],
                     'article_id': row[4], 'balance_id': row[5]} for row in operations]

    def add_operation(self, expense_amount, income_amount, operation_date, article_id):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("INSERT INTO operations (expense_amount, income_amount, operation_date, article_id) VALUES (%s, %s, %s, %s)",
                           (expense_amount, income_amount, operation_date, article_id))
            self.db_manager.conn.commit()

    def update_operation(self, operation_id, expense_amount, income_amount, operation_date, article_id):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("UPDATE operations SET expense_amount = %s, income_amount = %s, operation_date = %s, article_id = %s WHERE id = %s",
                           (expense_amount, income_amount, operation_date, article_id, operation_id))
            self.db_manager.conn.commit()

    def delete_operation(self, operation_id):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("DELETE FROM operations WHERE id = %s",
                           (operation_id,))
            self.db_manager.conn.commit()