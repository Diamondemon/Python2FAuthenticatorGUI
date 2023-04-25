import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal


class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    
    def start(self, priority: QThread.Priority = ...) -> None:
        self._run_flag = True
        super().start(priority)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
