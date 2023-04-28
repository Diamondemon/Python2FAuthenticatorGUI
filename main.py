from sys import argv, exit
from PySide6.QtWidgets import QApplication
from UI.UIWindow import UIWindow

if __name__ == '__main__':
    app = QApplication(argv)
    window = UIWindow()
    window.show()
    exit(app.exec())
