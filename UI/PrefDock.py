from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QDockWidget, QGridLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from UI.FoldableArea import FoldableArea
from utils.VaultManager import VaultManager


class PrefDock(QDockWidget):
    password_change_signal = Signal()
    remove_password_signal = Signal()

    def __init__(self, title: str, master: QWidget, vault_manager: VaultManager):
        super().__init__(title, master)
        self.vault_manager = vault_manager

        self.content_widget = QWidget(self)
        layout = QVBoxLayout(self.content_widget)
        layout.addWidget(FoldableArea(self, self.tr("Général"), 1))

        self.security_menu = FoldableArea(self, self.tr("Sécurité"), 1)
        self.password_label = QLabel(self.tr("Mot de passe actuel"))
        self.password_edit = QLineEdit()
        self.change_button = QPushButton(self.tr("Changer le mot de passe"))

        self.setup_security_menu()

        layout.addWidget(self.security_menu)
        layout.addStretch(1)
        self.content_widget.setLayout(layout)
        self.setWidget(self.content_widget)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setFloating(False)

        if self.vault_manager.is_locked:
            self.toggle_security_menu(True)

    def setup_security_menu(self):
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.returnPressed.connect(self.verify_password)
        layout = QGridLayout()
        layout.addWidget(self.password_label, 0, 0)
        layout.addWidget(self.password_edit, 0, 1)
        layout.addWidget(self.change_button, 1, 0, 1, 2)
        self.change_button.clicked.connect(self.verify_password)
        self.security_menu.set_content_layout(layout)
        self.encryption_toggled()

    @Slot()
    def encryption_toggled(self):
        if self.vault_manager.is_encryption_enabled:
            self.password_label.show()
            self.password_edit.show()
            self.change_button.setText(self.tr("Changer le mot de passe"))
        else:
            self.password_label.hide()
            self.password_edit.hide()
            self.change_button.setText(self.tr("Ajouter un mot de passe"))

    @Slot(bool)
    def toggle_security_menu(self, locked: bool):
        if locked:
            self.security_menu.hide()
        else:
            self.security_menu.show()

    @Slot()
    def verify_password(self):
        if self.password_edit.isVisible():
            if self.vault_manager.verify_password(self.password_edit.text()):
                self.password_change_signal.emit()
                self.password_edit.setText("")
        else:
            self.password_change_signal.emit()
