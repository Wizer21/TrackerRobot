from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import RPi.GPIO as GPIO # general-purpose input/output
from time import sleep 

class ServoThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.instructionServo = 0

    def setUpInstructions(self, val):
        self.instructionServo = val

    def run(self):
        position = ( self.instructionServo /2 )+ 5

        if position < 5 or position > 10:
            print("SLIDER DANGER " + str(position))
            return

        print("MOTOR POSITION SEND " + str(position))

        GPIO.setmode(GPIO.BOARD) # SERVO MOTOR
        GPIO.setup(8, GPIO.OUT) 
        pwm = GPIO.PWM(8, 50)
        pwm.start(0)

        pwm.ChangeDutyCycle(position)
        sleep(0.25)

        pwm.stop()
        GPIO.cleanup()