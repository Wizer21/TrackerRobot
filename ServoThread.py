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
        pwm.start(self.positionServo)

        pwm.ChangeDutyCycle(self.positionServo)     
        sleep(0.3)

        pwm.stop()

    def callPosition(self, val):
        if not 2.5 < val < 12.5:
            print("DANGER " + str(val))
        else:
            self.positionServo = val
            self.set_fixed_pos = True
            self.start() 

    def quick_movement(self, value):   
        newpos = self.positionServo + value
        if not 2.5 < newpos < 12.5:  # SECURITY
            print("DANGER " + str(newpos))
            return False

        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        pwm.start(self.positionServo)
                    
        pwm.ChangeDutyCycle(newpos) 
        sleep(0.05)  
         
        self.positionServo = newpos 
        return True


    def callMovement(self, value):     
        self.action = value

        self.run = True
        self.start() 

    def stop_servos(self):
        self.run = False

    def run(self):        
        GPIO.setup(self.controlPin, GPIO.OUT) 
        pwm = GPIO.PWM(self.controlPin, 50) # pwm pulse with moderation
        while self.run:
            newpos = round(self.positionServo + self.action, 2)
            if not 2.5 < newpos < 12.5:  # SECURITY
                print("DANGER " + str(newpos))
                break


            pwm.start(self.positionServo)                            
            pwm.ChangeDutyCycle(newpos)  
            self.positionServo = newpos 
            print("pos " + str(newpos))

            sleep(0.1)  

        pwm.stop()
