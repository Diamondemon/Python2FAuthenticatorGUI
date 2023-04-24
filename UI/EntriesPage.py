import time

from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from UI.EntryWidget import EntryWidget
from UI.ui_EntriesPage import Ui_EntriesPage
from utils.Vault import Vault
from utils.VaultEntry import VaultEntry
from utils.VaultRepository import VaultRepository


class EntriesPage(QWidget):

    def __init__(self, master, repo: VaultRepository = None):
        super().__init__(master)
        self.ui = Ui_EntriesPage()
        self.ui.setupUi(self)
        self.entries_period = 0
        self.vertical_layout = QVBoxLayout(self.ui.content)
        self.ui.content.setLayout(self.vertical_layout)

        self.repo = repo
        self.display_entries()

        if self.entries_period != -1:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_bar)
            self.timer.setInterval(100)
            self.timer.start()
        else:
            self.ui.progress_bar.hide()

    def display_entries(self):
        while self.vertical_layout.children():
            self.vertical_layout.removeItem(0)
        for entry in self.repo.get_vault().entries:
            self.vertical_layout.addWidget(EntryWidget(self.ui.content, entry))
            if (self.entries_period != 0 and self.entries_period != entry.period and entry.period != 0) \
                    or self.entries_period == -1:
                self.entries_period = -1
            else:
                self.entries_period = max(entry.period, self.entries_period)

    @Slot()
    def update_bar(self):
        self.ui.progress_bar.setValue(int((time.time() % self.entries_period)/self.entries_period *
                                          self.ui.progress_bar.maximum()))
        self.ui.progress_bar.update()
