# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/adding.ui'
#
# Created: Mon Jan 12 18:11:07 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(925, 542)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lcdNumber = QtGui.QLCDNumber(self.frame_2)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.verticalLayout_2.addWidget(self.lcdNumber)
        self.dial = QtGui.QDial(self.frame_2)
        self.dial.setMaximum(10)
        self.dial.setObjectName(_fromUtf8("dial"))
        self.verticalLayout_2.addWidget(self.dial)
        self.groupBox_2 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.valueBox = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.valueBox.setMinimum(0.1)
        self.valueBox.setMaximum(1.0)
        self.valueBox.setSingleStep(0.1)
        self.valueBox.setObjectName(_fromUtf8("valueBox"))
        self.gridLayout.addWidget(self.valueBox, 1, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.radiusBox = QtGui.QSpinBox(self.groupBox_2)
        self.radiusBox.setMinimum(2)
        self.radiusBox.setMaximum(20000)
        self.radiusBox.setObjectName(_fromUtf8("radiusBox"))
        self.gridLayout.addWidget(self.radiusBox, 2, 1, 1, 1)
        self.cellsBox = QtGui.QSpinBox(self.groupBox_2)
        self.cellsBox.setMinimum(1)
        self.cellsBox.setMaximum(9999)
        self.cellsBox.setProperty("value", 10)
        self.cellsBox.setObjectName(_fromUtf8("cellsBox"))
        self.gridLayout.addWidget(self.cellsBox, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.addButton = QtGui.QPushButton(self.frame_2)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_2.addWidget(self.addButton)
        self.optButton = QtGui.QPushButton(self.frame_2)
        self.optButton.setObjectName(_fromUtf8("optButton"))
        self.verticalLayout_2.addWidget(self.optButton)
        self.closeButton = QtGui.QPushButton(self.frame_2)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout_2.addWidget(self.closeButton)
        self.horizontalLayout.addWidget(self.frame_2)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.plotWidget = MplWidget(self.tab)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.horizontalLayout_2.addWidget(self.plotWidget)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.habWidget = MplWidget(self.tab_2)
        self.habWidget.setObjectName(_fromUtf8("habWidget"))
        self.verticalLayout.addWidget(self.habWidget)
        self.checkBox = QtGui.QCheckBox(self.tab_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.resultsWidget = MplWidget(self.tab_3)
        self.resultsWidget.setObjectName(_fromUtf8("resultsWidget"))
        self.verticalLayout_3.addWidget(self.resultsWidget)
        self.checkBox_2 = QtGui.QCheckBox(self.tab_3)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout_3.addWidget(self.checkBox_2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Optimise by adding", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Shape Options", None))
        self.label.setText(_translate("Dialog", "Shape", None))
        self.label_2.setText(_translate("Dialog", "Value", None))
        self.label_3.setText(_translate("Dialog", "Radius", None))
        self.label_4.setText(_translate("Dialog", "Cells", None))
        self.addButton.setText(_translate("Dialog", "Add Shapes", None))
        self.optButton.setText(_translate("Dialog", "Optimise", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Links", None))
        self.checkBox.setText(_translate("Dialog", "Zoom", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Habitat", None))
        self.checkBox_2.setText(_translate("Dialog", "Zoom", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Results", None))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

