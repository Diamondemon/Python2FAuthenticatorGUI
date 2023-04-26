from PySide6.QtCore import Signal, SIGNAL
from PySide6.QtWidgets import QWidget

from UI.ui_FirstUseWidget import Ui_FirstUseWidget


class FirstUseWidget(QWidget):
    new_signal = Signal()
    import_signal = Signal()

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_FirstUseWidget()
        self.ui.setupUi(self)
        self.ui.new_button.connect(SIGNAL("clicked()"), self.new_signal.emit)
        self.ui.import_button.connect(SIGNAL("clicked()"), self.import_signal.emit)
