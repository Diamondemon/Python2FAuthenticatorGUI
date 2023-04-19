from PySide6.QtCore import Slot, SIGNAL
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QGridLayout, QLabel

from utils.VaultFile import VaultFile
from UI.ui_AuthPage import Ui_AuthPage

class AuthPage(QWidget):

    def __init__(self, master=None):
        super(AuthPage, self).__init__(master)
        self.ui = Ui_AuthPage()
        self.ui.setupUi(self)

        self.passEntry = self.ui.pass_entry
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)
        #self.grid.addWidget(self.passEntry, 0, 0, 1, 2)

        #self.viewPass = QPushButton(self.tr("Voir"))
        self.connect(self.ui.view_pass, SIGNAL("pressed()"), self.displayPass)
        self.connect(self.ui.view_pass, SIGNAL("released()"), self.hidePass)
        #self.grid.addWidget(self.viewPass, 0, 2)

        self.validateEntry = self.ui.validate_entry
        #self.validateEntry: QPushButton = QPushButton(self.tr("Déverrouiller"))
        #self.grid.addWidget(self.validateEntry, 1, 1)

        #self.wrong_label = QLabel(self.tr("Impossible d'ouvrir le coffre-fort, mauvais mot de passe."))
        #self.grid.addWidget(self.wrong_label, 2, 0, 1, 3)
        self.ui.wrong_label.hide()

    @Slot()
    def displayPass(self):
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Normal)

    @Slot()
    def hidePass(self):
        self.ui.pass_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def wrongPass(self):
        self.ui.wrong_label.show()

    def goodPass(self):
        self.ui.wrong_label.hide()
