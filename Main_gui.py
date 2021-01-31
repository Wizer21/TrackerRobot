from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from ServoThread import*
from CameraThread import*
from imagePicker import*
from tracker import *
from shape import*
from numpy import *
from controlWidget import*
import os
from MotorThread import*
from controllerXbox import*
from Utils import*


class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.camera_image = QImage()
        self.range_color = 30
        self.tracking_on = False
        self.shape = Dynamic_shape()
        self.midColor = (0, 0, 0)
        self.pen_size = 5
        self.servo_tracking = False
        self.heatTimer = QTimer()
        # PI THREAD
        self.servo_thread_x = ServoThread(24)
        self.servo_thread_y = ServoThread(4)
        self.thread_camera = CameraThread()
        self.motor_thread = MotorThread()
        self.controller_xbox = controllerXbox()

        self.widgetMain = QWidget(self)
        self.layoutMain = QGridLayout(self)
        self.viewDisplayCamera = imagePicker(self)
        self.sceneDisplayCamera = QGraphicsScene(self)

        self.layoutPanel = QGridLayout(self)

        self.layoutColor = QGridLayout(self)
        self.labelColorTitle = QLabel("Color", self)
        self.labelColorHover = QLabel(self)
        self.labelColorMIN = QLabel(self)
        self.labelColorMID = QLabel(self)
        self.labelColorMAX = QLabel(self)
        self.sliderColorRange = QSlider(self)

        self.widgetControl = controlWidget(self)

        self.check_servo_tracking = QCheckBox("Item tracking", self)

        self.label_icon_pi = QLabel(self)
        self.label_heat = QLabel("0°", self)

        self.build()
        self.run_camera()
        self.resize(700, 700)
        self.heatTimer.start(1000)
        self.calculate_and_display_color_range()


    def build(self):
        # BUILD
        self.setCentralWidget(self.widgetMain)
        self.widgetMain.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.viewDisplayCamera, 0, 1)

        self.layoutMain.addLayout(self.layoutPanel, 0, 0)
        self.layoutPanel.addLayout(self.layoutColor, 0, 0, 1, 2)
        
        self.layoutColor.addWidget(self.labelColorTitle, 0, 0, 1, 3)
        self.layoutColor.addWidget(self.labelColorHover, 1, 0, 1, 3)
        self.layoutColor.addWidget(self.labelColorMIN, 2, 0)
        self.layoutColor.addWidget(self.labelColorMID, 2, 1)
        self.layoutColor.addWidget(self.labelColorMAX, 2, 2)
        self.layoutColor.addWidget(self.sliderColorRange, 3, 0, 1, 3)

        self.layoutPanel.addWidget(self.widgetControl, 1, 0, 1, 2)

        self.layoutPanel.addWidget(self.check_servo_tracking, 2, 0, 1, 2)

        self.layoutPanel.addWidget(self.label_icon_pi, 3, 0, Qt.AlignTop)
        self.layoutPanel.addWidget(self.label_heat, 3, 1)

        # PARAMETER
        self.sliderColorRange.setOrientation(Qt.Horizontal)
        self.sliderColorRange.setValue(self.range_color)
        self.sliderColorRange.setRange(0, 50)
        self.viewDisplayCamera.setScene(self.sceneDisplayCamera)
        self.label_icon_pi.setPixmap(Utils.get_resized_pixmap("pi", 0.8))
        self.layoutPanel.setAlignment(Qt.AlignTop)
        self.layoutPanel.setColumnStretch(0, 0)
        self.layoutPanel.setColumnStretch(1, 1)
        Utils.resize_font(self.label_heat, 2)
        Utils.resize_font(self.check_servo_tracking, 1.5)

        # SERVOS
        self.widgetControl.messager.servo_x_move.connect(self.camera_move_x_from_widget)
        self.widgetControl.messager.servo_y_move.connect(self.camera_move_y_from_widget)
        self.widgetControl.messager.servo_x_released.connect(self.camera_stop_x_from_widget)
        self.widgetControl.messager.servo_y_released.connect(self.camera_stop_y_from_widget)
        self.controller_xbox.messager.servo_move.connect(self.servos_move_controller)
        self.controller_xbox.messager.servo_stop.connect(self.x_motor_stop)
        self.controller_xbox.messager.servo_stop.connect(self.y_motor_stop)

        # MOTOR
        self.widgetControl.messager.motor_move.connect(self.motor_move_from_widget)
        self.widgetControl.messager.motor_released.connect(self.motor_leaved_from_widget)
        self.controller_xbox.messager.motor_move.connect(self.moveRobot)
        self.controller_xbox.messager.motor_stop.connect(self.stop_motor)
        self.controller_xbox.messager.speed_set.connect(self.set_motor_speed)

        # CAMERA 
        self.thread_camera.messager.cameraImages.connect(self.display_camera)
        self.thread_camera.messager.cameraSize.connect(self.set_up_view)

        # COLOR PICKER
        self.viewDisplayCamera.messager.pixel_selected.connect(self.color_clicked)
        self.viewDisplayCamera.messager.transfert_position.connect(self.color_hover)
        self.viewDisplayCamera.messager.selecter_leaved.connect(self.color_leaved)

        # HEAT TIMER
        self.heatTimer.timeout.connect(self.update_heat)

        # SERVO TRACKING
        self.check_servo_tracking.stateChanged.connect(self.toggle_servo_tracking)

        # WIDGET 
        self.sliderColorRange.valueChanged.connect(self.update_color_range)

    def set_up_view(self, w, h):
        self.viewDisplayCamera.setFixedSize(QSize(int(w * 1.03), int(h * 1.03)))

    # START CAMERA THREAD
    def run_camera(self):
        self.thread_camera.start()

    # SET QIMAGE FROM CAMERA THREAD
    def display_camera(self, img, ndarray):  
        self.camera_image = img

        if self.tracking_on:
            data = cam_tracker(ndarray)            
            # UPDATE REDRESH
            self.shape.build(data[0], data[1], data[2], data[3], data[4])

            # DRAW RECT/POINTS INDICATOR
            self.draw_shape()

            # REFRESH MID COLOR
            self.midColor = data[5]
            # CALCULATE MIN AND MAX RGB
            self.calculate_and_display_color_range()
            
            # MOVE SERVOS BASE ON THE ITEM POSITION
            if self.servo_tracking:
                self.calc_shape_position()
        
        self.sceneDisplayCamera.clear() 
        self.sceneDisplayCamera.addPixmap(QPixmap.fromImage(self.camera_image))
          
    def camera_move_x_from_widget(self, position):
        self.servo_thread_x.callMovement(position)

    def camera_move_y_from_widget(self, position):
        self.servo_thread_y.callMovement(-position)

    def camera_stop_x_from_widget(self):
        self.servo_thread_x.run_servo = False

    def camera_stop_y_from_widget(self):
        self.servo_thread_y.run_servo = False
              
    def motor_move_from_widget(self, position):
        if position[1] > 0:
            is_forward = False
            self.motor_thread.motor_speed = round(position[1] / 1.25)
        elif position[1] < 0:
            is_forward = True
            self.motor_thread.motor_speed = -round(position[1] / 1.25)
        else:
            is_forward = True
            self.motor_thread.motor_speed = 100


        print("MOTOR SPEED " + str(self.motor_thread.motor_speed))
        print("ORIENTATION " + str(position[0]))
        print("MAIN GUI rotation " + str(position[0]) + " " + str(is_forward))
        self.motor_thread.callMovement(-position[0], is_forward)

    def motor_leaved_from_widget(self):
        self.motor_thread.run_motor = False

    # COLOR PICKER CONNECTION
    def color_clicked(self, x, y):
        # SET COLOR
        pixel = self.camera_image.pixelColor(x, y)
        self.midColor = [pixel.red(), pixel.green(), pixel.blue()]
        self.calculate_and_display_color_range()

        # START TRACKING 
        new_pos(x, y, (pixel.red(), pixel.green(), pixel.blue()), self.range_color) 

        self.tracking_on = True

    # COLOR PICKER CONNECTION
    def color_hover(self, x, y):
        test = 0
        # pix = QPixmap(self.labelColorMID.size())
        # pixel = self.camera_image.pixelColor(x, y)        
        # pix.fill(QColor(pixel.red(), pixel.green(), pixel.blue()))     
        # self.labelColorHover.setPixmap(pix)

    # COLOR PICKER CONNECTION
    def color_leaved(self): 
        self.labelColorHover.clear()

    def calculate_and_display_color_range(self):
        # SET MID COLOR
        pix = QPixmap(self.labelColorMID.size())
        
        pix.fill(QColor(self.midColor[0], self.midColor[1], self.midColor[2]))        
        self.labelColorMID.setPixmap(pix)

        # SET MIN COLOR
        color = [self.midColor[0] - self.range_color, self.midColor[1] - self.range_color, self.midColor[2] - self.range_color]
        for it in color:
            if it < 0:
                it = 0

        pix.fill(QColor(color[0], color[1], color[2]))        
        self.labelColorMIN.setPixmap(pix)

        # SET MAX COLOR
        color = [self.midColor[0] + self.range_color, self.midColor[1] + self.range_color, self.midColor[2] + self.range_color]
        for it in color:
            if it > 255:
                it = 255

        pix.fill(QColor(color[0], color[1], color[2]))   
        self.labelColorMAX.setPixmap(pix)

    def draw_shape(self):
        paint = QPainter(self.camera_image)
        pen = QPen()
        pen.setWidth(self.pen_size)

        pen.setColor(QColor("#ff0048"))
        paint.setPen(pen)
        paint.drawRect(self.shape.top_left[0], self.shape.top_left[1], self.shape.width, self.shape.height)

        pen.setColor(QColor("#ffffff"))
        paint.setPen(pen)
        for point in self.shape.points:
            paint.drawPoint(point[0], point[1])
        
        pen.setColor(QColor("#0084ff"))
        paint.setPen(pen)
        paint.drawPoint(self.shape.center[0], self.shape.center[1])
        paint.end()


    def toggle_servo_tracking(self, state):
        if state == 2:
            self.servo_tracking = True        
        else:
            self.servo_tracking = False
            self.servo_thread_x.run_servo = False
            self.servo_thread_y.run_servo = False

    def calc_shape_position(self):
        render_size = self.camera_image.size()
        position = self.shape.center

        width_part = int(render_size.width() / 3)
        height_part = int(render_size.height() / 3)

        if position[0] < width_part:
            if not self.servo_thread_x.quick_movement(5):
                self.motor_thread.quick_motor_move("left")
        elif position[0] > int(width_part * 2):
            if not self.servo_thread_x.quick_movement(-5):
                self.motor_thread.quick_motor_move("right")
        else:
            self.servo_thread_x.run_servo = False
            
        if position[1] < height_part:
            self.servo_thread_y.quick_movement(-5)
        elif position[1] > int(height_part * 2):
            self.servo_thread_y.quick_movement(5)
        else:
            self.servo_thread_y.run_servo = False

    def update_heat(self):
        output = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        val = output[5:].replace("C", "")
        val = val.replace("/n", "")
        val = val.replace("'", "")
        val = float(val[:-1])

        self.label_heat.setText(output[5:])
        if val >= 75:
            Utils.resize_and_color_font(self.label_heat, 2, "#d32f2f")
        else:
            Utils.resize_and_color_font(self.label_heat, 2, "white")
            
        self.heatTimer.start(1000)
        
    def moveRobot(self, position):
        if position[1] < 32767.5:
            is_forward = True
        else:
            is_forward = False

        self.motor_thread.callMovement(round((position[0] - 32767.5) / 262.14), is_forward)

    def stop_motor(self):
        self.motor_speed = 0
        self.motor_thread.run_motor = False

    def x_motor_stop(self):
        self.servo_thread_x.run_servo = False
    
    def y_motor_stop(self):
        self.servo_thread_y.run_servo = False

    def servos_move_controller(self, position):
        x = (position[0] - 32767.5) / 3276.7
        x = -x
        self.servo_thread_x.callMovement(x)
        self.servo_thread_y.callMovement((position[1] - 32767.5) / 3276.7)

    def update_color_range(self, slider_value):
        self.range_color = slider_value
        new_color_range(slider_value)

        if not self.tracking_on:
            self.calculate_and_display_color_range()

    def set_motor_speed(self, value):
        self.motor_thread.update_speed(round(value / 10.23))