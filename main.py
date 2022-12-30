from sys import argv
from PySide6.QtWidgets import QApplication
from UI.UIWindow import UIWindow

if __name__ == '__main__':
    app = QApplication(argv)
    window = UIWindow()
    window.show()
    exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
