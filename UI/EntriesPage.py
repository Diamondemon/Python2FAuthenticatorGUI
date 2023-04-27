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
        self.update_entries_period()
        self.display_entries()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_bar)
        self.timer.setInterval(100)

        self.progress_bar_behaviour()

    def update_entries_period(self):
        self.entries_period = 0

        for entry in self.repo.get_vault().entries:
            if (self.entries_period != 0 and self.entries_period != entry.period and entry.period != 0) \
                    or self.entries_period == -1:
                self.entries_period = -1
            else:
                self.entries_period = max(entry.period, self.entries_period)

    @Slot()
    def display_entries(self):
        while self.vertical_layout.itemAt(0):
            item = self.vertical_layout.itemAt(0)
            item.widget().deleteLater()
            self.vertical_layout.removeWidget(item.widget())

        for entry in self.repo.get_vault().entries:
            widget = EntryWidget(self.ui.content, entry)
            widget.delete_signal.connect(self.remove_entry)
            self.vertical_layout.addWidget(widget)

    @Slot(EntryWidget)
    def remove_entry(self, widget: EntryWidget):
        self.repo.get_vault().entries.remove(widget.entry)
        widget.deleteLater()
        self.vertical_layout.removeWidget(widget)

        self.update_entries_period()
        self.progress_bar_behaviour()
        self.save_repo()

    @Slot(VaultEntry)
    def add_entry(self, new_entry: VaultEntry):
        self.repo.get_vault().entries.append(new_entry)
        widget = EntryWidget(self.ui.content, new_entry)
        widget.delete_signal.connect(self.remove_entry)
        self.vertical_layout.addWidget(widget)
        self.save_repo()
        self.update_entries_period()
        self.progress_bar_behaviour()

    def save_repo(self):
        self.repo.save()

    @Slot()
    def update_bar(self):
        self.ui.progress_bar.setValue(int((time.time() % self.entries_period)/self.entries_period *
                                          self.ui.progress_bar.maximum()))
        self.ui.progress_bar.update()

    def progress_bar_behaviour(self):
        self.timer.stop()
        if self.entries_period != -1 and self.entries_period != 0:
            self.timer.start()
            self.ui.progress_bar.show()
        else:
            self.ui.progress_bar.hide()
