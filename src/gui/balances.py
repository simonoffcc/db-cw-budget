from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QMessageBox)
from src.services.balance import BalanceService

class BalancesWindow(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.user = user
        self.balance_service = BalanceService(db_manager)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Balance')
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        self.update_table_button = QPushButton('Refresh Table', self)
        self.update_table_button.clicked.connect(self.load_balances)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_table_button)

        if self.user['role'] == 'admin':
            self.generate_balances_button = QPushButton('Generate Balances', self)
            self.generate_balances_button.clicked.connect(self.generate_balances)

            self.unbalance_balance_button = QPushButton('Disband Balances', self)
            self.unbalance_balance_button.clicked.connect(self.unbalance_balances)

            button_layout.addWidget(self.generate_balances_button)
            button_layout.addWidget(self.unbalance_balance_button)

        layout.addLayout(button_layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_balances()

    def load_balances(self):
        try:
            balances = self.balance_service.get_all_balances()
            self.table_widget.setRowCount(len(balances))
            self.table_widget.setColumnCount(5)
            self.table_widget.setHorizontalHeaderLabels(['ID', 'Expense', 'Income', 'Net Profit', 'Date'])

            for row_idx, balance in enumerate(balances):
                self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(balance['id'])))
                self.table_widget.setItem(row_idx, 1, QTableWidgetItem(str(balance['expense_sum'])))
                self.table_widget.setItem(row_idx, 2, QTableWidgetItem(str(balance['income_sum'])))
                self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(balance['net_profit'])))
                self.table_widget.setItem(row_idx, 4, QTableWidgetItem(str(balance['balance_date'])))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error loading operations: {e}')

    def generate_balances(self):
        try:
            self.balance_service.generate_balances()
            self.load_balances()
            QMessageBox.information(self, 'Success', 'Balances generated successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to generate balances: {str(e)}')

    def unbalance_balances(self):
        try:
            self.balance_service.unbalance_balances()
            self.load_balances()
            QMessageBox.information(self, 'Success', f'All balances has been unbalanced.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to unbalance: {str(e)}')