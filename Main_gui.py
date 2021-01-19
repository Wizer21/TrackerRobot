from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from ServoThread import*
from CameraThread import*

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.thread_servos = ServoThread()
        self.thread_camera = CameraThread()

        self.widgetMain = QWidget(self)
        self.layoutMain = QGridLayout(self)
        self.labelTitle = QLabel("Tracker Robot !", self)
        self.sliderServo = QSlider(self)
        self.labelDisplayCamera = QLabel(self)

        self.build()
        self.run_camera()


    def build(self):
        self.setCentralWidget(self.widgetMain)
        self.widgetMain.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.labelTitle, 0, 0)
        self.layoutMain.addWidget(self.sliderServo, 1, 0)
        self.layoutMain.addWidget(self.labelDisplayCamera, 0, 1, 2, 1)

        self.sliderServo.setPageStep(1)
        self.sliderServo.setRange(4, 48)
        self.sliderServo.setOrientation(Qt.Horizontal)

        self.thread_camera.messager.cameraImages.connect(self.display_camera)
        self.sliderServo.valueChanged.connect(self.updateServoPosOnSlider)

    def updateServoPosOnSlider(self, val):
        self.thread_servos.setUpInstructions(val)
        self.thread_servos.start()

    def run_camera(self):
        self.thread_camera.start()

    def display_camera(self, img):     

        self.labelDisplayCamera.setPixmap(QPixmap.fromImage(img))