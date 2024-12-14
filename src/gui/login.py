from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox
from src.gui.main import MainWindow
from src.services.user import UserService

class LoginWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.user_service = UserService(db_manager)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(700, 200, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            user = self.user_service.authenticate(username, password)
            if user:
                self.main_window = MainWindow(self.db_manager, user)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid username or password')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to login: {e}')
