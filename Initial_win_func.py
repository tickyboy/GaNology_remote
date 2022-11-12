from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QIcon
import Ui_Lib.Initial_win as ui
from PyQt5.QtGui import *


class FunClass_Ini(QWidget):
    def __init__(self, parent=None):
        super(FunClass_Ini, self).__init__(parent)
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('GaNology Remote')
        self.setWindowIcon(QIcon('./images/iic.ico'))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./images/cover.jpg").scaledToWidth(700)))

        self.setPalette(palette)

