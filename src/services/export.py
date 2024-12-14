import pandas as pd

class ExportService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def fetch_articles(self):
        query = "SELECT name AS article_name FROM articles"
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            articles = cursor.fetchall()
            return pd.DataFrame(articles, columns=columns)

    def fetch_operations(self):
        query = """
            SELECT
                ROW_NUMBER() OVER() AS num,
                operation_date,
                income_amount,
                expense_amount,
                (SELECT name FROM articles WHERE articles.id = operations.article_id) AS article_name
            FROM operations
        """
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            operations = cursor.fetchall()
            return pd.DataFrame(operations, columns=columns)

    def fetch_balances(self):
        query = """
            SELECT
                ROW_NUMBER() OVER() AS num,
                expense_sum,
                income_sum,
                net_profit,
                balance_date
            FROM balances
        """
        with self.db_manager.get_cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            balances = cursor.fetchall()
            return pd.DataFrame(balances, columns=columns)

    def export_to_excel(self, file_name):
        articles_df = self.fetch_articles()
        operations_df = self.fetch_operations()
        balances_df = self.fetch_balances()

        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            articles_df.to_excel(writer, sheet_name='Статьи', index=False)
            operations_df.to_excel(writer, sheet_name='Операции', index=False)
            balances_df.to_excel(writer, sheet_name='Балансы', index=False)
