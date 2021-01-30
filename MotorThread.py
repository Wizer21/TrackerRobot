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

    def callMovement(self, movement):
        l_up = 0
        l_dw = 0
        r_up = 0
        r_dw = 0

        if movement[1] >= 0:        
            l_dw = 125 + movement[1]
            r_dw = 125 + movement[1]
            if movement[0] >= 0:
                r_dw -= movement[0]
            else:
                l_dw -= -movement[0]
        else:
            l_up = 125 + -movement[1]
            r_up = 125 + -movement[1]
            if movement[0] >= 0:
                r_up -= movement[0]
            else:
                l_up -= -movement[0]
        
        self.instructions = [[self.left_up, l_up], [self.left_down, l_dw], [self.right_up, r_up], [self.right_down, r_dw]] 

        if not self.run_motor:
            self.run_motor = True
            self.start()
        
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

