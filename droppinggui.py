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
import gdal
import droppingui
import matplotlib.pyplot as plt
import numpy as np
import logging
import tables
import numexpr as ne
import dropfilterui
import openhabitat

class DroppingThread(QtCore.QThread):
    def __init__(self,dropdlg):
        QtCore.QThread.__init__(self)
        self.dlg=dropdlg

#    def __del__(self):
#        self.wait()

    def run(self):
        self.dropping()
        self.emit(QtCore.SIGNAL("finishedDropping()"))
        # self.dlg.plotDrop()
        # self.dlg.plotFlow()
        # self.dlg.setButtonsFinished()
        # self.dlg.parent().setButtonStates()


    def dropping(self):
        drdlg=self.dlg
        x=drdlg.x
        y=drdlg.y
        ap=drdlg.ap
        or_x,or_y,tg_x,tg_y=drdlg.or_x,drdlg.or_y,drdlg.tg_x,drdlg.tg_y
        R,disp=drdlg.R,drdlg.disp
        cell=drdlg.cell
        xnew_=drdlg.xnew
        ynew_=drdlg.ynew
        apnew_=drdlg.apnew
        ORIGZ=x.size
        bignum=np.finfo('d').max        
        xnew,ynew,apnew=removeDups(x,y,ap,xnew_,ynew_,apnew_)
        drdlg.xnew=xnew
        drdlg.ynew=ynew
        drdlg.apnew=apnew
#        cell=(scn._v_attrs.map_x_scale*1.0)/1000.0
        
        
        N=xnew.size
        #xnew,ynew,apnew=xnew_,ynew_,apnew_
#        N=5
        xc=np.concatenate((x,xnew))
        yc=np.concatenate((y,ynew))
        apc=np.concatenate((ap,apnew))
        NEWZ=xc.shape[0]

        logging.debug("New size is: %d (%d duplicates removed)",xnew_.size,xnew_.size-xnew.size)

        if N > xnew.size:
            logging.info("Limiting dropping to %d cells",xnew.size)
            N = xnew.size
            
#        scn.progressBar.setValue(0)

        M0,cin,cout,cfree=calcM0(xc,yc,apc,or_x,or_y,tg_x,tg_y,R,disp,cell)
        inds=np.arange(cin.shape[0])
        self.dlg.indlist=[]
        self.dlg.flows=[]

        self.stop=False
        self.update=False
#        N=5
        for i in range(N):
#            scn.progressBar.setValue(i/float(N-1)*100)
            cond,fl=flow(M0,cin,cout,cfree)
            tflow=np.sum(fl)
            self.dlg.flows.append(cond)
            logging.debug("Flow for %d is: %e",i,cond)
            
            # Find the index of the smallest contribution
            fl[0:ORIGZ]=bignum
            todrop=np.argmin(fl)

            # Remove column and row from input arrays
            ii=np.arange(M0.shape[0])
            ii=np.delete(ii,todrop)
            cfree=cfree[ii,ii[:,np.newaxis]]
            cin=np.delete(cin,todrop)
            cout=np.delete(cout,todrop)
            M0=diag(cin + cout + cfree.sum(axis=0))-cfree
            self.dlg.indlist.append(inds[todrop]-ORIGZ)
            inds=np.delete(inds,todrop)
            
#            if i%self.updateSpinBox.value()==0:
            if i%10==0:
                self.emit(QtCore.SIGNAL("updateplots(PyQt_PyObject)"),i/float(N-1)*100)

                #self.plotAllDrop()

            if self.update:
                self.update=False
                self.emit(QtCore.SIGNAL("updateplots(PyQt_PyObject)"),i/float(N-1)*100)

            if self.stop:
                break

        self.emit(QtCore.SIGNAL("updateplots(PyQt_PyObject)"),i/float(N-1)*100)
        self.dlg.copyMain()
#        Need to move copymain into this thread?
#        Or call self.dlg.copyMain()?
        


        

def diag(v):
    return np.identity(v.shape[0])*v

def scind(v,cell):
    return (v+.5)*cell

def calcM0(x,y,ap,or_x,or_y,tg_x,tg_y,R,disp,cell):
    alpha=2.0/disp
    cnt=R*alpha**2/(2.0*np.pi)
    
    dm=np.sqrt((scind(x,cell)-scind(or_x,cell)[:,np.newaxis])**2  + (scind(y,cell)-scind(or_y,cell)[:,np.newaxis])**2)
    K=R*alpha**2/(2.0*np.pi)*cell**4
    cin=ne.evaluate("sum(K*ap*exp(-alpha*dm),axis=0)")
    dm=np.sqrt((scind(x,cell)-scind(tg_x,cell)[:,np.newaxis])**2  + (scind(y,cell)-scind(tg_y,cell)[:,np.newaxis])**2)
    cout=ne.evaluate("sum(K*ap*exp(-alpha*dm),axis=0)")
    dm=np.sqrt((scind(x,cell)-scind(x,cell)[:,np.newaxis])**2  + (scind(y,cell)-scind(y,cell)[:,np.newaxis])**2)
    apt=ap[:,np.newaxis]
    cfree=ne.evaluate("K*ap*apt*exp(-alpha*dm)")
    dd=np.arange(cfree.shape[0])
    cfree[dd,dd]=0

    M0=diag(cin + cout + cfree.sum(axis=0))-cfree
    return M0,cin,cout,cfree

def flow(M0,cin,cout,cfree):
    w=cin-cout
    V0 = np.linalg.solve(M0,w)
    Iout=(V0+1)*cout
    Iin=(1-V0)*cin
    cond=(np.sum(Iout) + np.sum(Iin))/2.0
    cur=cfree*(V0-V0[:,np.newaxis])
    flo=np.sum(np.abs(cur)/2.0,axis=0)
    I=flo/2.0+Iout+Iin
    return cond,I


def plotDrop(inds,scn,xnew,ynew):
    da=np.zeros((256,256))
    da[scn.x.read(),scn.y.read()]=1e10
    
#    for i in range(xnew.shape[0]):
    for i in range(len(inds)):
        logging.debug("i in testDrop2: %d",i)
        ii=inds[i]
        da[xnew[ii],ynew[ii]]=i

    plt.figure(0)
    plt.clf()
    cmap='cool'
    my_cmap = plt.cm.get_cmap(cmap)
    my_cmap.set_under('w')
    my_cmap.set_over('k')
    vmax=np.max(inds)
    vmin=vmax/1e16
    plt.imshow(np.transpose(da),vmin=vmin,vmax=vmax,cmap=my_cmap,interpolation='nearest')
    plt.colorbar()
    
def isin(xnew,ynew,x,y):
    for i in range(x.size):
        if (xnew == x[i] and ynew == y[i]):
            return True
    return False

def removeDups(x,y,ap,xnew,ynew,apnew):
    xr=[]
    yr=[]
    apr=[]
    for i in range(xnew.size):
        if not isin(xnew[i],ynew[i],x,y):
            xr.append(xnew[i])
            yr.append(ynew[i])
            apr.append(apnew[i])
    nxr=np.array(xr)
    nyr=np.array(yr)
    napr=np.array(apr)
    return nxr,nyr,napr
    

def getHabitat(fname,id,mincut=0):
    gd=gdal.Open(fname)
#    h=np.array(gd.GetRasterBand(1).ReadAsArray().astype(np.int32))
    h=np.array(gd.GetRasterBand(1).ReadAsArray())
    gt=gd.GetGeoTransform()
    orx=gt[0]
    ory=gt[3]
    scx=np.abs(gt[1]) # Because we get a crazy negative number in the scale
    scy=np.abs(gt[5]) # in Jenny's Y/H data.
    ca=scx*scy

    scx=np.abs(gt[1]) # Because we get a crazy negative number in the scale
    scy=np.abs(gt[5]) # in Jenny's Y/H data.
    projection=gd.GetProjection()
    projectionName="Not Implemented"
    hab=np.where(h>mincut)

    if id==-6:
        mincut=1

    hab=np.where(h>mincut)

    y=hab[0]
    x=hab[1]
    a=h[y,x]

    print "LENGTH OF X: ",x.size
    print "mincut: ",mincut

    # Note case -3 requires no alteration (proportion)
    if id==-2:
        print "Percentage. Divide by 100"
        print "Max area",np.max(a)
        a/=100.0
    if id==-3:
        a*=1.0
    if id==-4:
        print "Area. Divide by cell area (m^2)"
        a/=ca
        
    if id==-5:
        print "Area. Divide by cell area (km^2)"
        print "Cell area:",ca
        a/=ca/1e6
        
    if id==-6:
        print "Load as mask"
        a=a*0+1.0
    
    print "A is: ", a

#    a=h[y,x]/100.0
#    a=h[x,y]/np.max(h[x,y])

    print "min a",np.min(a),"max a",np.max(a)
    return x,y,a

def dropping(xc,yc,apc,or_x,or_y,tg_x,tg_y,R,disp,ORIGZ,N=20):
    bignum=np.finfo('d').max

    M0,cin,cout,cfree=calcM0(xc,yc,apc,or_x,or_y,tg_x,tg_y,R,disp)
    inds=np.arange(cin.shape[0])
    indlist=[]
    flows=[]

    for i in range(N):
        fl=flow(M0,cin,cout,cfree)
        tflow=np.sum(fl)
        flows.append(tflow)
        logging.debug("Flow for %d is: %e",i,tflow)
        
        # Find the index of the smallest contribution
        fl[0:ORIGZ]=bignum
        todrop=np.argmin(fl)

        # Remove column and row from input arrays
        ii=np.arange(M0.shape[0])
        ii=np.delete(ii,todrop)
        cfree=cfree[ii,ii[:,np.newaxis]]
        cin=np.delete(cin,todrop)
        cout=np.delete(cout,todrop)
        M0=diag(cin + cout + cfree.sum(axis=0))-cfree
        indlist.append(inds[todrop]-ORIGZ)
        inds=np.delete(inds,todrop)
        
    return flows,indlist


class DroppingDialog(QtGui.QDialog,droppingui.Ui_DroppingDialog):
    def __init__(self,parent=None,project=None):
        self.project=project
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.thread=DroppingThread(self)

        QtCore.QObject.connect(self.droppingRun, QtCore.SIGNAL("clicked()"), 
                               self.runDrop)

        QtCore.QObject.connect(self.droppingOpen, QtCore.SIGNAL("clicked()"), 
                               self.findHabitat)

        QtCore.QObject.connect(self.droppingRefresh, QtCore.SIGNAL("clicked()"), 
                               self.setUpdate)

        QtCore.QObject.connect(self.droppingStop, QtCore.SIGNAL("clicked()"), 
                               self.stopDropping)

        QtCore.QObject.connect(self.droppingCopy, QtCore.SIGNAL("clicked()"), 
                               self.copyMain)

#        QtCore.QObject.connect(self.droppingFilter, QtCore.SIGNAL("clicked()"),self.filter)
        QtCore.QObject.connect(self.thread, QtCore.SIGNAL('updateplots(PyQt_PyObject)'),self.plotAllDrop)
        QtCore.QObject.connect(self.thread, QtCore.SIGNAL('finishedDropping()'),self.finishedDropping)

        # QtCore.QObject.connect(self.droppingSync, QtCore.SIGNAL("clicked()"), 
        #                        self.sync)

#        QtCore.QObject.connect(self.droppingExport, QtCore.SIGNAL("clicked()"), 
#                               self.export_old)


        self.bignum=np.finfo('d').max
        self.h5=self.project.h5file
        self.init()
        self.enableButtons(state=False)

    def closeEvent(self,event):
        self.parent().actionBackwards_Improvement.setChecked(False)
        print "Closing dropping dialog"

    def finishedDropping(self):
        self.plotDrop()
        self.plotFlow()
        self.plotPercentFlow()
        self.setButtonsFinished()
        self.parent().setButtonStates()

        
    def enableButtons(self,state=True):
        self.droppingOpen.setEnabled(state)
        self.droppingRun.setEnabled(state)
        self.droppingRefresh.setEnabled(state)
        self.droppingStop.setEnabled(state)
        self.droppingCopy.setEnabled(state)
#        self.droppingFilter.setEnabled(state)
#        self.droppingSync.setEnabled(state)


    def setButtonsInit(self):
        self.enableButtons(False)
        self.droppingOpen.setEnabled(True)

    def setButtonsHabLoaded(self):
        self.enableButtons(False)
        self.droppingOpen.setEnabled(True)
        self.droppingRun.setEnabled(True)

    def setButtonsRunning(self):
        self.enableButtons(False)
        self.droppingRefresh.setEnabled(True)
        self.droppingStop.setEnabled(True)
        self.droppingCopy.setEnabled(True)

    def setButtonsFinished(self):
        self.enableButtons(False)
        self.droppingOpen.setEnabled(True)
        self.droppingRun.setEnabled(True)
#        self.droppingFilter.setEnabled(True)

    def setButtons(self):
        self.setButtonsInit()
        if self.project.scenario.__contains__("xnew"):
            self.setButtonsHabLoaded()
        if self.project.scenario.__contains__("indlist"):
            self.setButtonsFinished()

    def export_old(self):
        file = QtGui.QFileDialog.getSaveFileName(self, 
            "Save Layer As..", ".", "*.tif")
        if file:
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            

    def init(self):
        self.scn=self.project.scenario
        scn=self.scn
        self.x=scn.x.read()
        self.y=scn.y.read()
        self.ap=scn.ap.read()
        self.or_x=scn.or_x.read()
        self.or_y=scn.or_y.read()
        self.tg_x=scn.tg_x.read()
        self.tg_y=scn.tg_y.read()
        self.R=scn._v_attrs.R
        self.cell=scn._v_attrs.map_x_scale/1000.0
        self.disp=scn._v_attrs.dispersal
        self.ORIGZ=scn.x.shape[0]

        self.indlist=[]
        self.flows=[]
        self.xnew=[]
        self.ynew=[]
        self.apnew=[]

        if scn.__contains__("flows"):
            self.flows=scn.flows.read()
        if scn.__contains__("indlist"):
            self.indlist=scn.indlist.read()
        if scn.__contains__("xnew"):
            self.xnew=scn.xnew.read()
        if scn.__contains__("ynew"):
            self.ynew=scn.ynew.read()
        if scn.__contains__("apnew"):
            self.apnew=scn.apnew.read()

        self.plotOrigHabitat()
        self.plotDrop()
        self.plotFlow()
        self.plotPercentFlow()

        self.setButtons()

    def sync(self):
        logging.info("Syncing dropping module")
        self.init()

    def filter(self):
        self.parent().dropFilter()

    def stopDropping(self):
        self.stop=True

    def setUpdate(self):
        self.update=True

    def copyToMainApp(self):
        pr=self.project
        h5=pr.h5file
        scenario=pr.scenario

        if scenario.__contains__('xnew'):
            scenario.xnew.remove()
        h5.createArray(scenario,'xnew',self.xnew)

        if scenario.__contains__('ynew'):
            scenario.ynew.remove()
        h5.createArray(scenario,'ynew',self.ynew)

        if scenario.__contains__('apnew'):
            scenario.apnew.remove()
        h5.createArray(scenario,'apnew',self.apnew)

        if scenario.__contains__('indlist'):
            scenario.indlist.remove()
        h5.createArray(scenario,'indlist',np.array(self.indlist))

        if scenario.__contains__('flows'):
            scenario.flows.remove()
        h5.createArray(scenario,'flows',np.array(self.flows))

    def copyMain(self):
        self.copyToMainApp()
        self.parent().droppingView()

    def findHabitat(self):
        dlg=openhabitat.OpenHabitatDialog()
        e=dlg.exec_()
        if e:
            file,id,mincut=dlg.getValues()
            print "Filename is:",file
            print "ID:",id
            print "mincut: ",mincut
            fileinfo = QtCore.QFileInfo(file)
            sfile = str(fileinfo.canonicalFilePath())
            logging.debug("Open dropping %s",sfile)
            self.xnew,self.ynew,self.apnew=getHabitat(sfile,id,mincut=mincut) 
            print "xnew",self.xnew,"ynew",self.ynew
            self.plotNewHab()
            self.enableButtons()

    def findHabitat_old(self):
        file = QtGui.QFileDialog.getOpenFileName(self, \
                    "Open Source Layer [GDAL]", ".", "[GDAL] Raster (*)")
        if file:
            sfile=str(file)
            logging.debug("Open dropping %s",sfile)
            self.xnew,self.ynew,self.apnew=getHabitat(sfile) 
            print "xnew",self.xnew,"ynew",self.ynew
            self.plotNewHab()
            self.enableButtons()
            
    def plotOrigHabitat(self):
#        SZ=self.project.combinedSize()
        SZ=self.project.rasterSize()
        im=np.zeros(SZ)
        x=self.x
        y=self.y
        for i in range(x.shape[0]):
            im[x[i],y[i]]=1
#        im=self.project.habitatMask()
        can=self.dropPlot1.canvas
        my_cmap = plt.cm.get_cmap("Paired")
        my_cmap.set_under('w')
        my_cmap.set_over('k')
        vmax=np.max(im)*.99
        vmin=vmax/1e16

        can.ax.imshow(np.transpose(im),vmax=vmax,vmin=vmin,cmap=my_cmap)
        can.draw()

    def plotNewHab(self):
        xs=self.x
        ys=self.y
        x=self.xnew
        y=self.ynew
        print xs,ys,x,y
        SZX=np.max(np.array((np.max(xs),np.max(x))))
        SZY=np.max(np.array((np.max(ys),np.max(y))))
        im=np.zeros((SZX+1,SZY+1))
        for i in range(xs.shape[0]):
            if i%100==0:
                pass
#                logging.debug("i: %d, xs: %d, ys: %d",i, xs[i],ys[i])
            im[xs[i],ys[i]]=1.0
        for i in range(x.size):
#            print i,x[i],y[i]
            im[x[i],y[i]]+=0.05
        im[np.where(im>1.0)]=0.45
        can=self.dropPlot1.canvas
        can.ax=can.fig.add_subplot(111)
        my_cmap = plt.cm.get_cmap("Paired")
        my_cmap.set_under('w')
        my_cmap.set_over('k')
        vmax=np.max(im)*.99
        vmin=vmax/1e16

        can.ax.imshow(np.transpose(im),vmax=vmax,vmin=vmin,cmap=my_cmap)
        can.draw()

    def plotDrop(self):
        can=self.dropPlot3.canvas
        if len(self.indlist)==0:
            can.fig.clf()
            can.draw()
            return
        indlist=self.indlist
        scn=self.scn
        xnew,ynew=self.xnew,self.ynew
        xs=self.x
        ys=self.y
        SZX=np.max(np.array((np.max(xs),np.max(xnew))))
        SZY=np.max(np.array((np.max(ys),np.max(ynew))))

        da=np.zeros((SZX+1,SZY+1))
        da[self.x,self.y]=1e20
    
        for i in range(len(indlist)):
            ii=indlist[i]
            da[xnew[ii],ynew[ii]]=i

#        print "Max da", np.max(da)
#        print "shape da: ",da.shape
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        cmap='cool'
        my_cmap = plt.cm.get_cmap(cmap)
        my_cmap.set_under('w')
        my_cmap.set_over('k')
        vmax=len(indlist)
        vmin=0.1
        im=can.ax.imshow(np.transpose(da),vmin=vmin,vmax=vmax,cmap=my_cmap,interpolation='nearest')
#        can.fig.colorbar(im)
        can.draw()

    def plotFlow(self):
        can=self.dropPlot2.canvas
        if len(self.flows)==0:
            can.fig.clf()
            can.draw()
            return
        fl=np.array(self.flows)
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        can.ax.plot(1.0/fl)
        can.draw()

    def plotPercentFlow(self):
        can=self.dropPlot4.canvas
        if len(self.flows)==0:
            can.fig.clf()
            can.draw()
            return
        fl=np.array(self.flows)
        fl2=(fl/fl[0])*100
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        can.ax.plot(fl2)
        can.ax.axis((0,fl.size*1.1,0,110))
        can.draw()

    def plotAllDrop(self,i):
        self.plotDrop()
        self.plotFlow()
        self.plotPercentFlow()
        self.progressBar.setValue(i)
        
    def dropping_inui(self):
        x=self.x
        y=self.y
        ap=self.ap
        or_x,or_y,tg_x,tg_y=self.or_x,self.or_y,self.tg_x,self.tg_y
        R,disp=self.R,self.disp
        xnew_=self.xnew
        ynew_=self.ynew
        apnew_=self.apnew
        ORIGZ=x.size
        bignum=np.finfo('d').max        
        xnew,ynew,apnew=removeDups(x,y,ap,xnew_,ynew_,apnew_)
        self.xnew=xnew
        self.ynew=ynew
        self.apnew=apnew
        
        
        N=xnew.size
        #xnew,ynew,apnew=xnew_,ynew_,apnew_
#        N=5
        xc=np.concatenate((x,xnew))
        yc=np.concatenate((y,ynew))
        apc=np.concatenate((ap,apnew))
        NEWZ=xc.shape[0]

        logging.debug("New size is: %d (%d duplicates removed)",xnew_.size,xnew_.size-xnew.size)

        if N > xnew.size:
            logging.info("Limiting dropping to %d cells",xnew.size)
            N = xnew.size
            
        self.progressBar.setValue(0)

        M0,cin,cout,cfree=calcM0(xc,yc,apc,or_x,or_y,tg_x,tg_y,R,disp)
        inds=np.arange(cin.shape[0])
        self.indlist=[]
        self.flows=[]

        self.stop=False
        self.update=False
#        N=5
        for i in range(N):
            self.progressBar.setValue(i/float(N-1)*100)
            cond,fl=flow(M0,cin,cout,cfree)
            tflow=np.sum(fl)
            self.flows.append(cond)
            logging.debug("Flow for %d is: %e",i,cond)
            
            # Find the index of the smallest contribution
            fl[0:ORIGZ]=bignum
            todrop=np.argmin(fl)

            # Remove column and row from input arrays
            ii=np.arange(M0.shape[0])
            ii=np.delete(ii,todrop)
            cfree=cfree[ii,ii[:,np.newaxis]]
            cin=np.delete(cin,todrop)
            cout=np.delete(cout,todrop)
            M0=diag(cin + cout + cfree.sum(axis=0))-cfree
            self.indlist.append(inds[todrop]-ORIGZ)
            inds=np.delete(inds,todrop)

            
            if i%self.updateSpinBox.value()==0: 
                self.plotAllDrop()

            if self.update:
                self.update=False
                self.plotAllDrop()

            if self.stop:
                break

        self.plotAllDrop()
        self.copyMain()

#        return flows,indlist

    
    def runDrop(self):
        self.setButtonsRunning()
#        self.parent().closeFilterDlg()

        self.thread.start()
#        self.droppingFilter.setEnabled(state=True)
        self.parent().setButtonStates()
#        self.dropping()
#        self.plotDrop()
#        self.plotFlow()


  
