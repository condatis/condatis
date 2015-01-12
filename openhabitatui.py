# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/openhabitat.ui'
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

class Ui_OpenHabDlg(object):
    def setupUi(self, OpenHabDlg):
        OpenHabDlg.setObjectName(_fromUtf8("OpenHabDlg"))
        OpenHabDlg.resize(446, 541)
        self.verticalLayout = QtGui.QVBoxLayout(OpenHabDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(OpenHabDlg)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.frame)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.frame)
        self.groupBox = QtGui.QGroupBox(OpenHabDlg)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.verticalLayout_2.addWidget(self.radioButton_3)
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.verticalLayout_2.addWidget(self.radioButton_4)
        self.radioButton_5 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        self.verticalLayout_2.addWidget(self.radioButton_5)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.label_5)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(OpenHabDlg)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 220))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame_2 = QtGui.QFrame(self.groupBox_2)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.minSB = QtGui.QDoubleSpinBox(self.frame_2)
        self.minSB.setMinimum(-999999999.0)
        self.minSB.setMaximum(999999999.0)
        self.minSB.setSingleStep(1e-06)
        self.minSB.setObjectName(_fromUtf8("minSB"))
        self.horizontalLayout_3.addWidget(self.minSB)
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.maxSB = QtGui.QDoubleSpinBox(self.frame_2)
        self.maxSB.setMinimum(-999999999.0)
        self.maxSB.setMaximum(999999999.0)
        self.maxSB.setSingleStep(1e-06)
        self.maxSB.setObjectName(_fromUtf8("maxSB"))
        self.horizontalLayout_3.addWidget(self.maxSB)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.groupBox_2)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_6 = QtGui.QLabel(self.frame_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        self.minCutSB = QtGui.QDoubleSpinBox(self.frame_3)
        self.minCutSB.setObjectName(_fromUtf8("minCutSB"))
        self.horizontalLayout_2.addWidget(self.minCutSB)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(OpenHabDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OpenHabDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OpenHabDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OpenHabDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenHabDlg)

    def retranslateUi(self, OpenHabDlg):
        OpenHabDlg.setWindowTitle(_translate("OpenHabDlg", "Open Habitat Layer", None))
        self.label.setText(_translate("OpenHabDlg", "Habitat Layer", None))
        self.pushButton.setText(_translate("OpenHabDlg", "Find", None))
        self.groupBox.setTitle(_translate("OpenHabDlg", "Value of each cell represents", None))
        self.radioButton.setText(_translate("OpenHabDlg", "Percentage of the cell that contains habitat.", None))
        self.radioButton_2.setText(_translate("OpenHabDlg", "Proportion of the cell that contains habitat.", None))
        self.radioButton_3.setText(_translate("OpenHabDlg", "Habitat area in m^2.", None))
        self.radioButton_4.setText(_translate("OpenHabDlg", "Habitat area in km^2.", None))
        self.radioButton_5.setText(_translate("OpenHabDlg", "Load as mask  (presence / absence).*", None))
        self.label_5.setText(_translate("OpenHabDlg", "* Area information will be lost.", None))
        self.groupBox_2.setTitle(_translate("OpenHabDlg", "Cell area limits**", None))
        self.label_2.setText(_translate("OpenHabDlg", "Minimum", None))
        self.label_3.setText(_translate("OpenHabDlg", "Maximum", None))
        self.label_6.setText(_translate("OpenHabDlg", "Minimum percentage cell area to include", None))
        self.label_4.setText(_translate("OpenHabDlg", "**Maximum should be approximately 1 with layers that contain a cell with 100% habitat. Minimum is the minimum cell area and will be 1 for masks.", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OpenHabDlg = QtGui.QDialog()
    ui = Ui_OpenHabDlg()
    ui.setupUi(OpenHabDlg)
    OpenHabDlg.show()
    sys.exit(app.exec_())

