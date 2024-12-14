from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QHBoxLayout, QMessageBox)
from src.services.operation import OperationService

class OperationsWindow(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.user = user
        self.operation_service = OperationService(db_manager)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Operations')
        self.setGeometry(100, 100, 1000, 600)

        self.table_widget = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        self.update_table_button = QPushButton('Refresh Table', self)
        self.update_table_button.clicked.connect(self.load_operations)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.update_table_button)

        if self.user['role'] == 'admin':
            self.add_expense_input = QLineEdit(self)
            self.add_expense_input.setPlaceholderText('Expense Amount')
            self.add_income_input = QLineEdit(self)
            self.add_income_input.setPlaceholderText('Income Amount')
            self.add_date_input = QLineEdit(self)
            self.add_date_input.setPlaceholderText('Date (YYYY-MM-DD)')
            self.add_article_id_input = QLineEdit(self)
            self.add_article_id_input.setPlaceholderText('Article ID')

            self.add_operation_button = QPushButton('Add Operation', self)
            self.add_operation_button.clicked.connect(self.add_operation)

            self.update_operation_button = QPushButton('Update Selected Operation', self)
            self.update_operation_button.clicked.connect(self.update_operation)

            self.delete_operation_button = QPushButton('Delete Selected Operation', self)
            self.delete_operation_button.clicked.connect(self.delete_operation)

            input_layout.addWidget(self.add_expense_input)
            input_layout.addWidget(self.add_income_input)
            input_layout.addWidget(self.add_date_input)
            input_layout.addWidget(self.add_article_id_input)
            input_layout.addWidget(self.add_operation_button)
            input_layout.addWidget(self.update_operation_button)
            input_layout.addWidget(self.delete_operation_button)

        layout.addLayout(input_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_operations()

    def load_operations(self):
        try:
            operations = self.operation_service.get_all_operations()
            self.table_widget.setRowCount(len(operations))
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(['ID', 'Expense', 'Income', 'Date', 'Article ID', 'Balance ID'])

            for row_idx, operation in enumerate(operations):
                self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(operation['id'])))
                self.table_widget.setItem(row_idx, 1, QTableWidgetItem(str(operation['expense_amount'])))
                self.table_widget.setItem(row_idx, 2, QTableWidgetItem(str(operation['income_amount'])))
                self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(operation['operation_date'])))
                self.table_widget.setItem(row_idx, 4, QTableWidgetItem(str(operation['article_id'])))
                self.table_widget.setItem(row_idx, 5, QTableWidgetItem(str(operation['balance_id'])))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error loading operations: {e}')

    def add_operation(self):
        expense_amount = self.add_expense_input.text()
        income_amount = self.add_income_input.text()
        operation_date = self.add_date_input.text()
        article_id = self.add_article_id_input.text()
        if expense_amount and income_amount and operation_date and article_id:
            try:
                self.operation_service.add_operation(expense_amount, income_amount, operation_date, article_id)
                self.load_operations()
                self.add_expense_input.clear()
                self.add_income_input.clear()
                self.add_date_input.clear()
                self.add_article_id_input.clear()
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to add operation: {e}')
        else:
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled')

    def update_operation(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'No operation selected for update')
            return

        operation_id = int(selected_items[0].text())
        expense_amount = selected_items[1].text()
        income_amount = selected_items[2].text()
        operation_date = selected_items[3].text()
        article_id = selected_items[4].text()

        new_expense_amount = self.add_expense_input.text() or expense_amount
        new_income_amount = self.add_income_input.text() or income_amount
        new_operation_date = self.add_date_input.text() or operation_date
        new_article_id = self.add_article_id_input.text() or article_id

        try:
            self.operation_service.update_operation(operation_id, new_expense_amount, new_income_amount, new_operation_date, new_article_id)
            self.load_operations()
            self.add_expense_input.clear()
            self.add_income_input.clear()
            self.add_date_input.clear()
            self.add_article_id_input.clear()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to update operation: {e}')

    def delete_operation(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'No operation selected for delete')
            return

        operation_id = int(selected_items[0].text())

        try:
            self.operation_service.delete_operation(operation_id)
            self.load_operations()
            self.add_expense_input.clear()
            self.add_income_input.clear()
            self.add_date_input.clear()
            self.add_article_id_input.clear()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete operation: {e}')