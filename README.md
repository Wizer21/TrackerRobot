# TrackerRobot :robot:

This project is realized on Raspberry Pi 4.  

This robot is equipped with 2 DC motor that allow it to move around. Two servomotor control the camera which can in this way follow objects.
Both DC and servomotors can be controlled from the Qt interface or from an Xbox controller.

The camera output is displayed on the interface, this way we can click on it to select an item and begin the tracking.
The item is tracked the same way of my repository [Image_Tracker](https://www.youtube.com/watch?v=CWhhGOI1N1g).
By looking at the center point of the tracked item, I can define if the camera should move and if so, in each direction.

## Components
- Raspberry Pi 4B, 4GB
- Pi Camera V2
- RPi Ryanteck motor controller 
- 2 Servomotor SG90
- 2 DC motors 

## Programmatical part
- Python
- Qt for the GUI
- Open Cv, cv2 to access pixels map of the Pi Camera
- Pigpio for the pin control

Come see it moving on [youtube](https://youtu.be/DgQnd6pjFc4) ! :dancer:

<img width="600" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=19YppayCzsxNOGmvXjv0PW5tLqpgIL5mb">
