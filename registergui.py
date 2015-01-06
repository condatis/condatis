from PyQt4 import QtCore, QtGui
import registerui
import settingsgui

class registerDlg(QtGui.QDialog, registerui.Ui_Dialog):
    def __init__(self,parent=None):
        # Ui setup
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

        self.closeButton.clicked.connect(self.close)
        self.registerButton.clicked.connect(self.register)

    def register(self):
        txt=self.lineEdit.text()
        if txt=="436f6e6461746973":
            settingsgui.appsettings.registered=True
            settingsgui.saveSettings(settingsgui.appsettings)
            QtGui.QMessageBox.about(self, "Register","Thank you for registering Condatis")
            self.close()
        else:
            QtGui.QMessageBox.about(self, "Register","Sorry, the code is invalid")
