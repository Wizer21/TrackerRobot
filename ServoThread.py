from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import RPi.GPIO as GPIO # general-purpose input/output
from time import sleep 

class ServoThread(QThread):
    def __init__(self, pin):
        QThread.__init__(self)
        self.instructionServo = 10
        self.controlPin = pin

        self.start()

    def callPosition(self, val):
        if val < 1 or val > 12:
            print("SLIDER DANGER " + str(val))
            return False
        else:
            # IF THE POSITION IS SAFE, RUN THE THREAD
            self.instructionServo = val
            self.start() 
            return True
        
    def callMovement(self, isUp):
        if isUp:
            val = self.instructionServo + 0.5
        else:
            val = self.instructionServo - 0.5
            
        if val < 1 or val > 12:
            print("SLIDER DANGER " + str(val))
            return False
        else:
            # IF THE POSITION IS SAFE, RUN THE THREAD
            self.instructionServo = val
            self.start() 
            return True

    def run(self):
        position = round(self.instructionServo /1, 1)

        if position < 1 or position > 12:  # SECURITY
            print("SLIDER DANGER " + str(position))
            return

        print("MOTOR POSITION " + str(position))

        GPIO.setmode(GPIO.BOARD) # SERVO MOTOR
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        pwm.start(0)

        pwm.ChangeDutyCycle(position)        
        sleep(0.3)

        pwm.stop()
        GPIO.cleanup()
        self.exit()