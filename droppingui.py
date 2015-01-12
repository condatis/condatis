# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dropping.ui'
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

class Ui_DroppingDialog(object):
    def setupUi(self, DroppingDialog):
        DroppingDialog.setObjectName(_fromUtf8("DroppingDialog"))
        DroppingDialog.resize(645, 558)
        self.verticalLayout = QtGui.QVBoxLayout(DroppingDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(DroppingDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dropPlot2 = MplWidget(self.frame)
        self.dropPlot2.setObjectName(_fromUtf8("dropPlot2"))
        self.gridLayout.addWidget(self.dropPlot2, 0, 1, 1, 1)
        self.dropPlot1 = MplWidget(self.frame)
        self.dropPlot1.setObjectName(_fromUtf8("dropPlot1"))
        self.gridLayout.addWidget(self.dropPlot1, 0, 0, 1, 1)
        self.dropPlot3 = MplWidget(self.frame)
        self.dropPlot3.setObjectName(_fromUtf8("dropPlot3"))
        self.gridLayout.addWidget(self.dropPlot3, 1, 0, 1, 1)
        self.dropPlot4 = MplWidget(self.frame)
        self.dropPlot4.setObjectName(_fromUtf8("dropPlot4"))
        self.gridLayout.addWidget(self.dropPlot4, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(DroppingDialog)
        self.frame_2.setMaximumSize(QtCore.QSize(32000, 60))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.updateSpinBox = QtGui.QSpinBox(self.frame_2)
        self.updateSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.updateSpinBox.setMinimum(1)
        self.updateSpinBox.setMaximum(1000)
        self.updateSpinBox.setProperty("value", 10)
        self.updateSpinBox.setObjectName(_fromUtf8("updateSpinBox"))
        self.horizontalLayout.addWidget(self.updateSpinBox)
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.droppingOpen = QtGui.QPushButton(self.frame_2)
        self.droppingOpen.setMaximumSize(QtCore.QSize(40, 40))
        self.droppingOpen.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Folder-Open-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.droppingOpen.setIcon(icon)
        self.droppingOpen.setIconSize(QtCore.QSize(32, 32))
        self.droppingOpen.setObjectName(_fromUtf8("droppingOpen"))
        self.horizontalLayout.addWidget(self.droppingOpen)
        self.droppingRun = QtGui.QPushButton(self.frame_2)
        self.droppingRun.setMaximumSize(QtCore.QSize(40, 40))
        self.droppingRun.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Button-Play-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.droppingRun.setIcon(icon1)
        self.droppingRun.setIconSize(QtCore.QSize(32, 32))
        self.droppingRun.setObjectName(_fromUtf8("droppingRun"))
        self.horizontalLayout.addWidget(self.droppingRun)
        self.droppingStop = QtGui.QPushButton(self.frame_2)
        self.droppingStop.setMaximumSize(QtCore.QSize(40, 40))
        self.droppingStop.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Button-Stop-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.droppingStop.setIcon(icon2)
        self.droppingStop.setIconSize(QtCore.QSize(32, 32))
        self.droppingStop.setObjectName(_fromUtf8("droppingStop"))
        self.horizontalLayout.addWidget(self.droppingStop)
        self.droppingRefresh = QtGui.QPushButton(self.frame_2)
        self.droppingRefresh.setMaximumSize(QtCore.QSize(40, 40))
        self.droppingRefresh.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Button-Refresh-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.droppingRefresh.setIcon(icon3)
        self.droppingRefresh.setIconSize(QtCore.QSize(32, 32))
        self.droppingRefresh.setObjectName(_fromUtf8("droppingRefresh"))
        self.horizontalLayout.addWidget(self.droppingRefresh)
        self.droppingCopy = QtGui.QPushButton(self.frame_2)
        self.droppingCopy.setMaximumSize(QtCore.QSize(40, 40))
        self.droppingCopy.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/drop-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.droppingCopy.setIcon(icon4)
        self.droppingCopy.setIconSize(QtCore.QSize(32, 32))
        self.droppingCopy.setCheckable(True)
        self.droppingCopy.setObjectName(_fromUtf8("droppingCopy"))
        self.horizontalLayout.addWidget(self.droppingCopy)
        self.verticalLayout.addWidget(self.frame_2)
        self.progressBar = QtGui.QProgressBar(DroppingDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(DroppingDialog)
        QtCore.QMetaObject.connectSlotsByName(DroppingDialog)

    def retranslateUi(self, DroppingDialog):
        DroppingDialog.setWindowTitle(_translate("DroppingDialog", "Optimise By Dropping", None))
        self.label.setText(_translate("DroppingDialog", "Update every", None))
        self.label_2.setText(_translate("DroppingDialog", "cells", None))
        self.droppingOpen.setToolTip(_translate("DroppingDialog", "Open new habitat for dropping", None))
        self.droppingRun.setToolTip(_translate("DroppingDialog", "Start dropping", None))
        self.droppingStop.setToolTip(_translate("DroppingDialog", "Stop dropping", None))
        self.droppingRefresh.setToolTip(_translate("DroppingDialog", "Update Now", None))
        self.droppingCopy.setToolTip(_translate("DroppingDialog", "Copy plots to main app.", None))

from mplwidget import MplWidget
import econet_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DroppingDialog = QtGui.QDialog()
    ui = Ui_DroppingDialog()
    ui.setupUi(DroppingDialog)
    DroppingDialog.show()
    sys.exit(app.exec_())

