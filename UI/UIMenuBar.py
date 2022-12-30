from PySide6.QtWidgets import QMenuBar


class UIMenuBar(QMenuBar):

    def __init__(self, master):
        QMenuBar.__init__(self, master)
        filemenu = self.addMenu(self.tr("Fichier"))
        filemenu.addAction()
