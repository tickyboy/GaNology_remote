import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Ui_Lib.GaNology_remote_control as Main_Ui
import Ui_Lib.SMA100B_Ui as SMA100B_Ui
import Ui_Lib.SMB100A_Ui as SMB100A_Ui
import Ui_Lib.ZNB40_Ui as ZNB40_Ui
from Func_Lib.SMB100A_func import FuncClass_SMB100A as SMB100A_Window
from Func_Lib.FSV_func import FuncClass_FSV as FSV7G_Window
from Func_Lib.ZNB_func import FuncClass_ZNB40 as ZNB40_Window
from Initial_win_func import FunClass_Ini as Initial_win
from Func_Lib.Tuner_noise_func import FuncClass_Tuner as NF_Tuner_Window
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import Ui_Lib.Initial_win as ui
import Ui_Lib.Initial_win as ui
from PyQt5.QtGui import *
import ctypes



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Main_Ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionSMB100A.triggered.connect(self.slot_smb100a)
        self.ui.actionSMA100B.triggered.connect(self.slot_sma100b)
        self.ui.actionZNB40.triggered.connect(self.slot_znb40)
        self.ui.actionFSV7G.triggered.connect(self.slot_fsv7g)
        self.ui.actionNF_Sourcepull.triggered.connect(self.slot_NF)
        self.setWindowTitle('GaNology Remote')
        self.setWindowIcon(QIcon('./images/iic.ico'))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setStyleSheet("#MainWindow{border-image:url(./images/cover.jpg);}")

    def slot_smb100a(self):
        smb100a_ui.show()

    def slot_sma100b(self):
        sma100b_ui.show()

    def slot_znb40(self):
        znb40_ui.show()

    def slot_fsv7g(self):
        fsv7g_ui.show()

    def slot_NF(self):
        nf_tuner_ui.show()


class SMA100B_Window(QMainWindow):
    def __init__(self, parent=None):
        super(SMA100B_Window, self).__init__(parent)
        self.ui = SMA100B_Ui.Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_ui = MainWindow()
    Initial_Win = Initial_win()
    Initial_Win.show()

    timer = QTimer()
    timer.start(3000)
    timer.timeout.connect(Initial_Win.close)
    timer.timeout.connect(main_ui.show)


    smb100a_ui = SMB100A_Window()
    sma100b_ui = SMA100B_Window()
    znb40_ui = ZNB40_Window()
    fsv7g_ui = FSV7G_Window()
    nf_tuner_ui = NF_Tuner_Window()

    sys.exit(app.exec_())
