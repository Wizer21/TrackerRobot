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
        self.set_fixed_pos = True
                
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
        if val < 1 or val > 12.5:
            print("SLIDER DANGER " + str(val))
        else:
            self.positionServo = val
            self.set_fixed_pos = True
            self.start() 
        
    def callMovement(self, isUp):
        if isUp:
            self.action = 0.4
        else:
            self.action = -0.4

        self.set_fixed_pos = False
        self.run = True
        self.sleep = 0.03
        self.start() 

    def stop_servos(self):
        self.run = False

    def run(self):
        GPIO.setmode(GPIO.BCM) # SERVO MOTOR
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        pwm.start(0)

        if self.set_fixed_pos:
            pwm.ChangeDutyCycle(self.positionServo)     
            sleep(0.1)
        else:
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

