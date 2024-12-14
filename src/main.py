import sys
from PyQt5.QtWidgets import QApplication
from src.gui.login import LoginWindow
from src.database.db_manager import DBManager

def main():
    db_manager = DBManager(config_file='./src/config.ini')
    app = QApplication(sys.argv)
    login_window = LoginWindow(db_manager)
    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(e)
