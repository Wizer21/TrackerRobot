from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from Utils import*
from pos_picker import*

class Communication(QObject):
    servo_x_move = pyqtSignal(float)
    servo_y_move = pyqtSignal(float)
    servo_x_released = pyqtSignal()
    servo_y_released = pyqtSignal()
    motor_move = pyqtSignal(list)
    motor_released = pyqtSignal()


class controlWidget(QWidget):
    def __init__(self, nparent):
        QWidget.__init__(self, parent = nparent)
        self.messager = Communication()
        self.picker_size = 150
        self.ratio_servo = (self.picker_size / 2) / 10
        self.ratio_motor = (self.picker_size / 2) / 125
        self.min_range = round((self.picker_size / 5) * 2)
        self.max_range = round((self.picker_size / 5) * 3)
        
        # WIDGETS
        self.layoutMain = QGridLayout(self)
        self.labelServo = QLabel(self)
        self.picker_servo = pos_picker(self, [self.picker_size, self.picker_size])

        self.labelMotor = QLabel(self)
        self.picker_motor = pos_picker(self, [self.picker_size, self.picker_size])
        
        # UI
        self.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.labelServo, 0, 0)
        self.layoutMain.addWidget(self.picker_servo, 1, 0)
        
        self.layoutMain.addWidget(self.labelMotor, 2, 0)
        self.layoutMain.addWidget(self.picker_motor, 3, 0)

        # PARAMETERS 
        self.labelServo.setPixmap(Utils.get_pixmap("camera"))
        self.labelMotor.setPixmap(Utils.get_pixmap("engine")) 

        self.picker_servo.messager.pos_selected.connect(self.servo_picker_move)
        self.picker_servo.messager.pos_leaved.connect(self.servo_picker_released)
        self.picker_motor.messager.pos_selected.connect(self.motor_picker_move)
        self.picker_motor.messager.pos_leaved.connect(self.motor_picker_released)

        
    def servo_picker_move(self, x, y):
        if self.min_range < x < self.max_range:
            self.messager.servo_x_released.emit()
        else:
            self.messager.servo_x_move.emit(-((x - (self.picker_size / 2)) / self.ratio_servo))
        
        if self.min_range < y < self.max_range:
            self.messager.servo_y_released.emit()
        else:
            self.messager.servo_y_move.emit(-((y - (self.picker_size / 2)) / self.ratio_servo))

    def servo_picker_released(self):
        self.messager.servo_x_released.emit()
        self.messager.servo_y_released.emit()

    def motor_picker_move(self, x, y):
        if self.min_range < x < self.max_range:
            x = self.picker_size / 2
        
        if self.min_range < y < self.max_range:
            y = self.picker_size / 2

        self.messager.motor_move.emit([round(-(x - (self.picker_size / 2)) / self.ratio_motor), round((y - (self.picker_size / 2)) / self.ratio_motor)])

    def motor_picker_released(self):
        self.messager.motor_released.emit()
