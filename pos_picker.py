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

        self.cursor_off = QCursor()
        self.cursor_on = QCursor()

        self.draw_background()
        self.draw_cursor()

    def draw_background(self):        
        part = round(self.size[0]/5)

        img = QImage(self.size[0], self.size[1], QImage.Format_RGB32)
        img.fill(QColor("#212121"))

        paint = QPainter(img)
        pen = QPen()
        pen.setWidth(part)
        pen.setColor(QColor("#262626"))
        paint.setPen(pen)

        paint.drawLine(int(part * 2.5), 0, int(part * 2.5), self.size[1])
        paint.drawLine(0, int(part * 2.5), self.size[0], int(part * 2.5))
        
        paint.end()
        self.setPixmap(QPixmap.fromImage(img))

    def draw_cursor(self):
        cursor_size = round(self.size[0] / 14)
        img_off = QImage(cursor_size, cursor_size, QImage.Format_ARGB32)
        img_on = QImage(cursor_size, cursor_size, QImage.Format_ARGB32)
        img_off.fill(Qt.transparent)
        img_on.fill(Qt.transparent)
        
        mid = round(cursor_size / 2)

        painter_on = QPainter(img_on)
        painter_off = QPainter(img_off)

        pen_on = QPen()
        pen_off = QPen()
        pen_on.setWidth(cursor_size)
        pen_off.setWidth(cursor_size)
        pen_on.setColor(QColor("#d32f2f"))
        pen_off.setColor(QColor("#616161"))
        pen_on.setCapStyle(Qt.RoundCap)
        pen_off.setCapStyle(Qt.RoundCap)

        painter_on.setPen(pen_on)
        painter_off.setPen(pen_off)

        painter_on.drawPoint(mid, mid)
        painter_off.drawPoint(mid, mid)

        painter_on.end()
        painter_off.end()

        self.cursor_on = QCursor(QPixmap.fromImage(img_on), cursor_size, cursor_size)
        self.cursor_off = QCursor(QPixmap.fromImage(img_off), cursor_size, cursor_size)

    def enterEvent(self, event):
        self.setCursor(self.cursor_off)

    def leaveEvent(self, event):
        self.messager.pos_leaved.emit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.messager.pos_selected.emit(event.pos().x(), event.pos().y())
            self.setCursor(self.cursor_on)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if not 0 < event.pos().x() < self.size[0] or not 0 < event.pos().y() < self.size[1]:
                self.messager.pos_leaved.emit()
            else:
                self.messager.pos_selected.emit(event.pos().x(), event.pos().y())
                self.setCursor(self.cursor_on)

    def mouseReleaseEvent(self, event):
        self.messager.pos_leaved.emit()
        self.setCursor(self.cursor_off)
