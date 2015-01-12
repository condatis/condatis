from PyQt4 import QtCore, QtGui
import registerui
import settingsgui
import hashlib

class registerDlg(QtGui.QDialog, registerui.Ui_Dialog):
    def __init__(self,parent=None):
        # Ui setup
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

        self.closeButton.clicked.connect(self.close)
        self.registerButton.clicked.connect(self.register)
        
        
    def register(self):
        # Have to convert to a string or the MD5 is wrong
        email=str(self.emailEdit.text())
        txt=self.lineEdit.text()
        code = hashlib.md5("Condatis"+email).hexdigest()
        if txt==code:
            settingsgui.appsettings.registered=True
            settingsgui.saveSettings(settingsgui.appsettings)
#            QtGui.QMessageBox.about(self, "Register","Thank you for registering Condatis")
            self.close()
        else:
            QtGui.QMessageBox.about(self, "Register","Sorry, the code is invalid")
