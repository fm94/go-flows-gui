#!/usr/bin/python2
# -*- coding: utf-8 -*-

#******************************************************************************
#
# Copyright (C) 2019, Institute of Telecommunications, TU Wien
#
# Name        : key_maker.py
# Description : Convert simple formating of features into NTARC json format
# Author      : Fares Meghdouri
#
# Notes : known limitations: functions can take two arguments at maximum
#
#******************************************************************************

from PyQt4 import QtCore, QtGui
import json
import pickle
import os
import time
import re

#******************************************************************************

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

class Parser:
    @staticmethod
    def readFunction(word):
        
        featureFunction   = re.match(r'^(?P<feature>(?:(?!\().)*)\,(?P<function>(?:(?!\().)*)\(.*\)$'           , word)
        functionFeature   = re.match(r'^(?P<function>(?:(?!\().)*)\(.*\)\,(?P<feature>(?:(?!\().)*)$'           , word)
        featureFeature    = re.match(r'^(?P<feature1>(?:(?!\().)*)\,(?P<feature2>(?:(?!\().)*)$'                , word)
        functionFunction  = re.match(r'^(?P<function1>(?:(?!\().)*\(.*\))\,(?P<function2>(?:(?!\().)*\(.*\))$'  , word)
        feature           = re.match(r'^(?P<feature>(?:(?!.*\,.*).)(?:(?!\().)*)$'                              , word)
        functionB         = re.match(r'^(?P<function1>(?:(?!\().)*\(.*\))\,(?P<function2>(?:(?!\().)*\(.*\)\))$', word)
        functionA         = re.match(r'^(?P<function>(?:(?!\().)*)\((?P<feature>.*)\)$'                         , word)
        
        if featureFunction:
            return [featureFunction.groupdict()["feature"],
                    Parser.readingParser(featureFunction.groupdict()["function"])]
        
        if functionFeature:
            return [Parser.readingParser(functionFeature.groupdict()["function"]),
                   functionFeature.groupdict()["feature"]]
        
        if featureFeature:
            return [featureFeature.groupdict()["feature1"],
                    featureFeature.groupdict()["feature2"]]
        
        if functionFunction and not functionB:
            return [Parser.readingParser(functionFunction.groupdict()["function1"]),
                    Parser.readingParser(functionFunction.groupdict()["function2"])]
        
        if feature:
            return [feature.groupdict()["feature"]]
                    
        if functionA:
            return [Parser.readingParser(word)]
        

    @staticmethod
    def readingParser(word):

        parser_function       = re.match(r'^(?P<function>(?:(?!\().)*)\((?P<feature>.*)\)$', word)
        parser_feature        = re.match(r'^(?:(?!\().)*$', word)
        
        if parser_function:
            tmp               = {}
            tmp[parser_function.groupdict()["function"]] = Parser.readFunction(parser_function.groupdict()["feature"])
            toBeAppended      = tmp

        elif parser_feature:
            toBeAppended      = word
            
        else: # force a dictionnary # used mainly for testing # can read for instance '{"sum" : ["ipTTL"]}''
            toBeAppended      = json.loads(word)
        
        return toBeAppended


class Ui_DockWidget(object):

    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(510, 685)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))

        self.plainTextEdit = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 500, 600))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))

        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(115, 610, 80, 35))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 610, 130, 35))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.validate)

        self.pushButton_3 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setGeometry(QtCore.QRect(25, 610, 80, 35))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3.clicked.connect(self.clear)

        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_4.setGeometry(QtCore.QRect(335, 610, 130, 35))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_2"))

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

        # check if there is a configuration already
        if os.path.isfile('tmp.raw.Key') and not os.stat("tmp.raw.Key").st_size == 0:
            with open ('tmp.raw.Key', 'rb') as fp:
                #self.features = pickle.load(fp)
            #self.displayedText = [json.dumps(x) if type(x) == dict else x for x in self.features]
            #self.plainTextEdit.setPlainText(",\n".join(self.displayedText))
                self.plainTextEdit.setPlainText(fp.read())

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "NTARC Key Maker - TUWIEN - CN group", None))
        self.pushButton.setText(_translate("DockWidget", "Load", None))
        self.pushButton_2.setText(_translate("DockWidget", "Verify and Apply", None))
        self.pushButton_3.setText(_translate("DockWidget", "Clear", None))
        self.pushButton_4.setText(_translate("DockWidget", "Save to file", None))

    def check(self):
        self.features = []
        self.errors   = []
        for line in str(self.plainTextEdit.toPlainText()).split("\n"):
            try:
                self.features.append(Parser.readingParser(line))
            except Exception as e:
                print(e)
                self.errors.append('check: {}'.format(line))
            if len(self.errors) != 0:
                print("errors:\n {}".format(self.errors))

    def clear(self):
        self.plainTextEdit.setPlainText('')

    def validate(self):
        self.check()
        with open('tmp.raw.Key', 'w') as fp:
            fp.write(str(self.plainTextEdit.toPlainText()))
        with open('tmp.fe.Key', 'w') as fp:
            pickle.dump(self.features, fp)
        DockWidget.close()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DockWidget = QtGui.QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(DockWidget)
    DockWidget.show()
    sys.exit(app.exec_())

