from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from ServoThread import*

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.thread = ServoThread()

        self.widgetMain = QWidget(self)
        self.layoutMain = QGridLayout(self)
        self.labelTitle = QLabel("Tracker Robot !", self)
        self.sliderServo = QSlider(self)

        self.setCentralWidget(self.widgetMain)
        self.widgetMain.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.labelTitle)
        self.layoutMain.addWidget(self.sliderServo)

        self.sliderServo.setPageStep(1)
        self.sliderServo.setRange(0, 10)
        self.sliderServo.setOrientation(Qt.Horizontal)

        self.sliderServo.valueChanged.connect(self.updateServoPosOnSlider)

    def updateServoPosOnSlider(self, val):
        self.thread.setUpInstructions(val)
        self.thread.start()

    
