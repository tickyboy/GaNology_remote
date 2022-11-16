import telnetlib
import pyvisa, sys, csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject , pyqtSignal
from PyQt5.Qt import QApplication, QWidget, QPushButton, QThread, QMutex, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, \
    QPushButton, QFrame
import time
import Ui_Lib.Tuner_noise_calibration as ui
from PyQt5.QtGui import *
import threading

class message(QThread):
    signal = pyqtSignal()
    def __init__(self, FuncClass_Tuner):
        super(message, self).__init__()
        self.window = FuncClass_Tuner
    def run(self):
        self.signal.emit()

class FuncClass_Tuner(QWidget):
    def __init__(self, parent=None):
        super(FuncClass_Tuner, self).__init__(parent)
        self.QThread_errtext = ''
        self.message = message(self)
        self.log_creation()
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)
        self.ui_form.Stop_Button.clicked.connect(self.Stop)
        self.ui_form.NF_connect_button.clicked.connect(self.connect_button_clicked)
        self.ui_form.Calibration_button.clicked.connect(self.Tread_1)
        self.ui_form.Tuner_init_button.clicked.connect(self.Tunner_initial_function)
        self.ui_form.Tuner_init_button_NF.clicked.connect(self.Tunner_initial_function)
        self.ui_form.NF_measure_button.clicked.connect(self.Tread_2)
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
    def wait_function_NF(self, Check_list):
        # 保证上一个命令（移动）已经完成才向tuner发送下一个命令，防止命令冲突
        Check_index = True
        while Check_index:
            for index in Check_list:
                if index == 'completed':
                    Check_index = False
                    self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + 'Moving job completed')
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
    def wait_visa_command_NF(self, Device, complete_message):
        Check_status = True
        while Check_status:
            try:
                Device.write('*OPC?')
                Read_status = Device.read()
                Check_status = False
                time.sleep(1)
            except:
                self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + " Visa processing")
                time.sleep(1)
                continue
        if complete_message == '':
            pass
        else:
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + complete_message)
    def log_creation(self):
        self.log_name = str(time.ctime(time.time())).replace(':','_').replace(' ','_')
        self.logfile_log = open('E:/ITuner_data/LOG_DATA/'+self.log_name
                                +'_LOG_data.txt', 'w')
    def LOG_record(self,text):
        QApplication.processEvents()
        self.ui_form.textBrowser_LOG.append(text)
        QApplication.processEvents()
        with open('E:/ITuner_data/LOG_DATA/'+self.log_name
                                +'_LOG_data.txt',"a",newline='') as logfile:
            logfile.write(text+'\n')
            logfile.close()
        #self.logfile_log.write(text + '\n')
        #self.logfile_log.close()
    def LOG_record_NF_measure(self,text):
        QApplication.processEvents()
        self.ui_form.textBrowser_LOG_NF.append(text)
        QApplication.processEvents()
        with open('E:/ITuner_data/LOG_DATA/'+self.log_name
                                +'_LOG_data.txt',"a",newline='') as logfile:
            logfile.write(text+'\n')
            logfile.close()
        #self.logfile_log.write(text + '\n')
        #self.logfile_log.close()
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
        try:
            self.control_flag = 1
            self.freq_start = self.ui_form.freq_start_edit.text()
            self.freq_step = self.ui_form.freq_step_edit.text()
            self.freq_stop = self.ui_form.freq_stop_edit.text()
            self.preamp = self.ui_form.preamp_edit.text()
            self.cali_num = self.ui_form.Cal_number_edit.text()
            self.max_pos = self.ui_form.Max_POS_edit.text()
            self.VNA_SET = self.ui_form.VNA_SET_edit.text()
            self.Calpoint = self.ui_form.Calpoint_edit.text()
            self.confirm_message_set("Please Check the settings for the NF calibration:\n"+"Frequency:"+self.freq_start
                    +" to "+self.freq_stop+"\n"+"Frequency Step:"+self.freq_step+"\n"+"VNA SET Name:"+self.VNA_SET+'\n'
                    +'Calibration ID:'+self.cali_num+'\n'+'Preamplifier:'+self.preamp)
        except Exception as e:
            self.message_set(e)
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
            #===============检查MaX pos输入是否合法======================
            if int(self.max_pos)<34000 and int(self.max_pos)>0:
                self.Command_func(self.tn, 'Pos 3 '+self.max_pos, 'JOB')  # 有谐波的校准数据时，需要先将谐波探针移动到最大的x轴位置，具体位置在校准文件中获得
            else:
                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + '2nd Pos illegal. It should be in the range of 0 to 3400')
                return None

            Mov_query_res = Read_Result_Order
            self.wait_function(Mov_query_res)#等待tunner移动完毕

            self.Command_func(self.tn, 'DIR', '0169')
            calibration_points = Read_Result_Order[3]  # 获取校准点数量
            for cali_index in range(int(calibration_points)):
                if self.control_flag == 1:
                    pass
                else:
                    self.LOG_record('[' + str(time.ctime(time.time())) + '] Calibration Aborted, application will be terminated in 5 Seconds')
                    time.sleep(5)
                    sys.exit()
                    break

                self.LOG_record('[' + str(time.ctime(time.time())) + '] ' + '这是第' + str(cali_index + 1) + '个校准点，共'
                                +str(calibration_points)+'个校准点')

                # ========================================建立loss文件文件头==============================================
                logfile = open('E:/ITuner_data/LOSS_DATA/Tunerloss_calpoint' + str(cali_index + 1) + '.loss',
                               'w')  # 建立loss文件
                logfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<TableAttributes>\n <Header comment=""/>\n')
                # =====================================================================================================

                # ========================================tunner移动到校准文件相应位置=====================================
                self.Command_func(self.tn, 'CALPOINT? ' + str(cali_index + 1), 'xpos=')  # 询问这个校准点的x，y轴数据用于检查和对比

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

                # ===================================tuner移动完成，开始S参数扫描建立插损文件=========================
                self.RF_ZNB40.write(
                    "MMEM:LOAD:STAT 1, 'C:/Users/Public/Documents/Rohde-Schwarz/VNA/RecallSets/"+self.VNA_SET+"'")  # 矢网校准设置加载
                self.wait_visa_command(self.RF_ZNB40, 'Load VNA sets completed')
                self.RF_ZNB40.write("INIT:CONT:ALL OFF")
                self.RF_ZNB40.write("INIT:IMM; *WAI")
                self.wait_visa_command(self.RF_ZNB40, 'S-para Sweep complete')
                insertion_loss_string = ''

                for freq_point in range(self.sweep_points):
                    freq = str(self.start_freq + freq_point * self.step_freq)  # 当前频率点
                    self.RF_ZNB40.write("CALC1:PAR:SEL 'Trc3'")  # 选择Trc3为活跃曲线（选中Trc3）
                    self.RF_ZNB40.write("CALC1:MARK1 ON; MARK1:X " + freq + "Hz")
                    time.sleep(0.2)
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
                    "SENS:CORR:SAVE 'C:/R_S/Instr/user/Noise/Cal/Tuner_Cal#"+ str(self.cali_num) +"_Calipoint_" + str(cali_index + 1) + ".dfl'")
                self.wait_visa_command(self.RF_FSV3000, 'Saving calibration data completed\n')
            if self.control_flag == 1:
                self.LOG_record('[' + str(time.ctime(time.time())) + '] Calibration Completed')
                time.sleep(2)
                self.Tunner_initial_function()
            else:
                pass
        except Exception as e:
            self.message_set(e)
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+"Connect to Tunner("
                            + str(e) + "\n")
    def Tread_1(self):
        try:
            th_1 = threading.Thread(target=self.Calibration_clicked, name='calibration')
            th_1.start()
        except Exception as e:
            self.message_set(e)

            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+str(e) + "\n")
    def Stop(self):
        self.control_flag = 0
    def messagebox(self):
        try:
            self.box = QMessageBox()
            self.box.setIcon(3)
            self.box.setWindowTitle("Message")
            self.box.setText(str(self.QThread_errtext))
            self.yes = self.box.addButton('OK', QMessageBox.YesRole)
            self.no = self.box.addButton('Cancel', QMessageBox.NoRole)

            self.box.setIcon(3)
            self.box.exec_()
            #QMessageBox.information(self, 'Warning', self.QThread_errtext,QMessageBox.Ok)

        except Exception as e:
            #print('YES01')
            print(e)
    def message_set(self, text):
        self.QThread_errtext = text
        self.message.signal.connect(self.messagebox)
        self.message.start()
    def confirm_messagebox(self):
        try:
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText(str(self.QThread_errtext))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            if box.clickedButton() == yes:
                self.BeginCal()
            else:
                pass
        except Exception as e:
            #print('YES01')
            print(e)
    def confirm_message_set(self, text):
        self.QThread_errtext = text
        self.message.signal.connect(self.confirm_messagebox)
        self.message.start()
    def confirm_messagebox_forNF(self):
        try:
            box = QMessageBox()
            box.setIcon(1)
            box.setWindowTitle("Message")
            box.setText(str(self.QThread_errtext))
            yes = box.addButton('OK', QMessageBox.YesRole)
            no = box.addButton('Cancel', QMessageBox.NoRole)
            box.setIcon(1)
            box.exec_()
            if box.clickedButton() == yes:
                self.BeginMea()
            else:
                pass
        except Exception as e:
            print(e)
    def confirm_message_set_forNF(self, text):
        self.QThread_errtext = text
        self.message.signal.connect(self.confirm_messagebox_forNF)
        self.message.start()
    def Tread_2(self):
        try:
            th_2 = threading.Thread(target=self.NF_Measure_clicked, name='measure')
            th_2.start()
        except Exception as e:
            self.message_set(e)
            self.LOG_record('[' + str(time.ctime(time.time())) + '] '+str(e) + "\n")
    def NF_Measure_clicked(self):
        try:
            self.rm_DC = pyvisa.ResourceManager()
            self.RF_DC = self.rm_DC.open_resource('USB0::0x2A8D::0x1002::MY58420959::INSTR')
            self.RF_DC.write('*RST')
            self.RF_DC.write('*IDN?')
            self.connect_success_text = self.RF_DC.read()
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '
                                       + "Connect Successfully to " + self.connect_success_text)
            self.gate_voltage = self.ui_form.Vg_edit.text()
            self.drain_voltage = self.ui_form.Vd_edit.text()
            self.RF_DC.write(":APPLY P25V, 5, 0.1")
            self.RF_DC.write(":OUTPUT:STATE 1")
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '
                                       + 'Vg set, waiting for Vd')
            time.sleep(2)
            self.RF_DC.write(":APPLY P6V, 5, 0.1")
            self.RF_DC.write(":OUTPUT:STATE 1")
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '
                                       + 'Vd set')

        except Exception as e:
            self.message_set(e)
            ''''
            self.control_flag = 1
            self.freq_start = self.ui_form.freq_start_edit_NF.text()
            self.freq_step = self.ui_form.freq_step_edit_NF.text()
            self.freq_stop = self.ui_form.freq_stop_edit_NF.text()
            self.preamp = self.ui_form.preamp_edit_NF.text()
            self.cali_num = self.ui_form.Cal_number_edit_NF.text()
            self.max_pos = self.ui_form.Max_POS_edit_NF.text()
            self.Calpoint = self.ui_form.Calpoint_edit_NF.text()
            self.confirm_message_set_forNF("Please Check the settings for the NF measurement:\n"+"Frequency:"+self.freq_start
                    +" to "+self.freq_stop+"\n"+"Frequency Step:"+self.freq_step+"\n"+'\n'
                    +'Calibration ID:'+self.cali_num+'\n'+'Preamplifier:'+self.preamp)
        except Exception as e:
            self.message_set(e)
    def BeginMea(self):
        try:
            self.control_flag == 1
            #==========================settings==========================================
            self.RF_FSV3000.write("INST:CRE:NEW NOISE, 'Noise'")
            self.wait_visa_command_NF(self.RF_FSV3000, 'Noise Channel Setting completed')
            self.RF_FSV3000.write("SENS:FREQ:STAR " + self.freq_start)
            self.RF_FSV3000.write("SENS:FREQ:STOP " + self.freq_stop)
            self.RF_FSV3000.write("SENS:FREQ:STEP " + self.freq_step)
            self.RF_FSV3000.write("SWE:POIN?")
            self.sweep_points = int(self.RF_FSV3000.read())
            self.RF_FSV3000.write("SENS:FREQ:STAR?")
            self.start_freq = int(self.RF_FSV3000.read())
            self.RF_FSV3000.write("SENS:FREQ:STEP?")
            self.step_freq = int(self.RF_FSV3000.read())
            self.cali_num_NF = self.ui_form.Cal_number_edit_NF.text()
            self.max_pos_NF = self.ui_form.Max_POS_edit_NF.text()
            # =======================预放设置=============
            self.RF_FSV3000.write("INP:GAIN:STAT ON")
            self.RF_FSV3000.write("INP:GAIN:VAL " + self.preamp)
            # ==========================================

            self.Command_func(self.tn, 'LOADCAL ' + self.cali_num_NF, self.cali_num_NF)  # 加载特定idx的校准数据
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '+'Calibration data loaded')
            # ===============检查MaX pos输入是否合法======================
            if int(self.max_pos_NF) < 34000 and int(self.max_pos_NF) > 0:
                self.Command_func(self.tn, 'Pos 3 ' + self.max_pos_NF, 'JOB')  # 有谐波的校准数据时，需要先将谐波探针移动到最大的x轴位置，具体位置在校准文件中获得
            else:
                self.LOG_record_NF_measure(
                    '[' + str(time.ctime(time.time())) + '] ' + '2nd Pos illegal. It should be in the range of 0 to 34000')
                return None

            Mov_query_res = Read_Result_Order
            self.wait_function_NF(Mov_query_res)  # 等待tunner移动完毕

            self.Command_func(self.tn, 'DIR', '0169')
            calibration_points = Read_Result_Order[3]  # 获取校准点数量
            for cali_index in range(int(calibration_points)):
                if self.control_flag == 1:
                    pass
                else:
                    self.LOG_record_NF_measure('[' + str(
                        time.ctime(time.time())) + '] Calibration Aborted, application will be terminated in 5 Seconds')
                    time.sleep(5)
                    sys.exit()
                    break

                self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + '这是第' + str(cali_index + 1) + '个校准点，共'
                                + str(calibration_points) + '个校准点')



                # ========================================tunner移动到校准文件相应位置=====================================
                self.Command_func(self.tn, 'CALPOINT? ' + str(cali_index + 1), 'xpos=')  # 询问这个校准点的x，y轴数据用于检查和对比

                normalize_list = Read_Result_Order[1].split('=')  # 中转数组，用于寻找y轴数值
                Read_Result_Order[1] = normalize_list[1]  # 标准化数组输入
                calipoint_index_list = Read_Result_Order  # 将标准化数组输入转存特定数组
                # =================检查校准数据是否合理？（x和y轴是否在合理区间内？）
                if 0 <= int(calipoint_index_list[0]) and int(calipoint_index_list[0]) <= 34000:
                    pass
                else:
                    self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' +
                                    'calibration data wrong, x=' + calipoint_index_list[0])
                    break
                if 0 <= int(calipoint_index_list[1]) and int(calipoint_index_list[1]) <= 8230:
                    self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + 'Calibration data checked')
                    pass
                else:
                    self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + 'calibration data wrong, y='
                                    + calipoint_index_list[1])
                    break
                self.Command_func(self.tn, 'CALPOINT ' + str(cali_index + 1), 'JOB')  # 移动探针到指定的校准点
                Status_Check = Read_Result_Order  # 检查移动是否完毕
                self.wait_function_NF(Status_Check)

                self.Command_func(self.tn, 'Pos?', ' ')  # 询问当前位置
                current_xposition = Read_Result_Order[0].split('=')[1]
                current_yposition = Read_Result_Order[4].split('=')[1]
                current_HighFreq_yposition = Read_Result_Order[1].split('=')[1]
                self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + '当前x=' + current_xposition + ', 低频针y='
                                + current_yposition + ', 高频针y=' + current_HighFreq_yposition)
                self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] ' + '校准文件位置x=' + calipoint_index_list[0] + ', y=' +
                                calipoint_index_list[1])
                time.sleep(1)

                # ========================================建立measure文件文件头==============================================
                with open('E:/ITuner_data/Measurement_Results/' + self.log_name
                          + 'NF_results_of_Cali-point#' + str(cali_index + 1) + '.csv', "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Frequency", "CPCold", "CPHot", "CYFactor",
                                     "Gain", "Noise", "NunCertainty", "PCold", "Phot", "Temp", "YFactor"])
                # =====================================================================================================



                self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '+ 'Loading calibration file')
                self.RF_FSV3000.write("SENS:CORR:REC 'C:/R_S/Instr/user/Noise/Cal/Tuner_Cal#"+self.cali_num_NF
                                      +"_Calipoint_" + str(cali_index + 1) + ".dfl'")
                self.wait_visa_command_NF(self.RF_FSV3000, "Tuner_Cal#"+self.cali_num_NF
                                      +"_Calipoint_" + str(cali_index + 1) + ".dfl loaded")
                self.RF_FSV3000.write("SENS:CONF:LIST:SINGL")
                self.RF_FSV3000.write("INIT:IMM; *WAI")
                self.wait_visa_command_NF(self.RF_FSV3000, 'NF Measurement completed')

                #========================大Marker拿数据======================================
                for freq_point in range(self.sweep_points):
                    freq = str(self.start_freq + freq_point * self.step_freq)  # 当前频率点
                    self.RF_FSV3000.write("CALC:MARK1:TRAC 1")
                    self.RF_FSV3000.write("CALC:MARK1:X "+freq+"Hz")
                    time.sleep(0.2)
                    #===============读取数据=======================
                    self.RF_FSV3000.write("CALC:MARK1:Y? CPC")
                    self.marker_CPCold = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'CPC')
                    self.RF_FSV3000.write("CALC:MARK1:Y? CPH")
                    self.marker_CPHot = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'CPH')
                    self.RF_FSV3000.write("CALC:MARK1:Y? CYF")
                    self.marker_CYFactor = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'CYF')
                    self.RF_FSV3000.write("CALC:MARK1:Y? GAIN")
                    self.marker_Gain = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'GAIN')
                    self.RF_FSV3000.write("CALC:MARK1:Y? NOIS")
                    self.marker_Noise = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'NOIS')
                    self.RF_FSV3000.write("CALC:MARK1:Y? NUNC")
                    self.marker_NunCertainty = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'NUNC')
                    self.RF_FSV3000.write("CALC:MARK1:Y? PCOL")
                    self.marker_PCold = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'PCOL')
                    self.RF_FSV3000.write("CALC:MARK1:Y? PHOT")
                    self.marker_Phot = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'PHOT')
                    self.RF_FSV3000.write("CALC:MARK1:Y? TEMP")
                    self.marker_Temp = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'TEMP')
                    self.RF_FSV3000.write("CALC:MARK1:Y? YFAC")
                    self.marker_YFactor = self.RF_FSV3000.read()
                    # self.wait_visa_command(self.RF_FSV3000, 'YFAC')
                    with open('E:/ITuner_data/Measurement_Results/' + self.log_name
                          + 'NF_results_of_Cali-point#' + str(cali_index + 1) + '.csv', "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows([[int(freq),float(self.marker_CPCold), float(self.marker_CPHot),
                                           float(self.marker_CYFactor), float(self.marker_Gain)
                                              , float(self.marker_Noise), float(self.marker_NunCertainty),
                                           float(self.marker_PCold),float(self.marker_Phot),
                                           float(self.marker_Temp), float(self.marker_YFactor)]])
                self.LOG_record_NF_measure('NF Measurement results saved')
            self.LOG_record_NF_measure('Measurement Complete')
            time.sleep(2)
            self.Tunner_initial_function()

        except Exception as e:
            self.message_set(e)
            self.LOG_record_NF_measure('[' + str(time.ctime(time.time())) + '] '+"Connect to Tunner("
                            + str(e) + "\n")
'''