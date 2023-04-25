import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal


class VideoThread(QThread):
    """Thread handling a camera feed"""
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    
    def start(self, priority: QThread.Priority = None) -> None:
        """
        Starts the thread
        :param priority: Priority of the thread
        :return: None
        """
        self._run_flag = True
        if priority is None:
            super().start()
        else:
            super().start(priority)

    def run(self):
        """
        Captures the frames from a camera feed
        :return: None
        """
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """
        Sets run flag to False and waits for thread to finish
        :return: None
        """
        self._run_flag = False
        self.wait()
