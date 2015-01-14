"""
Condatis; software to assist with the planning of habitat restoration

www.condatis.org.uk

Copyright (c) 2015 D.W. Wallis and J.A. Hodgson

The latest information about Condatis can be found at www.condatis.org.uk, including links to the source distribution, preferred citations, and contact details for the copyright holders.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License (GPL) as published by the Free Software Foundation, version 3 of the license, and the additional term below. 
Additional term under GNU GPL version 3 section 7.

A1) If you convey a modified version of this work:
(i) you should delete the text that appears in the Acknowledgements tab of the About box in the Condatis user interface.
(ii) a comment at the head of any file containing the source code derived from this covered work should read: "Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  Our modification was permitted by the GNU General Public License v.3. Instructions for obtaining the original version of Condatis can be found at www.condatis.org.uk. Any modified or verbatim copies of our work must preserve this notice." Where text in square brackets should be replaced by the appropriate numbers.
(iii) if your modified work has a user interface, the user interface should prominently display the notice: "Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  See www.condatis.org.uk." Where text in square brackets should be replaced by the appropriate numbers.
"""
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
