from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Communication(QObject):
    x_is_move_up = pyqtSignal(bool)
    y_is_move_up = pyqtSignal(bool)
    x_released = pyqtSignal()
    y_released = pyqtSignal()
    motor_move = pyqtSignal(str)
    motor_released = pyqtSignal()


class controlWidget(QWidget):
    def __init__(self, nparent):
        QWidget.__init__(self, parent = nparent)
        self.messager = Communication()
        
        # WIDGETS
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
        
        # UI
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

        # CONNECTIONS
        ## SERVOS PRESSED
        self.buttonUp.pressed.connect(self.sendUp)
        self.buttonRight.pressed.connect(self.sendRight)
        self.buttonBot.pressed.connect(self.sendDown)
        self.buttonLeft.pressed.connect(self.sendLeft)

        self.buttonUp.released.connect(self.y_servo_released)
        self.buttonRight.released.connect(self.x_servo_released)
        self.buttonBot.released.connect(self.y_servo_released)
        self.buttonLeft.released.connect(self.x_servo_released)

        ## MOTOR PRESSED
        self.buttonUpMotor.pressed.connect(self.motor_movement)
        self.buttonRightMotor.pressed.connect(self.motor_movement)
        self.buttonBotMotor.pressed.connect(self.motor_movement)
        self.buttonLeftMotor.pressed.connect(self.motor_movement)
        # MOTOR RELEASED
        self.buttonUpMotor.released.connect(self.released_motor)
        self.buttonRightMotor.released.connect(self.released_motor)
        self.buttonBotMotor.released.connect(self.released_motor)
        self.buttonLeftMotor.released.connect(self.released_motor)
    
    def sendUp(self):
        self.messager.y_is_move_up.emit(False)

    def sendDown(self):
        self.messager.y_is_move_up.emit(True)

    def sendRight(self):
        self.messager.x_is_move_up.emit(False)

    def sendLeft(self):
        self.messager.x_is_move_up.emit(True)

    def motor_movement(self):
        self.messager.motor_move.emit(self.sender().objectName())

    def released_motor(self):
        self.messager.motor_released.emit()
        
    def x_servo_released(self):
        self.messager.x_released.emit()

    def y_servo_released(self):
        self.messager.y_released.emit()
