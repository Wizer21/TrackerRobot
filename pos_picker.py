from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Communication(QObject):
    pos_selected = pyqtSignal(int, int)
    pos_leaved = pyqtSignal()

class pos_picker(QLabel):
    def __init__(self, new_parent, size):
        QLabel.__init__(self, new_parent)
        self.messager = Communication()
        self.setFixedSize(QSize(size[0], size[1]))
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)   

        part = round(size[0]/5)

        img = QImage(size[0], size[1], QImage.Format_RGB32)
        img.fill(QColor("#bdbdbd"))

        paint = QPainter(img)
        pen = QPen()
        pen.setWidth(part)
        pen.setColor(QColor("#9e9e9e"))
        paint.setPen(pen)

        paint.drawLine(int(part * 2.5), 0, int(part * 2.5), size[1])
        paint.drawLine(0, int(part * 2.5), size[0], int(part * 2.5))
        
        self.setPixmap(QPixmap.fromImage(img))
        paint.end()

    def enterEvent(self, event):
        test = 0

    def leaveEvent(self, event):
        self.messager.pos_leaved.emit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.messager.pos_selected.emit(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.messager.pos_selected.emit(event.pos().x(), event.pos().y())

    def releaseMouse(self, event):
        self.messager.pos_leaved.emit()
