from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class Utils:
    def __init__(self, new_pixelsize, new_resolution):
        global resolution
        global map_size
        global pixmap_dict
        global pixelsize

        width_from_rez = int(new_resolution[1] / 40)
        resolution = new_resolution

        pixelsize = new_pixelsize

        size = [width_from_rez, width_from_rez]
        map_size = [int(size[0] * 2), int(size[1] * 2)]
        pixmap_dict = {
            "camera": self.scale_pixmap("./files/camera.png", map_size[0], map_size[1]),
            "up": self.scale_pixmap("./files/up.png", map_size[0], map_size[1]),
            "right": self.scale_pixmap("./files/right.png", map_size[0], map_size[1]),
            "down": self.scale_pixmap("./files/down.png", map_size[0], map_size[1]),
            "left": self.scale_pixmap("./files/left.png", map_size[0], map_size[1]),
            "pi": self.scale_pixmap("./files/pi.png", map_size[0], map_size[1]),
            "engine": self.scale_pixmap("./files/engine.png", map_size[0], map_size[1])
        }

    def scale_pixmap(self, url, w, h):
        return QPixmap(url).scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    @staticmethod
    def get_pixmap(name):
        return pixmap_dict[name]
    
    @staticmethod
    def get_resized_pixmap(name, ratio):
        return pixmap_dict[name].scaled(int(map_size[0] * ratio), int(map_size[1] * ratio), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    @staticmethod
    def set_icon(widget, pixmap_name, scale):
        widget.setIcon(QIcon(pixmap_dict[pixmap_name]))
        widget.setIconSize(QSize(int(map_size[0] * scale), int(map_size[1] * scale)))

    @staticmethod
    def resize_font(widget, value):
        widget.setStyleSheet("font-size: {0}px;".format(int(pixelsize * value)))

    @staticmethod
    def resize_and_color_font(widget, value, color):
        widget.setStyleSheet("font-size: {0}px; color: {1}; font: bold;".format(int(pixelsize * value), color))

    @staticmethod
    def resize_window_from_resolution(window, ratio_w, ratio_h):
        window.resize(int(resolution[0] * ratio_w), int(resolution[1] * ratio_h))
    
    @staticmethod
    def fixedsize_from_resolution(window, ratio_w, ratio_h):
        window.setFixedSize(int(resolution[0] * ratio_w), int(resolution[1] * ratio_h))



