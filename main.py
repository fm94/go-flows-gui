#!/usr/bin/python2
# -*- coding: utf-8 -*-

#******************************************************************************
#
# Copyright (C) 2019, Institute of Telecommunications, TU Wien
#
# Name        : main.py
# Description : a GUI for the Flow Extractor with all basic features
# Author      : Fares Meghdouri
#
# Notes : known limitations: online-offline modes are not implemented yet
#                            saving and loading configurations (features, key, json are not implemented yet)
#
#
#******************************************************************************

import os
import subprocess
from PyQt4 import QtCore, QtGui
import pickle
import json
import PyQt4

pcaps = []
options = {}
l_short = []
l_long = []
_type = False

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def callFeaturesMaker():
    os.system("./features_maker.py")
    return

def callKeyMaker():
    os.system("./key_maker.py")
    return

def Run(file):
    #go-flows run -sort start features CAIA.json export csv Monday.csv source libpcap /home/meghdouri/Desktop/datasets/CIC-IDS-2017/PCAPs/Monday-WorkingHours.pcap
    global options

    command = []
    command.append("go-flows")
    command.append("run")
    """
    if options["mode"] == "online":
        pass
    elif options["mode"] == "offline":
        pass
    """
    if "active" in options:
        command.append("-active")
        command.append(str(options["active"]))

    if "expire" in options:
        command.append("-expire")
        command.append(str(options["expire"]))

    if "idle" in options:
        command.append("-idle")
        command.append(str(options["idle"]))

    if "expireTCP" in options:
        command.append("-expireTCP")

    if "expireWindow" in options:
        command.append("-expireWindow")

    if "perPacket" in options:
        command.append("-perPacket")

    if "sort" in options:
        command.append("-sort")
        command.append(str(options["sort"]))

    if "allowZero" in options:
        command.append("-allowZero")

    command.append("features")
    command.append("default_configuration.json")

    # for now support only csv export
    command.append("export")
    command.append("csv")
    command.append(os.path.join(str(options["output"]), "{}.csv".format(os.path.basename(str(file)))))

    # for now support only libpcap import
    command.append("source")
    command.append("libpcap")
    command.append(str(file))

    print(command)

    run = subprocess.Popen(" ".join(command), stdout=subprocess.PIPE, shell=True)
    output = run.communicate()[0]

    return

def createConfig():

    cfg = {}

    with open ('tmp.fe.Features', 'rb') as fp:
        features = pickle.load(fp)
    with open ('tmp.fe.Key', 'rb') as fp:
        key      = pickle.load(fp)

    cfg["features"] = features
    cfg["key_features"] = key
    cfg["bidirectionnal"] = not _type

    with open("default_configuration.json", 'w') as f:
        json.dump(cfg, f)

class Ui_MainWindow(object):
    

    def selectPCAPs(self):
        global l_short, l_long

        try:
            self.pcaps = QtGui.QFileDialog.getOpenFileNames(caption="Select capture files", directory="/home/", filter="*.pcap")

            for pcap in self.pcaps:
                l_short.append(os.path.basename(unicode(pcap)))
                l_long.append(unicode(pcap))

            self.pcapListStr = l_long
            self.textEdit.setPlainText(", ".join(l_short))

        except Exception as e:
            print e
            print "No Valid PCAPs selected"

    def selectOutput(self):
        try:
            self.output = QtGui.QFileDialog.getExistingDirectory(caption="Select output directory", directory="/home/")
            self.textEdit_2.setPlainText(self.output)

        except Exception as e:
            print e
            print "No Valid output directory selected"

    def readUserChoices(self):
        global options, l_long

        if self.checkBox.isChecked():
            options["active"] = self.textEdit_3.toPlainText()

        if self.checkBox_2.isChecked():
            options["expire"] = self.textEdit_4.toPlainText()

        if self.checkBox_3.isChecked():
            options["idle"] = self.textEdit_5.toPlainText()

        if self.checkBox_4.isChecked():
            options["expireTCP"] = True

        if self.checkBox_5.isChecked():
            options["expireWindow"] = True

        if self.checkBox_6.isChecked():
            options["perPackett"] = True

        if self.checkBox_7.isChecked():
            options["log"] = True

        if self.checkBox_8.isChecked():
            options["sort"] = self.textEdit_6.toPlainText()

        if self.checkBox_9.isChecked():
            options["allowZero"] = True

        options["output"] = self.output

        self.label_5.setText("Running...")

        for link in l_long:
            Run(link)

        self.label_5.setText("Done!")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(886, 596)
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.grid = QtGui.QGridLayout()
        self.grid.setColumnStretch ( 1, 1)
        self.grid.setRowStretch ( 1, 1)

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 90, 97, 30))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.selectPCAPs)

        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 90, 711, 30))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(750, 130, 97, 30))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.selectOutput)

        self.textEdit_2 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 130, 711, 30))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 170, 251, 30))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_3.clicked.connect(callFeaturesMaker)

        self.mode_group=QtGui.QButtonGroup(self.centralwidget)
        self.radioButton = QtGui.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(150, 20, 115, 22))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.mode_group.addButton(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(150, 50, 115, 22))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.mode_group.addButton(self.radioButton_2)

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))

        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(30, 260, 311, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))

        self.textEdit_3 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(340, 256, 91, 30))
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))

        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 304, 311, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))

        self.textEdit_4 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(340, 300, 91, 30))
        self.textEdit_4.setObjectName(_fromUtf8("textEdit_4"))

        self.checkBox_3 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 344, 311, 22))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))

        self.textEdit_5 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_5.setGeometry(QtCore.QRect(340, 340, 91, 30))
        self.textEdit_5.setObjectName(_fromUtf8("textEdit_5"))

        self.checkBox_4 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 424, 441, 22))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))

        self.checkBox_5 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 464, 311, 22))
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))

        self.checkBox_6 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(30, 500, 311, 22))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))

        self.checkBox_7 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_7.setGeometry(QtCore.QRect(500, 260, 311, 22))
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))

        self.checkBox_8 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_8.setGeometry(QtCore.QRect(500, 294, 311, 22))
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))

        self.textEdit_6 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_6.setGeometry(QtCore.QRect(650, 290, 91, 30))
        self.textEdit_6.setObjectName(_fromUtf8("textEdit_6"))

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(500, 330, 271, 21))
        self.label_2.setAcceptDrops(False)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(510, 350, 241, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.checkBox_9 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_9.setGeometry(QtCore.QRect(500, 420, 311, 22))
        self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))

        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(750, 500, 91, 27))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.readUserChoices)

        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(590, 500, 151, 27))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(290, 170, 251, 30))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(callKeyMaker)

        self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(550, 170, 191, 30))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_7.clicked.connect(createConfig)

        self.type_group=QtGui.QButtonGroup(self.centralwidget)
        self.radioButton_3 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(640, 50, 121, 22))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.type_group.addButton(self.radioButton_3)

        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 40, 121, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.radioButton_4 = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(640, 20, 115, 22))
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.type_group.addButton(self.radioButton_4)
        global _type
        _type = self.radioButton_4

        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(300, 30, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Flow Extractor - GUI - TUWIEN - CN group", None))
        self.pushButton.setText(_translate("MainWindow", "PCAPs", None))
        self.pushButton_2.setText(_translate("MainWindow", "Output", None))
        self.pushButton_3.setText(_translate("MainWindow", "Select features", None))
        self.radioButton.setText(_translate("MainWindow", "Online", None))
        self.radioButton_2.setText(_translate("MainWindow", "Offline", None))
        self.label.setText(_translate("MainWindow", "Select the mode:", None))
        self.checkBox.setText(_translate("MainWindow", "Active timeout in seconds (default 1800)", None))
        self.checkBox_2.setText(_translate("MainWindow", "Expire timeout in seconds (default 100)", None))
        self.checkBox_3.setText(_translate("MainWindow", "Idle timeout in seconds (default 300)", None))
        self.checkBox_4.setText(_translate("MainWindow", "TCP flows are expired upon RST or FIN-teardown (default true)", None))
        self.checkBox_5.setText(_translate("MainWindow", "Expire all flows after every window", None))
        self.checkBox_6.setText(_translate("MainWindow", "Export one flow per Packet", None))
        self.checkBox_7.setText(_translate("MainWindow", "Get a log file about performance", None))
        self.checkBox_8.setText(_translate("MainWindow", "sort the flows", None))
        self.label_2.setText(_translate("MainWindow", "Sort output by \"start\" time, \"stop\" time,", None))
        self.label_3.setText(_translate("MainWindow", " \"expiry\" time, or unsorted (\"none\") ", None))
        self.checkBox_9.setText(_translate("MainWindow", "Accept packets that have no transport port", None))
        self.pushButton_4.setText(_translate("MainWindow", "Run!", None))
        self.pushButton_5.setText(_translate("MainWindow", "Save configuration", None))
        self.pushButton_6.setText(_translate("MainWindow", "Select key", None))
        self.pushButton_7.setText(_translate("MainWindow", "Create configuration", None))
        self.radioButton_3.setText(_translate("MainWindow", "Bidirectionnal", None))
        self.label_4.setText(_translate("MainWindow", "Select flows type:", None))
        self.radioButton_4.setText(_translate("MainWindow", "Unidirectionnal", None))
        self.label_5.setText(_translate("MainWindow", "IDLE", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

