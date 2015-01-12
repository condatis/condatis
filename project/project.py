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
import numpy as np
from osgeo import gdal, osr
import dwwspatial as sp
import vlevels
import ntpath
import contable8 as con

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl
import copy
import os.path
import logging
import tables
import scipy.sparse

def topNindsDelete(A,N=10):
    at=np.triu(A)
    af=at.flatten()
    aas=np.argsort(af)[-N:]
    return np.unravel_index(aas,A.shape)

class Project():
    def __init__(self,name,title='Econet habitat optimiser'):
        if os.path.isfile(name):
            self.loadProject(name)
        else:
            self.newProject(name,title)
        self.powerThreshold=1.0
        self.cumPowerThreshold=50.0
        self.VLPdict={}
        self.topNIndsDict={}

    def newProject(self,filename,title):
        logging.info("Making new project with filename: " + filename )
        self.h5file=con.makeProject(filename,title)
        self.scenario=[]

    def containsScenario(self,sname):
        return self.h5file.root.__contains__(sname)

    def closeProject(self):
        self.h5file.close()

    def saveProject(self):
        self.h5file.flush()

    def loadProject(self,filename):
        logging.info("Loading project: %s", filename)
        self.h5file=tables.openFile(filename,mode='a')

    
    def closeProject(self):
        self.h5file.close()

########## PLOTTING #################################

    def scVLP(self):
        nm=self.scenario._v_name
        if nm in self.VLPdict:
            logging.debug("Found a VLP")
            return self.VLPdict[nm]
        else:
            logging.debug("VLP not found")
            return []

    def scVLPadd(self,VLP):
        nm=self.scenario._v_name
        self.VLPdict[nm]=VLP
        logging.debug("Added to VLP")

    def scVLPclear(self):
        nm=self.scenario._v_name
        if nm in self.VLPdict:
            del self.VLPdict[nm]
    
    def scTopNInds(self,full,N=10):
        nm=self.scenario._v_name
        if nm in self.topNIndsDict:
            logging.debug("Found a Inds dict")
            return self.topNIndsDict[nm]
        else:
            logging.debug("Inds dict not found")
            return []
        
    def scTopNIndsadd(self,inds):
        nm=self.scenario._v_name
        self.topNIndsDict[nm]=inds
        logging.debug("Added to Inds")

    def scTopNIndsclear(self):
        nm=self.scenario._v_name
        if nm in self.topNIndsDict:
            del self.topNIndsDict[nm]
    
########## FILE ########################################################




########## EDITING #####################################################


    def clearSource(self):
        con.clearSource(self.h5file,self.scenario)

    def clearTarget(self):
        con.clearTarget(self.h5file,self.scenario)

    def clearSourceTarget(self):
        self.clearSource()
        self.clearTarget()
        
    # This is just for the habitat layer. Source and sink
    # can be done easily with sets
    def isin(self,xx,yy):
        x,y=self.habitat()
        for i in range(len(x)):
            if x[i]==xx and y[i]==yy:
                return True
        return False

    # This is just for the habitat layer. Source and sink
    # can be done easily with sets
    def removeDuplicates(self,xnew,ynew,val):
        if not isinstance(xnew, list):
            return xnew,ynew,val
        xxnew=[]
        yynew=[]
        vval=[]
        for i in range(len(xnew)):
            if not self.isin(xnew[i],ynew[i]):
               xxnew.append(xnew[i]) 
               yynew.append(ynew[i])
               vval.append(val[i])
        return xxnew,yynew,vval


    # This is in here because just appending the new locations to the old
    # ones and replacing the x,y,ap arrays in the hdf5 file made all
    # the new values have voltages of about 1.
    # Writing to a new tiff file and loading it back in again solved the
    # problem. Not ideal, but it works.
    def writeNewTiff(self,x,y,v):
        tmpfn='add2hab.tiff'
        scfn=self.scenario._v_attrs.habfilename
        SourceDS = gdal.Open(scfn, gdal.GA_ReadOnly)
        xsize = SourceDS.RasterXSize
        ysize = SourceDS.RasterYSize
        Projection = osr.SpatialReference()
        Projection.ImportFromWkt(SourceDS.GetProjectionRef())
        GeoT = SourceDS.GetGeoTransform()
        dtype=gdal.GDT_Float64
        driver=gdal.GetDriverByName('GTiff')
        DataSet = driver.Create( tmpfn, xsize, ysize, 1, dtype )
        DataSet.SetProjection( Projection.ExportToWkt() )
        DataSet.SetGeoTransform(GeoT)
        a=sp.xyv22d(x,y,xsize,ysize,v)                            
        DataSet.GetRasterBand(1).WriteArray(np.transpose(a).astype(np.float64))
        
    def add2hab(self,xnew,ynew,val):
        x,y=self.habitat()
        ap=self.scenario.ap.read()
        xxnew,yynew,vval=self.removeDuplicates(xnew,ynew,val)
        xx=np.append(x,xxnew).astype(int)
        yy=np.append(y,yynew).astype(int)
        vv=np.append(ap,vval)
        self.writeNewTiff(xx,yy,vv)
        con.addHabTif(self.h5file,self.scenario,'add2hab.tiff')

#        con.addHab(self.h5file,self.scenario,xx,yy,vv)

#        con.generateCombinedHabitat(self.h5file,self.scenario)
        
    def add2source(self,xnew,ynew):
        x,y=self.source()
        xx=np.append(x,xnew).astype(int)
        yy=np.append(y,ynew).astype(int)
        # Make arrays unique
        xxyy=np.array(list(set(zip(list(xx),list(yy)))))
        xxx=xxyy[:,0]
        yyy=xxyy[:,1]
        con.addSrc(self.h5file,self.scenario,xxx,yyy)
        con.remDupsSS(self.h5file,self.scenario)

    def add2target(self,xnew,ynew):
        x,y=self.sink()
        xx=np.append(x,xnew).astype(int)
        yy=np.append(y,ynew).astype(int)
        # Make arrays unique
        xxyy=np.array(list(set(zip(list(xx),list(yy)))))
        xxx=xxyy[:,0]
        yyy=xxyy[:,1]
        con.addSink(self.h5file,self.scenario,xxx,yyy)
        con.remDupsSS(self.h5file,self.scenario)

########## HABITAT FILE LOADING ########################################

    def calcap(self):
        con.calcap(self.h5file,self.scenario)

    def loadInputGeo(self,name='maps/l_m_1.tif',scn_name=None,mincut=0):
        rasterName=ntpath.basename(name)
        root,ext=ntpath.splitext(rasterName)
        if scn_name==None:
            scn_name=os.path.splitext(rasterName)[0]
        scenario=con.makeScenario(self.h5file,scn_name)
        con.addHabTif(self.h5file,scenario,name,mincut=mincut)
#        con.addSrcSinkTif(self.h5file,scenario,'maps/source.tif','maps/sink.tif')
        scenario._v_attrs.rasterName=rasterName
#        scenario._v_attrs.sourceName=source
#        scenario._v_attrs.sink=sink
        self.scenario = scenario
        con.generateCombinedHabitat(self.h5file,self.scenario)
        self.h5file.flush()

    def loadSourceSink(self,sourceName='maps/source.tif',srcval=1,snkval=2):
        con.addSrcSinkTif1(self.h5file,self.scenario,sourceName,srcval,snkval)#,sinkName)
        con.remDupsSS(self.h5file,self.scenario)
        con.generateCombinedHabitat(self.h5file,self.scenario)

    def loadInputCsv(self,name='',source='maps/source.csv',\
                     sink='maps/sink.csv'):
        pass

    def addSrcSink(self,sx,sy,tx,ty):
        con.addSrc(self.h5file,self.scenario,sx,sy)
        con.addSink(self.h5file,self.scenario,tx,ty)
        con.remDupsSS(self.h5file,self.scenario)

    def loadInput(self,name='l_m_1.tif',source='maps/source.tif', \
                  sink='maps/sink.tif'):
        root,ext=ntpath.splitext(name)
        if ext ==".csv":
            self.loadInputCsv(name=name,source=source,sink=sink)
        else:
            self.loadInputGeo(name=name,source=source,sink=sink)

    def deleteScenario(self):
        if self.numberOfScenarios() > 1:
            n=self.scenario
            self.h5file.removeNode(n,recursive=True)
            children=self.h5file.root.scenarios._v_children.keys()
            self.scenario=self.h5file.root.scenarios._v_children[children[0]]

    def renameScenario(self,newName):
        self.h5file.renameNode(self.scenario,newName)
        scn=self.h5file.getNode('/scenarios/'+newName)
        self.scenario=scn
        
    def duplicateScenario(self,scn1,newname):
        print "In duplicate. Old x scale: ", scn1._v_attrs.map_x_scale
        self.h5file.copyNode(scn1,newname=newname,recursive=True)
        scn=self.h5file.getNode('/scenarios/'+newname)
        scn._v_attrs.rasterName=newname
        scn._v_attrs.ind=self.h5file.root.scenarios._v_attrs.nextIndex
        self.h5file.root.scenarios._v_attrs.nextIndex+=1
        self.scenario=scn
        print "In duplicate. New x scale: ", scn._v_attrs.map_x_scale
        logging.info("Scenario duplicated. Index is %d", self.scenario._v_attrs.ind)
        return scn
        # scn2=con.makeScenario(self.h5file,newname)
        # self.h5file.copyChildren(scn1,scn2,recursive=True,overwrite=True)
        # return scn2

    def selectedN(self):
        cur=self.scenario._v_name
        logging.debug("Current scenario is " + cur)
#        print self.h5file.root.scenarios._v_children.keys()
        return self.h5file.root.scenarios._v_children.keys().index(cur)

    def numberOfScenarios(self):
        children=self.h5file.root.scenarios._v_children.keys()
        logging.debug("Getting length of children %d" % len(children))
        return len(children)

    
    def hasDropped(self):
        return self.scenario.__contains__('indlist')

    def hasBeenCalculated(self):
        return not self.scenario._v_attrs.I0==0

    def hasScenario(self):
        return self.numberOfScenarios() > 0


    def hasTag(self,t):
        return self.scenario.__contains__(t)

        
    def hasHabitat(self):
        if not self.hasTag('x'):
            return False
        if self.scenario.x.shape[0] == 0:
            return False
        return True

    def hasSource(self):
        if not self.hasTag('or_x'):
            return False
        if self.scenario.or_x.shape[0]==0:
            return False
        return True

    def hasSink(self):
        if not self.hasTag('tg_x'):
            return False
        if self.scenario.tg_x.shape[0]==0:
            return False
        return True

    def hasSourceOrSink(self):
        return (self.hasSource() or self.hasSink())

    def hasSourceAndSink(self):
        return (self.hasSource() and self.hasSink())

    def hasKernParams(self):
        return self.scenario._v_attrs.__contains__('R') and \
            self.scenario._v_attrs.__contains__('dispersal')

    def canCalculateScenario(self):
        if self.scenario==[]:
            return False
        if self.hasHabitat():
            if self.hasSourceAndSink():
                if self.hasKernParams():
                    return True
        return False

    def dispersal(self):
        return self.scenario._v_attrs.dispersal

    def R(self):
        return self.scenario._v_attrs.R

########## CALCULATE ############################################
    def calcConductance(self):
        con.addIpv(self.h5file,self.scenario)
        con.solve(self.h5file,self.scenario)

    def calcPower(self):
        con.calcPower(self.h5file,self.scenario)

    def calcScenarioPower(self,sc):
        con.calcPower(self.h5file,sc)

    def calcDists(self):
        con.calcDists(self.h5file,self.scenario)

    def distsCalculated(self):
        return self.scenario.__contains__('dmin')

    def calcIpvIn(self):
        con.ipvIn(self.h5file,self.scenario)

    def calcIpvOut(self):
        con.ipvOut(self.h5file,self.scenario)

    def calcIpvFree(self):
        con.ipvFree(self.h5file,self.scenario)

    def calcCond(self):
        con.solve(self.h5file,self.scenario)

    def calcCombinedHabitat(self):
        con.generateCombinedHabitat(self.h5file, self.scenario)

    def calcSplitLevels(self,N=7):
        V0=self.scenario.V0.read()
        self.levels=vlevels.splitLevels(V0,N)

    def calc(self,pmatrix=False,verb=True):
        if verb:
            logging.info("Calculating conductance...")
        self.calcConductance()
        if verb:
            logging.info("Calculating levels...")
        self.calcSplitLevels()
        if pmatrix:
            if verb:
                logging.info("Calculating power matrix")
            self.calcLayerPowerMatrix()
        self.calcCombinedHabitat()
        logging.info("End of calculation")

########## ACCESS ###############################################

    def hasDropping(self):
        return self.scenario.__contains__("xnew")

    def filename(self):
        return self.h5file.filename
    
    def dispersal(self):
        if self.scenario._v_attrs.__contains__('dispersal'):
            return self.scenario._v_attrs.dispersal
        else:
            return 0.0

    def R(self):
        if self.scenario._v_attrs.__contains__('R'):
            return self.scenario._v_attrs.R
        else:
            return 0.0

    def flow(self):
        if self.scenario._v_attrs.__contains__('I0'):
            return self.scenario._v_attrs.I0
        else:
            return 0.0



    def mapscale(self):
        return self.scenario._v_attrs.mapscale

    def areascale(self):
        return self.scenario._v_attrs.areascale

    def sigPower(self):
        if self.scenario.__contains__("sorted_sig_power"):
            return self.scenario.sorted_sig_power.read()
        else:
            return 0

    def maxPower(self):
        if self.scenario._v_attrs.__contains__("maxEdgePower"):
            return self.scenario._v_attrs.maxEdgePower
        else:
            return 0
        

    def totalPower(self):
        if self.scenario._v_attrs.__contains__("totalEdgePower"):
#            print "****************Got total power: ", self.scenario._v_attrs.totalEdgePower
            return self.scenario._v_attrs.totalEdgePower
        else:
            return 0
#        ep=self.edgePower()
#        return np.sum(ep)


    def metapopCapacity(self):
        if self.scenario._v_attrs.__contains__('metapopCapacity'):
 #           print "Got metapop cap: ",self.scenario._v_attrs.metapopCapacity
            return self.scenario._v_attrs.metapopCapacity
        else:
            return 0.0

    def totalLinkStrength(self):
        if self.scenario._v_attrs.__contains__('totalLinkStrength'):
#            print "Got total link strength, it's ",self.scenario._v_attrs.totalLinkStrength
            return self.scenario._v_attrs.totalLinkStrength
        else:
            return 0

    def totalFlow(self):
        if self.hasBeenCalculated():
            return self.scenario._v_attrs.I0
        else:
            return 0

    def input(self):
        return con.input(self.scenario)

    def combinedHabitat(self):
        return self.scenario.combined.x.read(),self.scenario.combined.y.read()

    def mapSize(self):
        x=self.scenario._v_attrs.map_x_size
        y=self.scenario._v_attrs.map_y_size
        return x,y

    def rasterSize_old(self):
        return self.mapSize()


    def rasterSize(self,scenario=False):
        if not scenario:
            scenario=self.scenario
        x=self.scenario._v_attrs.map_x_size
        y=self.scenario._v_attrs.map_y_size
        return x,y
        

    def rasterSizeOrig(self):
        x,y=self.combinedHabitat()
        xz=int(np.max(x)+1)
        yz=int(np.max(y)+1)
        return xz,yz

    def habitatSize(self):
        x,y=self.habitat()
        xz=int(np.max(x)+1)
        yz=int(np.max(y)+1)
        return xz,yz
        
    def combinedSize(self):
        expand=2
        x,y=self.combinedHabitat()
        xz=int(np.max(x)-np.min(x)+expand)
        yz=int(np.max(y)-np.min(y)+expand)
        return xz,yz

    def areaBounds(self):
        x,y=self.combinedHabitat()
        xmin=np.min(x)
        ymin=np.min(y)
        xmax=np.max(x)
        ymax=np.max(y)
        return xmin,ymin,xmax,ymax

    def cellArea(self,scenario=False):
        if not scenario:
            scenario=self.scenario
        xx=scenario._v_attrs.map_x_scale
        yy=scenario._v_attrs.map_y_scale
        return xx*yy

    def totalArea(self,scenario=False):
        if not scenario:
            scenario=self.scenario
        h=scenario.ap.read()
        return np.sum(h*self.cellArea(scenario))/1e6

    def networkFlow(self):
        return self.scenario._v_attrs.I0

    def habitat(self):
        return self.scenario.x.read(),self.scenario.y.read()

    def habitatMaskUnexpanded(self):
        x,y=self.habitat()
        return sp.xyv22d(x,y,*self.rasterSize())

    def habitatMask(self):
        x,y=self.habitat()
        xc,yc=self.combinedHabitat()
        x-=np.min(xc)
        y-=np.min(yc)
        return sp.xyv22d(x,y,*self.combinedSize())

    def source(self):
        if self.scenario.__contains__("or_x"):
            return self.scenario.or_x.read(),self.scenario.or_y.read()
        else:
            return np.empty(0),np.empty(0)

    def sourceMask(self):
        x,y=self.source()
        if x.size==0:
            return np.zeros(self.combinedSize())
        else:
            xc,yc=self.combinedHabitat()
            x-=np.min(xc)
            y-=np.min(yc)
            return sp.xyv22d(x,y,*self.combinedSize())

    def sourceMaskUnexpanded(self):
        x,y=self.source()
        if x.size==0:
            return np.zeros(self.rasterSize())
        else:
            xc,yc=self.combinedHabitat()
            x-=np.min(xc)
            y-=np.min(yc)
            return sp.xyv22d(x,y,*self.rasterSize())

    def sink(self):
        if self.scenario.__contains__("tg_x"):
            return self.scenario.tg_x.read(),self.scenario.tg_y.read()
        else:
            return np.empty(0),np.empty(0)

    def sinkMask(self):
        x,y=self.sink()
        if x.size==0:
            return np.zeros(self.combinedSize())
        else:
            xc,yc=self.combinedHabitat()
            x-=np.min(xc)
            y-=np.min(yc)
            return sp.xyv22d(x,y,*self.combinedSize())

    def sinkMaskUnexpanded(self):
        x,y=self.sink()
        if x.size==0:
            return np.zeros(self.rasterSize())
        else:
            xc,yc=self.combinedHabitat()
            x-=np.min(xc)
            y-=np.min(yc)
            return sp.xyv22d(x,y,*self.rasterSize())

    def nodeVoltage(self):
        return self.scenario.V0.read()
        
    def nodeVoltageA(self):
        x,y=self.habitat()
        return sp.xyv22d(x,y,*self.rasterSize(),val=self.nodeVoltage())

    def nodeFlow(self):
        return self.scenario.I.read()

    def nodeFlowA(self):
        x,y=self.habitat()
        return sp.xyv22d(x,y,*self.rasterSize(),val=self.nodeFlow())

    def nodeArea(self):
        return self.scenario.ap.read()

    def nodeAreaA(self):
        x,y=self.habitat()
#        logging.debug("nodeAreaA(): rasterSize(): %d",self.rasterSize())
        logging.debug("nodeAreaA(): max(x): %d, max(y): %d",np.max(x), np.max(y))
        return sp.xyv22d(x,y,*self.rasterSize(),val=self.nodeArea())

    # Metrics
    def metricsCalculated(self):
        return self.scenario.metrics.__contains__("ViS")

    def nodePatchPArea(self):
        return self.scenario.metrics.ViS.read()

    def patchPAreaA(self):
        x,y=self.habitat()
        return sp.xyv22d(x,y,*self.rasterSize(),val=self.nodePatchPArea())

    def nodePatchLoss(self):
        return self.scenario.metrics.ViL.read()

    def patchLossA(self):
        x,y=self.habitat()
        return sp.xyv22d(x,y,*self.rasterSize(),val=self.nodePatchLoss())

    def calcPowerMap(self):
        dlg=calcdialog.CalculatingDialog(pcnt=np.arange(7)*100.0/7)
        dlg.show()
        dlg.setState(0)
        
        logging.debug("Flattening")
        pp=project.edgePower().flatten()
        dlg.setState(1)
        logging.debug("Sorting")
        pps=np.sort(pp)
        dlg.setState(2)
        logging.debug("Cumulative sum")
        pp_cum=np.cumsum(pps)
        dlg.setState(3)
        frc=project.cumPowerThreshold/100.0
        logging.debug("Power max and fraction is: %f, %f",np.max(pp_cum),frc)
        logging.debug("Finding Fraction")
        ppw=np.where(pp_cum>np.max(pp_cum)*frc)[0]
        N=ppw.size
        dlg.setState(4)
        logging.debug("Number of power links to plot: %d", N)
        initfig(can)
        x,y=project.habitat()
        XZ,YZ=project.rasterSize()
        logging.debug("Rendering")
        rend=renderEdges(x,y,project.edgePower()*1e6,XZ,YZ,N)
        dlg.setState(5)
        logging.debug("Min rend: %f, max rend: %f",np.min(rend),np.max(rend))
        im=np.transpose(np.asarray(rend))

        if self.scenario._v_attrs.contains('powerMap'):
            self.scenario._v_attrs.powerMap.remove()

        self.scenario._v_attrs.powerMap[:]=im

    def edgeVoltageDrop(self):
        return self.scenario.edgeVoltageDrop.read()
#        V0=self.nodeVoltage()
#        return V0*V0[:,np.newaxis]
#        return sp.outer_s(V0,V0)

    def edgeConductance(self):
        return self.scenario.M0.read()

    def edgeCurrent(self):
        return self.scenario.I2ij.read()

    def sparseEdgePower(self):
        ep=self.edgePower()
        maxep=np.max(ep)
        ep[np.where(ep < maxep/1000.0)]=0
        return scipy.sparse.coo_matrix(ep)

    def edgePower_old(self):
        if self.hasBeenCalculated():
            return self.scenario.edgePower.read()
            # return np.abs(self.edgeVoltageDrop()*self.edgeCurrent())
        else:
            return 0.0

    def powerCalculated(self):
        return self.scenario.__contains__("edgePower")

    def edgePower(self):
        if not self.powerCalculated():
            self.calcPower()
        return self.scenario.edgePower.read()

    def sortedEdgePowerInds(self,N=10):
        return topNinds(self.edgePower(),N=N)

    def sortedEdgeCurrentInds(self,N=10):
        return topNinds(self.edgeCurrent(),N=N)

    def sortedEdgeVoltageInds(self,N=10):
        return topNinds(self.edgeVoltageDrop(),N=N)

    def sortedEdgeConductanceInds(self,N=10):
        return topNinds(self.edgeConductance(),N=N)

    def originX(self):
        return self.scenario._v_attrs.map_x_origin

    def originY(self):
        return self.scenario._v_attrs.map_y_origin

    def cellSizeX(self):
        return self.scenario._v_attrs.map_x_scale

    def cellSizeY(self):
        return self.scenario._v_attrs.map_y_scale

    def projection(self):
        return self.scenario._v_attrs.map_projection

    def projectionName(self):
        return self.scenario._v_attrs.map_projectionName

########## CROSS SCENARIO #########################################
    def allFlows(self):
        logging.info("Calculating all flows")
        N=self.numberOfScenarios()
        logging.debug("Number of scenarios N=%d",N)
        r=np.zeros(N)
        for i in range(N):
            logging.debug("In loop, i=%d",i)
            tmpscn=con.getNth(self.h5file,i)
            print tmpscn
            if tmpscn:
                r[i]=tmpscn._v_attrs.I0
            else:
                r[i]=0
        return r


    def allTLS(self):
        N=self.numberOfScenarios()
        curr=self.scenario
        r=np.zeros(N)
        for i in range(N):
            self.scenario=con.getNth(self.h5file,i)
            r[i]=self.totalLinkStrength()
        self.scenario=curr
        return r

    def allAreas(self):
        N=self.numberOfScenarios()
        r=np.zeros(N)
        for i in range(N):
            ai=con.getNth(self.h5file,i).ap.read()
            r[i]=np.sum(ai)
        return r

    def allMetapopCapacity(self):
        N=self.numberOfScenarios()
        r=np.zeros(N)
        for i in range(N):
            ai=con.getNth(self.h5file,i).ap.read()
            scn=con.getNth(self.h5file,i)
            if scn._v_attrs.__contains__('metapopCapacity'):
                r[i]=scn._v_attrs.metapopCapacity
            else:
                r[i]=0
        return r

    def allNames(self): 
        N=self.numberOfScenarios()
        r=[]
        for i in range(N):
            r.append(con.getNth(self.h5file,i)._v_name)
        return r
       

########## ANALYSIS ###############################################
    def grabLevel(self,L):
        V0=self.nodeVoltage()
        vs=self.levels
        ind=np.where((V0 > vs[L]) & (V0  <= vs[L+1]))[0]
        return ind

    def closestPoint(self,L1,L2):
        x,y=self.habitat()
        la1=self.grabLevel(L1)
        la2=self.grabLevel(L2)
        return vlevels.closest(la1,la2,x,y)

    def closestInd(self,L1,L2):
        x,y=self.habitat()
        la1=self.grabLevel(L1)
        la2=self.grabLevel(L2)
        return vlevels.closestInd(la1,la2,x,y)

    def habitatN(self):
        return self.scenario.x.shape[0]


############ ADDING ########################

    def addPoint(self,xn,yn):
        x,y=self.habitat()
    

############ DROPPING #######################
    def hasDropping(self):
        return True

    def projectMask(self):
        x=scenario.dropping_x
        y=scenario.dropping_y
        return sp.xyv22d(x,y,*self.rasterSize())

def testLandOld(fname='maps/l_m_7.tif'):
    pr=con.makeProject("fract.h5","Fractal Landscapes")
    ls=Project(pr,name=fname)
    ls.calcConductance()
    return pr,ls

def testLand(fname='maps/l_m_8.tif'):
    pr=Project(name=fname)
    return pr
    
