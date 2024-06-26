from PySide6.QtCore import QCoreApplication, Slot, SIGNAL
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QLineEdit, QWidget

from UI.QrDialog import QrDialog
from UI.UrlDialog import UrlDialog
from UI.ui_AddDialog import Ui_AddDialog
from utils.OtpInfo import OtpInfo
from utils.TotpInfo import TotpInfo
from utils.VaultEntry import VaultEntry


class AddDialog(QDialog):
    """
    Dialog to add or edit an entry.

    Provides fields to input all the information needed to create a VaultEntry and an option to load an entry
    from a qr code or an url.
    """

    def __init__(self, master: QWidget = None, entry: VaultEntry | None = None):
        """
        Initializes the dialog.
        :param master: master widget
        :param entry:  entry to edit, if any
        """
        super().__init__(master)
        self.ui = Ui_AddDialog()
        self.ui.setupUi(self)
        self.ui.secret_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.ui.group_combo.insertItems(-1, [QCoreApplication.translate(b"AddDialog", b"Aucun groupe", None)])
        self.ui.hash_combo.insertItems(-1, ["SHA1", "SHA256", "SHA512"])
        self.ui.type_combo.insertItems(-1, ["TOTP"])  # "HOTP"
        self.ui.period_edit.setValidator(QIntValidator(bottom=0))
        self.ui.use_edit.setValidator(QIntValidator(bottom=0))
        self.ui.digits_edit.setValidator(QIntValidator(bottom=0))
        self.ui.qr_button.connect(SIGNAL(b"clicked()"), self.display_qr)
        self.ui.url_button.connect(SIGNAL(b"clicked()"), self.display_url)

        self.entry = entry

        if self.entry is not None:
            self.load_entry()

    def load_entry(self):
        """
        Loads the entry into the different fields.
        :return: None
        """
        self.ui.name_edit.setText(self.entry.name)
        self.ui.issuer_edit.setText(self.entry.issuer)
        self.ui.note_edit.setText(self.entry.note)
        self.ui.secret_edit.setText(self.entry.secret)

        index = self.ui.type_combo.findData(self.entry.info_type)
        if index != -1:
            self.ui.type_combo.setCurrentIndex(index)

        index = self.ui.hash_combo.findData(self.entry.hash)
        if index != -1:
            self.ui.hash_combo.setCurrentIndex(index)

        self.ui.period_edit.setText(str(self.entry.period))
        self.ui.digits_edit.setText(str(self.entry.digits))
        self.ui.use_edit.setText(str(self.entry.uses))

    @Slot()
    def display_qr(self):
        """
        Opens the dialog to load the entry from a qr code, then loads it.
        :return: None
        """
        dlg = QrDialog(self)
        button = dlg.exec()
        if button == 1:
            try:
                entry = VaultEntry.from_url(dlg.resolved_url)
            except ValueError as e:
                print(f"Loading entry from qr code failed: {e}")
                return
            self.entry = entry
            self.load_entry()

    @Slot()
    def display_url(self):
        """
        Opens the dialog to load the entry from an url, then loads it.
        :return: None
        """
        dlg = UrlDialog(self)
        button = dlg.exec()
        if button == 1:
            url = dlg.ui.url_edit.text()
            try:
                entry = VaultEntry.from_url(url)
            except ValueError as e:
                print(f"Loading entry from url failed: {e}")
                return
            self.entry = entry
            self.load_entry()

    def recompute_entry(self):
        """
        Recomputes the entry according to all the input fields
        :return: recomputed entry
        """
        if self.entry is None:
            self.entry = VaultEntry()
        self.entry.set_base(self.ui.name_edit.text(), self.ui.issuer_edit.text(), self.ui.group_combo.currentText())
        self.entry.note = self.ui.note_edit.text()

        info_json = {
            "secret": self.ui.secret_edit.text(),
            "algo": self.ui.hash_combo.currentText(),
            "digits": int(self.ui.digits_edit.text())
        }

        if self.ui.type_combo.currentText() == "TOTP":
            otp_id = TotpInfo.ID
            info_json["period"] = int(self.ui.period_edit.text())
        else:
            raise NotImplementedError("Types other than TOTP are not implemented.")

        self.entry.set_info(OtpInfo.from_json(otp_id, info_json))
        self.entry.set_uses(int(self.ui.use_edit.text()))

        return self.entry
