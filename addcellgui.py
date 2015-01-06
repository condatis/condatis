from mplwidget import MplWidget
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import logging
import tables
import addcellui



class AddCellDialog(QtGui.QDialog,addcellui.Ui_AddCellDialog):
    def __init__(self,parent=None,project=None):
        self.project=project
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.comboBox.addItems(['Habitat','Source','Target'])
        self.pointRB.toggled.connect(self.setPointOptions)
        self.solidCRB.toggled.connect(self.setCircleOptions)
        self.starRB.toggled.connect(self.setOtherOptions)
#        self.bBallRB.toggled.connect(self.setOtherOptions)
        self.randUniformRB.toggled.connect(self.setOtherOptions)
        self.randNormalRB.toggled.connect(self.setOtherOptions)

        self.buttonGroup=QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.pointRB)
        self.buttonGroup.addButton(self.solidCRB)
        self.buttonGroup.addButton(self.starRB)
        self.buttonGroup.addButton(self.randUniformRB)
        self.buttonGroup.addButton(self.randNormalRB)

        
    def setxy(self,x,y):
        self.xSpinBox.setValue(x)
        self.ySpinBox.setValue(y)

    def getValues(self):
        return self.xSpinBox.value(),self.ySpinBox.value(),self.valSpinBox.value(),self.radiusSpinBox.value(),self.numberOfCellsSpinBox.value()

    def getLayer(self):
        return self.comboBox.currentIndex()

    def getPattern(self):
        return self.buttonGroup.checkedId()

    def setPointOptions(self,state):
        if state:
            self.radiusSpinBox.setEnabled(False)
            self.numberOfCellsSpinBox.setEnabled(False)
        
    def setCircleOptions(self,state):
        if state:
            self.radiusSpinBox.setEnabled(True)
            self.numberOfCellsSpinBox.setEnabled(False)
        
    def setOtherOptions(self,state):
        if state:
            self.radiusSpinBox.setEnabled(True)
            self.numberOfCellsSpinBox.setEnabled(True)
