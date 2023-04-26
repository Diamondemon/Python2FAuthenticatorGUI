import qrcode
from PIL.ImageQt import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QGraphicsScene

from UI.ui_QrDisplay import Ui_QrDisplay


class QrDisplay(QDialog):

    def __init__(self, master, url: str):
        super().__init__(master)
        self.ui = Ui_QrDisplay()
        self.ui.setupUi(self)
        scene = QGraphicsScene()
        self.ui.qr_view.setScene(scene)
        qr_image = ImageQt(qrcode.make(url))
        qr_image = qr_image.scaled(self.ui.qr_view.width(), self.ui.qr_view.height(), Qt.KeepAspectRatio)
        scene.addPixmap(QPixmap.fromImage(qr_image))
