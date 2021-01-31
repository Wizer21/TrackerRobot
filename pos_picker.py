from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Communication(QObject):
    pos_selected = pyqtSignal(int, int)
    pos_leaved = pyqtSignal()

class pos_picker(QLabel):
    def __init__(self, new_parent, new_size):
        QLabel.__init__(self, new_parent)
        self.size = new_size
        self.messager = Communication()
        self.setFixedSize(QSize(new_size[0], new_size[1]))
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)   

        part = round(new_size[0]/5)

        img = QImage(new_size[0], new_size[1], QImage.Format_RGB32)
        img.fill(QColor("#212121"))

        paint = QPainter(img)
        pen = QPen()
        pen.setWidth(part)
        pen.setColor(QColor("#262626"))
        paint.setPen(pen)

        paint.drawLine(int(part * 2.5), 0, int(part * 2.5), new_size[1])
        paint.drawLine(0, int(part * 2.5), new_size[0], int(part * 2.5))
        
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
            if not 0 < event.pos().x() < self.size[0] or not 0 < event.pos().y() < self.size[1]:
                self.messager.pos_leaved.emit()
            else:
                self.messager.pos_selected.emit(event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        self.messager.pos_leaved.emit()
