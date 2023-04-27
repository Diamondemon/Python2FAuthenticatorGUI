from PySide6.QtCore import SIGNAL, Slot
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit

from UI.ui_NewAuthDialog import Ui_NewAuthDialog
from utils import CryptoUtils
from utils.SCryptParams import SCryptParams
from utils.Slots.PasswordSlot import PasswordSlot
from utils.VaultFileCredentials import VaultFileCredentials


class NewAuthDialog(QDialog):

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_NewAuthDialog()
        self.ui.setupUi(self)
        self.ui.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.connect(self.ui.type_combo, SIGNAL("currentIndexChanged(int)"), self.index_changed)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).connect(SIGNAL("clicked()"), self.accept)

        self.connect(self.ui.see_button, SIGNAL("pressed()"), self.display_pass)
        self.connect(self.ui.see_button, SIGNAL("released()"), self.hide_pass)


    @Slot(int)
    def index_changed(self, index: int):
        if index == 0:
            self.ui.password_label.hide()
            self.ui.password_edit.hide()
            self.ui.confirm_label.hide()
            self.ui.confirm_edit.hide()
            self.ui.see_button.hide()
            return

        if index == 1:
            self.ui.password_label.show()
            self.ui.password_edit.show()
            self.ui.confirm_label.show()
            self.ui.confirm_edit.show()
            self.ui.see_button.show()
            return

    @Slot()
    def display_pass(self):
        self.ui.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        self.ui.confirm_edit.setEchoMode(QLineEdit.EchoMode.Normal)

    @Slot()
    def hide_pass(self):
        self.ui.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def compute_credentials(self):
        if self.ui.type_combo.currentIndex() == 1:
            creds = VaultFileCredentials()
            passw = self.ui.password_edit.text()
            conf_passw = self.ui.confirm_edit.text()
            if passw != conf_passw:
                return

            slot = PasswordSlot()
            salt = CryptoUtils.generate_salt()
            scrypt_params = SCryptParams(
                CryptoUtils.CRYPTO_SCRYPT_N,
                CryptoUtils.CRYPTO_SCRYPT_r,
                CryptoUtils.CRYPTO_SCRYPT_p,
                salt
            )
            key = slot.derive_key(passw, scrypt_params)
            slot.set_key(creds.master_key, slot.create_encrypt_cipher(key))
            creds.slots.append(slot)

            return creds

        return None

