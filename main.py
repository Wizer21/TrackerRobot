import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from Main_gui import*

if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = Main_gui()
    gui.show()

    with open("./theme.qss") as file:
        theme = file.read()
        app.setStyleSheet(theme)

    sys.exit(app.exec_())