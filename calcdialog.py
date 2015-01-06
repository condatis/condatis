from PyQt4 import QtCore, QtGui
import calculatingui


class CalculatingDialog(QtGui.QDialog,calculatingui.Ui_CalculatingDialog):
    def __init__(self,parent=None,pcnt=[10,20,50,75,100]):
        QtGui.QDialog.__init__(self,parent),
        self.setupUi(self)
        self.stop=False
        self.percentages=pcnt

        # QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), 
        #                        self.cancel)

        self.strings=["Generating input vector","Generating output vector", "Generating free matrix", "Solving equations"]

        # for i in range(len(self.strings)):
        #     self.listWidget.addItem(self.strings[i])

    def setState(self,st):
        self.progressBar.setValue(self.percentages[st])
        QtGui.QApplication.processEvents()

    # def setStateFull(self,st):
    #     self.progressBar.setValue(st)
    #     self.listWidget.clear()
    #     print "Setting state: %d" % st
    #     for i in range(len(self.strings)):
    #         str=self.strings[i]
    #         if i <= st:
    #             str+=" - Completed"
    #         self.listWidget.addItem(str)
    #     QtGui.QApplication.processEvents()
    
    def cancel(self):
        self.stop=True
