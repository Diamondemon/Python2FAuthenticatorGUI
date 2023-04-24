from PySide6 import QtCore
from PySide6.QtCore import Slot, SIGNAL
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget

from UI.AddDialog import AddDialog
from UI.ui_EntryWidget import Ui_EntryWidget
from utils.VaultEntry import VaultEntry


class EntryWidget(QWidget):

    def __init__(self, master, entry: VaultEntry):
        super().__init__(master)
        self.ui = Ui_EntryWidget()
        self.ui.setupUi(self)
        self.ui.host_label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setFixedHeight(120)
        self.ui.pushButton.connect(SIGNAL("clicked()"), self.edit_entry)
        self.entry = entry

        self.setup_host_name()
        self.refresh_otp()
        secs = self.entry.period
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh_otp)
        self.timer.setInterval(secs * 1000)

        def start_point():
            self.timer.timeout.emit()
            self.timer.start()

        d1 = QtCore.QDateTime.currentDateTimeUtc()
        d2 = QtCore.QDateTime(d1)
        t1 = d1.time()
        d2.setTime(QtCore.QTime(t1.hour(), t1.minute(), 30))
        if t1.second() > secs:
            d2 = d2.addSecs(30)
        QtCore.QTimer.singleShot(d1.msecsTo(d2), start_point)

    @Slot()
    def refresh_otp(self):
        otp = self.entry.get_otp()
        self.ui.code_label.setText(otp[:3] + " " + otp[3:])

    def setup_host_name(self):
        host = ""
        if self.entry.issuer:
            host += f"**{self.entry.issuer}**"
        if self.entry.issuer and self.entry.name:
            host += " ("
        if self.entry.name:
            host += self.entry.name
        if self.entry.issuer and self.entry.name:
            host += ")"
        self.ui.host_label.setText(host)

    @Slot()
    def edit_entry(self):
        dial = AddDialog(self, self.entry)
        dial.open()
