from PySide6.QtWidgets import QMenuBar


class UIMenuBar(QMenuBar):

    def __init__(self, master):
        QMenuBar.__init__(self, master)
        self.filemenu = self.addMenu(self.tr("Fichier"))

    def addFileAction(self, name:str, member, shortcut = None):
        if (shortcut):
            self.filemenu.addAction(name, shortcut, member)
            return

        self.filemenu.addAction(name, member)