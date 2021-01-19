from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import RPi.GPIO as GPIO # general-purpose input/output
from time import sleep 

class ServoThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.instructionServo = 0
        self.difference = 0

    def setUpInstructions(self, val):
        self.instructionServo = val

    def run(self):
        position = ( self.instructionServo /4 )

        if position < 1 or position > 10:
            print("SLIDER DANGER " + str(position))
            # return

        print("MOTOR POSITION " + str(position))

        GPIO.setmode(GPIO.BOARD) # SERVO MOTOR
        GPIO.setup(8, GPIO.OUT) 
        pwm = GPIO.PWM(8, 50) # pwm pulse with moderation
        pwm.start(0)

        if self.instructionServo > self.difference:
            sleep_time = self.instructionServo - self.difference
        else:
            sleep_time = self.difference - self.instructionServo

        sleep_time = round(0.15 * sleep_time, 2)
        pwm.ChangeDutyCycle(position)        
        sleep(sleep_time)
        print("FINAL SLEEP " + str(sleep_time))

        pwm.stop()
        GPIO.cleanup()
        self.difference = self.instructionServo
        self.exit()