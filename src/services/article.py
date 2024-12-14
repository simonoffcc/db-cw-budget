class ArticleService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_articles(self):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("SELECT id, name FROM articles")
            articles = cursor.fetchall()
            return [{'id': row[0], 'name': row[1]} for row in articles]

    def add_article(self, name):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("INSERT INTO articles (name) VALUES (%s)", (name,))
            self.db_manager.conn.commit()

    def update_article(self, article_id, new_name):
        print(f'ArticleService: updating article id {article_id} with new name {new_name}')
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("UPDATE articles SET name = %s WHERE id = %s", (new_name, article_id))
            self.db_manager.conn.commit()

    def delete_article(self, article_id):
        with self.db_manager.get_cursor() as cursor:
            cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
            self.db_manager.conn.commit()
