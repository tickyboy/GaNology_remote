import telnetlib
import pyvisa, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import (QApplication, QWidget, QPushButton, QThread)
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
        self.ui_form.Calibration_button.clicked.connect(self.Calibration_clicked)
        self.ui_form.Tuner_init_button.clicked.connect(self.Tunner_initial_function)
        self.setWindowTitle('GaNology Tuner NF Measurement')
        self.setWindowIcon(QIcon('./images/iic.ico'))

    def wait_function(self, Check_list):
        # 保证上一个命令（移动）已经完成才向tuner发送下一个命令，防止命令冲突
        Check_index = True
        while Check_index:
            for index in Check_list:
                if index == 'completed':
                    Check_index = False
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + 'Moving job completed')
                else:
                    time.sleep(1)

    def wait_visa_command(self, Device, complete_message):
        Check_status = True
        while Check_status:
            try:
                Device.write('*OPC?')
                Read_status = Device.read()
                Check_status = False
                time.sleep(1)
            except:
                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + " Visa processing")
                time.sleep(1)
                continue
        if complete_message == '':
            pass
        else:
            self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + complete_message)

    def log_creation(self):
        self.logfile_log = open('E:/ITuner_data/LOG_DATA/'+str(time.ctime(time.time())).replace(':','_').replace(' ','_')+'_LOG_data.txt', 'w')

    def LOG_record(self,text):
        QApplication.processEvents()
        self.ui_form.textBrowser_LOG.append(text)
        QApplication.processEvents()
        self.logfile_log.write(text + '\n')

    def connect_button_clicked(self):
        self.rm_VNA = pyvisa.ResourceManager()
        self.rm_Spectrum = pyvisa.ResourceManager()
        #==================================connect to VNA==========================================================
        try:
            self.RF_ZNB40 = self.rm_VNA.open_resource('TCPIP0::'+self.ui_form.VNA_IP_edit.text()+'::inst0::INSTR')
            self.RF_ZNB40.write('*RST')
            self.RF_ZNB40.write('*IDN?')
            self.connect_success_text = self.RF_ZNB40.read()
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText("Connect Successfully" + "\n" + self.connect_success_text)
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            self.LOG_record('['+str(time.ctime(time.time()))+'] '+"Connect Successfully to " + self.connect_success_text)

        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect to VNA(" +self.ui_form.VNA_IP_edit.text()+") Failed" + "\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+
                            "Connect to VNA(" +self.ui_form.VNA_IP_edit.text()+") Failed" + "\n" + str(e) + "\n")
            pass

            # ==================================connect to Spectrum Analyzer==========================================
        try:
            self.RF_FSV3000 = self.rm_Spectrum.open_resource(
                'TCPIP0::' + self.ui_form.Spectrum_IP_edit.text() + '::inst0::INSTR')
            self.RF_FSV3000.write('*RST')
            self.RF_FSV3000.write('*IDN?')
            self.connect_success_text = self.RF_FSV3000.read()
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText("Connect Successfully" + "\n" + self.connect_success_text)
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            self.LOG_record(
                '[' + str(time.ctime(time.time())) + '] ' + "Connect Successfully to " + self.connect_success_text)
        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect to SPA(" +self.ui_form.Spectrum_IP_edit.text()+") Failed" + "\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.LOG_record('[' + str(time.ctime(time.time())) + '] ' +
                            "Connect to SPA" + self.ui_form.VNA_IP_edit.text() + ") Failed" + "\n" + str(e) + "\n")
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
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+"Connect Successfully to " + self.ui_form.Tunner_IP_edit.text())
        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText("Connect to Tunner(" + self.ui_form.Tunner_IP_edit.text() + ") Failed" + "\n" + str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+"Connect to Tunner("
                            + self.ui_form.Tunner_IP_edit.text() + ") Failed" + "\n" + str(e) + "\n")

            pass

    def Command_func(self, Device, Order, Read_Trigger):
        global Read_Result_Order
        Device.write(Order.encode('UTF-8') + b'\n')
        Device.read_until(Read_Trigger.encode('UTF-8'), timeout=60)
        Read_Result_Order = Device.read_very_eager().decode('UTF-8')
        Read_Result_Order = Read_Result_Order.replace("\r", " ").replace("\n", " ").split(" ")
        temper_list = []
        for index in Read_Result_Order:
            if index == '':
                pass
            else:
                temper_list.append(index)
        Read_Result_Order = temper_list
        return Read_Result_Order

    def Tunner_initial_function(self):

        try:
            cont = 0
            self.Command_func(self.tn, 'Init', 'Result')  # initialize the tuner
            Check_index = False
            while True:
                cont = cont + 1
                if cont == 100:  # time out conting
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + 'Initialization time out')
                    #self.ui_form.textBrowser_LOG.append('[' + str(time.ctime(time.time())) + '] ' + 'Initialization time out')
                    #self.logfile_log.write('[' + str(time.ctime(time.time())) + '] ' + 'Initialization time out' + '\n')
                    break
                else:
                    pass
                self.Command_func(self.tn, 'Init?', 'INIT: ')
                Init_query_res = Read_Result_Order
                for terms in Init_query_res:
                    if terms == '0x00':
                        Check_index = True
                        break
                    else:
                        pass
                if Check_index == True:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + "Initialization complete")
                    break
                else:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + "Initializing")
                time.sleep(2)
            self.Command_func(self.tn, 'Pos?', ' ')
            Pos_query_res = Read_Result_Order
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

    def Calibration_clicked(self):
        self.freq_start = self.ui_form.freq_start_edit.text()
        self.freq_step = self.ui_form.freq_step_edit.text()
        self.freq_stop = self.ui_form.freq_stop_edit.text()
        self.preamp = self.ui_form.preamp_edit.text()
        self.cali_num = self.ui_form.Cal_number_edit.text()
        self.max_pos = self.ui_form.Max_POS_edit.text()
        self.VNA_SET = self.ui_form.VNA_SET_edit.text()
        self.Calpoint = self.ui_form.Calpoint_edit.text()

        box = QMessageBox()
        box.setIcon(1)
        box.setWindowTitle("Settings Configeration")
        box.setText("Please Check the settings for the NF measurement:\n"+"Frequency:"+self.freq_start
                    +" to "+self.freq_stop+"\n"+"Frequency Step:"+self.freq_step+"\n"+"VNA SET Name:"+self.VNA_SET+'\n'
                    +'Calibration ID:'+self.cali_num+'\n'+'Preamplifier:'+self.preamp)
        yes = box.addButton('Begin', QMessageBox.YesRole)
        no = box.addButton('Change Settings', QMessageBox.NoRole)
        box.setIcon(1)
        box.exec_()
        if box.clickedButton() == yes:
            self.BeginCal()
        else:
            pass

    def BeginCal(self):


        try:
            # =========================建立Noise测试channel===========================
            self.RF_FSV3000.write("INST:CRE:NEW NOISE, 'Noise'")
            self.wait_visa_command(self.RF_FSV3000, 'Noise Channel Setting completed')
            self.RF_FSV3000.write("SENS:FREQ:STAR "+self.freq_start)
            self.RF_FSV3000.write("SENS:FREQ:STOP "+self.freq_stop)
            self.RF_FSV3000.write("SENS:FREQ:STEP "+self.freq_step)
            self.RF_FSV3000.write("SWE:POIN?")
            self.sweep_points = int(self.RF_FSV3000.read())
            self.RF_FSV3000.write("SENS:FREQ:STAR?")
            self.start_freq = int(self.RF_FSV3000.read())
            self.RF_FSV3000.write("SENS:FREQ:STEP?")
            self.step_freq = int(self.RF_FSV3000.read())
            #=========================================================================
            self.Command_func(self.tn, 'LOADCAL '+self.cali_num, self.cali_num)  # 加载特定idx的校准数据
            self.Command_func(self.tn, 'Pos 3 '+self.max_pos, 'JOB')  # 有谐波的校准数据时，需要先将谐波探针移动到最大的x轴位置，具体位置在校准文件中获得
            Mov_query_res = Read_Result_Order
            self.wait_function(Mov_query_res)#等待tunner移动完毕

            self.Command_func(self.tn, 'DIR', '0169')
            calibration_points = Read_Result_Order[3]  # 获取校准点数量
            for cali_index in range(int(calibration_points)):
                print(1)
                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + '这是第' + str(cali_index + 1) + '个校准点，共'
                                +str(calibration_points)+'个校准点')
                print(1)
                # ========================================建立loss文件文件头==============================================
                logfile = open('E:/ITuner_data/LOSS_DATA/Tunerloss_calpoint' + str(cali_index + 1) + '.loss',
                               'w')  # 建立loss文件
                logfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<TableAttributes>\n <Header comment=""/>\n')
                # =====================================================================================================
                print(1)
                # ========================================tunner移动到校准文件相应位置=====================================
                self.Command_func(self.tn, 'CALPOINT? ' + str(cali_index + 1), 'xpos=')  # 询问这个校准点的x，y轴数据用于检查和对比
                print(1)
                normalize_list = Read_Result_Order[1].split('=')  # 中转数组，用于寻找y轴数值
                Read_Result_Order[1] = normalize_list[1]  # 标准化数组输入
                calipoint_index_list = Read_Result_Order  # 将标准化数组输入转存特定数组
                # =================检查校准数据是否合理？（x和y轴是否在合理区间内？）
                if 0 <= int(calipoint_index_list[0]) and int(calipoint_index_list[0]) <= 34000:
                    pass
                else:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' +
                                    'calibration data wrong, x=' + calipoint_index_list[0])
                    break
                if 0 <= int(calipoint_index_list[1]) and int(calipoint_index_list[1]) <= 8230:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + 'Calibration data checked')
                    pass
                else:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + 'calibration data wrong, y='
                                    + calipoint_index_list[1])
                    break
                self.Command_func(self.tn, 'CALPOINT ' + str(cali_index + 1), 'JOB')  # 移动探针到指定的校准点
                Status_Check = Read_Result_Order  # 检查移动是否完毕
                self.wait_function(Status_Check)

                self.Command_func(self.tn, 'Pos?', ' ')  # 询问当前位置
                current_xposition = Read_Result_Order[0].split('=')[1]
                current_yposition = Read_Result_Order[4].split('=')[1]
                current_HighFreq_yposition = Read_Result_Order[1].split('=')[1]
                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + '当前x=' + current_xposition + ', 低频针y='
                      + current_yposition + ', 高频针y=' + current_HighFreq_yposition)
                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + '校准文件位置x=' + calipoint_index_list[0] + ', y=' +
                      calipoint_index_list[1])
                time.sleep(1)
                print(1)
                # ===================================tuner移动完成，开始S参数扫描建立插损文件=========================
                self.RF_ZNB40.write(
                    "MMEM:LOAD:STAT 1, 'C:/Users/Public/Documents/Rohde-Schwarz/VNA/RecallSets/"+self.VNA_SET+"'")  # 矢网校准设置加载
                self.wait_visa_command(self.RF_ZNB40, 'Load VNA sets completed')
                self.RF_ZNB40.write("INIT:CONT:ALL OFF")
                self.RF_ZNB40.write("INIT:IMM; *WAI")
                self.wait_visa_command(self.RF_ZNB40, 'S-para Sweep complete')
                insertion_loss_string = ''
                print(1)
                for freq_point in range(self.sweep_points):
                    print(1)
                    freq = str(self.start_freq + freq_point * self.step_freq)  # 当前频率点
                    self.RF_ZNB40.write("CALC1:PAR:SEL 'Trc3'")  # 选择Trc3为活跃曲线（选中Trc3）
                    self.RF_ZNB40.write("CALC1:MARK1 ON; MARK1:X " + freq + "Hz")
                    time.sleep(0.2)
                    print(1)
                    self.RF_ZNB40.write("CALC1:MARK1:X?")
                    read_marker_x = self.RF_ZNB40.read().replace("\n", "")
                    self.RF_ZNB40.write("CALC1:MARK1:Y?")
                    read_marker_y = str(abs(float(self.RF_ZNB40.read().replace("\n", ""))))
                    logfile.write(' <Data value="' + read_marker_y + '" freq="' + read_marker_x + '"/>\n')

                    insertion_loss_string = insertion_loss_string + read_marker_x + 'Hz,' + str(read_marker_y)
                    if freq_point == self.sweep_points - 1:
                        pass
                    else:
                        insertion_loss_string = insertion_loss_string + ','

                self.RF_FSV3000.write("CORR:LOSS:INP:MODE TABL")
                self.RF_FSV3000.write("CORR:LOSS:INP:TABL " + insertion_loss_string)
                logfile.write('</TableAttributes>')

                # =======================预放设置=============
                self.RF_FSV3000.write("INP:GAIN:STAT ON")
                self.RF_FSV3000.write("INP:GAIN:VAL "+self.preamp)
                # ==========================================

                # =============开始校准=======================
                self.RF_FSV3000.write("SENS:CONF:CORR")
                self.RF_FSV3000.write("INIT:IMM")

                self.wait_visa_command(self.RF_FSV3000, 'Noise Calibration Complete')

                self.RF_FSV3000.write(
                    "SENS:CORR:SAVE 'C:/R_S/Instr/user/Noise/Cal/Tuner_Calipoint_" + str(cali_index + 1) + ".dfl'")
                self.wait_visa_command(self.RF_FSV3000, 'Saving calibration data completed\n')




        except Exception as e:
            box = QMessageBox()
            box.setIcon(3)
            box.setWindowTitle("Message")
            box.setText(str(e))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(3)
            box.exec_()
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+"Connect to Tunner("
                            + str(e) + "\n")

