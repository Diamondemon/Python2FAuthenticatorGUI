import numpy as np
import cv2
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap, QImage, QCloseEvent
from PySide6.QtWidgets import QDialog, QGraphicsPixmapItem, QGraphicsScene

from UI.VideoThread import VideoThread
from UI.ui_QrDialog import Ui_QrDialog


class QrDialog(QDialog):

    def __init__(self, master):
        super().__init__(master)
        self.ui = Ui_QrDialog()
        self.ui.setupUi(self)
        self.resolved_url = ""
        scene = QGraphicsScene(self)
        self.ui.graphicsView.setScene(scene)
        self.displayed_graphics = QGraphicsPixmapItem()
        scene.addItem(self.displayed_graphics)

        self.detector = cv2.QRCodeDetector()
        self.refresh_thread = VideoThread()
        self.refresh_thread.change_pixmap_signal.connect(self.refresh_image)
        self.refresh_thread.start()
        self.ui.source_group.connect("idClicked(int)", self.change_source)

    @Slot(int)
    def change_source(self, button_id: int):
        # TODO
        pass
        # if buttonId == 0:
        #    self.

    @Slot(np.ndarray)
    def refresh_image(self, image: np.ndarray):
        self.displayed_graphics.setPixmap(self.convert_cv_qt(image))

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

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        self.refresh_thread.stop()

    def accept(self) -> None:
        self.refresh_thread.stop()
        super().accept()

    def reject(self) -> None:
        self.refresh_thread.stop()
        super().reject()
