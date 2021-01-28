from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from evdev import*

class Communication(QObject):
    motor_mouvement = pyqtSignal(str)
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


        self.joy_y = 5
        self.joy_x = 2
        self.joy_position = [0, 0]
        self.servo_position = [0, 0]

        self.directionnal_button_x = 16
        self.directionnal_button_y = 17

        self.null_min = int( 65535 / 2 ) - 3000
        self.null_max = int( 65535 / 2 ) + 3000

        self.start()
        

    def run(self):
        while self.controller_on:
            for event in self.gamepad.read_loop():
                #JOYSTICK
                if event.type == ecodes.EV_ABS: 
                    # JOY 2
                    if event.code == self.joy_x:            
                        self.joy_position[0] = int(event.value)                  
                        if not self.null_min < event.value < self.null_max:
                            self.servo_position[0] = int(event.value)
                            self.messager.servo_move.emit(self.servo_position)
                        elif self.null_min < self.joy_position[1] < self.null_max:
                            self.messager.servo_stop.emit()

                    elif event.code == self.joy_y: 
                        self.joy_position[1] = int(event.value)  
                        if not self.null_min < event.value < self.null_max:
                            self.servo_position[1] = int(event.value)
                            self.messager.servo_move.emit(self.servo_position)
                        elif self.null_min < self.joy_position[0] < self.null_max:
                            self.messager.servo_stop.emit()

                    # DIRECTIONAL BUTTON AXIS Y
                    elif event.code == self.directionnal_button_y:  
                        pos = int(str(event.value).replace("L", ""))
                        if pos > 0:
                            self.messager.motor_mouvement.emit("back")
                        elif pos < 0:
                            self.messager.motor_mouvement.emit("front")
                        elif pos == 0:
                            self.messager.motor_stop.emit()

                    # DIRECTIONAL BUTTON AXIS X
                    elif event.code == self.directionnal_button_x:
                        pos = int(str(event.value).replace("L", ""))
                        if pos > 0:
                            self.messager.motor_mouvement.emit("right")
                        elif pos < 0:
                            self.messager.motor_mouvement.emit("left")
                        elif pos == 0:
                            self.messager.motor_stop.emit()
    
