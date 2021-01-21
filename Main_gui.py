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

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.camera_image = QImage()
        self.range_color = 30
        self.tracking_on = False
        self.shape = Dynamic_shape()
        self.midColor = (0, 0, 0)
        self.pen_size = 3
        # PI THREAD
        self.servo_thread_x = ServoThread(3)
        self.servo_thread_y = ServoThread(8)
        self.thread_camera = CameraThread()

        self.widgetMain = QWidget(self)
        self.layoutMain = QGridLayout(self)
        self.viewDisplayCamera = imagePicker(self)
        self.sceneDisplayCamera = QGraphicsScene(self)

        self.layoutPanel = QGridLayout(self)

        self.layoutColor = QGridLayout(self)
        self.labelColorTitle = QLabel("Color", self)
        self.labelColorHover = QLabel("hover", self)
        self.labelColorMIN= QLabel("min", self)
        self.labelColorMID = QLabel("mid", self)
        self.labelColorMAX = QLabel("max", self)
        self.sliderColorRange = QSlider(self)

        self.widgetControl = controlWidget(self)

        self.build()
        self.run_camera()
        self.resize(700, 700)


    def build(self):
        # BUILD
        self.setCentralWidget(self.widgetMain)
        self.widgetMain.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.viewDisplayCamera, 0, 1)

        self.layoutMain.addLayout(self.layoutPanel, 0, 0)
        self.layoutPanel.addLayout(self.layoutColor, 0, 0)
        
        self.layoutColor.addWidget(self.labelColorTitle, 0, 0, 1, 3)
        self.layoutColor.addWidget(self.labelColorHover, 1, 0, 1, 3)
        self.layoutColor.addWidget(self.labelColorMIN, 2, 0)
        self.layoutColor.addWidget(self.labelColorMID, 2, 1)
        self.layoutColor.addWidget(self.labelColorMAX, 2, 2)
        self.layoutColor.addWidget(self.sliderColorRange, 3, 0, 1, 3)

        self.layoutPanel.addLayout(self.layoutColor, 0, 0)

        self.layoutPanel.addWidget(self.widgetControl, 1, 0)

        # PARAMETER
        self.sliderColorRange.setOrientation(Qt.Horizontal)
        self.layoutPanel.setAlignment(Qt.AlignTop)
        self.viewDisplayCamera.setScene(self.sceneDisplayCamera)
        
        # Motors
        self.widgetControl.messager.xIsMoveUp.connect(self.cameraMoveFromPlayer_X)
        self.widgetControl.messager.yIsMoveUp.connect(self.cameraMoveFromPlayer_Y)

        self.viewDisplayCamera.messager.pixel_selected.connect(self.color_clicked)
        self.viewDisplayCamera.messager.transfert_position.connect(self.color_hover)
        self.viewDisplayCamera.messager.selecter_leaved.connect(self.color_leaved)
        self.thread_camera.messager.cameraImages.connect(self.display_camera)
        self.thread_camera.messager.cameraSize.connect(self.set_up_view)

    def set_up_view(self, w, h):
        self.viewDisplayCamera.setFixedSize(QSize(w, h))

    # START CAMERA THREAD
    def run_camera(self):
        self.thread_camera.start()

    # SET QIMAGE FROM CAMERA THREAD
    def display_camera(self, img, ndarray):  
        self.camera_image = img

        self.sceneDisplayCamera.clear() 

        self.sceneDisplayCamera.addPixmap(QPixmap.fromImage(img))

        if self.tracking_on:
            data = cam_tracker(ndarray)            
            self.shape.build(data[0], data[1], data[2], data[3], data[4])
            self.draw_shape()
            print("adaptive color " + str(data[5]))
          
    def cameraMoveFromPlayer_X(self, isUp):
        if isUp:
            self.servo_thread_x.callMovement(True)
        else:
            self.servo_thread_x.callMovement(False)

    def cameraMoveFromPlayer_Y(self, isUp):
            if isUp:
                self.servo_thread_y.callMovement(True)
            else:
                self.servo_thread_y.callMovement(False)


    # COLOR PICKER CONNECTION
    def color_clicked(self, x, y):
        pix = QPixmap(self.labelColorMID.size())
        pixel = self.camera_image.pixelColor(x, y)
        pix.fill(QColor(pixel.red(), pixel.green(), pixel.blue()))        
        new_pos(x, y, (pixel.red(), pixel.green(), pixel.blue()), self.range_color)  

        self.labelColorMID.setPixmap(pix)
        self.calculate_and_display_color_range([pixel.red(), pixel.green(), pixel.blue()])

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

    def calculate_and_display_color_range(self, RGB):
        self.midColor = RGB

        pix = QPixmap(self.labelColorMIN.size())

        # SET MIN COLOR
        color = [RGB[0] - self.range_color, RGB[1] - self.range_color, RGB[2] - self.range_color]
        for it in color:
            if it < 0:
                it = 0

        pix.fill(QColor(color[0], color[1], color[2]))        
        self.labelColorMIN.setPixmap(pix)

        # SET MAX COLOR
        color = [RGB[0] + self.range_color, RGB[1] + self.range_color, RGB[2] + self.range_color]
        for it in color:
            if it > 255:
                it = 255

        pix.fill(QColor(color[0], color[1], color[2]))   
        self.labelColorMAX.setPixmap(pix)

    def draw_shape(self):
        color_points = QPen(QColor("#ffffff"))
        color_points.setWidth(self.pen_size)
        color_square = QPen(QColor("#ff0048"))
        color_square.setWidth(self.pen_size)
        color_middle = QPen(QColor("#0084ff"))
        color_middle.setWidth(self.pen_size)
        middle_width = 10

        points = self.shape.points
        for i in range(len(self.shape.points)):
            self.sceneDisplayCamera.addLine(points[i][0] - self.pen_size, points[i][1], points[i][0] + self.pen_size, points[i][1], color_points)
            self.sceneDisplayCamera.addLine(points[i][0], points[i][1] - self.pen_size, points[i][0], points[i][1] + self.pen_size, color_points)
     
        self.sceneDisplayCamera.addRect(self.shape.top_left[0], self.shape.top_left[1], self.shape.width, self.shape.height, color_square)
        
        self.sceneDisplayCamera.addLine(self.shape.center[0] - middle_width, self.shape.center[1], self.shape.center[0] + middle_width, self.shape.center[1], color_middle)
        self.sceneDisplayCamera.addLine(self.shape.center[0], self.shape.center[1] - middle_width, self.shape.center[0], self.shape.center[1] + middle_width, color_middle)

