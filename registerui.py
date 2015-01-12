# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/register.ui'
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
        Dialog.resize(938, 656)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.label = QtGui.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(245, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.frame_3 = QtGui.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout = QtGui.QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.closeButton = QtGui.QPushButton(self.frame_3)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.registerButton = QtGui.QPushButton(self.frame_3)
        self.registerButton.setObjectName(_fromUtf8("registerButton"))
        self.gridLayout.addWidget(self.registerButton, 4, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.emailEdit = QtGui.QLineEdit(self.frame_3)
        self.emailEdit.setObjectName(_fromUtf8("emailEdit"))
        self.gridLayout.addWidget(self.emailEdit, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.frame)
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("http://registration.condatis.org.uk/form.html")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.horizontalLayout.addWidget(self.webView)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Register Condatis", None))
        self.label_4.setText(_translate("Dialog", "REGISTER CONDATIS", None))
        self.label_3.setText(_translate("Dialog", "Please take a moment to register Condatis. Use the web form on the right to send your details. You will be sent an email with a registration code. Type this, and your email address,  in to the box below and press \'Regsiter\'.", None))
        self.label.setText(_translate("Dialog", "Why register? Firstly, if we know what our users are using the software for, that will help us to improve its functionality in the future. Secondly, this is a not-for-profit project and the more users we have, the more likely we are to obtain funding to develop it further. Thirdly, we will give priority to registered users when they request help.\n"
"We will send you one e-mail, a few months after you register, to askhow you\'re getting on. We will not send further unsolicited e-mail unless you contact us or you choose to join our mailing list. If you have a query about registration, or wish to leave the mailing list, please e-mail econets@liverpool.ac.uk.", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))
        self.label_2.setText(_translate("Dialog", "Registration Code:", None))
        self.registerButton.setText(_translate("Dialog", "Register", None))
        self.label_5.setText(_translate("Dialog", "Email:", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

