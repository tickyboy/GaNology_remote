import pyvisa
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, \
    QPushButton, QFrame
import time
import Ui_Lib.ZNB40_Ui as ui
from PyQt5.QtGui import *


class FuncClass_ZNB40(QWidget):

    # rm = pyvisa.ResourceManager()
    # RF_source_SMB100A = rm.open_resource('TCPIP0::rssmb100a181560::inst0::INSTR')

    def __init__(self, parent=None):
        super(FuncClass_ZNB40, self).__init__(parent)
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)
        self.ui_form.Apply_freq_swp_pushButton.clicked.connect(self.FreqApplyButton_clicked)

    def connectfunction(self):
        try:
            self.rm = pyvisa.ResourceManager()
            self.RF_source_ZNB40 = self.rm.open_resource('TCPIP0::rssmb100a181560::inst0::INSTR')
            self.RF_source_ZNB40.write('*RST')
            self.RF_source_ZNB40.write('*IDN?')
            self.connect_success_text = self.RF_source_ZNB40.read()
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText("Connect Successfully" + "\n" + self.connect_success_text)
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            self.ui_form.textBrowser_log.append("Connect Successfully to " + self.connect_success_text)

        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect Failed" + "\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            self.ui_form.textBrowser_log.append("Connect Failed" + "\n" + str(e) + "\n")

    def FreqApplyButton_clicked(self):
        print(self.check_input(self.ui_form.lineEdit_start_fre.text(), 'Start Frequency', 100000, 40000000000))
        print(self.check_input(self.ui_form.lineEdit_stop_fre.text(), 'Stop Frequency', 100000, 40000000000))
        print(self.check_input(self.ui_form.lineEdit_step_fre.text(), 'Step Frequency', 10, 40000000000))
        print(self.check_input(self.ui_form.lineEdit_center_fre.text(), 'Center Frequency', 100000, 40000000000))
        print(self.check_input(self.ui_form.lineEdit_span_fre.text(), 'Span Frequency', 1, 40000000000))



    def command_record(self):
        self.RF_source_ZNB40.write('SENS1:SWE:TYPE LIN')#LIN for linear frequency sweep; POW for power sweep; LOG for Logarithmic frequency sweep; time sweep CW; segmented frequency sweep SEGM
        #frequency sweep commands records
        self.RF_source_ZNB40.write('SENS1:FREQ:STAR 10MHz')
        self.RF_source_ZNB40.write('SENS1:FREQ:STOP 10MHz')
        self.RF_source_ZNB40.write('SENS1:FREQ:CENT 10MHz')
        self.RF_source_ZNB40.write('SENS1:SWE:STEP 10MHz')#POIN?
        self.RF_source_ZNB40.write('SENS1:FREQ:SPAN 10MHz')#0.1KHz increment

        self.RF_source_ZNB40.write('SENS1:FREQ:FIX 10MHz')
        self.RF_source_ZNB40.write('SENS1:SWE:TYPE POW')
        self.RF_source_ZNB40.write('SOUR1:POW:START 0')
        self.RF_source_ZNB40.write('SOUR1:POW:STOP 1')
        self.RF_source_ZNB40.write('SENS1:SWE:POIN 201')
        self.RF_source_ZNB40.write('SOUR1:POW:STAT ON/OFF')

        self.RF_source_ZNB40.write('SENS1:BWID 1.1KHz')
        self.RF_source_ZNB40.write('SENS1:AVER ON')
        self.RF_source_ZNB40.write('SENS1:AVER:COUN 1000')

    def check_input(self, input_string, name_of_lineEdit, low_limit, up_limit):
        try:
            input_string_list = input_string.split('.')
            if len(input_string_list) == 1:
                digit_input_string = ''.join(list(filter(str.isdigit, input_string_list[0])))#抽取输入字符串当中的数字信息
                digit_input_string = float(digit_input_string)  # 转为浮点数验证输入频率
                alpha_input_string = ''.join(list(filter(str.isalpha, input_string_list[0])))  # 抽取输入字符串当中的字母信息
            elif len(input_string_list) == 2:
                digit_input_string_index0 = ''.join(list(filter(str.isdigit, input_string_list[0])))
                digit_input_string = ''.join(list(filter(str.isdigit, input_string_list[1])))  # 抽取输入字符串当中的数字信息
                digit_input_string = float(digit_input_string_index0 + '.' + digit_input_string)#转为浮点数验证输入频率
                alpha_input_string = ''.join(list(filter(str.isalpha, input_string_list[1])))#抽取输入字符串当中的字母信息

            #---------------数字化输入字符串-------------------------------
            if alpha_input_string == 'k' or alpha_input_string == 'K':
                input_freq = digit_input_string * 1000
            elif alpha_input_string == 'm' or alpha_input_string == 'M':
                input_freq= digit_input_string * 1000000
            elif alpha_input_string == 'g' or alpha_input_string == 'G':
                input_freq = digit_input_string * 1000000000
            else:
                input_freq = digit_input_string
                pass

            #--------------检查输入频率大小是否在合理输入范围---------------------
            if input_freq < low_limit or input_freq > up_limit:
                box = QMessageBox()
                box.setIcon(3)
                box.setWindowTitle(f'{name_of_lineEdit}')
                box.setText(f'Apply Failed\nPlease ensure the {name_of_lineEdit} is in the rational range for the VNA')
                yes = box.addButton('OK', QMessageBox.YesRole)
                no = box.addButton('Cancel', QMessageBox.NoRole)
                # 设置消息框中内容前面的图标
                box.setIcon(3)
                box.exec_()
            else:
                return(str(digit_input_string) + alpha_input_string)
        except:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle(f'{name_of_lineEdit}')
            box.setText('Check Your Input !')
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            return



    #    self.ui_form.checkBox.stateChanged.connect(self.singlecheck_1)
    #    self.ui_form.checkBox_2.stateChanged.connect(self.singlecheck_2)
    #def singlecheck_1(self):
    #    if self.ui_form.checkBox.isChecked() == True:
    #        self.ui_form.checkBox_2.setChecked(False)
    #    else:
    #        pass
    #def singlecheck_2(self):
    #    if self.ui_form.checkBox_2.isChecked() == True:
    #        self.ui_form.checkBox.setChecked(False)
    #    else:
    #        pass

