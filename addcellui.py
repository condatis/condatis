# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/addcell.ui'
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

class Ui_AddCellDialog(object):
    def setupUi(self, AddCellDialog):
        AddCellDialog.setObjectName(_fromUtf8("AddCellDialog"))
        AddCellDialog.resize(549, 308)
        self.gridLayout = QtGui.QGridLayout(AddCellDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_3 = QtGui.QGroupBox(AddCellDialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pointRB = QtGui.QRadioButton(self.groupBox_3)
        self.pointRB.setChecked(True)
        self.pointRB.setObjectName(_fromUtf8("pointRB"))
        self.verticalLayout.addWidget(self.pointRB)
        self.solidCRB = QtGui.QRadioButton(self.groupBox_3)
        self.solidCRB.setObjectName(_fromUtf8("solidCRB"))
        self.verticalLayout.addWidget(self.solidCRB)
        self.starRB = QtGui.QRadioButton(self.groupBox_3)
        self.starRB.setObjectName(_fromUtf8("starRB"))
        self.verticalLayout.addWidget(self.starRB)
        self.randUniformRB = QtGui.QRadioButton(self.groupBox_3)
        self.randUniformRB.setObjectName(_fromUtf8("randUniformRB"))
        self.verticalLayout.addWidget(self.randUniformRB)
        self.randNormalRB = QtGui.QRadioButton(self.groupBox_3)
        self.randNormalRB.setObjectName(_fromUtf8("randNormalRB"))
        self.verticalLayout.addWidget(self.randNormalRB)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(AddCellDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.xSpinBox = QtGui.QSpinBox(self.groupBox)
        self.xSpinBox.setMaximum(99999)
        self.xSpinBox.setObjectName(_fromUtf8("xSpinBox"))
        self.gridLayout_2.addWidget(self.xSpinBox, 0, 1, 1, 1)
        self.ySpinBox = QtGui.QSpinBox(self.groupBox)
        self.ySpinBox.setMaximum(99999)
        self.ySpinBox.setObjectName(_fromUtf8("ySpinBox"))
        self.gridLayout_2.addWidget(self.ySpinBox, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.radiusSpinBox = QtGui.QSpinBox(self.groupBox)
        self.radiusSpinBox.setEnabled(False)
        self.radiusSpinBox.setMinimum(1)
        self.radiusSpinBox.setMaximum(999999999)
        self.radiusSpinBox.setProperty("value", 10)
        self.radiusSpinBox.setObjectName(_fromUtf8("radiusSpinBox"))
        self.gridLayout_2.addWidget(self.radiusSpinBox, 3, 1, 1, 1)
        self.valSpinBox = QtGui.QDoubleSpinBox(self.groupBox)
        self.valSpinBox.setMaximum(1.0)
        self.valSpinBox.setSingleStep(0.01)
        self.valSpinBox.setProperty("value", 1.0)
        self.valSpinBox.setObjectName(_fromUtf8("valSpinBox"))
        self.gridLayout_2.addWidget(self.valSpinBox, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.numberOfCellsSpinBox = QtGui.QSpinBox(self.groupBox)
        self.numberOfCellsSpinBox.setEnabled(False)
        self.numberOfCellsSpinBox.setMinimum(1)
        self.numberOfCellsSpinBox.setMaximum(99999999)
        self.numberOfCellsSpinBox.setProperty("value", 16)
        self.numberOfCellsSpinBox.setObjectName(_fromUtf8("numberOfCellsSpinBox"))
        self.gridLayout_2.addWidget(self.numberOfCellsSpinBox, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AddCellDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(AddCellDialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 4, 0, 1, 1)
        self.label_6 = QtGui.QLabel(AddCellDialog)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 2)
        self.checkBox = QtGui.QCheckBox(AddCellDialog)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)

        self.retranslateUi(AddCellDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddCellDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddCellDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddCellDialog)

    def retranslateUi(self, AddCellDialog):
        AddCellDialog.setWindowTitle(_translate("AddCellDialog", "Add Cells", None))
        self.groupBox_3.setTitle(_translate("AddCellDialog", "Pattern", None))
        self.pointRB.setText(_translate("AddCellDialog", "Point", None))
        self.solidCRB.setText(_translate("AddCellDialog", "Solid Circle", None))
        self.starRB.setText(_translate("AddCellDialog", "Star", None))
        self.randUniformRB.setText(_translate("AddCellDialog", "Random - Uniformly Distributed", None))
        self.randNormalRB.setText(_translate("AddCellDialog", "Random - Normally Distributed", None))
        self.groupBox.setTitle(_translate("AddCellDialog", "Cells", None))
        self.label_3.setText(_translate("AddCellDialog", "Value", None))
        self.label.setText(_translate("AddCellDialog", "Horizontal Centre", None))
        self.label_4.setText(_translate("AddCellDialog", "Radius", None))
        self.label_2.setText(_translate("AddCellDialog", "Vertical Centre", None))
        self.label_5.setText(_translate("AddCellDialog", "Number of Cells*", None))
        self.label_6.setText(_translate("AddCellDialog", "*For the star pattern, this represents the number of cells along each line. For random patterns it is the total number of cells.", None))
        self.checkBox.setText(_translate("AddCellDialog", "Redraw main map?", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AddCellDialog = QtGui.QDialog()
    ui = Ui_AddCellDialog()
    ui.setupUi(AddCellDialog)
    AddCellDialog.show()
    sys.exit(app.exec_())

