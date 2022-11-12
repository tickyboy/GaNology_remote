import pyvisa
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, \
    QPushButton, QFrame
import time
import Ui_Lib.SMB100A_Ui as ui
from PyQt5.QtGui import *


class FuncClass_SMB100A(QWidget):

    # rm = pyvisa.ResourceManager()
    # RF_source_SMB100A = rm.open_resource('TCPIP0::rssmb100a181560::inst0::INSTR')

    def __init__(self, parent=None):
        super(FuncClass_SMB100A, self).__init__(parent)
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)

        self.ui_form.QueryButton.clicked.connect(self.Queryfun)
        self.ui_form.ApplyButton.clicked.connect(self.Frequency_set_fun)
        self.ui_form.CheckButton.clicked.connect(self.Check_show)
        self.ui_form.ClearButton.clicked.connect(self.Clear_logs)
        self.ui_form.doubleSpinBox_freG.editingFinished.connect(self.Frequency_input)
        self.ui_form.doubleSpinBox_freM.editingFinished.connect(self.Frequency_input)
        self.ui_form.doubleSpinBox_pow.editingFinished.connect(self.Frequency_input)
        self.ui_form.textBrowser_log.setPlainText(
            "WARNING: Everytime when you open this window, 'Query' button should be considered to be pressed first to connect the device.\n")
        self.ui_form.RFONButton.clicked.connect(self.RFONfunc)
        self.ui_form.RFOFFButton.clicked.connect(self.RFOFFfunc)
        self.setWindowTitle('GaNology Remote-SMB100A')
        self.setWindowIcon(QIcon('./images/iic.ico'))

    def Queryfun(self):  # 仪表连接测试函数，用于测试某个仪表的VISA连接是否正常
        self.rm = pyvisa.ResourceManager()

        try:
            self.RF_source_SMB100A = self.rm.open_resource('TCPIP0::rssmb100a181560::inst0::INSTR')
            self.RF_source_SMB100A.write('*RST')
            self.RF_source_SMB100A.write('*IDN?')
            # print(RF_source_SMB100A.read())
            self.connect_success_text = self.RF_source_SMB100A.read()
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText("Connect Successfully" + "\n" + self.connect_success_text)
            # 添加按钮，可用中文
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(1)
            box.exec_()
            self.ui_form.textBrowser_log.append("Connect Successfully to " + self.connect_success_text)


        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect Failed" + "\n" + str(e))

            # 添加按钮
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            self.ui_form.textBrowser_log.append("Connect Failed" + "\n" + str(e) + "\n")
            # if box.clickedButton() == yes:
            #    print('OK')
            # else:
            #    print('Cancel')

    def Frequency_input(self):
        return str(self.ui_form.doubleSpinBox_freG.value()), str(self.ui_form.doubleSpinBox_freM.value())
        pass

    def Frequency_set_fun(self):
        # ==========================================================频率设置以及相应大小合理性检测=======================================================================================
        self.set_fre = float(self.ui_form.doubleSpinBox_freG.value()) * 10 ** 9 + float(
            self.ui_form.doubleSpinBox_freM.value()) * 10 ** 6
        if self.set_fre < 100000 or self.set_fre > 40000000000:
            self.ui_form.textBrowser_log.append(
                "Apply Failed\n" + "Frequency should in the range of 100 KHz to 40 GHz, but the current frequency is set to be " + str(
                    self.set_fre / 10 ** 9) + "GHz\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText(
                "Apply Failed\n" + "Frequency should in the range of 100 KHz to 40 GHz, but the current frequency is set to be " + str(
                    self.set_fre / 10 ** 9) + "GHz")
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            return
        else:
            pass
        # =============================================================================================================================================================================

        # ==========================================================功率设置以及相应大小合理性检测=======================================================================================
        self.set_pow = str(self.ui_form.doubleSpinBox_pow.value())  # 功率设置读取
        if float(self.set_pow) > 8:
            self.ui_form.textBrowser_log.append(
                "Apply Failed\n" + "Power level should no more than 8dBm, but the current power level is set to be " + self.set_pow + "dBm\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText(
                "Apply Failed\n" + "Power level should no more than 8dBm, but the current power level is set to be " + self.set_pow + "dBm")
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            return
        else:
            pass
        # =============================================================================================================================================================================

        try:
            self.fre_str = 'SOUR1:FREQ ' + str(self.set_fre) + ' Hz'
            self.RF_source_SMB100A.write(self.fre_str)
            self.pow_str = 'SOUR1:POW ' + self.set_pow + 'dBm'
            self.RF_source_SMB100A.write(self.pow_str)
            time.sleep(1)
            self.ui_form.textBrowser_log.append(
                "Frequency set to " + str(self.set_fre) + ' Hz\n' + "Power set to " + self.set_pow + "dBm\n")
        except Exception as e:
            self.ui_form.textBrowser_log.append("Apply Failed" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Apply Failed" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.")
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()

    def Check_show(self):
        try:
            ###========================检查频率设置并显示结果=======================================
            self.text_content = self.RF_source_SMB100A.query('SOUR1:FREQ?')
            if float(self.text_content) < 1000000:
                self.ui_form.textBrowser_freq.setPlainText(self.text_content)
            elif float(self.text_content) >= 1000000 and float(self.text_content) < 1000000000:
                self.text_content = str(float(self.text_content) / 1000000) + " M"
                self.ui_form.textBrowser_freq.setPlainText(self.text_content)
            elif float(self.text_content) >= 1000000000:
                self.text_content = str(float(self.text_content) / 1000000000) + " G"
                self.ui_form.textBrowser_freq.setPlainText(self.text_content)

            ###=====================检查功率状态并显示结果=========================================
            if self.RF_source_SMB100A.query("OUTP?") == "0\n":
                self.ui_form.textBrowser_powstate.setPlainText("OFF")
                self.power_state_recoder = "OFF"
            elif self.RF_source_SMB100A.query("OUTP?") == "1\n":
                self.ui_form.textBrowser_powstate.setPlainText("ON")
                self.power_state_recoder = "ON"

            ###=========================检查功率设置并显示结果======================================
            self.ui_form.textBrowser_pow.setPlainText(self.RF_source_SMB100A.query('SOUR1:POW?'))

            self.ui_form.textBrowser_log.append("States: Frequency: " + self.text_content + "Hz\n" + "Power: " + str(
                float(self.RF_source_SMB100A.query(
                    'SOUR1:POW?'))) + "dBm\n" + "Power: " + self.power_state_recoder + "\n")


        except Exception as e:
            self.ui_form.textBrowser_log.append("Fail to read data from the device" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Fail to read data from the device" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.")

            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()

    def RFONfunc(self):
        try:
            self.RF_source_SMB100A.write("OUTP ON")
            self.ui_form.textBrowser_log.append("RF ON")
        except Exception as e:
            self.ui_form.textBrowser_log.append("Fail to turn RF source on" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Fail to turn RF source on" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.")

            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            pass

    def RFOFFfunc(self):
        try:
            self.RF_source_SMB100A.write("OUTP OFF")
            self.ui_form.textBrowser_log.append("RF OFF")
        except Exception as e:
            self.ui_form.textBrowser_log.append("Fail to turn RF source off" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.\n")
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Fail to turn RF source off" + "\nErrorCode: " + str(
                e) + "\nConnection may lost. Check the connection and click the 'Query' button to reconnect to the device.")

            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            # 设置消息框中内容前面的图标
            box.setIcon(3)
            box.exec_()
            pass

    def Clear_logs(self):
        box = QMessageBox()
        box.setIcon(2)
        box.setWindowTitle("Message")
        box.setText("Are you sure to clear the log?")
        yes = box.addButton('OK', QMessageBox.YesRole)
        no = box.addButton('Cancel', QMessageBox.NoRole)
        # 设置消息框中内容前面的图标
        box.setIcon(2)
        box.exec_()

        if box.clickedButton() == yes:
            self.ui_form.textBrowser_log.clear()
        else:
            pass
        pass
