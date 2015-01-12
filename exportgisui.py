# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/exportgis.ui'
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

class Ui_ExportGisDialog(object):
    def setupUi(self, ExportGisDialog):
        ExportGisDialog.setObjectName(_fromUtf8("ExportGisDialog"))
        ExportGisDialog.resize(496, 212)
        self.gridLayout = QtGui.QGridLayout(ExportGisDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(ExportGisDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 2, 1, 1)
        self.label_3 = QtGui.QLabel(ExportGisDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(ExportGisDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.comboBox = QtGui.QComboBox(ExportGisDialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 5, 2, 1, 1)
        self.label = QtGui.QLabel(ExportGisDialog)
        self.label.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ExportGisDialog)
        self.label_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(ExportGisDialog)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 2, 2, 1, 1)
        self.pushButton = QtGui.QPushButton(ExportGisDialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 4, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(ExportGisDialog)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 2, 4, 1, 1)

        self.retranslateUi(ExportGisDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExportGisDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExportGisDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportGisDialog)

    def retranslateUi(self, ExportGisDialog):
        ExportGisDialog.setWindowTitle(_translate("ExportGisDialog", "Export GIS raster", None))
        self.label_3.setText(_translate("ExportGisDialog", "Output type", None))
        self.lineEdit.setToolTip(_translate("ExportGisDialog", "Output file name", None))
        self.lineEdit.setStatusTip(_translate("ExportGisDialog", "Enter a name for the file you want to create or use the \'Find\' button to select a file to overwrite.", None))
        self.comboBox.setStatusTip(_translate("ExportGisDialog", "Enter the GIS format that you want the  file to be created in.", None))
        self.label.setText(_translate("ExportGisDialog", "Output file name", None))
        self.label_2.setText(_translate("ExportGisDialog", "Copy projection from", None))
        self.lineEdit_2.setStatusTip(_translate("ExportGisDialog", "Enter a file that can be used to copy projection information. By default, this is the habitat file that you used to create the scenario", None))
        self.pushButton.setStatusTip(_translate("ExportGisDialog", "Set the output filename using a save file dialog", None))
        self.pushButton.setText(_translate("ExportGisDialog", "Find", None))
        self.pushButton_2.setText(_translate("ExportGisDialog", "Find", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExportGisDialog = QtGui.QDialog()
    ui = Ui_ExportGisDialog()
    ui.setupUi(ExportGisDialog)
    ExportGisDialog.show()
    sys.exit(app.exec_())

