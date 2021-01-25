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
        self.lastpos = 0

        GPIO.setmode(GPIO.BCM) # SERVO MOTOR
                
        # SET INITIAL POS
        self.ini_position()

    def ini_position(self):     
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50)
        pwm.start(0)

        pwm.ChangeDutyCycle(self.positionServo)     
        sleep(0.3)

        pwm.stop()
        GPIO.cleanup()

    def callPosition(self, val):
        if val < 1 or val > 12.5:
            print("SLIDER DANGER " + str(val))
        else:
            self.positionServo = val
            self.set_fixed_pos = True
            self.start() 
        
    def callMovement(self, value):     
        self.action = value

        self.run = True
        self.start() 

    def stop_servos(self):
        self.run = False

    def run(self):
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        pwm.start(0)

        while self.run:
            newpos = self.positionServo + self.action

            if not 1 < newpos < 12.5:  # SECURITY
                print("SLIDER DANGER " + str(newpos))
                break
            

            self.positionServo = newpos
            pwm.ChangeDutyCycle(newpos)   

            print("dab")

            if self.lastpos > newpos:
                difference = self.lastpos - newpos
            else:
                difference = newpos - self.lastpos
            print("diff " + str(difference))

            tims_to_sleep = (difference * 0.3) / 11.5
            print("sleep " + str(tims_to_sleep))

            sleep(tims_to_sleep)  

            self.lastpos = newpos

        pwm.stop()

