from PyQt4 import QtCore, QtGui
import addingui
import numpy as np
import matplotlib.pyplot as plt
import ecoplot
import math
import patterns
import copy
import numexpr as ne

# The above function '2opNinds2' is probably a better approach
# but without the triangular bit.
def topNinds_(full,N=10):
    # Get the indices for the largest `num_largest` values.
    num_largest = N
    indices = (-full).argpartition(num_largest, axis=None)[:num_largest]
    xl, yl = np.unravel_index(indices, full.shape)
    return xl,yl

def mid(x1,x2):
    return (x2-x1)/2.0 + x1

def piv(xp,yp):
    return mid(xp[1],xp[0]),mid(yp[1],yp[0])
    
def lnlength(xp,yp):
    return math.sqrt((xp[1]-xp[0])**2 + (yp[1]-yp[0])**2)


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

class AddingThread(QtCore.QThread):
    def __init__(self,dlg):
        QtCore.QThread.__init__(self)
        self.dlg=dlg
        self.project=dlg.project
#        self.dlg=addingdlg
        self.flowarray=0
        
    def run(self):
        print "Running add"
        self.adding()
        print "Adding finished"
#        self.emit(QtCore.SIGNAL("finishedAdding()"))

    def adding(self):
        print "In adding"
        pr=self.project
        scn=pr.scenario

        print "Getting parameters"
        # Get scenario parameters
        x=scn.x.read()
        y=scn.y.read()
        ap=scn.ap.read()
        or_x=scn.or_x.read()
        or_y=scn.or_y.read()
        tg_x=scn.tg_x.read()
        tg_y=scn.tg_y.read()
        R=scn._v_attrs.R
        cell=scn._v_attrs.map_x_scale/1000.0
        disp=scn._v_attrs.dispersal
        ORIGZ=scn.x.shape[0]

        print "copying"
        # Make a copy of x,y,ap
        copyx=np.zeros(x.size)
        copyy=np.zeros(x.size)
        copyap=np.zeros(x.size)
        copyx[:]=x[:]
        copyy[:]=y[:]
        copyap[:]=ap[:]
        
        print "makeing flow array"
        # Array to hold the results
        self.flowarray=np.zeros(copyx.size+1)

        print "Calulating base flow"
        # get flow for no added cell
        print "Calculating M0"
        M0,cin,cout,cfree=calcM0(copyx,copyy,copyap,or_x,or_y,tg_x,tg_y,R,disp,cell)
        print "Calculating flow"
        cond,fl=flow(M0,cin,cout,cfree)
        print "cond is:",cond
        print "setting flow"
        self.flowarray[0]=cond

        print "Drop parameters"
        print "R:",R
        print "Disp:",disp
        print "Cell:",cell

        
        print "Get new habitat"
        xnew,ynew,apnew=self.dlg.getNewHab()

        print "Original flow is ", cond
        
        print "starting loop"
        for i in range(xnew.size):
            print "In adding loop:",i
            workingx=np.append(copyx,xnew[i])
            workingy=np.append(copyy,ynew[i])
            workingap=np.append(copyap,apnew[i])

            M0,cin,cout,cfree=calcM0(copyx,copyy,copyap,or_x,or_y,tg_x,tg_y,R,disp,cell)
            cond,fl=flow(M0,cin,cout,cfree)
            self.flowarray[i+1]=cond
            print "Flow for %i is %2.15e" % (i,cond)
        
class addingDlg(QtGui.QDialog, addingui.Ui_Dialog):
    def __init__(self,parent=None,project=None):
        # Ui setup
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.comboBox.addItems(['Random','Beach Ball','Circle','Star','Normal'])
        self.NLINKS=100
        self.dial.setMaximum(self.NLINKS)
        
        # Variables
        self.project=project
        self.currentLink=0

        self.thread=AddingThread(self)
        
        # Connections
        self.dial.valueChanged.connect(self.dialChanged)
        self.closeButton.clicked.connect(self.close)
        self.addButton.clicked.connect(self.add)
        self.optButton.clicked.connect(self.optimise)
        
        # Actions
        self.calcTopInds()
        self.init2()


        
    def init2(self):
        self.x, self.y=self.project.habitat()
        self.hab=self.project.nodeVoltageA()
        self.newHab=self.hab*0.0
        self.draw(self.currentLink)
        self.showNewHab()

        
    def calcTopInds(self):
        print "Calculating top inds"
        self.i,self.j=topNinds_(self.project.edgePower(),N=self.NLINKS+1)
        print "Calculated"
        
    def dialChanged(self,val):
        self.lcdNumber.display(val)
        self.draw(val)
        self.currentLink=val
        xp,yp=self.getLine(val)
        self.radiusBox.setValue(lnlength(xp,yp))
        
    def closeEvent(self,event):
        self.parent().actionForward_Optimise.setChecked(False)

    def getLine(self,N):
        x,y=self.project.habitat()
        ii=self.i[N]
        jj=self.j[N]
        x1=x[ii]
        x2=x[jj]
        y1=y[ii]
        y2=y[jj]
        xp=[x1,x2]
        yp=[y1,y2]
        return xp,yp
    
    def drawLink(self,N):
        can=self.plotWidget.canvas
        xp,yp=self.getLine(N)
        can.ax.plot(xp,yp,color='red')
        
    def draw(self,val):
        can=self.plotWidget.canvas
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        my_cmap = plt.cm.get_cmap('Paired')
        im=ecoplot.myIM(can,self.hab)
        self.drawLink(val)
        ecoplot.fullzoom(can,self.project)
        can.draw()

    def showNewHab(self):
        can=self.habWidget.canvas
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        my_cmap = plt.cm.get_cmap('Paired')
        im=ecoplot.myIM(can,self.newHab)
        ecoplot.fullzoom(can,self.project)
        can.draw()
        

    def addRandom(self,xc,yc,R,cells,val):
        print "Making random pattern"
        x,y=patterns.uniform(xc,yc,R,cells)
        print self.newHab.shape
        self.newHab[x,y]=val
        
    def add(self):
        xp,yp=self.getLine(self.currentLink)
        xc,yc=piv(xp,yp)
        print "xc,yc",xc,yc
        cells=self.cellsBox.value()
        print "cells",cells
        R=self.radiusBox.value()
        val=self.valueBox.value()
        
        pat=self.comboBox.currentIndex()
        if pat==0:
            self.addRandom(xc,yc,R,cells,val)

        self.showNewHab()

    def getNewHab(self):
        x,y=np.where(self.newHab)
        v=self.newHab[(x,y)]
        return x,y,v
        
    def optimise(self):
        x,y,v=self.getNewHab()
        print "x",x
        print "y",y
        print "v",v
        
        self.thread.start()
