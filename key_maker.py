#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'key_maker.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

import pickle
from PyQt4 import QtCore, QtGui

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

class Ui_DockWidget(object):

    def validate(self):
        try:
            os.remove("key")
        except:
            pass
        with open("key", "wb") as fp:
            pickle.dump(str(self.plainTextEdit.toPlainText()).split("\n"), fp)

    def checkValidity(self):
        try:
            os.remove("key")
        except:
            pass
        with open("key", "wb") as fp:
            pickle.dump(self.plainTextEdit.toPlainText().split("\n"), fp)

    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(602, 690)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))

        self.plainTextEdit = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 601, 601))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))

        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 610, 171, 51))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.checkValidity)

        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(130, 610, 161, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.validate)

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Key maker", None))
        self.pushButton_2.setText(_translate("DockWidget", "Validate", None))
        self.pushButton.setText(_translate("DockWidget", "Check validity", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DockWidget = QtGui.QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(DockWidget)
    DockWidget.show()
    sys.exit(app.exec_())

