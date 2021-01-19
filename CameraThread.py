from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import cv2

class Communication(QObject):
    cameraImages = pyqtSignal(QImage)

class CameraThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()


    def run(self):
        keep = True        

        test = 0
        my_width = 1000
        my_height = 500
        cap = cv2.VideoCapture(0)

        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, my_width)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, my_height)
        #cap.set(10, 4)  # SET BRIGHNESS TO 5
        #cap.set(12, 20)  # SET SATURATION TO 10

        while keep:
            test += 1
            print(str(test))
            ret, frame = cap.read()
            if ret:
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = cv_image.shape
                bytesPerLine = 3 * width
                qImg1 = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()


                self.messager.cameraImages.emit(qImg1)