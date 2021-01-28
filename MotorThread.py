from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import RPi.GPIO as GPIO # general-purpose input/output
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

        GPIO.setmode(GPIO.BCM) # SERVO MOTOR
        # MOTOR RIGHT
        GPIO.setup(self.right_up, GPIO.OUT) # FORWARD
        GPIO.setup(self.right_down, GPIO.OUT) # BACKWARD

        # MOTOR LEFT
        GPIO.setup(self.left_down, GPIO.OUT) # BACKWARD
        GPIO.setup(self.left_up, GPIO.OUT) # FORWARD

        # STOP MOTOR
        self.cut_motor()

    def quick_motor_move(self, quick_move):
        self.quick = True
        self.instructions = self.moveList[quick_move]
        self.start()
       
    def cut_motor(self):
        GPIO.output(self.right_up, 0)
        GPIO.output(self.right_down, 0)
        GPIO.output(self.left_up, 0)
        GPIO.output(self.left_down, 0)

    def callMovement(self, movement):
        self.instructions = self.moveList[movement]
        self.run_motor = True
        self.start()
        
    def run(self):       
        if self.quick:
            for move in self.instructions:
                GPIO.output(move[0], move[1])
            sleep(0.05)
            self.quick = False
        else:       
            for move in self.instructions:
                GPIO.output(move[0], move[1])
            while self.run_motor:
                sleep(0.2)
       
        self.cut_motor()

