from PySide6.QtCore import Slot, QSize, Qt, QMetaObject, Signal
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (QMainWindow, QFileDialog)
from os import path

from UI.AddDialog import AddDialog
from UI.EntriesPage import EntriesPage
from UI.FirstUseWidget import FirstUseWidget
from UI.NewAuthDialog import NewAuthDialog
from UI.PrefDock import PrefDock
from UI.UIMenuBar import UIMenuBar
from utils.VaultEntry import VaultEntry

from utils.VaultManager import VaultManager
from utils.VaultRepository import VaultRepository
from utils.VaultFile import VaultFile
from utils.VaultFileCredentials import VaultFileCredentials
from utils.Slots.PasswordSlot import PasswordSlot
from UI.AuthPage import AuthPage
import utils.Slots as Slots


class UIWindow(QMainWindow):
    refresh_signal = Signal(VaultEntry)
    locked_signal = Signal(bool)

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
        self.uiMenuBar.addAction(self.tr("Préférences"), QKeySequence(self.tr("Ctrl+P")), self.open_preferences)
        self.setMenuBar(self.uiMenuBar)

        self.auth_page: AuthPage = AuthPage()
        self.preferences_dock = PrefDock(self.tr("Préférences"), self, self.manager)
        self.preferences_dock.setFixedWidth(300)
        self.addDockWidget(Qt.RightDockWidgetArea, self.preferences_dock)
        self.preferences_dock.hide()

        self.preferences_dock.password_change_signal.connect(self.change_vault_creds)
        self.preferences_dock.remove_password_signal.connect(self.remove_vault_creds)
        self.locked_signal.connect(self.preferences_dock.toggle_security_menu)

        self.auth_page.password_entered_signal.connect(self.decrypt_task)

        try:
            self.manager.load_vault_file()
            self.preferences_dock.encryption_toggled()
            if self.manager.is_vault_loaded():
                self.display_vault()
            else:
                self.setCentralWidget(self.auth_page)
        except FileNotFoundError:
            widget = FirstUseWidget(self)
            widget.new_signal.connect(self.create_blank_vault)
            widget.import_signal.connect(self.import_file)
            self.setCentralWidget(widget)

    @Slot()
    def export(self):
        if self.manager.is_vault_loaded():
            filename = QFileDialog.getSaveFileName(self, self.tr("Exporter le fichier de coffre"),
                                                   f"{path.dirname(__file__)}/2fa-export.json",
                                                   self.tr("Fichiers json (*.json)"))
            if filename[0]:
                self.manager.export(filename[0])

    @Slot()
    def import_file(self):
        filename = QFileDialog.getOpenFileName(self, self.tr("Sélectionnez un fichier de coffre"),
                                               path.dirname(__file__), self.tr("Fichiers json (*.json)"))
        if not filename[0]:
            return
        self.vaultFile = VaultRepository.from_file_import(filename[0])
        if self.vaultFile.is_encrypted():
            self.takeCentralWidget()
            self.setCentralWidget(self.auth_page)
        else:
            self.manager.load_from(self.vaultFile, None)
            self.vaultFile = None
            self.display_vault()

    @Slot()
    def create_blank_vault(self):
        dial = NewAuthDialog(self)
        button = dial.exec()

        if button == 1:
            creds = dial.compute_credentials()
            self.manager.init_new(creds)
            self.display_vault()
            self.preferences_dock.encryption_toggled()

    @Slot()
    def change_vault_creds(self):
        dial = NewAuthDialog(self)
        button = dial.exec()

        if button == 1:
            creds = dial.compute_credentials()
            self.manager.change_credentials(creds)
            self.preferences_dock.encryption_toggled()

    @Slot()
    def remove_vault_creds(self):
        if self.manager.is_vault_loaded():
            self.manager.change_credentials(None)
            self.preferences_dock.encryption_toggled()

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
            self.preferences_dock.encryption_toggled()

        else:
            try:
                creds = self.unlock_with_pass(self.manager.vault_file, passw)
            except ValueError:
                self.auth_page.wrong_pass()
                return

            self.auth_page.good_pass()
            self.manager.unlock(creds)
        self.display_vault()

    @Slot()
    def open_preferences(self):
        if self.preferences_dock.isVisible():
            self.preferences_dock.hide()
        else:
            self.preferences_dock.show()

    def display_vault(self):
        self.takeCentralWidget()
        entries_page = EntriesPage(self, self.manager.repo)
        self.refresh_connection = self.refresh_signal.connect(entries_page.add_entry)
        self.setCentralWidget(entries_page)
        self.locked_signal.emit(False)

    @staticmethod
    def unlock_with_pass(vault_file: VaultFile, password: str) -> VaultFileCredentials:
        for slot in vault_file.header.slots:
            if type(vault_file.header.slots[slot]) == PasswordSlot:
                pass_slot:  Slots.Slot| PasswordSlot = vault_file.header.slots[slot]
                key = pass_slot.derive_key(password)
                master_key = pass_slot.get_key(pass_slot.create_decrypt_cipher(key))

                return VaultFileCredentials(master_key, vault_file.header.slots)

    @Slot()
    def lock_vault(self):
        if self.manager.is_vault_loaded() and self.manager.repo.is_encryption_enabled():
            self.takeCentralWidget().disconnect(self.refresh_connection)
            self.refresh_connection = None
            self.setCentralWidget(self.auth_page)
            self.manager.lock(True)
            self.locked_signal.emit(True)

    @Slot()
    def quit_window(self):
        """
        Quits the window
        :return: None
        """
        self.close()
