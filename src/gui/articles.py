from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QHBoxLayout, QMessageBox)
from src.services.article import ArticleService

class ArticlesWindow(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.user = user
        self.article_service = ArticleService(db_manager)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Articles')
        self.setGeometry(100, 100, 600, 600)

        self.table_widget = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        self.update_table_button = QPushButton('Refresh Table', self)
        self.update_table_button.clicked.connect(self.load_articles)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.update_table_button)

        if self.user['role'] == 'admin':
            self.add_name_input = QLineEdit(self)
            self.add_name_input.setPlaceholderText('Article Name')

            self.add_article_button = QPushButton('Add Article', self)
            self.add_article_button.clicked.connect(self.add_article)

            self.update_article_button = QPushButton('Update Selected Article', self)
            self.update_article_button.clicked.connect(self.update_article)

            self.delete_article_button = QPushButton('Delete Selected Article', self)
            self.delete_article_button.clicked.connect(self.delete_article)

            input_layout.addWidget(self.add_name_input)
            input_layout.addWidget(self.add_article_button)
            input_layout.addWidget(self.update_article_button)
            input_layout.addWidget(self.delete_article_button)

        layout.addLayout(input_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_articles()

    def load_articles(self):
        try:
            articles = self.article_service.get_all_articles()
            self.table_widget.setRowCount(len(articles))
            self.table_widget.setColumnCount(2)
            self.table_widget.setHorizontalHeaderLabels(['ID', 'Name'])

            for row_idx, article in enumerate(articles):
                self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(article['id'])))
                self.table_widget.setItem(row_idx, 1, QTableWidgetItem(article['name']))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error loading articles: {e}')

    def add_article(self):
        name = self.add_name_input.text()
        if name:
            try:
                self.article_service.add_article(name)
                self.load_articles()
                self.add_name_input.clear()
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to add article: {e}')
        else:
            QMessageBox.warning(self, 'Input Error', 'Article name cannot be empty')

    def update_article(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'No article selected for update')
            return

        article_id = int(selected_items[0].text())
        new_name = self.add_name_input.text()

        if not new_name:
            QMessageBox.warning(self, 'Input Error', 'Article name cannot be empty')
            return

        try:
            self.article_service.update_article(article_id, new_name)
            self.load_articles()
            self.add_name_input.clear()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to update article: {e}')

    def delete_article(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'No article selected for delete')
            return

        article_id = int(selected_items[0].text())

        try:
            self.article_service.delete_article(article_id)
            self.load_articles()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete article: {e}')