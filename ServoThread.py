from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import RPi.GPIO as GPIO # general-purpose input/output
from time import sleep 

class ServoThread(QThread):
    def __init__(self, pin):
        QThread.__init__(self)
        self.positionServo = 6.5
        self.controlPin = pin
        self.run = False
        self.action = 0.5

        # SET INITIAL POS
        self.ini_position()

    def ini_position(self):     
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50)
        pwm.start(0)

        pwm.ChangeDutyCycle(self.positionServo)     
        sleep(0.3)

        pwm.stop()
        GPIO.cleanup()
        self.exit()

    def callPosition(self, val):
        if val < 1 or val > 12:
            print("SLIDER DANGER " + str(val))
            return False
        else:
            # IF THE POSITION IS SAFE, RUN THE THREAD
            self.positionServo = val
            self.start() 
            return True
        
    def callMovement(self, isUp):
        if isUp:
            self.action = 0.4
        else:
            self.action = -0.4

        self.run = True
        self.start() 

    def stop_servos(self):
        self.run = False

    def run(self):
        GPIO.setmode(GPIO.BCM) # SERVO MOTOR
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        pwm.start(0)

        while self.run:
            newpos = self.positionServo + self.action

            if newpos < 1 or newpos > 12:  # SECURITY
                print("SLIDER DANGER " + str(newpos))
                self.exit()
                break
            
            self.positionServo = newpos
            pwm.ChangeDutyCycle(newpos)     
            sleep(0.03)

        pwm.stop()
        GPIO.cleanup()
        self.exit()

