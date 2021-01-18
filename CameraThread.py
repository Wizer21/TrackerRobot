from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from picamera import PiCamera
from io import BytesIO
from picamera.array import PiRGBArray

class Communication(QObject):
    cameraImages = pyqtSignal(QImage)

class CameraThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()


    def run(self):
        keep = True        

        with PiCamera() as camera:
            camera.resolution = (384, 216)
            camera.shutter_speed = 0

            with PiRGBArray(camera) as rawCapture:
                while keep:
                    camera.capture(rawCapture, format = "rgb")

                    image = rawCapture.array
                    rawCapture.truncate(0)
                    h, w, ch = image.shape
                    bytesPerLine = ch*w
                    qt_image = QImage(image, w, h, bytesPerLine, QImage.Format_RGB888)

                    self.messager.cameraImages.emit(qt_image)
