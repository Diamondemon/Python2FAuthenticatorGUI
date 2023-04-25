from PySide6.QtWidgets import QDialog

from UI.ui_UrlDialog import Ui_UrlDialog


class UrlDialog(QDialog):
    """Dialog used to scan an url to load an OTP entry"""

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_UrlDialog()
        self.ui.setupUi(self)
