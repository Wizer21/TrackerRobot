from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import cv2
from numpy import *

class Communication(QObject):
    cameraImages = pyqtSignal(QImage, ndarray)

class CameraThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()


    def run(self):    
        my_width = 1000
        my_height = 500
        cap = cv2.VideoCapture(0)

        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, my_width)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, my_height)
        #cap.set(10, 4)  # SET BRIGHNESS TOcameraImages 5
        #cap.set(12, 20)  # SET SATURATION TO 10

        keep = True   
        while keep:
            ret, frame = cap.read()
            if ret:
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = cv_image.shape
                bytesPerLine = 3 * width
                self.messager.cameraImages.emit(QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped(), cv_image)