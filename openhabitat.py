import openhabitatui
from PyQt4 import QtCore, QtGui
import numpy as np
import os.path
from osgeo import gdal, osr
import settingsgui 

class OpenHabitatDialog(QtGui.QDialog,openhabitatui.Ui_OpenHabDlg):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

        
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), 
                               self.findButClicked)

#        QtCore.QObject.connect(self.updateButton, QtCore.SIGNAL("clicked()"), 
#                               self.updateButClicked)

#        QtCore.QObject.connect(self.sinkPb, QtCore.SIGNAL("clicked()"), 
#                               self.sinkButClicked)
        self.buttonGroup=QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.radioButton)
        self.buttonGroup.addButton(self.radioButton_2)
        self.buttonGroup.addButton(self.radioButton_3)
        self.buttonGroup.addButton(self.radioButton_4)
        self.buttonGroup.addButton(self.radioButton_5)
        
        self.radioButton.toggled.connect(self.change)
        self.radioButton_2.toggled.connect(self.change)
        self.radioButton_3.toggled.connect(self.change)
        self.radioButton_4.toggled.connect(self.change)
        self.radioButton_5.toggled.connect(self.change)


    def get_xya_gt(self):
        fname = str(self.lineEdit.text())
        id = self.buttonGroup.checkedId();
        if os.path.isfile(fname):
            gd=gdal.Open(fname)
            try:
                h=np.array(gd.GetRasterBand(1).ReadAsArray())
            except:
                self.minSB.setValue(0)
                self.maxSB.setValue(0)
                return
            gt=gd.GetGeoTransform()
            scx=np.abs(gt[1]) 
            scy=np.abs(gt[5]) 
            ca=scx*scy
            hab=np.where(h>0)
    
            y=hab[0]
            x=hab[1]
            a=h[y,x]*1.0

            # Note case -3 requires no alteration (proportion)
            if id==-2:
                a/=100.0
            if id==-3:
                a*=1.0
            if id==-4:
                a/=ca
            if id==-5:
                a/=ca/1e6
            if id==-6:
                a=x*0+1.0
            return (x,y,a,gt)

    def getValues(self):
        fname = str(self.lineEdit.text())
#        fname = self.lineEdit.text()
        id = self.buttonGroup.checkedId();
        mincut=self.minCutSB.value()


        gd=gdal.Open(fname)
        try:
            h=np.array(gd.GetRasterBand(1).ReadAsArray())
        except:
            self.minSB.setValue(0)
            self.maxSB.setValue(0)
            return fname,id,0.0

        gt=gd.GetGeoTransform()
        scx=np.abs(gt[1]) 
        scy=np.abs(gt[5]) 
        ca=scx*scy
            
        if id==-2:
            mincut=mincut
        if id==-3:
            mincut/=100.0
        if id==-4:
            mincut/=ca
            mincut/=100.0
        if id==-5:
            mincut/=ca/1e6
            mincut/=100.0
        if id==-6:
            mincut*=1.0
            mincut/=100.0

        return fname,id,mincut

    def findButClicked(self):
        dlg=QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.AnyFile);
        dlg.setWindowTitle('Open Habitat Layer')
        path=settingsgui.appsettings.path+'/maps'
        print "PATH:",path
        dlg.setDirectory(path)
        e=dlg.exec_()
        if e:
            file=dlg.selectedFiles()[0]
            self.lineEdit.setText(file)
            self.change()

    def change(self):
        fname = str(self.lineEdit.text())
        if os.path.isfile(fname):
            (x,y,a,gt)=self.get_xya_gt()
            minh=np.min(a)
            maxh=np.max(a)
        
            self.minSB.setValue(minh)
            self.maxSB.setValue(maxh)
            

    def updateButClicked(self):
        fname = str(self.lineEdit.text())
        id = self.buttonGroup.checkedId();
        if os.path.isfile(fname):
            gd=gdal.Open(fname)
            try:
                h=np.array(gd.GetRasterBand(1).ReadAsArray())
            except:
                self.minSB.setValue(0)
                self.maxSB.setValue(0)
                return
            gt=gd.GetGeoTransform()
            scx=np.abs(gt[1]) 
            scy=np.abs(gt[5]) 
            ca=scx*scy

            hab=np.where(h>0)
    
            y=hab[0]
            x=hab[1]
            a=h[y,x]

            # Note case -3 requires no alteration (proportion)
            if id==-2:
                a/=100.0
            if id==-4:
                a/=ca
        
            if id==-5:
                a/=ca/1e6
        
            if id==-6:
                a=x*0+1.0

            minh=np.min(a)
            maxh=np.max(a)

            self.minSB.setValue(minh)
            self.maxSB.setValue(maxh)
            
