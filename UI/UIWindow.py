from PySide6.QtCore import Slot, SIGNAL
from PySide6.QtWidgets import (QMainWindow)

from UI.UIMenuBar import UIMenuBar


class UIWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("2F Authenticator")

        self.setMenuBar(UIMenuBar)
