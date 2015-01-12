from PyQt4 import QtCore, QtGui
import settingsui
import matplotlib.pyplot as plt
import numpy as np
import os.path
import cPickle as pickle

class Settings():
    def __init__(self):
        self.habitatcm=57
        self.voltagecm=13
        self.flowcm=42
        self.powercm=42
        self.reverse=[False,False,False,False]
        self.scalebarlength=10
        self.path=os.path.expanduser('~')+'/condatis'
        self.manpath='doc/manual'
        self.path=''
        # self.projectpath='/projects'
        # self.exports='/exports'
        self.cmaps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))
        self.registered=False

    def exportspath(self):
        return self.path+'exports'

    def mapsPath(self):
        return self.path+'maps'

    def projectsPath(self):
        return self.path+'projects'

    def getMap(self,cm,rev):
        ending=''
        if rev:
            ending='_r'
        return self.cmaps[cm]+ending

    def gethabitatcm(self):
        return self.getMap(self.habitatcm,self.reverse[0])
    
    def getvoltagecm(self):
        return self.getMap(self.voltagecm,self.reverse[1])

    def getflowcm(self):
        return self.getMap(self.flowcm,self.reverse[2])

    def getpowercm(self):
        return self.getMap(self.powercm,self.reverse[3])
    
def saveSettings(s):
    with open("condatis.save","wb") as f:
        pickle.dump(s,f)

def loadSettings():
    with open("condatis.save","rb") as f:
        return pickle.load(f)

    
class SettingsDialog(QtGui.QDialog,settingsui.Ui_settingsDialog):
    def __init__(self,parent=None,project=None):
#        self.project=project
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        initcmapvals=[57,13,42,42]
        self.cmaps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))

        self.habComboBox.addItems(self.cmaps)
        self.voltageComboBox.addItems(self.cmaps)
        self.flowComboBox.addItems(self.cmaps)
        self.powerComboBox.addItems(self.cmaps)

        self.voltageComboBox.setCurrentIndex(initcmapvals[1])
        self.flowComboBox.setCurrentIndex(initcmapvals[2])
        self.powerComboBox.setCurrentIndex(initcmapvals[3])
        self.habComboBox.setCurrentIndex(initcmapvals[0])

        self.habComboBox.currentIndexChanged.connect(self.onHabChange)
        self.voltageComboBox.currentIndexChanged.connect(self.onVoltageChange)
        self.flowComboBox.currentIndexChanged.connect(self.onFlowChange)
        self.powerComboBox.currentIndexChanged.connect(self.onPowerChange)

        self.habReverse.stateChanged.connect(self.onHabChange)
        self.voltageReverse.stateChanged.connect(self.onVoltageChange)
        self.flowReverse.stateChanged.connect(self.onFlowChange)
        self.powerReverse.stateChanged.connect(self.onPowerChange)

        self.habComboBox.setFocus()
        self.plotCb(self.cmaps[self.habComboBox.currentIndex()])

    def onHabChange(self,val):
        col=self.cmaps[self.habComboBox.currentIndex()]
        if self.habReverse.isChecked():
            col+='_r'
        self.plotCb(col)

    def onVoltageChange(self,val):
        col=self.cmaps[self.voltageComboBox.currentIndex()]
        if self.voltageReverse.isChecked():
            col+='_r'
        self.plotCb(col)
        
    def onFlowChange(self,val):
        col=self.cmaps[self.flowComboBox.currentIndex()]
        if self.flowReverse.isChecked():
            col+='_r'
        self.plotCb(col)

    def onPowerChange(self,val):
        col=self.cmaps[self.powerComboBox.currentIndex()]
        if self.powerReverse.isChecked():
            col+='_r'
        self.plotCb(col)

    def plotCb(self,colmap):
        self.currentMap=colmap
        cbar=self.cbar.canvas.ax
        im=np.arange(255)*np.ones(10)[:,np.newaxis]
        cbar.set_xticklabels([])
        cbar.set_yticklabels([])
        cbar.imshow(im,aspect='auto',cmap=colmap)
        self.cbar.canvas.draw()

    def getMap(self,combobox,checkbox):
        ending=''
        if checkbox.isChecked():
            ending='_r'
        return self.cmaps[combobox.currentIndex()]+ending

    def setFromSettings(self,s):
        self.habComboBox.setCurrentIndex(s.habitatcm)
        self.habReverse.setChecked(s.reverse[0])

        self.voltageComboBox.setCurrentIndex(s.voltagecm)
        self.voltageReverse.setChecked(s.reverse[1])

        self.flowComboBox.setCurrentIndex(s.flowcm)
        self.flowReverse.setChecked(s.reverse[2])

        self.powerComboBox.setCurrentIndex(s.powercm)
        self.powerReverse.setChecked(s.reverse[3])

        self.condatisEdit.setText(s.path)
        self.manualEdit.setText(s.manpath)
        self.scalebarSB.setProperty("value", s.scalebarlength)

    def getRawData(self):
        s=Settings()
        s.habitatcm=self.habComboBox.currentIndex()
        s.reverse[0]=self.habReverse.isChecked()
        s.voltagecm=self.voltageComboBox.currentIndex()
        s.reverse[1]=self.voltageReverse.isChecked()
        s.flowcm=self.flowComboBox.currentIndex()
        s.reverse[2]=self.flowReverse.isChecked()
        s.powercm=self.powerComboBox.currentIndex()
        s.reverse[3]=self.powerReverse.isChecked()
        s.path=self.condatisEdit.text()
        s.manpath=self.manualEdit.text()
        s.scalebarlength = self.scalebarSB.value()
        return s
        
        
appsettings=Settings()
        


