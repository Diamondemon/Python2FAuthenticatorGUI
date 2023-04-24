from PySide6.QtWidgets import QDialog

from UI.ui_QrDialog import Ui_QrDialog


class QrDialog(QDialog):

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_QrDialog()
        self.ui.setupUi(self)
        self.resolved_url = ""

