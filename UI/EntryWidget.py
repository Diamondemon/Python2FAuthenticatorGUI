import qrcode
from PIL.ImageQt import ImageQt
from PySide6 import QtCore
from PySide6.QtCore import Slot, SIGNAL, Signal, QSize
from PySide6.QtGui import Qt, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QLabel

from UI.AddDialog import AddDialog
from UI.QrDisplay import QrDisplay
from UI.ui_EntryWidget import Ui_EntryWidget
from utils.VaultEntry import VaultEntry


class EntryWidget(QWidget):
    delete_signal = Signal(QWidget)

    def __init__(self, master, entry: VaultEntry):
        super().__init__(master)
        self.ui = Ui_EntryWidget()
        self.ui.setupUi(self)
        self.ui.host_label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setFixedHeight(120)
        self.ui.pushButton.connect(SIGNAL("clicked()"), self.edit_entry)
        self.setup_actions()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.entry = entry

        self.setup_host_name()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh_otp)
        self.schedule_timers()

    def setup_actions(self):
        icon = QIcon()
        icon_theme_name = u"document-send"
        if QIcon.hasThemeIcon(icon_theme_name):
            icon = QIcon.fromTheme(icon_theme_name)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.addAction(icon, self.tr("Envoyer en QR Code"), self.to_qr_code)

        icon_theme_name = u"edit"
        if QIcon.hasThemeIcon(icon_theme_name):
            icon = QIcon.fromTheme(icon_theme_name)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.addAction(icon, self.tr("Modifier"), self.edit_entry)

        icon_theme_name = u"edit-delete"
        if QIcon.hasThemeIcon(icon_theme_name):
            icon = QIcon.fromTheme(icon_theme_name)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.addAction(icon, self.tr("Supprimer"), self.launch_delete)

    @Slot()
    def launch_delete(self):
        button = QMessageBox(QMessageBox.Icon.Warning, self.tr("Supprimer l'entrée"),
                    self.tr("Cette action est irreversible, êtes-vous sûr?"),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                    self
                 ).exec()

        if button == QMessageBox.StandardButton.Yes:
            self.delete_signal.emit(self)

    def schedule_timers(self):
        self.timer.stop()
        self.refresh_otp()
        secs = self.entry.period
        self.timer.setInterval(secs * 1000)

        # TODO fix definition of interval
        d1 = QtCore.QDateTime.currentDateTimeUtc()
        d2 = QtCore.QDateTime(d1)
        t1 = d1.time()
        d2.setTime(QtCore.QTime(t1.hour(), t1.minute(), 30))
        if t1.second() >= secs:
            d2 = d2.addSecs(secs)
        QtCore.QTimer.singleShot(d1.msecsTo(d2), self.start_main_timer)

    def start_main_timer(self):
        self.timer.timeout.emit()
        self.timer.start()

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
        button = dial.exec()
        if button == 1:
            self.entry = dial.recompute_entry()
            self.setup_host_name()
            self.schedule_timers()

    @Slot()
    def to_qr_code(self):
        url = self.entry.to_url()

        dial = QrDisplay(self, url)
        dial.exec()

