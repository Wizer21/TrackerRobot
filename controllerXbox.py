from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from evdev import*

class Communication(QObject):
    motor_move = pyqtSignal(list)
    motor_stop = pyqtSignal()
    servo_move = pyqtSignal(list)
    servo_stop = pyqtSignal()

class controllerXbox(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()     
        self.controller_on = True  

        try:
            self.gamepad = InputDevice('/dev/input/event4')
        except FileNotFoundError:
            print("NO CONTROLLER FOUND")
            return

        self.joy1_y = 1
        self.joy1_x = 0
        self.joy1_position = [0, 0]

        self.joy2_y = 5
        self.joy2_x = 2
        self.joy2_position = [0, 0]

        self.servo_position = [0, 0]
        self.motor_position = [0, 0]

        self.null_min = int( 65535 / 2 ) - 3000
        self.null_max = int( 65535 / 2 ) + 3000

        self.start()
        

    def run(self):
        while self.controller_on:
            for event in self.gamepad.read_loop():
                #JOYSTICK
                if event.type == ecodes.EV_ABS: 
                    # JOY 2 SERVOS CONTROL
                    if event.code == self.joy2_x:            
                        self.joy2_position[0] = int(event.value)                  
                        if not self.null_min < event.value < self.null_max:
                            self.servo_position[0] = int(event.value)
                            self.messager.servo_move.emit(self.servo_position)
                        elif self.null_min < self.joy2_position[1] < self.null_max:
                            self.messager.servo_stop.emit()

                    elif event.code == self.joy2_y: 
                        self.joy2_position[1] = int(event.value)  
                        if not self.null_min < event.value < self.null_max:
                            self.servo_position[1] = int(event.value)
                            self.messager.servo_move.emit(self.servo_position)
                        elif self.null_min < self.joy2_position[0] < self.null_max:
                            self.messager.servo_stop.emit()

                    # JOY 1 MOTOR CONTROL
                    elif event.code == self.joy1_x:            
                        self.joy1_position[0] = int(event.value)                  
                        if not self.null_min < event.value < self.null_max:
                            self.motor_position[0] = int(event.value)
                            self.messager.motor_move.emit(self.motor_position)
                        elif self.null_min < self.joy1_position[1] < self.null_max:
                            self.messager.motor_stop.emit()

                    elif event.code == self.joy1_y: 
                        self.joy1_position[1] = int(event.value)  
                        if not self.null_min < event.value < self.null_max:
                            self.motor_position[1] = int(event.value)
                            self.messager.motor_move.emit(self.motor_position)
                        elif self.null_min < self.joy1_position[0] < self.null_max:
                            self.messager.motor_stop.emit()
    
