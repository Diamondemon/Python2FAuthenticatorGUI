from PySide6.QtCore import Slot, SIGNAL, QKeyCombination, QSize, Qt, QMetaObject, Signal
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import (QMainWindow, QFileDialog, QWidget)
from os import path

from UI.AddDialog import AddDialog
from UI.EntriesPage import EntriesPage
from UI.EntryWidget import EntryWidget
from UI.FirstUseWidget import FirstUseWidget
from UI.UIMenuBar import UIMenuBar
from utils.VaultEntry import VaultEntry

from utils.VaultManager import VaultManager
from utils.VaultRepository import VaultRepository
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials
from utils.Slots.PasswordSlot import PasswordSlot
from UI.AuthPage import AuthPage


class UIWindow(QMainWindow):
    refresh_signal = Signal(VaultEntry)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("2F Authenticator")
        self.setMinimumSize(QSize(720, 405))

        self.manager = VaultManager()

        self.vaultFile: VaultFile | None = None
        self.refresh_connection: QMetaObject.Connection | None = None

        self.uiMenuBar = UIMenuBar(self)
        self.uiMenuBar.addFileAction(self.tr("Importer"), self.import_file)
        self.uiMenuBar.addFileAction(self.tr("Exporter"), self.export)
        self.uiMenuBar.addFileAction(self.tr("Quitter"), self.quit_window, QKeySequence(self.tr("Ctrl+Q")))
        self.uiMenuBar.addAction(self.tr("Verrouiller"), QKeySequence(self.tr("Ctrl+L")), self.lock_vault)
        self.uiMenuBar.addAction(self.tr("Ajouter"), QKeySequence(self.tr("Ctrl+A")), self.add_entry)
        self.setMenuBar(self.uiMenuBar)

        self.auth_page: AuthPage = AuthPage()
        self.connect(self.auth_page.validateEntry, SIGNAL("clicked()"), self.decrypt_task)

        try:
            self.manager.load_vault_file()
            self.setCentralWidget(self.auth_page)
        except FileNotFoundError:
            widget = FirstUseWidget(self)
            widget.new_signal.connect(self.create_blank_vault)
            widget.import_signal.connect(self.import_file)
            self.setCentralWidget(widget)

    @Slot()
    def export(self):
        # TODO
        pass

    @Slot()
    def import_file(self):
        filename = QFileDialog.getOpenFileName(self, self.tr("Sélectionnez un fichier de coffre"),
                                               path.dirname(__file__), self.tr("Fichiers json (*.json)"))
        if not filename[0]:
            return
        self.vaultFile = VaultRepository.from_file_import(filename[0])
        self.setCentralWidget(self.auth_page)

    @Slot()
    def create_blank_vault(self):
        # TODO
        raise NotImplementedError

    @Slot()
    def add_entry(self):
        if self.manager.is_vault_loaded():
            dial = AddDialog(self)
            button = dial.exec()
            if button == 1:
                self.refresh_signal.emit(dial.recompute_entry())

    @Slot()
    def decrypt_task(self):
        """
        Decrypts the content of the vault file.
        :return: None
        """
        passw = self.auth_page.pass_entry.text()

        if self.vaultFile is not None:
            try:
                creds = self.unlock_with_pass(self.vaultFile, passw)
            except ValueError:
                self.auth_page.wrong_pass()
                return

            self.auth_page.good_pass()
            self.manager.load_from(self.vaultFile, creds)
            self.manager.save()
            self.vaultFile = None

        else:
            try:
                creds = self.unlock_with_pass(self.manager.vault_file, passw)
            except ValueError:
                self.auth_page.wrong_pass()
                return

            self.auth_page.good_pass()
            self.manager.unlock(creds)

        # self.auth_page: AuthPage | QWidget =
        self.takeCentralWidget()
        entries_page = EntriesPage(self, self.manager.repo)
        self.refresh_connection = self.refresh_signal.connect(entries_page.add_entry)
        self.setCentralWidget(entries_page)

    @staticmethod
    def unlock_with_pass(vault_file: VaultFile, password: str) -> VaultFileCredentials:
        for slot in vault_file.header.slots:
            if type(vault_file.header.slots[slot]) == PasswordSlot:
                pass_slot: PasswordSlot | Slot = vault_file.header.slots[slot]
                key = pass_slot.derive_key(password)
                master_key = pass_slot.get_key(pass_slot.create_decrypt_cipher(key))

                return VaultFileCredentials(master_key, vault_file.header.slots)

    @Slot()
    def lock_vault(self):
        if self.manager.is_vault_loaded():
            self.takeCentralWidget().disconnect(self.refresh_connection)
            self.refresh_connection = None
            self.setCentralWidget(self.auth_page)
            self.manager.lock(True)

    @Slot()
    def quit_window(self):
        """
        Quits the window
        :return: None
        """
        self.close()
