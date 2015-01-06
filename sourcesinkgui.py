from PyQt4 import QtCore, QtGui
import sourcesinkui

class SourceSinkDialog(QtGui.QDialog, sourcesinkui.Ui_SourceSinkDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.sourcePb, QtCore.SIGNAL("clicked()"), 
                               self.sourceButClicked)
        # QtCore.QObject.connect(self.clearSrcPB, QtCore.SIGNAL("clicked()"), 
        #                        self.clearSource)
        # QtCore.QObject.connect(self.clearTargetPB, QtCore.SIGNAL("clicked()"), 
        #                        self.clearTarget)
        # QtCore.QObject.connect(self.clearBothPB, QtCore.SIGNAL("clicked()"), 
        #                        self.clearBoth)
        self.buttonGroup=QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.radioButton)
        self.buttonGroup.addButton(self.radioButton_2)
        self.buttonGroup.addButton(self.radioButton_3)
        self.buttonGroup.addButton(self.radioButton_4)

        self.clearGroup=QtGui.QButtonGroup()
        self.clearGroup.addButton(self.clearSourceRB)
        self.clearGroup.addButton(self.clearTargetRB)
        self.clearGroup.addButton(self.clearBothRB)
                                
    def getValues(self):
        if self.tabWidget.currentIndex() == 0:
            return 0,self.sourceText.text(),self.srcValSpinBox.value(),self.snkValSpinBox.value()
        if self.tabWidget.currentIndex() == 1:
            id = self.buttonGroup.checkedId();
            width=self.spinBox_2.value()
            ch=self.checkBox_2.isChecked()
            return 1,id,width,ch
        if self.tabWidget.currentIndex()==2:
            clr=self.clearGroup.checkedId()
            return 2,clr

    def sourceButClicked(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 
            "Open Source Layer [GDAL]", ".", "[GDAL] Raster (*)")
        self.sourceText.setText(file)

    def sinkButClicked(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 
            "Open Target Layer [GDAL]", ".", "[GDAL] Raster (*)")
        self.sinkText.setText(file)
