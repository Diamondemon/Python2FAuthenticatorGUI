from PySide6.QtCore import Slot, SIGNAL, QKeyCombination, QSize, Qt
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import (QMainWindow, QFileDialog)
from os import path

from UI.EntriesPage import EntriesPage
from UI.EntryWidget import EntryWidget
from UI.UIMenuBar import UIMenuBar

from utils.VaultManager import VaultManager
from utils.VaultRepository import VaultRepository
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials
from utils.Slots.PasswordSlot import PasswordSlot
from UI.AuthPage import AuthPage


class UIWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("2F Authenticator")
        self.setMinimumSize(QSize(720, 405))

        self.manager = VaultManager()
        self.vaultFile: VaultFile | None = None
        self.repo: VaultRepository | None = None

        self.uiMenuBar = UIMenuBar(self)
        self.uiMenuBar.addFileAction(self.tr("Importer"), self.import_file)
        self.uiMenuBar.addFileAction(self.tr("Exporter"), self.export)
        self.uiMenuBar.addFileAction(self.tr("Quitter"), self.quit_window, QKeySequence(self.tr("Ctrl+Q")))
        self.setMenuBar(self.uiMenuBar)

        self.authPage = AuthPage()
        self.connect(self.authPage.validateEntry, SIGNAL("clicked()"), self.decrypt_task)

    @Slot()
    def export(self):
        pass

    @Slot()
    def import_file(self):
        filename = QFileDialog.getOpenFileName(self, self.tr("Sélectionnez un fichier de coffre"),
                                               path.dirname(__file__), self.tr("Fichiers json (*.json)"))
        if not filename[0]:
            return
        self.vaultFile = VaultRepository.from_file_import(filename[0])
        self.setCentralWidget(self.authPage)

    @Slot()
    def decrypt_task(self):
        passw = self.authPage.passEntry.text()
        for slot in self.vaultFile.header.slots:
            if type(self.vaultFile.header.slots[slot]) == PasswordSlot:
                passSlot: PasswordSlot = self.vaultFile.header.slots[slot]
                key = passSlot.derive_key(passw)
                try:
                    masterKey = passSlot.get_key(passSlot.create_decrypt_cipher(key))
                except ValueError:
                    self.authPage.wrongPass()
                    return
                self.authPage.goodPass()
                creds = VaultFileCredentials(masterKey, self.vaultFile.header.slots)
                self.repo = VaultRepository.from_vault_file(self.vaultFile, creds)
                self.authPage = self.takeCentralWidget()
                self.setCentralWidget(EntriesPage(self, self.repo))

    @Slot()
    def quit_window(self):
        self.close()
