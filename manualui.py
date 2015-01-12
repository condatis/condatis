# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/manual.ui'
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

class Ui_ManualDialog(object):
    def setupUi(self, ManualDialog):
        ManualDialog.setObjectName(_fromUtf8("ManualDialog"))
        ManualDialog.resize(568, 645)
        self.verticalLayout = QtGui.QVBoxLayout(ManualDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(ManualDialog)
        self.frame.setMaximumSize(QtCore.QSize(240, 80))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pbBack = QtGui.QPushButton(self.frame)
        self.pbBack.setMinimumSize(QtCore.QSize(0, 0))
        self.pbBack.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pbBack.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Actions-go-previous-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbBack.setIcon(icon)
        self.pbBack.setIconSize(QtCore.QSize(32, 32))
        self.pbBack.setObjectName(_fromUtf8("pbBack"))
        self.horizontalLayout.addWidget(self.pbBack)
        self.pbForwards = QtGui.QPushButton(self.frame)
        self.pbForwards.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pbForwards.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Actions-go-next-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbForwards.setIcon(icon1)
        self.pbForwards.setIconSize(QtCore.QSize(32, 32))
        self.pbForwards.setObjectName(_fromUtf8("pbForwards"))
        self.horizontalLayout.addWidget(self.pbForwards)
        self.pbHome = QtGui.QPushButton(self.frame)
        self.pbHome.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Actions-go-home-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbHome.setIcon(icon2)
        self.pbHome.setIconSize(QtCore.QSize(32, 32))
        self.pbHome.setObjectName(_fromUtf8("pbHome"))
        self.horizontalLayout.addWidget(self.pbHome)
        self.pbClose = QtGui.QPushButton(self.frame)
        self.pbClose.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pbClose.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Actions-process-stop-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbClose.setIcon(icon3)
        self.pbClose.setIconSize(QtCore.QSize(32, 32))
        self.pbClose.setObjectName(_fromUtf8("pbClose"))
        self.horizontalLayout.addWidget(self.pbClose)
        self.verticalLayout.addWidget(self.frame)
        self.webView = QtWebKit.QWebView(ManualDialog)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)

        self.retranslateUi(ManualDialog)
        QtCore.QMetaObject.connectSlotsByName(ManualDialog)

    def retranslateUi(self, ManualDialog):
        ManualDialog.setWindowTitle(_translate("ManualDialog", "Manual", None))
        self.pbBack.setToolTip(_translate("ManualDialog", "Backwards", None))
        self.pbForwards.setToolTip(_translate("ManualDialog", "Forwards", None))
        self.pbHome.setToolTip(_translate("ManualDialog", "Index", None))
        self.pbClose.setToolTip(_translate("ManualDialog", "Close manual", None))

from PyQt4 import QtWebKit
import econet_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ManualDialog = QtGui.QDialog()
    ui = Ui_ManualDialog()
    ui.setupUi(ManualDialog)
    ManualDialog.show()
    sys.exit(app.exec_())

