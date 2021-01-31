from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import pigpio
from time import sleep 

class MotorThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.run_motor = False
        self.right_up = 17 
        self.right_down = 18
        self.left_up = 23
        self.left_down = 22
        self.instructions = []
        self.quick = False

        self.motor_speed = 0
        self.rotation = 0
        self.is_forward = True

        self.moveList = {
            "front": [[self.left_up, 1], [self.left_down, 0],[self.right_up, 1], [self.right_down, 0]],
            "right": [[self.left_up, 1], [self.left_down, 0],[self.right_up, 0], [self.right_down, 1]],
            "back": [[self.left_up, 0], [self.left_down, 1],[self.right_up, 0], [self.right_down, 1]],
            "left": [[self.left_up, 0], [self.left_down, 1],[self.right_up, 1], [self.right_down, 0]]
        }

        self.pi = pigpio.pi()

        # STOP MOTOR
        self.cut_motor()

    def quick_motor_move(self, quick_move):
        self.quick = True
        self.instructions = self.moveList[quick_move]
        self.start()
       
    def cut_motor(self):
        self.pi.write(self.right_up, 0)
        self.pi.write(self.right_down, 0)
        self.pi.write(self.left_up, 0)
        self.pi.write(self.left_down, 0)

    def callMovement(self, movement, set_is_forward):
        if -20 < movement < 20:
            self.rotation = 0
        else:
            self.rotation = round(movement* 0.8)
        self.is_forward = set_is_forward
        
        self.set_instructions()

        if not self.run_motor:
            self.run_motor = True
            self.start()
    
    def update_speed(self, speed):
        self.motor_speed = speed
        self.set_instructions()
        
    def set_instructions(self):        
        l_up = 0
        l_dw = 0
        r_up = 0
        r_dw = 0

        speed = (125/100) * self.motor_speed

        print("INIT " + str(self.rotation))
        rotated = (self.rotation / 100) * self.motor_speed
        if rotated < 0:
            rotated = -rotated
        rotated = 100 - rotated
        print("ROTATED " + str(rotated))

        if self.motor_speed != 0:
            if self.is_forward:
                l_up = 125
                r_up = 125
                if self.rotation > 0:
                    l_up += speed
                    r_up += rotated
                elif self.rotation < 0:
                    l_up += rotated
                    r_up += speed
                else:
                    l_up += speed
                    r_up += speed
            else:  
                l_dw = 125
                r_dw = 125           
                if self.rotation > 0:
                    l_dw += speed
                    r_dw += rotated
                elif self.rotation < 0:
                    l_dw += rotated
                    r_dw += speed
                else:
                    l_dw += speed
                    r_dw += speed

        
        self.instructions = [[self.left_up, l_up], [self.left_down, l_dw], [self.right_up, r_up], [self.right_down, r_dw]] 
        print(str(self.instructions))


    def run(self):       
        if self.quick:
            for move in self.instructions:
                self.pi.write(move[0], move[1])
            sleep(0.05)
            self.quick = False
        else:     
            while self.run_motor: 
                for move in self.instructions:
                    self.pi.set_PWM_dutycycle(move[0], move[1])
                sleep(0.05)
       
        self.cut_motor()

