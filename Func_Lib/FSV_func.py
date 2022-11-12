import pyvisa
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox, QGridLayout, QLabel, \
    QPushButton, QFrame
import time
import Ui_Lib.FSV_Ui as ui
from PyQt5.QtGui import *


class FuncClass_FSV(QWidget):
    maker_index = [1, 2, 3, 4, 5, 6]
    maker_fre_info = [0, 0, 0, 0, 0, 0]

    def __init__(self, parent=None):
        super(FuncClass_FSV, self).__init__(parent)
        self.ui_form = ui.Ui_Form()
        self.ui_form.setupUi(self)
        self.ui_form.QueryButton.clicked.connect(self.Queryfun)
        self.ui_form.ApplyButton_basic_settings.clicked.connect(self.ApplyButton)
        self.ui_form.AddButton_Maker.clicked.connect(self.AddMarker)
        self.ui_form.measTOI_Button.clicked.connect(self.Third_order_point_Measurement)
        self.setWindowTitle('GaNology Remote-FSV7G')
        self.setWindowIcon(QIcon('./images/iic.ico'))

        self.rm = pyvisa.ResourceManager()

    def Queryfun(self):
        self.rm = pyvisa.ResourceManager()

        try:
            self.RF_source_FSV = self.rm.open_resource('TCPIP0::10.0.0.13::inst0::INSTR')
            self.RF_source_FSV.write('*RST')
            self.RF_source_FSV.write('*IDN?')
            # print(RF_source_FSV.read())
            self.connect_success_text = self.RF_source_FSV.read()
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

    def TDP_Measurement(self):
        # Used to perform the time domain power (TDP) measurement
        # ---------------------Default Settings----------------------------------------------
        self.RF_source_FSV.write("*RST")  # Reset the dvice
        self.RF_source_FSV.write("INIT:CONT OFF")  # Single Sweep
        self.RF_source_FSV.write("SYST:DISP:UPD ON")  # Turn on the display on the device screen
        # --------------------Configure R&S FSV for time domain power measurement-------------
        self.RF_source_FSV.write("FREQ:CENT 100 MHz;SPAN 0Hz")  # set the frequency and the span
        self.RF_source_FSV.write("BAND:RES 300 kHz")  # resolution Bandwidth settings
        self.RF_source_FSV.write("SWE:TIME 200US")  # Sweep time settings
        self.RF_source_FSV.write("CALC:MARK:FUNC:SUMM:PPE ON")  # Peak measurement on
        self.RF_source_FSV.write("CALC:MARK:FUNC:SUMM:MEAN ON")  # Mean measurement on
        self.RF_source_FSV.write("CALC:MARK:FUNC:SUMM:RMS ON")  # RMS measurement on
        self.RF_source_FSV.write("CALC:MARK:FUNC:SUMM:SDEV ON")  # Standard deviation on
        # ---------------------Rerformance measurement and query results----------------------
        self.RF_source_FSV.write("INIT;*WAI")  # Perform sweep with sync
        # Results query
        self.RF_source_FSV.write(
            "CALC:MARK:FUNC:SUMM:PPE:RES?;" + ":CALC:MARK:FUNC:SUMM:MEAN:RES?;" + ":CALC:MARK:FUNC:SUMM:RMS:RES?;" + ":CALC:MARK:FUNC:SUMM:SDEV:RES?")
        self.ui_form.textBrowser_log.append(self.RF_source_FSV.read())
        pass

    def Power_Measurement_with_MultiSummary_Marker(self):
        # The multi-summary marker function is suitable for measuring the power of a sequence of pulses with the following characteristics:
        # 1.The pulses occur at identical time intervals, which is typical of GSM transmission in slots, for example.
        # 2.The level of the first signal is reliably above threshold.
        # 3.The subsequent pulses may have any levels.
        # 4.The function uses the first pulse as a trigger signal. The power of the subsequent pulses is determined exclusively via the timing
        #  pattern selected for the pulse sequence. The function is, therefore, suitable for adjustments where the DUT output power varies
        #  considerably and is not reliably above the trigger threshold.
        # 5.The measurement accuracy is determined by the ratio of pulse duration to total measurement time; this should not be below 1:50.
        # 6.The function always uses TRACE 1.
        # Refernce code:https://www.rohde-schwarz.com/webhelp/fsv_rsanalyzerhelp/fsv_rsanalyzerhelp.htm

        # In the example below, a GSM pulse sequence of 8 pulses is measured with an offset of 50 ms of the first pulse, 450 ms measurement time/pulse and 576.9 ms pulse period.
        # ---------------------Default Settings----------------------------------------------
        self.RF_source_FSV.timeout = 25000
        self.RF_source_FSV.write("*RST")  # Reset the dvice
        self.RF_source_FSV.write("INIT:CONT OFF")  # Single Sweep
        self.RF_source_FSV.write("SYST:DISP:UPD ON")  # Turn on the display on the device screen
        # ------------------Configure R&S FSV for power measurement in time domain --------------------------------
        self.RF_source_FSV.write("FREQ:CENT 935.2 MHz;SPAN 0Hz")  # Frequency setting
        self.RF_source_FSV.write("DISP:WIND:TRAC:Y:RLEV 10 dBm")  # Set reference level to 10 dB
        self.RF_source_FSV.write("INP:ATT 30 dB")  # Set input attenuation to 30 dB
        self.RF_source_FSV.write("BAND:RES 1 MHz;VID 3 MHz")  # Bandwidth setting
        self.RF_source_FSV.write("DET RMS")  # Select RMS detector
        self.RF_source_FSV.write("TRIG:SOUR VID")  # Trigger source: video
        self.RF_source_FSV.write("TRIG:LEV:VID 50 PCT")  # Trigger threshold: 50 %
        self.RF_source_FSV.write("SWE:TIME 50ms")  # Sweep time ≥ 1 frame
        # ---------------------Perform measurement and query results-----------------------------------------------
        self.query_cmd = "CALC:MARK:FUNC:MSUM?" + "50US,"  # Offset of first pulse
        self.query_cmd = self.query_cmd + "450US,"  # Measurement time
        self.query_cmd = self.query_cmd + "576.9US,"  # Pulse period
        self.query_cmd = self.query_cmd + "8"  # Number of bursts
        # self.RF_source_FSV.write(self.query_cmd)
        self.ui_form.textBrowser_log.append(self.RF_source_FSV.query(self.query_cmd))
        pass

    def Third_order_point_Measurement(self):
        #  The third order intercept point (TOI) is the (virtual) level of two adjacent useful signals at which the intermodulation
        # products of third order have the same level as the useful signals.
        #  The intermodulation product at fS2 is obtained by mixing the first harmonic of the useful signal PN2 with signal PN1,
        # the intermodulation product at fS1 by mixing the first harmonic of the useful signal PN1 with signal PN2.
        # fs1 = 2 × fn1 – fn2 (1); fs2 = 2 × fn2 – fn1 (2)
        #  The following example is based on two adjacent signals with a level of -30 dBm at 100 MHz and 110 MHz. The intermodulation
        # products lie at 90 MHz and 120 MHz according to the above formula. The frequency is set so that the examined
        # mixture products are displayed in the diagram. Otherwise, the default setting of the R&S FSVA/FSV is used for measurements
        # (SetupInstrument).
        # ------------------------RF Tone 1 fre & pow settings------------------------------
        try:
            self.RF_source_SMB100A = self.rm.open_resource(
                'TCPIP0::rssmb100a181560::inst0::INSTR')  # connect to the rf source 1
        except:
            self.Err_Message(3, "Failed to connect to the RF tone 1 (SMB100A)")

        self.fretext_debug = self.ui_form.textEdit_tone1_fre.toPlainText().split(" ")
        self.powtext_debug = self.ui_form.textEdit_tone1_pow.toPlainText().split(" ")
        if len(self.fretext_debug) == 1 and len(self.powtext_debug) == 1:
            # ------------------------check frequency settings---------------------------------------------------------------------------
            try:
                self.text_debug_member1 = float(self.fretext_debug[0])
                if self.text_debug_member1 < 100000 or self.text_debug_member1 > 40000000000:
                    self.Err_Message(3,
                                     "Please ensure that the frequency of RF tone 1 is in the range of 100KHz to 40GHz.")
                    return
                else:
                    pass
                self.RF_tone1_fre_text = 'SOUR1:FREQ ' + self.fretext_debug[
                    0] + 'Hz'  # creat the frequency setting command for source 1
                self.RF_source_SMB100A.write(self.RF_tone1_fre_text)

            except:
                self.Err_Message(3,
                                 "Please enter pure digital frequency information for RF tone 1 if you do not want to text in the form of 'XX G'")
                return

            # ---------------------------check power settings-----------------------------------------------------------------------------
            try:
                self.text_debug_member1_pow = float(self.powtext_debug[0])
                if self.text_debug_member1_pow > 8:
                    self.Err_Message(3, "Please ensure that the power of RF tone 1 is smaller than 8dBm.")
                    return
                else:
                    pass
                self.RF_tone1_pow_text = 'SOUR1:POW ' + self.powtext_debug[
                    0] + 'dBm'  # read the input string and creat the power setting command for source 1
                self.RF_source_SMB100A.write(self.RF_tone1_pow_text)

            except:
                self.Err_Message(3, "Please enter pure digital power information for RF tone 1.")
                return

        elif len(self.fretext_debug) == 2 and len(self.powtext_debug) == 1:
            # ---------------------------check power settings-----------------------------------------------------------------------------
            try:
                self.text_debug_member1_pow = float(self.powtext_debug[0])
                if self.text_debug_member1_pow > 8:
                    self.Err_Message(3, "Please ensure that the power of RF tone 1 is smaller than 8dBm.")
                    return
                else:
                    pass
                self.RF_tone1_pow_text = 'SOUR1:POW ' + self.powtext_debug[
                    0] + 'dBm'  # read the input string and creat the power setting command for source 1
                self.RF_source_SMB100A.write(self.RF_tone1_pow_text)

            except:
                self.Err_Message(3, "Please enter pure digital power information for RF tone 1.")
                return

            # ----------------------------check frequency settings--------------------------------------------------------------------------
            try:
                self.text_debug_member1 = float(self.fretext_debug[0])
                # ----------------------------------Convert text input to numbers-----------------------------------------------
                if self.fretext_debug[1] == 'G':
                    self.text_debug_member1 = self.text_debug_member1 * 1000000000
                elif self.fretext_debug[1] == 'M':
                    self.text_debug_member1 = self.text_debug_member1 * 1000000
                elif self.fretext_debug[1] == 'K':
                    self.text_debug_member1 = self.text_debug_member1 * 1000
                else:
                    self.Err_Message(3, "Please enter frequency information for RF tone 1 in the form of 'XX G/M/K'")
                    return

                if self.text_debug_member1 < 100000 or self.text_debug_member1 > 40000000000:
                    self.Err_Message(3,
                                     "Please ensure that the frequency of RF tone 1 is in the range of 100KHz to 40GHz.")
                    return
                else:
                    pass

                self.RF_tone1_fre_text = 'SOUR1:FREQ ' + str(
                    self.text_debug_member1) + ' Hz'  # creat the frequency setting command for source 1
                self.RF_source_SMB100A.write(self.RF_tone1_fre_text)

            except:
                self.Err_Message(3,
                                 "Please enter pure digital frequency information for RF tone 1 if you do not want to text in the form of 'XX G/M/K'")
                return

        else:
            self.Err_Message(3,
                             "Please Check the settings for RF tone 1!\nFrequency should in the range of 100KHz to 40GHz and in the form of pure digital information or 'XX G/M/K'\n Power should be set no more than 8dBm while it is in the form of pure digital information.")
            return

        # self.RF_tone1_fre_text = 'SOUR1:FREQ ' + self.ui_form.textEdit_tone1_fre.toPlainText() + 'Hz'#read the input string and creat the frequency setting command for source 1

        # self.RF_source_SMB100A.write(self.RF_tone1_fre_text)#set the frequency for rf source 1
        # self.RF_tone1_pow_text = 'SOUR1:POW ' + self.ui_form.textEdit_tone1_pow.toPlainText() + 'dBm'#read the input string and creat the power setting command for source 1
        # self.RF_source_SMB100A.write(self.RF_tone1_pow_text)#set the power for rf source 1
        # self.RF_source_SMB100A.write("OUTP ON")#turn on the rf power of tone 1

        # ---------------------Default Settings----------------------------------------------
        self.RF_source_FSV.write("*RST")  # Reset the dvice
        self.RF_source_FSV.write("INIT:CONT OFF")  # Single Sweep
        self.RF_source_FSV.write("SYST:DISP:UPD ON")  # Turn on the display on the device screen
        # ---------------------Setings for the measurement-----------------------------------
        self.RF_source_FSV.write("FREQ:STARt 85 MHz;STOP 125 MHz")  # Frequency settings
        self.RF_source_FSV.write("DISP:WIND:TRAC:Y:RLEV -20 dBm")  # Reference level
        self.RF_source_FSV.write("INIT;*WAI")  # Perform sweep with sync
        # ----------------------------Measuremnet--------------------------------------------
        self.RF_source_FSV.write("CALC:MARK:PEXC 6 DB")  # Peak excursion
        self.RF_source_FSV.write("CALC:MARK:FUNC:TOI ON")  # Switch on TOI measurement
        self.RF_source_FSV.write("CALC:MARK:FUNC:TOI:RES?")  # read out results
        self.ui_form.textBrowser_log.append(
            '=================TOI Measurement=================\n' + 'RF Tone 1 power set to (dBm):' + self.RF_source_SMB100A.query(
                'SOUR1:POW?'))
        self.ui_form.textBrowser_log.append(
            'RF Tone 1 freq. set to (Hz):' + self.RF_source_SMB100A.query('SOUR1:FREQ?'))
        self.ui_form.textBrowser_log.append(
            self.RF_source_FSV.read() + '=================================================')
        pass

    def Measuring_AM_Modulation_Depth(self):
        # The example below is based on an AM-modulated signal at 100 MHz with the following characteristics: -30 dBm Carrier signal level; AF frequency with 100KHz; Modulation depth of 50%
        # ------------------------ Peak search -----------------------------
        self.RF_source_FSV.write("BAND:RES 30 kHz")  # Set appropriate RBW
        self.RF_source_FSV.write("INIT:CONT OFF")  # Single sweep
        self.RF_source_FSV.write("INIT;*WAI")  # Perform sweep with sync
        self.RF_source_FSV.write("CALC:MARK:PEXC 6 DB")  # Peak excursion
        self.RF_source_FSV.write("CALC:MARK:STAT ON")  # Marker 1 on
        self.RF_source_FSV.write("CALC:MARK:TRAC 1")  # Assign marker1 to trace1
        # --------------- Measure modulation depth -------------------------
        self.RF_source_FSV.write("CALC:MARK:MAX;FUNC:MDEP ON")  # Marker to Peak
        self.RF_source_FSV.write("CALC:MARK:FUNC:MDEP:RES?")  # Measure mod. depth
        # ---------------Show results---------------------------------------

        self.ui_form.textBrowser_log.append(self.RF_source_FSV.read())

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

    def testfunction(self):
        # self.RF_source_FSV.write("CALC:MARK1 ON")
        self.RF_source_FSV.write("INIT:CONT OFF")
        self.RF_source_FSV.write("CALC:MARK1 ON")
        self.RF_source_FSV.write("CALC:MARK2 ON")
        self.RF_source_FSV.write("CALC:MARK2:X 2 GHz")
        # self.RF_source_FSV.write("")
        # self.RF_source_FSV.write("CALC:MARK:COUN ON")
        # self.RF_source_FSV.write("CALC:MARK:COUN:FREQ 2 GHz")
        self.RF_source_FSV.write("INIT;*WAI")
        # self.RF_source_FSV.write("CALC:MARK:COUN:FREQ?")
        self.RF_source_FSV.write("CALC:MARK2:Y?")
        self.ui_form.textBrowser_log.append(self.RF_source_FSV.read())

    def Err_Message(self, Msg_num, Msg_text):
        box = QMessageBox()
        box.setIcon(Msg_num)
        box.setWindowTitle("Message")
        box.setText(Msg_text)
        yes = box.addButton('OK', QMessageBox.YesRole)
        no = box.addButton('Cancel', QMessageBox.NoRole)
        box.setIcon(Msg_num)
        box.exec_()

    def ApplyButton(self):
        try:
            self.RF_source_SMB100A = self.rm.open_resource(
                'TCPIP0::rssmb100a181560::inst0::INSTR')  # connect to the rf source 1
        except:
            self.Err_Message(3, "Failed to connect to the RF tone 1 (SMB100A)")

        self.get_text_centerfreqG = self.ui_form.spinBox_CenterFreqG.value()
        self.doubleSpinBox_CenterFreqM = self.ui_form.doubleSpinBox_CenterFreqM.value()
        self.get_centerfreq = self.get_text_centerfreqG * 1000000000 + self.doubleSpinBox_CenterFreqM * 1000000
        self.get_centerfreq = str(self.get_centerfreq)
        self.get_freqspan = str(self.ui_form.doubleSpinBox_Span.value())
        self.get_att = str(self.ui_form.spinBox_RFattu.value())
        self.get_sweeppoints = str(self.ui_form.spinBox_sweep_points.value())

        self.RF_source_FSV.write(
            "FREQ:CENT " + self.get_centerfreq + "Hz;SPAN " + self.get_freqspan + "Hz")  # set the frequency and the span
        self.RF_source_FSV.write("INP:ATT " + self.get_att + " dB")
        self.RF_source_FSV.write("SWE:POIN " + self.get_sweeppoints)
        if self.ui_form.checkBox_singlesweep.isChecked() == True and self.ui_form.checkBox_continuesweep.isChecked() == False:
            self.RF_source_FSV.write("INIT:CONT OFF")
        # self.RF_source_FSV.write("INIT;*WAI")#Perform sweep with sync
        elif self.ui_form.checkBox_singlesweep.isChecked() == False and self.ui_form.checkBox_continuesweep.isChecked() == True:
            self.RF_source_FSV.write("INIT:CONT ON")
        else:
            self.Err_Message(3,
                             "You can not check both single sweep and continues sweep or do not choose any of them at the same time.")
            return

    def AddMarker(self):
        self.ui_form.textBrowser_mannual_meas.clear()
        self.get_markerindex = int(self.ui_form.spinBox_marker_index.value())
        self.get_markerfre = self.ui_form.spinBox_markerfreG.value() * 1000000000 + self.ui_form.doubleSpinBox_freM.value() * 1000000
        FuncClass_FSV.maker_fre_info[self.get_markerindex - 1] = self.get_markerfre
        print(FuncClass_FSV.maker_fre_info)

        for index in FuncClass_FSV.maker_index:
            if FuncClass_FSV.maker_fre_info[index - 1] == 0:
                self.RF_source_FSV.write("CALC:MARK" + str(index) + " OFF")
                pass
            else:
                self.RF_source_FSV.write("CALC:MARK" + str(index) + " ON")
                self.RF_source_FSV.write(
                    "CALC:MARK" + str(index) + ":X " + str(FuncClass_FSV.maker_fre_info[index - 1]) + "Hz")
        self.RF_source_SMB100A.write("OUTP ON")
        time.sleep(1)
        self.RF_source_FSV.write("INIT;*WAI")  # Perform sweep with sync
        for index in FuncClass_FSV.maker_index:
            if FuncClass_FSV.maker_fre_info[index - 1] == 0:
                pass
            else:

                self.display_marker = "Marker" + str(index) + ":\n" + "Frequency: " + str(
                    float(self.RF_source_FSV.query("CALC:MARK" + str(index) + ":X? "))) + " Hz; Power: " + str(
                    float(self.RF_source_FSV.query("CALC:MARK" + str(index) + ":Y? "))) + " dBm"
                self.ui_form.textBrowser_mannual_meas.append(self.display_marker)
        pass
        self.RF_source_SMB100A.write("OUTP OFF")
