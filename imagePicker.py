from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Communication(QObject):
    transfert_position = pyqtSignal(int, int)
    pixel_selected = pyqtSignal(int, int)
    selecter_leaved = pyqtSignal()

class imagePicker(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView .__init__(self, parent=parent)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.messager = Communication()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.messager.pixel_selected.emit(event.pos().x(), event.pos().y())


    def mouseMoveEvent(self, event):
        self.messager.transfert_position.emit(event.pos().x(), event.pos().y())
        if event.buttons() == Qt.LeftButton:
            self.messager.pixel_selected.emit(event.pos().x(), event.pos().y())


    def leaveEvent(self, event):
        self.messager.selecter_leaved.emit()