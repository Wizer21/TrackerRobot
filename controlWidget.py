from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Communication(QObject):
    xIsMoveUp = pyqtSignal(bool)
    yIsMoveUp = pyqtSignal(bool)
    motorMove = pyqtSignal(str)


class controlWidget(QWidget):
    def __init__(self, nparent):
        QWidget.__init__(self, parent = nparent)
        self.messager = Communication()

        self.layoutMain = QGridLayout(self)
        self.labelServo = QLabel("Servo", self)
        self.buttonUp = QPushButton("up", self)
        self.buttonRight = QPushButton("right", self)
        self.buttonBot = QPushButton("bot", self)
        self.buttonLeft = QPushButton("left", self)

        self.labelMotor = QLabel("Motor", self)
        self.buttonUpMotor = QPushButton("front", self)
        self.buttonRightMotor = QPushButton("right", self)
        self.buttonBotMotor = QPushButton("back", self)
        self.buttonLeftMotor = QPushButton("left", self)

        self.buttonUpMotor.setObjectName("front")
        self.buttonRightMotor.setObjectName("right")
        self.buttonBotMotor.setObjectName("back")
        self.buttonLeftMotor.setObjectName("left")
        
        self.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.labelServo, 0, 0)
        self.layoutMain.addWidget(self.buttonUp, 1, 1)
        self.layoutMain.addWidget(self.buttonRight, 2, 2)
        self.layoutMain.addWidget(self.buttonBot, 2, 1)
        self.layoutMain.addWidget(self.buttonLeft, 2, 0)
        
        self.layoutMain.addWidget(self.labelMotor, 3, 0)
        self.layoutMain.addWidget(self.buttonUpMotor, 4, 1)
        self.layoutMain.addWidget(self.buttonRightMotor, 5, 2)
        self.layoutMain.addWidget(self.buttonBotMotor, 5, 1)
        self.layoutMain.addWidget(self.buttonLeftMotor, 5, 0)
        
        self.buttonUp.clicked.connect(self.sendUp)
        self.buttonRight.clicked.connect(self.sendRight)
        self.buttonBot.clicked.connect(self.sendDown)
        self.buttonLeft.clicked.connect(self.sendLeft)

        self.buttonUpMotor.clicked.connect(self.motorMovement)
        self.buttonRightMotor.clicked.connect(self.motorMovement)
        self.buttonBotMotor.clicked.connect(self.motorMovement)
        self.buttonLeftMotor.clicked.connect(self.motorMovement)
    
    def sendUp(self):
        self.messager.yIsMoveUp.emit(False)

    def sendDown(self):
        self.messager.yIsMoveUp.emit(True)

    def sendRight(self):
        self.messager.xIsMoveUp.emit(False)

    def sendLeft(self):
        self.messager.xIsMoveUp.emit(True)

    def motorMovement(self):
        self.messager.motorMove.emit(self.sender().objectName())
