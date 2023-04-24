from PySide6.QtWidgets import QDialog

from UI.ui_UrlDialog import Ui_UrlDialog


class UrlDialog(QDialog):

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_UrlDialog()
        self.ui.setupUi(self)

