from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Communication(QObject):
    xIsMoveUp = pyqtSignal(bool)
    yIsMoveUp = pyqtSignal(bool)


class controlWidget(QWidget):
    def __init__(self, nparent):
        QWidget.__init__(self, parent = nparent)
        self.messager = Communication()

        self.layoutMain = QGridLayout(self)
        self.buttonUp = QPushButton("up", self)
        self.buttonRight = QPushButton("right", self)
        self.buttonBot = QPushButton("bot", self)
        self.buttonLeft = QPushButton("left", self)

        self.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.buttonUp, 0, 1)
        self.layoutMain.addWidget(self.buttonRight, 1, 2)
        self.layoutMain.addWidget(self.buttonBot, 1, 1)
        self.layoutMain.addWidget(self.buttonLeft, 1, 0)
        
        self.buttonUp.clicked.connect(self.sendUp)
        self.buttonRight.clicked.connect(self.sendRight)
        self.buttonBot.clicked.connect(self.sendDown)
        self.buttonLeft.clicked.connect(self.sendLeft)
    
    def sendUp(self):
        self.messager.yIsMoveUp.emit(False)

    def sendDown(self):
        self.messager.yIsMoveUp.emit(True)

    def sendRight(self):
        self.messager.xIsMoveUp.emit(False)

    def sendLeft(self):
        self.messager.xIsMoveUp.emit(True)


