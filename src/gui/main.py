from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox
from src.gui.balances import BalancesWindow
from src.gui.operations import OperationsWindow
from src.gui.articles import ArticlesWindow
from src.services.export import ExportService


class MainWindow(QMainWindow):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.user = user
        self.articles_window = None
        self.operations_window = None
        self.balance_window = None
        self.export_service = ExportService(db_manager)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Home Budget Manager')
        self.setGeometry(700, 200, 300, 400)

        menubar = self.menuBar()

        operations_menu = menubar.addMenu('Operations')
        articles_menu = menubar.addMenu('Articles')
        balance_menu = menubar.addMenu('Balance')
        report_menu = menubar.addMenu('Report')
        user_menu = menubar.addMenu('User')

        view_operations_action = QAction('View Operations', self)
        view_operations_action.triggered.connect(self.show_operations_window)
        operations_menu.addAction(view_operations_action)

        manage_articles_action = QAction('Manage Articles', self)
        manage_articles_action.triggered.connect(self.show_articles_window)
        articles_menu.addAction(manage_articles_action)

        view_balance_action = QAction('View Balance', self)
        view_balance_action.triggered.connect(self.show_balance_window)
        balance_menu.addAction(view_balance_action)

        export_tables_action = QAction('Export tables', self)
        export_tables_action.triggered.connect(self.export_tables)
        report_menu.addAction(export_tables_action)

        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        user_menu.addAction(logout_action)

    def show_operations_window(self):
        if self.operations_window is None:
            self.operations_window = OperationsWindow(self.db_manager, self.user)
        self.operations_window.show()

    def show_articles_window(self):
        if self.articles_window is None:
            self.articles_window = ArticlesWindow(self.db_manager, self.user)
        self.articles_window.show()

    def show_balance_window(self):
        if self.balance_window is None:
            self.balance_window = BalancesWindow(self.db_manager, self.user)
        self.balance_window.show()

    def export_tables(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel file", "", "Excel Files (*.xlsx)", options=options)
        if file_name:
            try:
                self.export_service.export_to_excel(file_name)
                QMessageBox.information(self, 'Success', 'Tables exported successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error exporting tables: {e}')


    def logout(self):
        self.close()