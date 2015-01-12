# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dropfilter.ui'
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

class Ui_DropFilter(object):
    def setupUi(self, DropFilter):
        DropFilter.setObjectName(_fromUtf8("DropFilter"))
        DropFilter.resize(655, 528)
        self.verticalLayout = QtGui.QVBoxLayout(DropFilter)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plotWidget = MplWidget(DropFilter)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.verticalLayout.addWidget(self.plotWidget)
        self.groupBox = QtGui.QGroupBox(DropFilter)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalSlider = QtGui.QSlider(self.groupBox)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout.addWidget(self.horizontalSlider, 0, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(self.groupBox)
        self.spinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.spinBox.setReadOnly(False)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(999999)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtGui.QFrame(DropFilter)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.flowSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.flowSpinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.flowSpinBox.setDecimals(22)
        self.flowSpinBox.setMaximum(999999999.0)
        self.flowSpinBox.setObjectName(_fromUtf8("flowSpinBox"))
        self.horizontalLayout.addWidget(self.flowSpinBox)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.flowPCSpinBox = QtGui.QDoubleSpinBox(self.frame)
        self.flowPCSpinBox.setDecimals(5)
        self.flowPCSpinBox.setMaximum(100.0)
        self.flowPCSpinBox.setObjectName(_fromUtf8("flowPCSpinBox"))
        self.horizontalLayout.addWidget(self.flowPCSpinBox)
        self.exportButton = QtGui.QPushButton(self.frame)
        self.exportButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Layers-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportButton.setIcon(icon)
        self.exportButton.setIconSize(QtCore.QSize(32, 32))
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.horizontalLayout.addWidget(self.exportButton)
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Button-Close-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon1)
        self.closeButton.setIconSize(QtCore.QSize(32, 32))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(DropFilter)
        QtCore.QMetaObject.connectSlotsByName(DropFilter)

    def retranslateUi(self, DropFilter):
        DropFilter.setWindowTitle(_translate("DropFilter", "Filter Dropped Cells", None))
        self.groupBox.setTitle(_translate("DropFilter", "Number of cells", None))
        self.label_2.setText(_translate("DropFilter", "Flow", None))
        self.label.setText(_translate("DropFilter", "Flow (%)", None))
        self.exportButton.setToolTip(_translate("DropFilter", "Export as GIS layer", None))
        self.closeButton.setToolTip(_translate("DropFilter", "Close", None))

from mplwidget import MplWidget
import econet_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DropFilter = QtGui.QDialog()
    ui = Ui_DropFilter()
    ui.setupUi(DropFilter)
    DropFilter.show()
    sys.exit(app.exec_())

