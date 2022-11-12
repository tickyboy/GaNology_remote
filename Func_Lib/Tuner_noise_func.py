import pyvisa
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, \
    QPushButton, QFrame
import time
import Ui_Lib.Tuner_noise_calibration as ui
from PyQt5.QtGui import *

class FuncClass_Tuner(QWidget):
    def __init__(self, parent=None):
        super(FuncClass_Tuner, self).__init__(parent)
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)