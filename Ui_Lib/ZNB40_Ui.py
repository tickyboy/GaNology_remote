# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ZNB40_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(996, 544)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(12, 50, 459, 193))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(6, 6, 81, 19))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(6, 30, 441, 160))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.freqsweep_tab = QtWidgets.QWidget()
        self.freqsweep_tab.setObjectName("freqsweep_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.freqsweep_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_9 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.label_24 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_2.addWidget(self.label_24)
        self.label_26 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_2.addWidget(self.label_26)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_start_fre = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_start_fre.setObjectName("lineEdit_start_fre")
        self.verticalLayout_3.addWidget(self.lineEdit_start_fre)
        self.lineEdit_center_fre = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_center_fre.setObjectName("lineEdit_center_fre")
        self.verticalLayout_3.addWidget(self.lineEdit_center_fre)
        self.lineEdit_BW = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_BW.setObjectName("lineEdit_BW")
        self.verticalLayout_3.addWidget(self.lineEdit_BW)
        self.lineEdit_Average = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_Average.setObjectName("lineEdit_Average")
        self.verticalLayout_3.addWidget(self.lineEdit_Average)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.label_11 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_4.addWidget(self.label_11)
        self.label_25 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_4.addWidget(self.label_25)
        spacerItem = QtWidgets.QSpacerItem(20, 35, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 4, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.label_10 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_5.addWidget(self.label_10)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEdit_stop_fre = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_stop_fre.setObjectName("lineEdit_stop_fre")
        self.verticalLayout_6.addWidget(self.lineEdit_stop_fre)
        self.lineEdit_span_fre = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_span_fre.setObjectName("lineEdit_span_fre")
        self.verticalLayout_6.addWidget(self.lineEdit_span_fre)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.label_12 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_7.addWidget(self.label_12)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 2, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.lineEdit_step_fre = QtWidgets.QLineEdit(self.freqsweep_tab)
        self.lineEdit_step_fre.setObjectName("lineEdit_step_fre")
        self.horizontalLayout_4.addWidget(self.lineEdit_step_fre)
        self.label_8 = QtWidgets.QLabel(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 53, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 55, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 2, 1)
        self.Apply_freq_swp_pushButton = QtWidgets.QPushButton(self.freqsweep_tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Apply_freq_swp_pushButton.setFont(font)
        self.Apply_freq_swp_pushButton.setObjectName("Apply_freq_swp_pushButton")
        self.gridLayout.addWidget(self.Apply_freq_swp_pushButton, 3, 2, 1, 1)
        self.tabWidget.addTab(self.freqsweep_tab, "")
        self.powersweep_tab = QtWidgets.QWidget()
        self.powersweep_tab.setObjectName("powersweep_tab")
        self.Apply_pow_swp_pushButton = QtWidgets.QPushButton(self.powersweep_tab)
        self.Apply_pow_swp_pushButton.setGeometry(QtCore.QRect(342, 92, 75, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Apply_pow_swp_pushButton.setFont(font)
        self.Apply_pow_swp_pushButton.setObjectName("Apply_pow_swp_pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.powersweep_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 12, 141, 112))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.lineEdit_start_pow = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_start_pow.setObjectName("lineEdit_start_pow")
        self.horizontalLayout_8.addWidget(self.lineEdit_start_pow)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_8.addWidget(self.label_14)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_7.addWidget(self.label_15)
        self.lineEdit_stop_pow = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_stop_pow.setObjectName("lineEdit_stop_pow")
        self.horizontalLayout_7.addWidget(self.lineEdit_stop_pow)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_7.addWidget(self.label_16)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_17 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_10.addWidget(self.label_17)
        self.lineEdit_step_pow = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_step_pow.setObjectName("lineEdit_step_pow")
        self.horizontalLayout_10.addWidget(self.lineEdit_step_pow)
        self.label_18 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setText("")
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_22 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_11.addWidget(self.label_22)
        self.lineEdit_step_pow_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_step_pow_2.setObjectName("lineEdit_step_pow_2")
        self.horizontalLayout_11.addWidget(self.lineEdit_step_pow_2)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_11.addWidget(self.label_23)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.widget = QtWidgets.QWidget(self.powersweep_tab)
        self.widget.setGeometry(QtCore.QRect(190, 8, 183, 79))
        self.widget.setObjectName("widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_21 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_8.addWidget(self.label_21)
        self.label_27 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.verticalLayout_8.addWidget(self.label_27)
        self.label_28 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.verticalLayout_8.addWidget(self.label_28)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lineEdit_start_pow_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_start_pow_2.setObjectName("lineEdit_start_pow_2")
        self.verticalLayout_9.addWidget(self.lineEdit_start_pow_2)
        self.lineEdit_BW_pow = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_BW_pow.setObjectName("lineEdit_BW_pow")
        self.verticalLayout_9.addWidget(self.lineEdit_BW_pow)
        self.lineEdit_Average_pow = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_Average_pow.setObjectName("lineEdit_Average_pow")
        self.verticalLayout_9.addWidget(self.lineEdit_Average_pow)
        self.horizontalLayout_5.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_20 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_10.addWidget(self.label_20)
        self.label_29 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.verticalLayout_10.addWidget(self.label_29)
        spacerItem3 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_10)
        self.tabWidget.addTab(self.powersweep_tab, "")
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(4, 4, 987, 28))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(488, 48, 389, 195))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.label_19 = QtWidgets.QLabel(self.frame_2)
        self.label_19.setGeometry(QtCore.QRect(6, 6, 81, 19))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Stimulus"))
        self.label_4.setText(_translate("Form", "Start:"))
        self.label_9.setText(_translate("Form", "Center:"))
        self.label_24.setText(_translate("Form", "BW:"))
        self.label_26.setText(_translate("Form", "Average:"))
        self.label_3.setText(_translate("Form", "Hz"))
        self.label_11.setText(_translate("Form", "Hz"))
        self.label_25.setText(_translate("Form", "Hz"))
        self.label_5.setText(_translate("Form", "Stop:"))
        self.label_10.setText(_translate("Form", "Span:"))
        self.label_6.setText(_translate("Form", "Hz"))
        self.label_12.setText(_translate("Form", "Hz"))
        self.label_7.setText(_translate("Form", "Step:"))
        self.label_8.setText(_translate("Form", "Hz"))
        self.Apply_freq_swp_pushButton.setText(_translate("Form", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.freqsweep_tab), _translate("Form", "Frequency Sweep"))
        self.Apply_pow_swp_pushButton.setText(_translate("Form", "Apply"))
        self.label_13.setText(_translate("Form", "Start:"))
        self.label_14.setText(_translate("Form", "dBm"))
        self.label_15.setText(_translate("Form", "Stop:"))
        self.label_16.setText(_translate("Form", "dBm"))
        self.label_17.setText(_translate("Form", "Points:"))
        self.label_22.setText(_translate("Form", "Step:"))
        self.label_23.setText(_translate("Form", "dBm"))
        self.label_21.setText(_translate("Form", "Freq:"))
        self.label_27.setText(_translate("Form", "BW:"))
        self.label_28.setText(_translate("Form", "Average:"))
        self.label_20.setText(_translate("Form", "Hz"))
        self.label_29.setText(_translate("Form", "Hz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.powersweep_tab), _translate("Form", "Power Sweep"))
        self.label.setText(_translate("Form", "Vector Network Analyzer"))
        self.label_19.setText(_translate("Form", "Channel"))
