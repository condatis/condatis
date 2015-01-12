#import lscclass.lscclass
import numpy as np
# The next line is needed by cx_Freeze
import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt
import project.dwwspatial as sp
import project.vlevels as vlevels
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
from PIL import ImageDraw
import calculatingui
import calcdialog  
import gc
import scipy.sparse
import tables
import logging
import scipy.interpolate
import settingsgui as settings

topgap=.95
bottomgap=.05
leftgap=.05
rightgap=.95

cols=['white','black', 'DarkRed',
      'OliveDrab', 'DodgerBlue', 
      'GoldenRod','PowderBlue',
      'DarkSlateBlue','red','DarkGray']

interp='nearest'
#globorig='upper'
globorig='lower'


def plotScaleBar(can, project,colour='green'):
    sblen=10000.0
    sbkm=settings.appsettings.scalebarlength
    sblen=sbkm*1000.0
    cs=project.cellSizeX()
    pix=sblen/cs
    x=[10,pix+10]
    y=[10,10]
    can.ax.plot(x,y,color=colour)
    can.ax.text(pix+20,10, "%dkm" % sbkm,color=colour)

def initfig(can,ticksOff=True):
    can.fig.clf()
    can.ax=can.fig.add_subplot(111)
    if ticksOff:
        can.ax.set_xticklabels([])
        can.ax.set_yticklabels([])
    can.draw()

def showNull(can,project):
    initfig(can)
    pass


def fullSTzoom(can,project):
    x,y=project.combinedSize()
    xmax=x-1
    ymax=y-1
    
    can.ax.axis((0,xmax,0,ymax))
    can.ax.invert_yaxis()

def fullzoom(can,project):
#    x,y=project.combinedSize()
    x,y=project.mapSize()
    xmax=x-1
    ymax=y-1
    
    can.ax.axis((0,xmax,0,ymax))
    can.ax.invert_yaxis()
#    xmin,ymin,xmax,ymax=lsc.areaBounds()
#    marg=0
#    #print "Xmin: %d, ymin: %d, xmax: %d, ymax: %d" % (xmin,ymin,xmax,ymax)
#    can.ax.axis((-marg,xmax+marg,-marg,ymax+marg))

def showVoltageContour(can,project):
    if project.hasBeenCalculated():
        initfig(can)
        x,y=project.habitat()
        v=project.nodeVoltage()
        XZ=project.rasterSize()[0]
        YZ=project.rasterSize()[1]
        xx,yy=np.meshgrid(np.arange(XZ),np.arange(YZ))
        gd=scipy.interpolate.griddata((x,y),v,(xx,yy),method="cubic")
        cs=can.ax.contourf(xx,-yy,gd,cmap=settings.appsettings.getvoltagecm())
        can.fig.colorbar(cs)
        cp=can.ax.contour(xx,-yy,gd,colors='k',hold='on')
        can.ax.clabel(cp)
        can.ax.set_title("Progress Contours")
        can.draw()
    
def showVoltageLayersContour(can,project):
    if project.hasBeenCalculated():
        initfig(can)
        x,y=project.habitat()
        v=project.nodeVoltage()
        XZ=project.rasterSize()[0]
        YZ=project.rasterSize()[1]
        xx,yy=np.meshgrid(np.arange(XZ),np.arange(YZ))
        gd=scipy.interpolate.griddata((x,y),v,(xx,yy),method="cubic")
        can.ax.contourf(xx,-yy,gd)
        can.ax.contour(xx,-yy,gd,colors='k',hold='on')
        can.draw()
    
def showHabitat(can,project):
    global globorig
    global interp
    initfig(can)
    if project.hasHabitat():
#        im=myIM(can,project.nodeAreaA(),cmap='gist_rainbow')
        dat=project.nodeAreaA()
        cm=settings.appsettings.gethabitatcm()
        im=can.ax.imshow(np.transpose(dat),interpolation=interp,origin='upper',cmap=cm)

#        im.set_cmap('gist_rainbow')
        can.ax.set_title("Habitat")
        can.fig.colorbar(im)
#        fullzoom(can,project)
        plotScaleBar(can,project)
        fullzoom(can,project)
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
#        divider = make_axes_locatable(can.ax)
#        cax = divider.append_axes("right", size="5%", pad=0.05)
#        plt.colorbar(im, cax=cax)
        can.draw()

def myIM(can,im,alpha=1.0,vmin=-0.01,cmap='Paired'):
    global globorig
    global interp
    my_cmap = plt.cm.get_cmap(cmap)
    my_cmap.set_under('w')
    vmax=np.max(im)
    vmin=vmax/1e16
    im=can.ax.imshow(np.transpose(np.asarray(im)),
                     vmin=vmin,vmax=vmax,cmap=my_cmap,alpha=alpha,interpolation=interp,origin=globorig)
    can.draw()
    return im
        

def showDroppingNewHab(can,proj):
    global interp
    initfig(can)
    if proj.hasDropped():
        xs=proj.scenario.x.read()
        ys=proj.scenario.y.read()
        x=proj.scenario.xnew
        y=proj.scenario.ynew
        SZX=np.max(np.array((np.max(xs),np.max(x))))
        SZY=np.max(np.array((np.max(ys),np.max(y))))
        im=np.zeros((SZX+1,SZY+1))
        for i in range(xs.shape[0]):
            im[xs[i],ys[i]]=1.0
        for i in range(x.shape[0]):
            im[x[i],y[i]]+=0.05
        im[np.where(im>1.0)]=0.45
        my_cmap = plt.cm.get_cmap("Paired")
        my_cmap.set_under('w')
        my_cmap.set_over('k')
        vmax=np.max(im)*.99
        vmin=vmax/1e16
        can.ax.imshow(np.transpose(im),vmax=vmax,vmin=vmin,cmap=my_cmap,interpolation=interp)
        plotScaleBar(can,proj)
        fullzoom(can,proj)
        can.draw()

def showDroppingDropped(can,proj):
    global interp
    initfig(can)
    if proj.hasDropped():
        scn=proj.scenario
        indlist=scn.indlist.read()
        xnew,ynew=scn.xnew.read(),scn.ynew.read()
        x=scn.x.read()
        y=scn.y.read()
        SZX=np.max(np.array((np.max(xnew),np.max(x))))
        SZY=np.max(np.array((np.max(ynew),np.max(y))))
        da=np.zeros((SZX+1,SZY+1))
        da[x,y]=1e20

        for i in range(indlist.size):
            ii=indlist[i]
            da[xnew[ii],ynew[ii]]=i
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        cmap='cool'
        my_cmap = plt.cm.get_cmap(cmap)
        my_cmap.set_under('w')
        my_cmap.set_over('k')
        vmax=indlist.size
        vmin=0.1
        im=can.ax.imshow(np.transpose(da),vmin=vmin,vmax=vmax,cmap=my_cmap,interpolation='nearest')
        can.fig.colorbar(im)
        plotScaleBar(can,proj)
        fullzoom(can,proj)
        can.draw()
        
def showDroppingFlow(can,project):
    initfig(can)
    if project.hasDropped():
        fl=np.array(project.scenario.flows.read())
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        can.ax.plot(1./fl)
        can.ax.set_title("Speed")
        can.ax.set_ylabel("Speed")
        can.ax.set_xlabel("Number of Cells")
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()
    
def showDroppingPCFlow(can,project):
    initfig(can)
    if project.hasDropped():
        fl=np.array(project.scenario.flows.read())
        fl=fl/fl[0]*100
        can.fig.clf()
        can.ax=can.fig.add_subplot(111)
        can.ax.axis((0,fl.size*1.1,0,110))
        can.ax.plot(fl)
        can.ax.set_title("Percentage Flow")
        can.ax.set_ylabel("Percentage Flow")
        can.ax.set_xlabel("Number of Cells")
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        plotScaleBar(can,project)
        can.draw()
    
def showSource(can,project):
    global globorig
    initfig(can)
    if project.hasSource():
        im=can.ax.imshow(np.transpose(project.sourceMask()),interpolation='nearest',origin=globorig)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        cm=settings.appsettings.gethabitatcm()
        im.set_cmap(cm)
        can.ax.set_title("Source")
        plotScaleBar(can,project)
        fullSTzoom(can,project)
        can.draw()

def showSink(can,project):
    global globorig
    initfig(can)
    if project.hasSink():
        im=can.ax.imshow(np.transpose(project.sinkMask()),interpolation='nearest',origin=globorig)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        cm=settings.appsettings.gethabitatcm()
        im.set_cmap(cm)
        can.ax.set_title("Target")
        plotScaleBar(can,project)
        fullSTzoom(can,project)
        can.draw()

def showHabSourceSink(can,project):
    initfig(can)
    if project.hasSourceOrSink() and project.hasHabitat():
        hab=project.habitatMask()
        src=project.sourceMask()
        snk=project.sinkMask()
        m=hab*3+src+snk*2
        im=can.ax.imshow(np.transpose(m),interpolation='nearest')
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        cm=settings.appsettings.gethabitatcm()
        im.set_cmap(cm)
        can.ax.set_title("Habitat, Source and Target")
        plotScaleBar(can,project)
        fullSTzoom(can,project)
        can.draw()

def showVoltage(can,project):
    initfig(can)
    if project.hasBeenCalculated():
        im=myIM(can,project.nodeVoltageA(),cmap=settings.appsettings.getvoltagecm())
        fullzoom(can,project)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        can.ax.set_title("Progress")
        can.fig.colorbar(im)
        plotScaleBar(can,project)
        can.draw()

def showFlow(can,project):
    initfig(can)
    if project.hasBeenCalculated():
        im=myIM(can,project.nodeFlowA(),cmap=settings.appsettings.getflowcm())
        fullzoom(can,project)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        can.ax.set_title("Flow")
        can.fig.colorbar(im)
        plotScaleBar(can,project)
        can.draw()

def showPatchLoss(can,project):
    initfig(can)
    if project.metricsCalculated():
        im=myIM(can,project.patchLossA())
        fullzoom(can,project)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        can.ax.set_title("Survival Core")
        can.fig.colorbar(im)
        plotScaleBar(can,project)
        can.draw()

def showPatchPArea(can,project):
    initfig(can)
    if project.metricsCalculated():
        im=myIM(can,project.patchPAreaA())
        fullzoom(can,project)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        can.ax.set_title("Area Loss")
        can.fig.colorbar(im)
        plotScaleBar(can,project)
        can.draw()

def calcVoltageLayers(project):
    V0=project.nodeVoltage()
    x,y=project.habitat()
    xz,yz=project.rasterSize()
    ls=np.zeros([xz,yz])
    project.calcSplitLevels()
    vs=project.levels
    for i in range(7+1):
        inds=project.grabLevel(i)
        meanV=np.mean(V0[inds])
        ls+=sp.xyv22d(x[inds],y[inds],xz,yz)*(i+1)-.0
    return ls

def showVoltageLayers(can,project,alpha=1,clear=True,scalebar=True):
    if project.hasBeenCalculated():
        if clear:
            initfig(can)
        global cols
        V0=project.nodeVoltage()
        x,y=project.habitat()
        xz,yz=project.rasterSize()
        ls=np.zeros([xz,yz])
        project.calcSplitLevels()
        vs=project.levels
        for i in range(7+1):
            inds=project.grabLevel(i)
            meanV=np.mean(V0[inds])
            ls+=sp.xyv22d(x[inds],y[inds],xz,yz)*(i+1)-.0
        im=myIM(can,ls/np.max(ls),alpha=alpha)
        fullzoom(can,project)
        can.ax.set_title("Isolated Areas")
        if scalebar:
            can.fig.colorbar(im,ticks=range(11))
        plotScaleBar(can,project)
        can.draw()

def showSortedVoltage(can,project):
    initfig(can,ticksOff=False)
    if project.hasBeenCalculated():
        sV0=np.sort(project.nodeVoltage())
        can.ax.plot(sV0,'black')
        can.ax.set_title("Layers")
        can.ax.set_xlabel("Habitat cell (sorted)")
        can.ax.set_ylabel("Progress")
        can.ax.axis([0,sV0.size,-.5,1.5])
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

def showConnections(can,project):
    initfig(can,ticksOff=False)

def showFlowComparison(can,project):
    initfig(can,ticksOff=False)
    y=project.allFlows()
    x=np.arange(y.size)
#    logging.debug("Flow Comparisons, x: %d" % x)
#    logging.debug("Flow Comparisons, y: %f" % y)
    binnames=project.allNames()
    can.ax.set_xticks(x+.3)
    can.ax.set_xticklabels(binnames)
    width=.6
    can.ax.bar(x,y,width)
    can.ax.set_title('Speed')
    can.ax.set_xlabel("Scenario")
    can.ax.set_ylabel("Speed")
#    can.ax.axis([-.5,y.size-.5,0,np.max(y)*1.2])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()

def showAreaComparison(can,project):
    initfig(can,ticksOff=False)
    y=project.allAreas()
    x=np.arange(y.size)
    binnames=project.allNames()
    can.ax.set_xticks(x+.3)
    can.ax.set_xticklabels(binnames)
    width=.6
    can.ax.bar(x,y,width)
    can.ax.set_title('Landscape Area')
    can.ax.set_xlabel("Scenario")
    can.ax.set_ylabel("Area")
#    can.ax.axis([-.5,y.size-.5,0,np.max(y)*1.2])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()

def showMetapopComparison(can,project):
    initfig(can,ticksOff=False)
    y=project.allMetapopCapacity()
    x=np.arange(y.size)
    binnames=project.allNames()
    can.ax.set_xticks(x+.3)
    can.ax.set_xticklabels(binnames)
    width=.6
    can.ax.bar(x,y,width)
    can.ax.set_title('Metatpopulation Capacity')
    can.ax.set_xlabel("Scenario")
    can.ax.set_ylabel("Metapopulation Capacity")
#    can.ax.axis([-.5,y.size-.5,0,np.max(y)*1.2])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()

def showTLSComparison(can,project):
    initfig(can,ticksOff=False)
    y=project.allTLS()
    x=np.arange(y.size)
    binnames=project.allNames()
    can.ax.set_xticks(x+.3)
    can.ax.set_xticklabels(binnames)
    width=.6
    can.ax.bar(x,y,width)
    can.ax.set_title('Total Link Strength')
    can.ax.set_xlabel("Scenario")
    can.ax.set_ylabel("Total Link Strength")
#    can.ax.axis([-.5,y.size-.5,0,np.max(y)*1.2])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()


############### ADDING ######################################
def grabLevel(project,L):
    V0=project.nodeVoltage()
    vs=project.levels
    ind=np.where((V0 > vs[L]) & (V0  <= vs[L+1]))[0]
    return ind
    
def closestPoint(project,L1,L2):
    la1=grabLevel(project,L1)
    la2=grabLevel(project,L2)
    x,y=project.habitat()
    return vlevels.closest(la1,la2,x,y) #,self.soln)

def closestInd(project,L1,L2):
    la1=grabLevel(project,L1)
    la2=grabLevel(project,L2)
    x,y=project.habitat()
    return vlevels.closestInd(la1,la2,x,y)#,self.soln)

def closestComb(project,L1,L2):
    la1=grabLevel(project,L1)
    la2=grabLevel(project,L2)
    x,y=project.habitat()
    return vlevels.closestComb(la1,la2,x,y)

def connection(project,L1,L2):
    x1,y1,x2,y2=closestPoint(project,L1,L2)
    xx1,yy1=closestInd(project,L1,L2)
    P=project.edgePower()
    Pl=P[xx1,yy1][0]
#    xx=np.array([x1,x2])
#    yy=np.array([y1,y2])
    xx=(x1,x2)
    yy=(y1,y2)
    return xx,yy,Pl

def connections(project):
    r = [[0]*8 for i in xrange(8)] 
    for i in range(8):
        for j in range(8):
            r[i,j]=connection(project,i,j)
    return r

def bestconnections(project):
    r=[]
    pom=np.max(project.edgePower())
    thresh=pom*project.powerThreshold/100.0
    for i in range(8):
        for j in range(8):
            tx,ty,tp=connection(project,i,j)
            if tp > thresh:
                r.append((tx,ty,tp))
    return r

def midp(a1,a2):
    return (a2-a1)/2.0 + a1

def midpoint(x1,y1,x2,y2):
    return midp(x1,x2),midp(y1,y2)

def defineNewPatches(project):
    l=bestconnections(project)
    N=len(l)
#    r=np.zeros(3,N)
    r=[]
    for i in l:
        x1=i[0][0]
        x2=i[0][1]
        y1=i[1][0]
        y2=i[1][1]
        power=i[2]
        mid=midpoint(x1,y1,x2,y2)
        pat=list(mid)
        pat.append(power)
        r.append(pat)
    L=len(r)/2
    return np.array(r[0:L])

def showTopPowers(can,project):
#    showVoltageLayers(can,project,scalebar=False)
    project.calcSplitLevels()
    ra=defineNewPatches(project)
#    #print ra
    xa=ra[:,0]
    ya=ra[:,1]
    pa=ra[:,2]
#    #print "X is: ",xa
#    #print "Y is: ",ya
    can.ax.plot(xa,ya,'ro')
    can.draw()

def showImprovement(can,project):
    project.calcSplitLevels()
    ra=defineNewPatches(project)
#    #print ra
    xa=ra[:,0]
    ya=ra[:,1]
    pa=ra[:,2]
#    #print "X is: ",xa
#    #print "Y is: ",ya
    N=xa.size
    for i in range(N):
        x=xa[i]
        y=ya[i]
        

def connectVoltageLayersPower(can,project,L1in,L2in,P):
    L1=L1in
    L2=L2in
#    #print "Doing closest point"
    x1,y1,x2,y2=closestPoint(project,L1,L2)
#    #print "Doing closest ind"
    xx1,yy1=closestInd(project,L1,L2)
#    #print "Getting edge power"
#    P=project.edgePower()
#    #print "Getting power level"
    Pl=P[xx1,yy1][0]
    colval=np.abs(Pl/np.max(P))
    col=plt.cm.Paired(colval)
    xx=np.array([x1,x2])
    yy=np.array([y1,y2])
    wval=4
#    thresh=np.max(P)*project.powerThreshold/100.0
    thresh=project.powerThreshold/100.0
#    #print "Threshold is %e" % thresh
    if colval < thresh:
        wval=.1
    can.ax.plot(xx,yy,color=col,linewidth=wval)
    if colval >= thresh:
        logging.debug("Connection: x1: %f, y1: %f, x2: %f, y2: %f",x1,x2,y1,y2)
        mx,my=midpoint(x1,y1,x2,y2)
#        #print "Mid x: %f" % mx
#        #print "Mid y: %f" % my


def calcVoltageLayersPower_(project,L1in,L2in,P):
    L1=L1in
    L2=L2in
#    #print "Doing closest point"
    x1,y1,x2,y2=closestPoint(project,L1,L2)
#    #print "Doing closest ind"
    xx1,yy1=closestInd(project,L1,L2)
#    #print "Getting edge power"
#    P=project.edgePower()
#    #print "Getting power level"
    Pl=P[xx1,yy1][0]
    colval=np.abs(Pl/np.max(P))
    col=plt.cm.Paired(colval)
    xx=np.array([x1,x2])
    yy=np.array([y1,y2])
    return xx,yy,colval

def rect(v,N):
    M=v.shape[0]
    return np.tile(v,N).reshape(N,M)

def removeClosestTemps(sc):
    if sc.__contains__('x1'):
        sc.x1.remove()
    if sc.__contains__('x2'):
        sc.x2.remove()
    if sc.__contains__('y1'):
        sc.y1.remove()
    if sc.__contains__('y2'):
        sc.y2.remove()
    if sc.__contains__('r'):
        sc.r.remove()

def closestComb(la1,la2,x,y,project):
    sc=project.scenario
    h5=project.h5file
    logging.info("Making m1")
    m1=rect(la1,la2.shape[0])
    logging.info(">Making m2")
    m2=np.transpose(rect(la2,la1.shape[0]))

    logging.info(">Making x1,x2,y1,y2")
    removeClosestTemps(sc)
    x1=h5.createArray(sc,'x1',x[m1])
    y1=h5.createArray(sc,'y1',y[m1])
    x2=h5.createArray(sc,'x2',x[m2])
    y2=h5.createArray(sc,'y2',y[m2])
    # x1=x[m1]
    # y1=y[m1]
    # x2=x[m2]
    # y2=y[m2]

    logging.info(">making r")
    rf=h5.create_carray(sc,'r',tables.Float64Atom(),sc.x1.shape)
    ex=tables.Expr('sqrt((x1-x2)**2 + (y1-y2)**2)')
    ex.set_output(rf)
    ex.eval()
    r=sc.r.read()
#    r=np.sqrt((x1-x2)**2 + (y1-y2)**2)
    logging.info(">Doing where")
    mn=np.where(r==np.min(r))
    logging.info(">Assigning")

    xx1=sc.x1.read()[mn[0],mn[1]][0]
    xx2=sc.x2.read()[mn[0],mn[1]][0]
    yy1=sc.y1.read()[mn[0],mn[1]][0]
    yy2=sc.y2.read()[mn[0],mn[1]][0]

    xx1m=m1[mn[0],mn[1]]
    xx2m=m2[mn[0],mn[1]]

    logging.info(">returning")
    return xx1,yy1,xx2,yy2,xx1m,xx2m


def calcVoltageLayersPower(project,L1,L2,P):
    la1=grabLevel(project,L1)
    la2=grabLevel(project,L2)
    x,y=project.habitat()
    x1,y1,x2,y2,xx1,yy1=closestComb(la1,la2,x,y,project)
    Pl=P[xx1,yy1][0]
    colval=np.abs(Pl/np.max(P))
    col=plt.cm.Paired(colval)
    xx=np.array([x1,x2])
    yy=np.array([y1,y2])
    return xx,yy,colval

def calcAllVLP(project,P):
    NLEVS=8
    P=project.edgePower()
#    VLP = [[calcVoltageLayersPower(project,i,j,P) for i in range(8)] for j in range(8)]

    dlg=calcdialog.CalculatingDialog(pcnt=np.arange(NLEVS)*100.0/NLEVS)
    dlg.setWindowTitle('Calculating Layer Connections')
    dlg.show()
    dlg.setState(0)

    VLP=[]
    for j in range(NLEVS):
        dlg.setState(j)
        VLP.append([calcVoltageLayersPower(project,i,j,P) for i in range(NLEVS)])
    return VLP
    dlg.hide()

def plotVoltageLayer(can,project,xx,yy,colval):
    col=plt.cm.Paired(colval)
    wval=4
    thresh=project.powerThreshold/100.0
    if colval < thresh:
        wval=.1
    can.ax.plot(xx,yy,color=col,linewidth=wval)


def plotPowerConnects(can,project,N=8):
    P=project.edgePower()
    VLP=project.scVLP()
    if not VLP:
        VLP=calcAllVLP(project,P)
        project.scVLPadd(VLP)
    for i in range(0,N):
        for j in range(0,N):
            if not i==j:
                xxi,yyj,colval=VLP[i][j]
                plotVoltageLayer(can,project,xxi,yyj,colval)

def plotPowerConnects_(can,project,N=8):
    P=project.edgePower()
    for i in range(0,N):
        for j in range(0,N):
#            #print "i: %d, j: %d" % (i,j)
            if not i==j:
                connectVoltageLayersPower(can,project,i,j,P)


def showPowerConnects(can,project):#,N=8,fig=6):
    initfig(can)
    if project.powerCalculated():
        global cols
        V0=project.nodeVoltage()
        x,y=project.habitat()
        xz,yz=project.rasterSize()
        ls=np.zeros([xz,yz])
        project.calcSplitLevels()
        vs=project.levels
        for i in range(7+1):
            inds=project.grabLevel(i)
            meanV=np.mean(V0[inds])
            ls+=sp.xyv22d(x[inds],y[inds],xz,yz)*(i+1)-.0
        im=myIM(can,ls/np.max(ls))
        fullzoom(can,project)
        can.ax.set_title("Bottlenecks Between Isolated Areas")
        plotPowerConnects(can,project)
        can.fig.colorbar(im,ticks=range(11))
        plotScaleBar(can,project)
        can.draw()
    
def powerConnects(can,project,N=8):
    project.calcSplitLevels()
    rp=np.zeros((N,N))
    ri=np.zeros((N,N))
    rj=np.zeros((N,N))
    for i in range(0,N):
        for j in range(0,N):
            if not i==j:
                x1,y1,x2,y2=closestPoint(project,i,j)
                xx1,yy1=closestInd(project,i,j)
                P=project.edgePower()
                Pl=P[xx1,yy1][0]
                ri[i,j],rj[i,j],rp[i,j]=xx1,yy1,P[xx1,yy1]
    return ri,rj,np.triu(rp)
    
def showTopPowersOld(can,project):
    initfig(can)
    ii,jj,pp=powerConnects(can,project)
    #print ii.flatten()
    #print jj.flatten()
    #print pp.flatten()

    ppf=pp.flatten()
    inds=np.argsort(ppf)

    iisf=ii.flatten()[inds]
    jjsf=jj.flatten()[inds]
    ppsf=pp.flatten()[inds]

    maxpow=np.max(ppsf)

    wval=np.where(ppsf>maxpow*project.powerThreshold/100.)
    ppsf_=ppsf[wval]
    iisf_=iisf[wval]
    jjsf_=jjsf[wval]

    #print iisf_
    NNi=ii2f_[0]
    NNj=jj2f_[0]
    x,y=project.habitat()
    x1,y1=x[NN],y[NN]

    can.ax
    
def topNinds2(A,N=10):
    at=np.triu(A)
    af=at.flatten()
    aas=np.argsort(af)[-N:]
    return np.unravel_index(aas,A.shape)

# The above function '2opNinds2' is probably a better approach
# but without the triangular bit.
def topNinds_(full,N=10):
    # Get the indices for the largest `num_largest` values.
    num_largest = N
    indices = (-full).argpartition(num_largest, axis=None)[:num_largest]
    xl, yl = np.unravel_index(indices, full.shape)
    return xl,yl

def topNinds(project,full,N=10):
    top=project.scTopNInds(full,N)
    if top:
        return top
    else:
        top=topNinds_(full,N)
        project.scTopNIndsadd(top)
        return top
        

def showVoltageLayersForPower(can,project,alpha=.1):
    global cols
    V0=project.nodeVoltage()
    x,y=project.habitat()
    xz,yz=project.rasterSize()
    ls=np.zeros([xz,yz])
    project.calcSplitLevels()
    vs=project.levels
    for i in range(7+1):
        inds=project.grabLevel(i)
        meanV=np.mean(V0[inds])
        ls+=sp.xyv22d(x[inds],y[inds],xz,yz)*(i+1)-.0
    ls=ls/8.0*project.maxPower()
    im=myIM(can,ls,alpha=alpha)
    fullzoom(can,project)
    can.fig.colorbar(im)
    can.draw()

def showBackgroundForPower(can,project,alpha=.5):
    global cols
    V0=project.nodeVoltage()
    x,y=project.habitat()
    xz,yz=project.rasterSize()
    ls=np.zeros([xz,yz])+1
    ls[x,y]=0
    im=myIM(can,ls,alpha=alpha)
    im.set_cmap("hot")
    fullzoom(can,project)
#    can.fig.colorbar(im)
    can.draw()


def renderEdges(project,x,y,M,XZ,YZ,N=100):
    """ Renders the N biggest links in matrix M onto a PIL image """
    logging.info("Before topNinds")
    i,j=topNinds(project,M,N=N)
    logging.info("After topNinds")
    x1=x[i]
    x2=x[j]
    y1=y[i]
    y2=y[j]
#    img = Image.new('F',(265,265),0.0)
    img = Image.new('F',(XZ,YZ),0.0)
    draw = ImageDraw.Draw(img)

    ra=np.arange(N)
    #print "M shape: ",M.shape
    Mall=M[i[ra],j[ra]]
#    #print "Mall shape: ",Mall.shape
#    #print "i,j: ",i,j
    isorted=np.argsort(Mall)
    for item in range(N):
#        #print "In loop: ",item
        ii=isorted[item]
        color=M[i[ii],j[ii]]
        draw.line(((x1[ii],y1[ii]),(x2[ii],y2[ii])), fill=color, width=1)

    return img

def renderPower(project,N):
    XZ,YZ=project.rasterSize()
    img = Image.new('F',(XZ,YZ),0.0)
    draw = ImageDraw.Draw(img)

    sc=project.scenario
    sigx1=sc.sigx1.read()
    sigy1=sc.sigy1.read()
    sigx2=sc.sigx2.read()
    sigy2=sc.sigy2.read()
    sigep=sc.sig_pow.read()
    asep=np.argsort(sigep)[::-1]

    x1=sigx1[asep]
    y1=sigy1[asep]
    x2=sigx2[asep]
    y2=sigy2[asep]
    ep=sigep[asep]

    for ii in range(N)[::-1]:
        color=ep[ii]
        draw.line(((x1[ii],y1[ii]),(x2[ii],y2[ii])), fill=color, width=1)
    return img

def cooreshape(a, shape):
    """Reshape the sparse matrix `a`.

    Returns a coo_matrix with shape `shape`.
    """
    if not hasattr(shape, '__len__') or len(shape) != 2:
        raise ValueError('`shape` must be a sequence of two integers')

    c = a.tocoo()
    nrows, ncols = c.shape
    size = nrows * ncols

    new_size =  shape[0] * shape[1]
    if new_size != size:
        raise ValueError('total size of new array must be unchanged')

    flat_indices = ncols * c.row + c.col
    new_row, new_col = divmod(flat_indices, shape[1])

    b = scipy.sparse.coo_matrix((c.data, (new_row, new_col)), shape=shape)
    return b

def showSigEdgePower(can,project):
    initfig(can)
    if project.powerCalculated():
        sc=project.scenario

        spu=project.scenario.sig_pow.read()
        sp=np.sort(spu)
        csp=np.cumsum(sp)
#        print "sp",sp
#        print "csp",csp
        maxcsp=np.max(csp)
        yt=maxcsp-csp
        thresh=project.cumPowerThreshold/100.0 * maxcsp
        w=np.where(yt<thresh)[0]
        N=w.size
        logging.info("Drawing  %i lines on power map" % N)

        rend=renderPower(project,N)
        pl=np.asarray(rend)
        im=myIM(can, np.transpose(pl),cmap=settings.appsettings.getpowercm())
        can.fig.colorbar(im)
        showBackgroundForPower(can,project)
        fullzoom(can,project)
        can.draw()

def showEdgePower(can,project,N=100,alpha=.3):
    initfig(can)
    if project.powerCalculated():
        dlg=calcdialog.CalculatingDialog(pcnt=np.arange(7)*100.0/7)
        dlg.setWindowTitle('Calculating Power Connections')
        dlg.show()
        dlg.setState(0)

        pp=project.edgePower()
        frc=project.cumPowerThreshold/100.0
        pp2=pp[np.where(pp>np.max(pp)*frc)]
        logging.info("Flattening")
        ppf=pp2.flatten()
        logging.info("Sorting")
        pps=np.sort(ppf)
        logging.info("Cumulative sum")
        pp_cum=np.cumsum(pps)
        dlg.setState(3)
        frc=project.cumPowerThreshold/100.0
        mx=float(pp_cum.max())
        logging.debug("Power max and fraction is: %f, %f",mx,frc)
        logging.info("Finding Fraction")
        ppw=np.where(pp_cum>mx*frc)[0]
        N=ppw.size


        dlg.setState(4)
        logging.info("Number of power links to plot: %d",N)
        initfig(can)

        x,y=project.habitat()
        XZ,YZ=project.rasterSize()
        logging.info("Rendering")

        rend=renderEdges(project,x,y,project.edgePower(),XZ,YZ,N)

        dlg.setState(5)
        logging.debug("Min rend: %f, max rend: %f",np.min(rend),np.max(rend))

        pl=np.asarray(rend)
        logging.debug("Min im: %f, max im: %f",np.min(pl),np.max(pl))
        im=myIM(can, np.transpose(pl),cmap=settings.appsettings.getpowercm())
        can.fig.colorbar(im)

        logging.info("Showing voltage layers")
        showBackgroundForPower(can,project)
#        showVoltageLayersForPower(can,project)

        logging.info("Setting title")
        can.ax.set_title("Bottlenecks")
        logging.info("Drawing")
        dlg.setState(6)
        plotScaleBar(can,project)
        can.draw()
        dlg.hide()

        logging.info("Done")

def showEdgePower__(can,project,N=100,alpha=.3):
    dlg=calcdialog.CalculatingDialog(pcnt=np.arange(7)*100.0/7)
    dlg.setWindowTitle('Calculating Power Connections')
    dlg.show()
    dlg.setState(0)

    pp=project.edgePower()
    frc=project.cumPowerThreshold/100.0
    pp2=pp[np.where(pp>np.max(pp)*frc)]
    del(pp)
    gc.collect()
    #print "Flattening"
    ppf=pp2.flatten()
    #print "Sorting"
    pps=np.sort(ppf)
    #print "Cumulative sum"
    pp_cum=np.cumsum(pps)
#    ppw=pp_cum


    dlg.setState(3)
    frc=project.cumPowerThreshold/100.0
    mx=float(pp_cum.max())
    #print "Power max and fraction is: %f, %f" % (mx,frc)
    #print "Finding Fraction"
    ppw=np.where(pp_cum>mx*frc)[0]
#    #print ppw
    N=ppw.size
    dlg.setState(4)
    #print "Number of power links to plot: %d" % N
    initfig(can)
#    showVoltageLayers(can,project)
    x,y=project.habitat()
    XZ,YZ=project.rasterSize()
    #print "Rendering"
    rend=renderEdges(x,y,project.edgePower()*1e6,XZ,YZ,N)
#    rend=renderEdges(x,y,project.edgePower(),XZ,YZ,N)
#    rend=renderEdges(x,y,pp,XZ,YZ,N)
    dlg.setState(5)
    #print "Min rend: %f, max rend: %f" % (np.min(rend),np.max(rend))

    im=np.asarray(rend)
    #print "Min im: %f, max im: %f" % (np.min(im),np.max(im))
    myIM(can, np.transpose(im))
#    can.ax.plot(0,0,np.max(project.edgePower()))
    #print "Showing voltage layers"
    showVoltageLayersForPower(can,project)
    #print "Setting title"
    can.ax.set_title("Top Powers")
    #print "Drawing"
    dlg.setState(6)
    can.draw()
    #print "Done"

def showEdgePower_(can,project,N=100,alpha=.3):
    dlg=calcdialog.CalculatingDialog(pcnt=np.arange(7)*100.0/7)
    dlg.setWindowTitle('Calculating Power Connections')
    dlg.show()
    dlg.setState(0)

#    pp=project.edgePower()

#    frc=project.cumPowerThreshold/100.0
#    pp2=pp[np.where(pp>np.max(pp)*frc)]
#    del(pp)
#    gc.collect()
    # #print "Flattening"
    # ppf=pp2.flatten()
    # #print "Sorting"
    # pps=np.sort(ppf)
    # #print "Cumulative sum"
    # pp_cum=np.cumsum(pps)
    # ppw=pp_cum
 #   del(pp_cum)
 #   gc.collect()
    #print "Getting sparse matrix"
    ppi=project.sparseEdgePower()
    #print "Flattening"
    #print "ppi size: ", ppi.size
    #print "ppi shape: ", ppi.shape
    sh=ppi.shape
    zz=sh[0]*sh[1]
    pp=cooreshape(ppi,((1,zz)))
#    pp=ppi.reshape((ppi.size,))
#    pp=ppi.flatten()
    dlg.setState(1)
    #print "Sorting"
    pps=np.sort(pp)
    dlg.setState(2)
    #print "Cumulative sum"
    pp_cum=np.cumsum(pps)
    dlg.setState(3)
    frc=project.cumPowerThreshold/100.0
    mx=float(pp_cum.max())
    #print "Power max and fraction is: %f, %f" % (mx,frc)
    #print "Finding Fraction"
    ppw=np.where(pp_cum>mx*frc)[0]
#    #print ppw
    N=ppw.size
    dlg.setState(4)
    #print "Number of power links to plot: %d" % N
    initfig(can)
#    showVoltageLayers(can,project)
    x,y=project.habitat()
    XZ,YZ=project.rasterSize()
    #print "Rendering"
#    rend=renderEdges(x,y,project.edgePower()*1e6,XZ,YZ,N)
    rend=renderEdges(x,y,project.edgePower(),XZ,YZ,N)
#    rend=renderEdges(x,y,pp,XZ,YZ,N)
    dlg.setState(5)
    #print "Min rend: %f, max rend: %f" % (np.min(rend),np.max(rend))

    im=np.asarray(rend)
    #print "Min im: %f, max im: %f" % (np.min(im),np.max(im))
    myIM(can, np.transpose(im))
#    can.ax.plot(0,0,np.max(project.edgePower()))
    #print "Showing voltage layers"
    showVoltageLayersForPower(can,project)
    #print "Setting title"
    can.ax.set_title("Top Powers")
    #print "Drawing"
    dlg.setState(6)
    can.draw()
    #print "Done"


def showCumSumLog_(can,project):
    initfig(can,ticksOff=False)
    pp=project.sigPower()
    pp_cum=np.cumsum(pp)
    frc=project.cumPowerThreshold/100.0
    ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
    N=pp.size*1.0
    x=np.arange(N)/(N-1.0)*100.0
    can.ax.plot(x,pp_cum)
    can.ax.set_yscale('log')
    can.ax.set_title("Cummulative  Sum")  
    can.ax.set_ylabel("Cummulative Sum Power")
    can.ax.set_xlabel("Percentage of Power")
#    can.ax.axis([0,sV0.size,-.5,1.5])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()


def showCumSum_whatsthis(can,project):
    initfig(can,ticksOff=False)
    if project.powerCalculated():
        sc=project.scenario
        ppshape=sc._v_attrs.edgePowerShape
        pp=project.sigPower()
        sigshape=pp.shape
        sigsize=sigshape[0]
        ppsize=ppshape[0]*ppshape[1]
        prop=sigshape[0]*1.0/ppsize
        print "orig prop",prop
        # new
        prop=sigsize*1.0/ppsize
        print "new prop", prop
        # end new
        logging.debug("percent: %d", prop*100)
        logging.debug("1-pc: %f",(1.0-prop)*100)
        L=np.arange(sigsize)*1.0/sigsize*100
        L=L*prop+(1.0-prop)*100
        logging.debug("min x: %f", np.min(L))
        logging.debug("max x: %f", np.max(L))
        pp_cum=np.cumsum(pp)
        frc=project.cumPowerThreshold/100.0
        ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
        N=pp.size*1.0

        x=L
        can.ax.plot(x,pp_cum)

        can.ax.set_title("Cummulative  Sum")  
        can.ax.set_ylabel("Cummulative Sum Power")
        can.ax.set_xlabel("Percentage of Power")
        can.ax.axis([99,100,0,sc._v_attrs.maxEdgePower])

        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

def showCumSumLog_(can,project):
    initfig(can,ticksOff=False)
    sc=project.scenario
    ppshape=sc._v_attrs.edgePowerShape
    pp=project.sigPower()
    sigshape=pp.shape
    sigsize=sigshape[0]
    #print "pp shape", ppshape
    #print "sig shape", sigshape
    ppsize=ppshape[0]*ppshape[1]
    prop=sigshape[0]*1.0/ppsize
    #print "percent:", prop*100
    #print "1-pc",(1.0-prop)*100
    L=np.arange(sigsize)*1.0/sigsize*100
    L=L*prop+(1.0-prop)*100
    #print "min x", np.min(L)
    #print "max x", np.max(L)
    pp_cum=np.cumsum(pp)
    frc=project.cumPowerThreshold/100.0
    ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
    N=pp.size*1.0
#    x=np.arange(N)/(N-1.0)*100.0
    x=L
    can.ax.plot(x,pp_cum)
    can.ax.set_yscale('log')
    can.ax.set_title("Cummulative  Sum")  
    can.ax.set_ylabel("Cummulative Sum Power")
    can.ax.set_xlabel("Percentage of Power")
    can.ax.axis([99,100,0,sc._v_attrs.maxEdgePower])
#    can.ax.axis([0,sV0.size,-.5,1.5])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()

def showCumSumLog(can,project):
    initfig(can,ticksOff=False)
    sc=project.scenario
    ppshape=sc._v_attrs.edgePowerShape
    pp=project.sigPower()
    sigshape=pp.shape
    sigsize=sigshape[0]
    #print "pp shape", ppshape
    #print "sig shape", sigshape
    ppsize=ppshape[0]*ppshape[1]
    beta=sigshape[0]*1.0/ppsize
    alpha=1-beta
    #print "beta: ",beta
    #print "alpha: ",alpha
    L=np.arange(sigsize+0.0)/sigsize
    xd=L*beta + alpha
    x=xd*100
#    L=L*prop+(1.0-prop)*100
    #print "min x", np.min(x)
    #print "max x", np.max(x)
    pp_cum=np.cumsum(pp)
    frc=project.cumPowerThreshold/100.0
    ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
    N=pp.size*1.0
#    x=np.arange(N)/(N-1.0)*100.0
#    x=L
    can.ax.plot(x,pp_cum)
    can.ax.set_yscale('log')
    can.ax.set_title("Cummulative  Sum")  
    can.ax.set_ylabel("Cummulative Sum Power")
    can.ax.set_xlabel("Percentage of Power")
    imin=int(np.min(x))
    can.ax.axis([imin,100,0,sc._v_attrs.maxEdgePower])
#    can.ax.axis([0,sV0.size,-.5,1.5])
    can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
    can.draw()



def showCumSum(can,project):
    initfig(can)
    if project.powerCalculated():
        initfig(can,ticksOff=False)
        sc=project.scenario
        ppshape=sc._v_attrs.edgePowerShape
        sp=project.sigPower()
        sigshape=sp.shape
        sigsize=sigshape[0]
        ppsize=ppshape[0]*ppshape[1]
        beta=sigshape[0]*1.0/ppsize
        alpha=1-beta
        L=np.arange(sigsize+0.0)/sigsize

        xd=L*beta + alpha
        x=xd*100
        pp_cum=np.cumsum(sp)
        frc=project.cumPowerThreshold/100.0
#        ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
        N=sp.size*1.0

        # Plot cumulative power
        x=np.arange(pp_cum.size)
        x=-x
        x-=x[-1]
        y=np.max(pp_cum)-pp_cum
        can.ax.plot(x,y,'r.')

        # Plot threshold
        thresh=project.cumPowerThreshold/100.0
        thr=thresh*max(y)
        ythr=y*0+thr
        can.ax.plot(x,ythr)

        # Labels and axes
        can.ax.set_title("Cummulative Sum of Power")  
        can.ax.set_ylabel("Cummulative Sum Power")
        can.ax.set_xlabel("Link number")
        imin=int(np.min(x))
        x1,x2,y1,y2=can.ax.axis()
        x2=1000
        can.ax.axis((x1,x2,y1,y2))
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

def showCumSumPC(can,project):
    initfig(can)
    if project.powerCalculated():
        initfig(can,ticksOff=False)
        sc=project.scenario
        ppshape=sc._v_attrs.edgePowerShape
        sp=project.sigPower()
        sigshape=sp.shape
        sigsize=sigshape[0]
        ppsize=ppshape[0]*ppshape[1]
        beta=sigshape[0]*1.0/ppsize
        alpha=1-beta
        L=np.arange(sigsize+0.0)/sigsize

        xd=L*beta + alpha
        x=xd*100
        pp_cum=np.cumsum(sp)
        frc=project.cumPowerThreshold/100.0
#        ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
        N=sp.size*1.0

        # Plot cumulative power
        x=np.arange(pp_cum.size)
        x=-x
        x-=x[-1]
        y=np.max(pp_cum)-pp_cum
        maxy=np.max(y[-120:])
        can.ax.plot(x,y/maxy*100,'r.')

        # Plot threshold
        thresh=project.cumPowerThreshold/100.0
        thr=thresh*max(y)
        ythr=y*0+thr
        can.ax.plot(x,ythr/maxy*100)

        # Labels and axes
        can.ax.set_title("Percentage Cummulative Sum of Power")  
        can.ax.set_ylabel("Percentage Cummulative Sum Power")
        can.ax.set_xlabel("Link number")
        imin=int(np.min(x))
        x1,x2,y1,y2=can.ax.axis()
        x2=1000
        can.ax.axis((x1,x2,y1,y2))
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

def showCumSum__(can,project):
    initfig(can)
    print "showCumSum()"
    if project.powerCalculated():
        print "Inside cumsum"
        initfig(can,ticksOff=False)
        sc=project.scenario
        ppshape=sc._v_attrs.edgePowerShape
        sp=project.sigPower()
        sigshape=sp.shape
        sigsize=sigshape[0]
        ppsize=ppshape[0]*ppshape[1]
        beta=sigshape[0]*1.0/ppsize
        alpha=1-beta
        L=np.arange(sigsize+0.0)/sigsize

        L=sp/np.max(sp)
        
        xd=L*beta + alpha
        x=xd*100
        pp_cum=np.cumsum(sp)
        frc=project.cumPowerThreshold/100.0
#        ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
        N=sp.size*1.0

#        x=sp/np.max(sp)
        
        can.ax.plot(x,pp_cum)
        
        can.ax.set_title("Cummulative  Sum")  
        can.ax.set_ylabel("Cummulative Sum Power")
        can.ax.set_xlabel("Percentage Link power")
        imin=int(np.min(x))
        x1,x2,y1,y2=can.ax.axis()
        x1=imin
        can.ax.axis((x1,x2,y1,y2))
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

def showSigPower(can,project):
    initfig(can)
    if project.powerCalculated():
        initfig(can,ticksOff=False)

        sc=project.scenario
        ppshape=sc._v_attrs.edgePowerShape
        sp=project.sigPower()
        sigshape=sp.shape
        sigsize=sigshape[0]
        ppsize=ppshape[0]*ppshape[1]
        beta=sigshape[0]*1.0/ppsize
        alpha=1-beta
        L=np.arange(sigsize+0.0)/sigsize
        xd=L*beta + alpha
        x=xd*100
        pp_cum=np.cumsum(sp)
        frc=project.cumPowerThreshold/100.0
#        ppw=np.where(pp_cum>np.max(pp_cum)/frc)[0]
        N=sp.size*1.0

#        can.ax.plot(np.arange(sigsize),sp/np.max(sp))
        can.ax.plot(np.arange(sigsize),sp,'r.')

        can.ax.set_title("Significant power")
        can.ax.set_ylabel("Link Power")
        can.ax.set_xlabel("Link number")
        imin=int(np.min(x))
        x1,x2,y1,y2=can.ax.axis()
        x2=sigsize
        can.ax.axis((x1,x2,y1,y2))
        can.fig.subplots_adjust(bottom=.1,top=topgap,left=.15,right=rightgap)
        can.draw()

################ DROPPING ##################################
def showDroppingHab(can,project):
    global globorig
    initfig(can)
    if project.hasDropping():
        im=can.ax.imshow(np.transpose(project.droppingMask()),interpolation='nearest',origin=globorig)
        can.fig.subplots_adjust(bottom=bottomgap,top=topgap,left=leftgap,right=rightgap)
        im.set_cmap('Paired')
        can.ax.set_title("New Habitat")
        fullzoom(can,project)
        can.draw()


