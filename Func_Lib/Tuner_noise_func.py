import telnetlib
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
        self.log_creation()
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)
        self.ui_form.NF_connect_button.clicked.connect(self.connect_button_clicked)
        self.ui_form.Tuner_init_button.clicked.connect(self.Tunner_initial_function)
        self.setWindowTitle('GaNology Tuner NF Measurement')
        self.setWindowIcon(QIcon('./images/iic.ico'))

    def log_creation(self):
        self.logfile_log = open('C:/Users/Zhoujm_GaN/Desktop/LOG_data.txt', 'w')

    def connect_button_clicked(self):
        self.rm_VNA = pyvisa.ResourceManager()
        self.rm_Spectrum = pyvisa.ResourceManager()
        #==================================connect to VNA==========================================================
        try:
            self.RF_ZNB40 = self.rm_VNA.open_resource('TCPIP0::'+self.ui_form.VNA_IP_edit.text()+'::inst0::INSTR')
            self.RF_ZNB40.write('*RST')
            self.RF_ZNB40.write('*IDN?')
            self.connect_success_text = self.RF_source_SMB100A.read()
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText("Connect Successfully" + "\n" + self.connect_success_text)
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            self.ui_form.textBrowser_LOG.append('['+str(time.ctime(time.time()))+']')
            self.ui_form.textBrowser_LOG.append("Connect Successfully to " + self.connect_success_text)
        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect to VNA(" +self.ui_form.VNA_IP_edit.text()+") Failed" + "\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
            self.ui_form.textBrowser_LOG.append("Connect to VNA(" +self.ui_form.VNA_IP_edit.text()+") Failed" + "\n" + str(e) + "\n")
            pass

            # ==================================connect to Spectrum Analyzer==========================================
            try:
                self.RF_FSV3000 = self.rm_Spectrum.open_resource(
                    'TCPIP0::' + self.ui_form.Spectrum_IP_edit.text() + '::inst0::INSTR')
                self.RF_FSV3000.write('*RST')
                self.RF_FSV3000.write('*IDN?')
                self.connect_success_text = self.RF_source_SMB100A.read()
                box = QMessageBox()
                box.setIcon(1)
                box.setWindowTitle("Message")
                box.setText("Connect Successfully" + "\n" + self.connect_success_text)
                yes = box.addButton('OK', QMessageBox.YesRole)
                no = box.addButton('Cancel', QMessageBox.NoRole)
                box.setIcon(1)
                box.exec_()
                self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
                self.ui_form.textBrowser_LOG.append("Connect Successfully to " + self.connect_success_text)
            except Exception as e:
                box = QMessageBox()
                box.setIcon(3)
                box.setWindowTitle("Message")
                box.setText("Connect to SPA(" +self.ui_form.Spectrum_IP_edit.text()+") Failed" + "\n" + str(e))
                yes = box.addButton('OK', QMessageBox.YesRole)
                no = box.addButton('Cancel', QMessageBox.NoRole)
                box.setIcon(3)
                box.exec_()
                self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
                self.ui_form.textBrowser_LOG.append("Connect to SPA(" +self.ui_form.Spectrum_IP_edit.text()+") Failed" + "\n" + str(e) + "\n")
                pass

                # ==================================connect to Tunner==========================================
                try:
                    self.tn = telnetlib.Telnet(self.ui_form.Tunner_IP_edit.text(), port=23, timeout=10)  # 连接tunner
                    box = QMessageBox()
                    box.setIcon(1)
                    box.setWindowTitle("Message")
                    box.setText("Connect Successfully" + "\n" + self.ui_form.Tunner_IP_edit.text())
                    yes = box.addButton('OK', QMessageBox.YesRole)
                    no = box.addButton('Cancel', QMessageBox.NoRole)
                    box.setIcon(1)
                    box.exec_()
                    self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
                    self.ui_form.textBrowser_LOG.append("Connect Successfully to " + self.ui_form.Tunner_IP_edit.text())
                except Exception as e:
                    box = QMessageBox()
                    box.setIcon(3)
                    box.setWindowTitle("Message")
                    box.setText("Connect to Tunner(" + self.ui_form.Tunner_IP_edit.text() + ") Failed" + "\n" + str(e))
                    yes = box.addButton('OK', QMessageBox.YesRole)
                    no = box.addButton('Cancel', QMessageBox.NoRole)
                    box.setIcon(3)
                    box.exec_()
                    self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
                    self.ui_form.textBrowser_LOG.append(
                        "Connect to Tunner(" + self.ui_form.Tunner_IP_edit.text() + ") Failed" + "\n" + str(e) + "\n")
                    pass

    def Command_func(self, Device, Order, Read_Trigger):
        global Read_Result_Order
        Device.write(Order.encode('UTF-8') + b'\n')
        self.ui_form.textBrowser_LOG.append('2')
        Device.read_until(Read_Trigger.encode('UTF-8'), timeout=60)
        self.ui_form.textBrowser_LOG.append('3')
        Read_Result_Order = Device.read_very_eager().decode('UTF-8')
        self.ui_form.textBrowser_LOG.append('4')
        Read_Result_Order = Read_Result_Order.replace("\r", " ").replace("\n", " ").split(" ")
        temper_list = []
        for index in Read_Result_Order:
            if index == '':
                pass
            else:
                temper_list.append(index)
        Read_Result_Order = temper_list
        return Read_Result_Order

    def Tunner_initial_function(self,device):
        try:
            self.ui_form.textBrowser_LOG.append('1')
            cont = 0

            self.Command_func(device, 'Init', 'Result')  # initialize the tuner
            Check_index = False
            while True:
                cont = cont + 1
                if cont == 100:  # time out conting
                    self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + '] ' + 'Initialization time out')
                    self.logfile_log.write('[' + str(time.ctime(time.time())) + '] ' + 'Initialization time out' + '\n')
                    break
                else:
                    pass
                self.Command_func(device, 'Init?', 'INIT: ')
                Init_query_res = Read_Result_Order
                for terms in Init_query_res:
                    if terms == '0x00':
                        Check_index = True
                        break
                    else:
                        pass
                if Check_index == True:
                    self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + '] ' + "Initialization complete")
                    self.logfile_log.write('[' + str(time.ctime(time.time())) + '] ' + "Initialization complete")
                    break
                else:
                    self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + '] ' + "Initializing")
                    self.logfile_log.write('[' + str(time.ctime(time.time())) + '] ' + "Initializing")
                time.sleep(2)
            self.Command_func(device, 'Pos?', ' ')
            Pos_query_res = Read_Result_Order
            print(Pos_query_res)
        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Error\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + ']')
            self.ui_form.textBrowser_LOG.append("Error\n" + str(e) + "\n")
            pass

