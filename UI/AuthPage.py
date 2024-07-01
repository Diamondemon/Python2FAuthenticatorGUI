from PySide6.QtCore import Slot, SIGNAL, Signal
from PySide6.QtWidgets import QLineEdit, QWidget

from UI.ui_AuthPage import Ui_AuthPage


class AuthPage(QWidget):
    """
    First page of the application, used to authenticate the user to get access to the previously created vault.
    """
    password_entered_signal = Signal()

    def __init__(self, master: QWidget = None):
        super(AuthPage, self).__init__(master)
        self.ui = Ui_AuthPage()
        self.ui.setupUi(self)

        self.pass_entry = self.ui.pass_entry
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.pass_entry.returnPressed.connect(self.password_entered_signal.emit)
        self.ui.validate_entry.clicked.connect(self.password_entered_signal.emit)
        self.ui.wrong_label.hide()

        self.ui.view_pass.pressed.connect(self.display_pass)
        self.ui.view_pass.released.connect(self.hide_pass)

    @Slot()
    def display_pass(self):
        """
        Display the password in plain text
        :return: None
        """
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Normal)

    @Slot()
    def hide_pass(self):
        """
        Hide the password
        :return: None
        """
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def wrong_pass(self):
        """
        Display the "wrong password" label
        :return: None
        """
        self.ui.wrong_label.show()

    def good_pass(self):
        """
        Hide the "wrong password" label and clear the password entry
        :return: None
        """
        self.ui.wrong_label.hide()
        self.ui.pass_entry.setText("")
