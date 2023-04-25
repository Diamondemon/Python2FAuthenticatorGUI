from PySide6.QtCore import Slot, SIGNAL
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QGridLayout, QLabel

from UI.ui_AuthPage import Ui_AuthPage


class AuthPage(QWidget):

    def __init__(self, master=None):
        super(AuthPage, self).__init__(master)
        self.ui = Ui_AuthPage()
        self.ui.setupUi(self)

        self.pass_entry = self.ui.pass_entry
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)

        self.connect(self.ui.view_pass, SIGNAL("pressed()"), self.display_pass)
        self.connect(self.ui.view_pass, SIGNAL("released()"), self.hide_pass)

        self.validateEntry = self.ui.validate_entry
        self.ui.wrong_label.hide()

    @Slot()
    def display_pass(self):
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Normal)

    @Slot()
    def hide_pass(self):
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def wrong_pass(self):
        self.ui.wrong_label.show()

    def good_pass(self):
        self.ui.wrong_label.hide()
        self.ui.pass_entry.setText("")
