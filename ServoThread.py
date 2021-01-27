from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import pigpio
from time import sleep 

class ServoThread(QThread):
    def __init__(self, pin):
        QThread.__init__(self)
        self.controlPin = pin
        self.run_servo = False
        self.action = 0.5
        self.lastpos = 0
        self.quick = False
        if pin == 4:
            self.positionServo = 1000
        else:
            self.positionServo = 1500

        self.pi = pigpio.pi() # Connect to local pi
        self.pi.set_mode(pin, pigpio.OUTPUT)
        print(str(self.pi.get_PWM_real_range(pin)))
                
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
        #self.action =  value
        newpos = round(self.positionServo + value)
        if not 500 < newpos < 2500:  # SECURITY
            print("DANGER " + str(newpos))
            return False

        self.pi.set_servo_pulsewidth(self.controlPin, newpos)   
        sleep(0.01)
        self.pi.set_servo_pulsewidth(self.controlPin, 0)   
        self.positionServo = newpos

        #self.run_servo = True
        #self.quick = True
        #self.start()
        return True

    def callMovement(self, value):     
        self.action = value

        self.run_servo = True
        self.start() 

    def stop_servos(self):
        self.run_servo = False

    def run(self):      
        while self.run_servo:
            newpos = round(self.positionServo + self.action)
            if not 500 < newpos < 2500:  # SECURITY
                print("DANGER " + str(newpos))
                break
  
            self.pi.set_servo_pulsewidth(self.controlPin, newpos)   
            sleep(0.01)  
            print("pos " + str(newpos))

            self.positionServo = newpos 

            if self.quick:
                self.run_servo = False
                self.quick = False  

        self.pi.set_servo_pulsewidth(self.controlPin, 0)   