from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import pigpio
from time import sleep 
import os

class ServoThread(QThread):
    def __init__(self, pin):
        QThread.__init__(self)
        self.controlPin = pin
        self.run_servo = False
        self.action = 0.5
        self.lastpos = 0
        if pin == 4:
            self.positionServo = 1000
        else:
            self.positionServo = 1500

        try:
            self.pi = pigpio.pi() # Connect to local pi
            self.pi.set_mode(pin, pigpio.OUTPUT)
        except AttributeError:
            os.system("sudo pigpiod")
            self.pi = pigpio.pi() # Connect to local pi
            self.pi.set_mode(pin, pigpio.OUTPUT)

        # SET INITIAL POS
        self.ini_position()

    def ini_position(self):     
        self.pi.set_servo_pulsewidth(self.controlPin, self.positionServo)     
        sleep(0.2)

        self.pi.set_servo_pulsewidth(self.controlPin, 0)   

    def callPosition(self, val):
        if not 500 < val < 2500:
            print("DANGER " + str(val))
        else:
            self.positionServo = val
            self.set_fixed_pos = True
            self.start() 

    def quick_movement(self, value):   
        self.action =  value
        newpos = round(self.positionServo + value)
        if not 500 < newpos < 2500:  # SECURITY
            print("DANGER " + str(newpos))
            return False

        if not self.run_servo:
            self.run_servo = True
            self.start() 
        return True

    def callMovement(self, value):     
        self.action = value

        if not self.run_servo:
            
            self.run_servo = True
            self.start()
        
    def run(self):      
        while self.run_servo:
            newpos = round(self.positionServo + self.action)
            if not 500 < newpos < 2500:  # SECURITY
                print("DANGER " + str(newpos))
                break
  
            self.pi.set_servo_pulsewidth(self.controlPin, newpos)   
            sleep(0.01)  

            self.positionServo = newpos 

        self.pi.set_servo_pulsewidth(self.controlPin, 0)   