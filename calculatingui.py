# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/calculating2.ui'
#
# Created: Mon Jan 12 18:11:06 2015
#      by: PyQt4 UI code generator 4.10.4-snapshot-595c1453ae29
#
# WARNING! All changes made in this file will be lost!

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

class Ui_CalculatingDialog(object):
    def setupUi(self, CalculatingDialog):
        CalculatingDialog.setObjectName(_fromUtf8("CalculatingDialog"))
        CalculatingDialog.resize(336, 86)
        self.verticalLayout = QtGui.QVBoxLayout(CalculatingDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(CalculatingDialog)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(CalculatingDialog)
        QtCore.QMetaObject.connectSlotsByName(CalculatingDialog)

    def retranslateUi(self, CalculatingDialog):
        CalculatingDialog.setWindowTitle(_translate("CalculatingDialog", "Calculating Circuit Flow", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CalculatingDialog = QtGui.QDialog()
    ui = Ui_CalculatingDialog()
    ui.setupUi(CalculatingDialog)
    CalculatingDialog.show()
    sys.exit(app.exec_())

