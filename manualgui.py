class ManualDialog(QtGui.QDialog,manualui.Ui_ManualDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        path=os.getcwd()
        path=getScriptPath()
        url=QtCore.QUrl.fromLocalFile(path + "/doc/manual/index.html")
        logging.debug(str(url))
        self.home()

        self.connect(self.pbBack, QtCore.SIGNAL("clicked()"), self.webView.back)
        self.connect(self.pbForwards, QtCore.SIGNAL("clicked()"), self.webView.forward)
        self.connect(self.pbHome, QtCore.SIGNAL("clicked()"), self.home)
        self.connect(self.pbClose, QtCore.SIGNAL("clicked()"), self.winclose)

    def home(self):
        path=os.getcwd()
        url=QtCore.QUrl.fromLocalFile(path + "/doc/manual/index.html")
        self.webView.load(url)

    def winclose(self):
        self.close() 

    def closeEvent(self,event):
        self.parent().actionManual.setChecked(False)
