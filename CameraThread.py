from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import cv2
from numpy import *

class Communication(QObject):
    cameraSize = pyqtSignal(int, int)
    cameraImages = pyqtSignal(QImage, ndarray)

class CameraThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()


    def run(self):    
        my_width = 1000
        my_height = 500
        cap = cv2.VideoCapture(0)

        #cap.set(10, 4)  # SET BRIGHNESS TOcameraImages 5
        cap.set(cv2.CAP_PROP_SATURATION, 5)  # SET SATURATION TO 10

        cap.set(cv2.CAP_PROP_FPS, 10)
        print("fps: " + str(cap.get(cv2.CAP_PROP_FPS)))

        self.messager.cameraSize.emit(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        keep = True   
        while keep:
            ret, frame = cap.read()
            if ret:
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = cv_image.shape
                bytesPerLine = 3 * width
                self.messager.cameraImages.emit(QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888), cv_image) # FRAGMENTATION ERROR
                #self.messager.cameraImages.emit(QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped(), cv_image) # ORANGE IS BLUE