from os import path

import numpy as np
import cv2
from PySide6.QtCore import Slot, Qt, SIGNAL
from PySide6.QtGui import QPixmap, QImage, QCloseEvent
from PySide6.QtWidgets import QDialog, QGraphicsPixmapItem, QGraphicsScene, QAbstractButton, QFileDialog

from UI.VideoThread import VideoThread
from UI.ui_QrDialog import Ui_QrDialog


class QrDialog(QDialog):

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_QrDialog()
        self.ui.setupUi(self)
        self.resolved_url = ""
        self.from_image = True

        scene = QGraphicsScene(self)
        self.ui.graphicsView.setScene(scene)
        self.displayed_graphics = QGraphicsPixmapItem()
        scene.addItem(self.displayed_graphics)

        self.detector = cv2.QRCodeDetector()
        self.refresh_thread = VideoThread()
        self.refresh_thread.change_pixmap_signal.connect(self.refresh_image)
        self.ui.source_group.connect(SIGNAL("buttonClicked(QAbstractButton *)"), self.change_source)
        self.ui.file_button.connect(SIGNAL("clicked()"), self.open_image)

    @Slot(QAbstractButton)
    def change_source(self, button: QAbstractButton):
        if button == self.ui.camera_radio:
            self.refresh_thread.start()
            self.from_image = False
            return
        if button == self.ui.picture_radio:
            self.refresh_thread.stop()
            self.from_image = True
            return

    @Slot(np.ndarray)
    def refresh_image(self, image: np.ndarray):
        self.displayed_graphics.setPixmap(self.convert_cv_qt(image))
        self.scan_image(image)

    @Slot()
    def open_image(self):
        if not self.from_image:
            return
        filename = QFileDialog.getOpenFileName(self, self.tr("Sélectionnez un fichier avec un qr code"),
                                               path.dirname(__file__),
                                               self.tr("Fichiers images (*.png *.jpg *.jpeg *.bmp);;"
                                                       "Images PNG (*.png);;"
                                                       "Images compressées JPG (*.jpg *.jpeg);;"
                                                       "Images windows (*.bmp);;"
                                                       "Tous les fichiers (*)"))
        if filename[0]:
            convert_to_qt_format = QImage(filename[0])
            p = convert_to_qt_format.scaled(self.ui.graphicsView.width(), self.ui.graphicsView.height(),
                                            Qt.KeepAspectRatio)
            self.displayed_graphics.setPixmap(QPixmap.fromImage(p))
            self.scan_image(QrDialog.qimage_to_cvmat(convert_to_qt_format))

    def scan_image(self, image: np.ndarray):
        data, bbox, straight_qrcode = self.detector.detectAndDecode(image)
        if len(data) > 0 and len(self.resolved_url) == 0:
            self.resolved_url = data
            self.accept()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.ui.graphicsView.width(), self.ui.graphicsView.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @staticmethod
    def qimage_to_cvmat(incoming_image: QImage):
        '''  Converts a QImage into an opencv MAT format  '''

        width = incoming_image.width()
        height = incoming_image.height()

        ptr = incoming_image.constBits()
        # ptr.setsize(height * width * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
        return arr

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.refresh_thread.stop()

    def accept(self) -> None:
        self.refresh_thread.stop()
        super().accept()

    def reject(self) -> None:
        self.refresh_thread.stop()
        super().reject()
