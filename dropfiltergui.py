"""Condatis; software to assist with the planning of habitat restoration

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
(ii) a comment at the head of any file containing the source code derived from this covered work should read: ?Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  Our modification was permitted by the GNU General Public License v.3. Instructions for obtaining the original version of Condatis can be found at www.condatis.org.uk. Any modified or verbatim copies of our work must preserve this notice.? Where text in square brackets should be replaced by the appropriate numbers.
(iii) if your modified work has a user interface, the user interface should prominently display the notice: ?Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  See www.condatis.org.uk.? Where text in square brackets should be replaced by the appropriate numbers.
"""
from mplwidget import MplWidget
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np
import logging
import tables
import dropfilterui


class DropFilterDialog(QtGui.QDialog,dropfilterui.Ui_DropFilter):
    def __init__(self,parent=None,project=None):
        self.project=project
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        N=project.scenario.indlist.shape[0]
        self.horizontalSlider.setMaximum(N-1)
        self.spinBox.setMaximum(N-1)

        self.horizontalSlider.valueChanged.connect(self.sliderChanged)
        self.spinBox.valueChanged.connect(self.spinBoxChanged)
        self.closeButton.clicked.connect(self.close)
        self.exportButton.clicked.connect(self.export)

        self.draw()
        self.setFlow()

    def sliderChanged(self,val):
        self.spinBox.setValue(val)
        self.draw()
        self.setFlow()

    def spinBoxChanged(self,val):
        self.horizontalSlider.setValue(val)
        self.draw()
        self.setFlow()

    def setFlow(self):
        N=self.horizontalSlider.value()
        flows=self.project.scenario.flows.read()
        i=flows.size-N-1
        f=flows[i]
        fpc=f/flows[0]*100
        self.flowSpinBox.setValue(f)
        self.flowPCSpinBox.setValue(fpc)

    def export(self):
        self.parent().exportDroppedHabitat()

    def sync(self):
        N=self.parent().project.scenario.xnew.shape[0]
        print "Syncing filter box. N is:",N
        self.horizontalSlider.setMaximum(N-1)
        self.spinBox.setMaximum(N-1)
        self.draw()

    def draw(self):
        scn=self.project.scenario
        indlist=scn.indlist.read()
        xnew,ynew=scn.xnew.read(),scn.ynew.read()
        x=scn.x.read()
        y=scn.y.read()
#        SZ=self.project.combinedSize(
        SZX=np.max(np.array((np.max(xnew),np.max(x))))
        SZY=np.max(np.array((np.max(ynew),np.max(y))))

        da=np.zeros((SZX+1,SZY+1))
        da[x,y]=1.1

        N=self.horizontalSlider.value()
        for i in range(N):
            i1=indlist.size-i-1
            ii=indlist[i1]
            da[xnew[ii],ynew[ii]]=0.45
        can=self.plotWidget.canvas
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        cmap='Paired'
        my_cmap = plt.cm.get_cmap(cmap)
        my_cmap.set_under('w')
        my_cmap.set_over('k')
#        vmax=indlist.size
        vmax=1
        vmin=0.1
        im=can.ax.imshow(np.transpose(da),vmin=vmin,vmax=vmax,cmap=my_cmap,interpolation='nearest')
        #        can.fig.colorbar(im)
        can.draw()
        
    def closeEvent(self,event):
        self.parent().actionDropping_Filter.setChecked(False)


