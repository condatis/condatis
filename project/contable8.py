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
import tables
import numpy as np
import geofiles
import scipy.spatial.distance as distance
import dwwspatial as dwwsp
#mport gdal
from osgeo import gdal, osr
import gc
from scipy import sparse
import chunking as ch

# Only for debug
import matplotlib.pyplot as plt
import logging

CHUNK=4096
#MAX_SCENARIOS=1024
#nextIndex=0

def isin_(xnew,ynew,x,y):
    for i in range(x.size):
        if (xnew == x[i] and ynew == y[i]):
            return True
    return False

def removeDupsSS_(x,y,xnew,ynew):
    xr=[]
    yr=[]
    for i in range(xnew.size):
        if not isin_(xnew[i],ynew[i],x,y):
            xr.append(xnew[i])
            yr.append(ynew[i])
    nxr=np.array(xr)
    nyr=np.array(yr)
    return nxr,nyr

def habitat(h5,scenario):
    if scenario.__contains__('x'):
        return scenario.x.read(),scenario.y.read()
    else:
        return np.empty(0), np.empty(0)

def source(h5,scenario):
    if scenario.__contains__('or_x'):
        return scenario.or_x.read(),scenario.or_y.read()
    else:
        return np.empty(0), np.empty(0)

def target(h5,scenario):
    if scenario.__contains__('tg_x'):
        return scenario.tg_x.read(),scenario.tg_y.read()
    else:
        return np.empty(0), np.empty(0)

def remDupsSS(h5,scenario):
    # x=scenario.x.read()
    # y=scenario.y.read()
    # or_x=scenario.or_x.read()
    # or_y=scenario.or_y.read()
    # tg_x=scenario.tg_x.read()
    # tg_y=scenario.tg_y.read()

    x,y=habitat(h5,scenario)
    or_x,or_y=source(h5,scenario)
    tg_x,tg_y=target(h5,scenario)

    or_x_,or_y_=removeDupsSS_(x,y,or_x,or_y)
    tg_x_,tg_y_=removeDupsSS_(x,y,tg_x,tg_y)

    if scenario.__contains__('or_x'):
        scenario.or_x.remove()
    if scenario.__contains__('or_y'):
        scenario.or_y.remove()
    if scenario.__contains__('tg_x'):
        scenario.tg_x.remove()
    if scenario.__contains__('tg_y'):
        scenario.tg_y.remove()
    h5.createArray(scenario,'or_x',or_x_)
    h5.createArray(scenario,'or_y',or_y_)
    h5.createArray(scenario,'tg_x',tg_x_)
    h5.createArray(scenario,'tg_y',tg_y_)

    
def makeProject(projname,title):
    h5=tables.openFile(projname,mode="w",title=title)
    h5.createGroup("/",'scenarios','Scenarios')
    h5.root.scenarios._v_attrs.nextIndex=0
    return h5

def scenarioDefaults(scenario,R=100.0,dispersal=4.0):
    scenario._v_attrs.R=R
    scenario._v_attrs.dispersal=dispersal
    scenario._v_attrs.mapscale=1.0
    scenario._v_attrs.areascale=0

def makeScenario(h5,name):
    scenario=h5.createGroup("/scenarios",name,"Scenario")
    gname="/scenarios/"+name
    h5.createGroup(gname,"input","Landscape data")
    h5.createGroup(gname,"combined","Landscape combined with source and sink")
    h5.createGroup(gname,"metrics","Population Metrics")
    scenarioDefaults(scenario)
    scenario._v_attrs.ind=h5.root.scenarios._v_attrs.nextIndex
    h5.root.scenarios._v_attrs.nextIndex+=1
    return scenario

def clearSource(h5,scenario):
    if scenario.__contains__('or_x'):
        scenario.or_x.remove()
    if scenario.__contains__('or_y'):
        scenario.or_y.remove()
        
def clearTarget(h5,scenario):
    if scenario.__contains__('tg_x'):
        scenario.tg_x.remove()
    if scenario.__contains__('tg_y'):
        scenario.tg_y.remove()

def addSrc(h5,scenario,x,y):
    if scenario.__contains__('or_x'):
        scenario.or_x.remove()
    if scenario.__contains__('or_y'):
        scenario.or_y.remove()
    h5.createArray(scenario,'or_x',x)
    h5.createArray(scenario,'or_y',y)

def addSink(h5,scenario,x,y):
    if scenario.__contains__('tg_x'):
        scenario.tg_x.remove()
    if scenario.__contains__('tg_y'):
        scenario.tg_y.remove()
    h5.createArray(scenario,'tg_x',x)
    h5.createArray(scenario,'tg_y',y)
    
def calcap(h5,scenario):
    ascale=scenario._v_attrs.areascale
    area=10**ascale
    if scenario.__contains__('ap'):
        scenario.ap.remove()
    ap=scenario.area.read()/area
    h5.createArray(scenario,'ap',ap)

def addHab(h5,scenario,x,y,area):

    if scenario.__contains__('x'):
        scenario.x.remove()
        
    if scenario.__contains__('y'):
        scenario.y.remove()

    if scenario.__contains__('ap'):
        scenario.ap.remove()

    if scenario.__contains__('cell'):
        scenario.cell.remove()


    h5.createArray(scenario,'x',x)
    h5.createArray(scenario,'y',y)
#    h5.createArray(scenario,'area',area) #np.ones(x.size))
    h5.createArray(scenario,'ap',area) #np.ones(x.size))
    h5.createArray(scenario,'cell',np.ones(x.size))
    scenario._v_attrs.I0=0.0
#    calcap(h5,scenario)

def addHabTif(h5,scenario,habfilename,mincut=0):
    gd=gdal.Open(habfilename)
#    h=np.array(gd.GetRasterBand(1).ReadAsArray().astype(np.int32))
    h=np.array(gd.GetRasterBand(1).ReadAsArray())
    scenario._v_attrs.habfilename=habfilename
    gt=gd.GetGeoTransform()
    orx=gt[0]
    ory=gt[3]
    scx=np.abs(gt[1]) # Because we get a crazy negative number in the scale
    scy=np.abs(gt[5]) # in Jenny's Y/H data.

    # Need to do this properly. Is there a units in gt
    # To test for kilometers?

    # print "About to scale map!!!!"
    # if scx == 0.5:
    #     print "DON'T EVER RUN THIS BIT OF CODE!!!"
    #     print "Scaling map!!!"
    #     scx=10000.0
    #     scy=10000.0

    # if scx == 0.25:
    #     print "DON'T EVER RUN THIS BIT OF CODE!!!"
    #     print "Scaling map!!!"
    #     scx=5000.0
    #     scy=5000.0

    # if scx == 0.125:
    #     print "DON'T EVER RUN THIS BIT OF CODE!!!"
    #     print "Scaling map!!!"
    #     scx=2500.0
    #     scy=2500.0

    projection=gd.GetProjection()
#    print projection
    projectionName="Not Implemented"

    logging.debug("Minimum cut: %f", mincut)
    hab=np.where(h>mincut)
    y=hab[0]-0
    x=hab[1]-0
    a=h[y,x]/1.0
    # for i in a:
    #     if i==1:
    #         print i,
    #     else:
    #         print i
#    a=h[y,x]/100.0 This was the old percentage area!!
#    a=h[y,x]/(scx*scy)
 

    logging.debug("Max a: %d", np.max(a))
#    a=h[y,x]*1.0e-6

    addHab(h5,scenario,x,y,a)
    scenario._v_attrs.map_x_size=h.shape[1]
    scenario._v_attrs.map_y_size=h.shape[0]
    scenario._v_attrs.map_x_scale=scx
    scenario._v_attrs.map_y_scale=scy
    scenario._v_attrs.map_x_origin=orx
    scenario._v_attrs.map_y_origin=ory
    scenario._v_attrs.map_projection=projection
    scenario._v_attrs.map_projectionName=projectionName

def addSrcSinkTif1(h5,scenario,sourcename,srcval=1,snkval=2):#,sinkname):
    hab=np.where(geofiles.file2np(sourcename)==srcval)
    y=hab[0]
#    y=np.max(yy)-yy
    x=hab[1]
    addSrc(h5,scenario,x,y)
    hab2=np.where(geofiles.file2np(sourcename)==snkval)
    y2=hab2[0]
#    y2=np.max(yy2)-yy2
    x2=hab2[1]
    addSink(h5,scenario,x2,y2)

def addSrcSinkTif2(h5,scenario,sourcename,sinkname):#,sinkname):
    hab=np.where(geofiles.file2np(sourcename))
    y=hab[0]
#    y=np.max(yy)-yy
    x=hab[1]
    addSrc(h5,scenario,x,y)
    hab2=np.where(geofiles.file2np(sinkname))
    y2=hab2[0]
#    y2=np.max(yy2)-yy2
    x2=hab2[1]
    addSink(h5,scenario,x2,y2)

def input(scenario):
    x=scenario.x.read()
    y=scenario.y.read()
    or_x=scenario.or_x.read()
    or_y=scenario.or_y.read()
    tg_x=scenario.tg_x.read()
    tg_y=scenario.tg_y.read()
    ap=scenario.ap.read()
    cell=scenario.cell.read()
    return x,y,or_x,or_y,tg_x,tg_y,ap,cell

def generateCombinedHabitat(h5,scenario):
    x=scenario.x.read()
    y=scenario.y.read()
    ap=scenario.ap.read()
    cell=scenario.cell.read()
    if scenario.__contains__('or_x') and scenario.__contains__('tg_x'):
        or_x=scenario.or_x.read()
        or_y=scenario.or_y.read()
        tg_x=scenario.tg_x.read()
        tg_y=scenario.tg_y.read()
        xa=np.concatenate((x,or_x,tg_x))
        ya=np.concatenate((y,or_y,tg_y))
    else:
        xa,ya=x,y
    shape=xa.shape
    atom=tables.Int32Atom(shape=())
    filters = tables.Filters(complevel=0, complib='zlib')    
    if scenario.combined.__contains__('x'):
        scenario.combined.x.remove()
    if scenario.combined.__contains__('y'):
        scenario.combined.y.remove()
    if scenario.combined.__contains__('V'):
        scenario.combined.V.remove()
    h5.createArray(scenario.combined,'x',xa)
    h5.createArray(scenario.combined,'y',ya)
    h5.createArray(scenario.combined,'V',xa*0)

def addScenarioTif(h5,name,habname,\
                sourcename='maps/source.tif',\
                sinkname='maps/sink.tif'):
    scn=makeScenario(h5,name)
    addHabTif(scn,habname)
    addSrcSinkTif2(scn,sourcename,sinkname)
    generateCombinedHabitat(scn)
    return scn

def calcDists(h5,scn):
    if scn.__contains__("xdin"):
        scn.xdin.remove()

    if scn.__contains__("ydin"):
        scn.ydin.remove()

    if scn.__contains__("xdout"):
        scn.xdout.remove()

    if scn.__contains__("ydout"):
        scn.ydout.remove()

    if scn.__contains__("xdfree"):
        scn.xdfree.remove()

    if scn.__contains__("ydfree"):
        scn.ydfree.remove()

    if scn.__contains__("dmin"):
        scn.dmin.remove()

    if scn.__contains__("dmout"):
        scn.dmout.remove()

    if scn.__contains__("dmfree"):
        scn.dmfree.remove()

    if scn.__contains__("conpart"):
        scn.conpart.remove()

    logging.info("Getting input data")
    cell=(scn._v_attrs.map_x_scale*1.0)/1000.0
    x1=(scn.x.read()+.5)*cell
    y1=(scn.y.read()[::-1]+.5)*cell
    x2=((scn.or_x.read()+.5)*cell)[:,np.newaxis]
    y2=((scn.or_y.read()[::-1]+.5)*cell)[:,np.newaxis]


    xdsk=scn.x.read()
    ydsk=scn.y.read()
    val=scn.ap.read()
    


    dshape=(x2.shape[0],x1.shape[0])
    xdin=h5.create_carray(scn,'xdin',tables.Float64Atom(),dshape)
    ydin=h5.create_carray(scn,'ydin',tables.Float64Atom(),dshape)
    xdf=ch.outerdiff(x1,x2,chunk=CHUNK,r=xdin)
    ydf=ch.outerdiff(y1,y2,chunk=CHUNK,r=ydin)

    # xdf=x1-x2
    # ydf=y1-y2
    
    # print "diffx",xdf2-xdf
    # print "diffy",ydf2-ydf

#    for i in range(xdf1.shape[0]):
#        print i,xdf1[i,:]

#    print xdf.shape
#    print ydf.shape
    dmin=h5.create_carray(scn,'dmin',tables.Float64Atom(),dshape)
    exd=tables.Expr('sqrt(xdf**2 + ydf**2)')
    exd.set_output(dmin)
    logging.info("Evaluating in distances")
    exd.eval()
    logging.info("Done")

    logging.info("Getting output data")
    x2=((scn.tg_x.read()+.5)*cell)[:,np.newaxis]
    y2=((scn.tg_y.read()[::-1]+.5)*cell)[:,np.newaxis]
    dshape=(x2.shape[0],x1.shape[0])
    xdout=h5.create_carray(scn,'xdout',tables.Float64Atom(),dshape)
    ydout=h5.create_carray(scn,'ydout',tables.Float64Atom(),dshape)
    xdf=ch.outerdiff(x1,x2,chunk=CHUNK,r=xdout)
    ydf=ch.outerdiff(y1,y2,chunk=CHUNK,r=ydout)
    # xdf=x1-x2
    # ydf=y1-y2
    dmout=h5.create_carray(scn,'dmout',tables.Float64Atom(),dshape)
    exd=tables.Expr('sqrt(xdf**2 + ydf**2)')
    exd.set_output(dmout)
    logging.info("Evaluating out distances")
    exd.eval()
    logging.info("Done")

    logging.info("Getting free data")
    x2=((scn.x.read()+.5)*cell)[:,np.newaxis]
    y2=((scn.y.read()[::-1]+.5)*cell)[:,np.newaxis]
    dshape=(x2.shape[0],x1.shape[0])
    xdfree=h5.create_carray(scn,'xdfree',tables.Float64Atom(),dshape)
    ydfree=h5.create_carray(scn,'ydfree',tables.Float64Atom(),dshape)
    xdf=ch.outerdiff(x1,x2,chunk=CHUNK,r=xdfree)
    ydf=ch.outerdiff(y1,y2,chunk=CHUNK,r=ydfree)
    # xdf=x1-x2
    # ydf=y1-y2
    dmfree=h5.create_carray(scn,'dmfree',tables.Float64Atom(),dshape)
    exd=tables.Expr('sqrt(xdf**2 + ydf**2)')
    exd.set_output(dmfree)
    logging.info("Evaluating free distances")
    exd.eval()
    logging.info("Done")
    # expr=tables.Expr("ap*cell**4*R*alpha**2/(2*pi)")
    # conpart=h5.create_carray(scn,'conpart',tables.Float64Atom(),x1.shape)
    # expr.set_output(ipv_in1)
    # ip=expr.eval()


def ipvIn(h5,scn):
    if scn.__contains__("ipv_in1"):
        scn.ipv_in1.remove()

    if scn.__contains__("ipv_in"):
        scn.ipv_in.remove()

#     xdf=scn.xdin
#     ydf=scn.ydin
#     logging.debug("Array shape: %d",ydf.shape[0])
#     ap=scn.ap.read()
#     cell=scn.cell
#     cell=1.0
#     R=scn._v_attrs.R
#     pi=np.pi

#     dispersal=scn._v_attrs.dispersal*1.0
#     scale=scn._v_attrs.map_x_scale*1.0
#     dp=(dispersal/scale)*1000.0
#     alpha=2.0/dp
#     logging.debug("Alpha: %f",alpha)

#     x1=scn.x
#     shape=(x1.shape[0],)
#     dm=scn.dmin
#     cnt=R*alpha**2/(2.0*np.pi)

#     print dm.read()


#     gam=scale/1000.0
#     K=1.0/(gam**2)

#     K=(scale/1000.0)**4
    
# #    K=1.0/(gam**2)*(scale/1000.0)**2

    x1=scn.x
    shape=(x1.shape[0],)
    dm=scn.dmin
#    print "dm shape:",dm.shape
    R=scn._v_attrs.R
    ap=scn.ap.read()
    pi=np.pi
    dispersal=scn._v_attrs.dispersal*1.0
    alpha=2.0/dispersal
#    cell=1000./scn._v_attrs.map_x_scale
    cell=scn._v_attrs.map_x_scale/1000.0
    K=R*alpha**2/(2.0*np.pi)*cell**4

    # print "cell",cell
    # print "Constant:",K
    # print "summed shape",shape

    expr=tables.Expr("K*ap*exp(-alpha*dm)")
    ipv_in1=h5.create_carray(scn,'ipv_in1',tables.Float64Atom(),dm.shape)
    expr.set_output(ipv_in1)
    logging.info("Evaluating input conductances")
    ip=expr.eval()
#    print "ipvin before sum:",ipv_in1.read()
    logging.info("Done")
    ipv_in=h5.create_carray(scn,'ipv_in',tables.Float64Atom(),shape)
    logging.info("Summing")
    ch.sumax(ipv_in1,axis=0,r=ipv_in,chunk=CHUNK)
    # print "shape ipvin1",ipv_in1.read().shape
    # print "ipvin:",ipv_in.read()
    # print "Total sum ipvin1",np.sum(ipv_in1.read())
    # print "summed ipvin1",np.sum(ipv_in1.read(),axis=0)
    logging.info("Done")

def ipvOut(h5,scn):
    if scn.__contains__("ipv_out1"):
        scn.ipv_out1.remove()

    if scn.__contains__("ipv_out"):
        scn.ipv_out.remove()

#     xdf=scn.xdout
#     ydf=scn.ydout
#     logging.debug("Array shape: %d",ydf.shape[0])
#     ap=scn.ap.read()
#     cell=scn.cell
#     cell=1.0
#     R=scn._v_attrs.R
#     pi=np.pi
#     dispersal=scn._v_attrs.dispersal*1.0
#     scale=scn._v_attrs.map_x_scale*1.0
#     dp=(dispersal/scale)*1000.0
#     print "Dispersal (pixels):",dp
#     alpha=2.0/dp
#     logging.debug("Alpha: %f", alpha)

#     x1=scn.x
#     dm=scn.dmout
#     cnt=R*alpha**2/(2.0*np.pi)
#     cell=1.0

#     gam=scale/1000.0
#     K=1.0/(gam**2)
#     K=(scale/1000.0)**4
# #    K=1.0/(gam**2)*(scale/1000.0)**2

#     cell=scn._v_attrs.map_x_scale/1000.0
    x1=scn.x
    dm=scn.dmout
    R=scn._v_attrs.R
    ap=scn.ap.read()
    pi=np.pi
    dispersal=scn._v_attrs.dispersal*1.0
    alpha=2.0/dispersal
    cell=scn._v_attrs.map_x_scale/1000.0
    K=R*alpha**2/(2.0*np.pi)*cell**4

    expr=tables.Expr("K*ap*exp(-alpha*dm)")
    ipv_out1=h5.create_carray(scn,'ipv_out1',tables.Float64Atom(),scn.dmout.shape)
    expr.set_output(ipv_out1)
    logging.info("Evaluating output conductances")
    ip=expr.eval()
    logging.info("Done")
    shape=(x1.shape[0],)
    ipv_out=h5.create_carray(scn,'ipv_out',tables.Float64Atom(),shape)
    logging.info("Summing")
    ch.sumax(ipv_out1,axis=0,r=ipv_out,chunk=CHUNK)
    logging.info("Done")


def ipvFree(h5,scn):
    if scn.__contains__("ipv_free1"):
        scn.ipv_free1.remove()

    if scn.__contains__("ipv_free"):
        scn.ipv_free.remove()

    if scn.__contains__("apo"):
        scn.apo.remove()

 #    xdf=scn.xdfree
#     ydf=scn.ydfree
#     logging.debug("Array shape: %d",ydf.shape[0])
#     ap=scn.ap.read()
#     apt=scn.ap.read()[:,np.newaxis]
#     apo=h5.create_carray(scn,'apo',tables.Float64Atom(),scn.dmfree.shape)
#     ch.outerprod(ap,apt,r=apo,chunk=CHUNK)
#     cell=scn.cell.read()
#     cell=1.0
#     R=scn._v_attrs.R
#     pi=np.pi
#     dispersal=scn._v_attrs.dispersal*1.0
#     scale=scn._v_attrs.map_x_scale*1.0
#     dp=(dispersal/scale)*1000.0
#     alpha=2.0/dp
#     logging.debug("Alpha: %f",alpha)

#     x1=scn.x
#     shape=(x1.shape[0],)
#     dm=scn.dmfree.read()
#     cnt=R*alpha**2/(2.0*np.pi)
# #    ap=1.0
# #    cell=1.0

#     gam=scale/1000.0
#     K=1.0/(gam**2)
#     K=(scale/1000.0)**4
# ##    K=1.0/(gam**2)*(scale/1000.0)**2
#     print "Scaling links by:",K
    
    # cell=scn._v_attrs.map_x_scale/1000.0
    # K=R*alpha**2/(2.0*np.pi)*cell**2

    x1=scn.x
    shape=(x1.shape[0],)
    dm=scn.dmfree.read()
    R=scn._v_attrs.R
    ap=scn.ap.read()
    apt=scn.ap.read()[:,np.newaxis]
    pi=np.pi
    dispersal=scn._v_attrs.dispersal*1.0
    alpha=2.0/dispersal
    cell=scn._v_attrs.map_x_scale/1000.0

    K=R*alpha**2/(2.0*np.pi)*cell**4



    expr=tables.Expr("K*ap*apt*exp(-alpha*dm)")
#    expr=tables.Expr("ap*cell**4*R*alpha**2/(2*pi)*exp(-alpha*dm)")
    ipv_free=h5.create_carray(scn,'ipv_free',tables.Float64Atom(),scn.dmfree.shape)
    expr.set_output(ipv_free)
    logging.info("Evaluating free conductances")
    ip=expr.eval()
    logging.info("Done")
    i=np.arange(scn.x.shape[0])
    logging.info("Setting diagonals to zero")
    ipv_free[i,i]=0
    logging.info("Done")
    if scn.__contains__("apo"):
        scn.apo.remove()

#    ipv_out=h5.create_carray(scn,'ipv_out',tables.Float64Atom(),shape)
#    ch.sumax(ipv_out1,axis=0,r=ipv_out)



def addIpv(h5,scenario):
    # Is this the duplacate scenario source/sink bug?
    calcDists(h5,scenario)
    ipvIn(h5,scenario)
    ipvOut(h5,scenario)
    ipvFree(h5,scenario)

def solve(h5,sc):
    ipv_in=sc.ipv_in.read()
    ipv_out=sc.ipv_out.read()
    ipv_free=sc.ipv_free
    SZ=ipv_in.size

    logging.debug("Size is: %d", SZ)

    if sc.__contains__('V0'):
        sc.V0.remove()
    if sc.__contains__('Vij'):
        sc.Vij.remove()
    if sc.__contains__('M0'):
        sc.M0.remove()
    if sc.__contains__('I'):
        sc.I.remove()
    if sc.__contains__('I2ij'):
        sc.I2ij.remove()
    if sc.__contains__("tmp1"):
        sc.tmp1.remove()
    if sc.__contains__("tmp1a"):
        sc.tmp1a.remove()
    if sc.__contains__("tmp2"):
        sc.tmp2.remove()

    # This produces a vector of  in + out + sum(free)
    shape=(SZ,)
    tmp1=h5.create_carray(sc,'tmp1',tables.Float64Atom(),shape)


    logging.info("Making tmp1")
    tmp1=ch.sumax(ipv_free,axis=0)
#    ch.sumax(ipv_free,axis=0,r=tmp1)
#    tmp1[:]=np.sum(ipv_free.read(),axis=0)

    logging.info("Calculating tmp1a")
    # tmp1a=h5.create_carray(sc,'tmp1a',tables.Float64Atom(),(SZ,))
    # t1_ex=tables.Expr('tmp1 + ipv_in + ipv_out')
    # t1_ex.set_output(tmp1a)
    # t1_ex.eval()
    tmp1a=tables.Expr('tmp1 + ipv_in + ipv_out').eval()

    # This makes a diagonal matrix from the above
    logging.info("Making tmp2")
    shape=(SZ,SZ)
    tmp2=h5.create_carray(sc,'tmp2',tables.Float64Atom(),shape)
    i=np.arange(SZ)
    logging.info("Calculating tmp2")
#    tmp2[i,i]=tmp1a.read()
    tmp2[i,i]=tmp1a

    # This makes M0
    logging.info("Making M0")
    M0=h5.create_carray(sc,'M0',tables.Float64Atom(),shape)
    ex_M0=tables.Expr("tmp2-ipv_free")
    ex_M0.set_output(M0)
    logging.info("Calculating M0")
    ex_M0.eval()
    
    
    # This makes V0
    logging.info("Doing solve")
    V0=h5.create_carray(sc,'V0',tables.Float64Atom(),(SZ,))
    # print "M0.shape: ",M0.shape
    # print "M0: ",M0.read()
    # print "ipv_in.shape: ",ipv_in.shape
#    print "ipv_in: ",ipv_in.read()
    logging.info("Calling LAPACK")
    # *********** NOTE: IN CORE !!!!! ***********

    w=ipv_in-ipv_out
    V0[:] = np.linalg.solve(M0.read(),ipv_in)
    
    logging.info("Done solve")
#    print "V0.shape: ",V0.shape
    
    # *********** NOTE: IN CORE !!!!! *********** Because of sum() bug
    logging.info("Doing I0")
    I0 = np.sum(V0.read()*ipv_out)
    sc._v_attrs.I0=I0
    gc.collect()
    logging.info("Done I0")
    # Can condense this a bit
#    print "V0 shape: ", V0.shape
    # Do Vij amd I2ij out-of-core
    logging.info("Doing Vij")
    V0t=V0.read()[:,np.newaxis]
    Vij=h5.create_carray(sc,"Vij",tables.Float64Atom(),(SZ,SZ))
    ch.outerdiff(V0,V0t,chunk=CHUNK,r=Vij)
#    ex_Vij=tables.Expr("V0-V0t")
#    ex_Vij.set_output(Vij)
#    ex_Vij.eval()
    gc.collect()

    logging.info("Doing I2ij")
    I2ij=h5.create_carray(sc,"I2ij",tables.Float64Atom(),(SZ,SZ))
    ex_I2ij=tables.Expr("abs(Vij*ipv_free/2.0)")
    ex_I2ij.set_output(I2ij)
    ex_I2ij.eval()
    gc.collect()

    logging.info("Doing Sum(I2ij)")
    I=ch.sumax(I2ij,axis=0,chunk=CHUNK)
    logging.info("Storing sum(I2ij)")
    h5.createArray(sc,'I',I)

    logging.info("Doing total link strength")
    sc._v_attrs.totalLinkStrength=np.sum(tmp1a)
    
#    sc._v_attrs.totalLinkStrength=np.sum(sc.ipv_free.read())+np.sum(sc.ipv_in.read())+np.sum(sc.ipv_out.read())
#    sc._v_attrs.totalLinkStrength=ch.sumax(sc.ipv_free,chunk=CHUNK)+np.sum(sc.ipv_in)+np.sum(sc.ipv_out)
    if sc.__contains__("edgePower"):
        sc.edgePower.remove()
    gc.collect()


def topNinds_(full,N=10):
    # Get the indices for the largest `num_largest` values.
    num_largest = N
    indices = (-full).argpartition(num_largest, axis=None)[:num_largest]
    xl, yl = np.unravel_index(indices, full.shape)
    return xl,yl


def calcPower(h5,sc):
    if sc.__contains__("edgePower"):
        sc.edgePower.remove()

    SZ=sc.ipv_in.read().size
    logging.info("Doing edge power")
    eP=h5.create_carray(sc,"edgePower",tables.Float64Atom(),(SZ,SZ))
#    V0m=V0.read()
#    Vij=np.abs(V0m-V0m[:,np.newaxis])
#    eP[:]=I2ij*Vij
    I2ij=sc.I2ij
#    Vij=sc.I2ij
    Vij=sc.Vij
    ex_I2ij=tables.Expr("abs(I2ij*Vij)")
    ex_I2ij.set_output(eP)
    ex_I2ij.eval()
    gc.collect()

    # print "Doing sparse edge power"
    # fep=eP.read()
    # fep[where(sep<np.max(sep))=0]
    # sep=sparse.csr_matrix(fep)
    
    logging.info("Doing total power")
    pp1=sc.edgePower.read()
    pp=np.triu(pp1)
    logging.info("Calculating total edge power")
    sc._v_attrs.totalEdgePower=np.sum(pp)
    logging.info("Calculating max edge power")
    sc._v_attrs.maxEdgePower=np.max(pp)
    sc._v_attrs.edgePowerShape=pp.shape
    h5.flush()

    logging.info("Calculating significant edge power")
    maxep=sc._v_attrs.maxEdgePower    
#    pps=np.sort(pp[pp>maxep/100000.0].flatten())
    # This is where I need to put the code to extract
    # the x,y,ap for the significant power.

    x=sc.x.read()
    y=sc.y.read()
    ap=sc.ap.read()
    w=np.where(pp>maxep/100000.0)
    pps=np.sort(pp[w].flatten())
    wx1=x[w[0]]
    wx2=x[w[1]]
    wy1=y[w[0]]
    wy2=y[w[1]]
    wp=pp[w[0],w[1]]

    tn=topNinds_(pp,1000)
    xl=tn[0]
    yl=tn[1]
    wx1=x[xl]
    wy1=y[xl]
    wx2=x[yl]
    wy2=y[yl]
    wp=pp[tn]

    print wx1[0:10]
    print wx2[0:10]
    print wy1[0:10]
    print wy2[0:10]

    if sc.__contains__('sig_pow'):
        sc.sig_pow.remove()
    h5.createArray(sc,'sig_pow',wp)

    if sc.__contains__('sorted_sig_power'):
        sc.sorted_sig_power.remove()
    h5.createArray(sc,'sorted_sig_power',pps)

    if sc.__contains__('sigx1'):
        sc.sigx1.remove()
    h5.createArray(sc,'sigx1',wx1)

    if sc.__contains__('sigx2'):
        sc.sigx2.remove()
    h5.createArray(sc,'sigx2',wx2)

    if sc.__contains__('sigy1'):
        sc.sigy1.remove()
    h5.createArray(sc,'sigy1',wy1)

    if sc.__contains__('sigy2'):
        sc.sigy2.remove()
    h5.createArray(sc,'sigy2',wy2)

    h5.flush()

    # NS=pp.size
    # NN=1000
    # L=(np.arange(NN)+1)*NS/NN - 1
    # spp=pps[L]
    # if sc.__contains__('step_power'):
    #     sc.step_power.remove()
    # h5.createArray(sc,'step_power',spp)


    
def solve_(h5,sc):
    M0=dwwsp.diag(sc.ipv_in.read() + sc.ipv_out.read() + sc.ipv_free.read().sum(axis=0)) \
        - sc.ipv_free.read()

    w=ipv_in-ipv_out
    V0 = np.linalg.solve(M0,w) #sc.ipv_in.read())
#    I0 = np.sum(V0*sc.ipv_out.read())

    Iout=(V0+1)*ipv_out.read()
    Iin=(1-V0)*ipv_in.read()
    cur=cfree*(V0-V0[:,np.newaxis])
    flo=np.sum(np.abs(cur)/2.0,axis=0)
    I=flo/2.0+Iout+Iin    
    I2ij=cur

    atom=tables.Float64Atom(shape=())
    filters = tables.Filters(complevel=0, complib='zlib')    

    sc._v_attrs.I0=I0

    if sc.__contains__('V0'):
        sc.V0.remove()
    if sc.__contains__('M0'):
        sc.M0.remove()
    if sc.__contains__('I'):
        sc.I.remove()
    if sc.__contains__('I2ij'):
        sc.I2ij.remove()

    h5.createArray(sc,'V0',V0)
    h5.createArray(sc,'M0',M0)
    h5.createArray(sc,'I',I)
    h5.createArray(sc,'I2ij',I2ij)
    h5.flush()


def getNth_bad(h5,N):
    i=0
    for sc in h5.root.scenarios:
        if i==N:
            return sc
        i+=1
    logging.debug("Whoops. We didn't find the scenario.")
    return False

def getNth_orig2(h5,N):
    for i in h5.root.scenarios:
        print "i is:",i
        print "in is:",i._v_attrs.ind
        if i._v_attrs.ind==N:
            return i
    return False

def getNth(h5,N):
    for i in h5.root.scenarios:
        if i._v_attrs.ind==N:
            return i
    return -1

def getNs(h5):
    r=[]
    for i in h5.root.scenarios:
        r.append(i._v_attrs.ind)
    return r

def getScenarios(h5):
    return [i for i in h5.root.scenarios]

def getOrdered(h5):
    scns=getScenarios(h5)
    inds=np.argsort(np.array(getNs(h5)))
    return [scns[i] for i in inds]

def getOrderedInds(h5):
    scns=getScenarios(h5)
    inds=np.argsort(np.array(getNs(h5)))
    return [scns[i]._v_attrs.ind for i in inds]

def main(name='l_m_1'):
    h5=makeProject("fract.h5","Fractal Landscapes")
    scn=makeScenario(h5,name)
    addHabTif(h5,scn,'maps/l_m_1.tif')
    addSrcSinkTif2(h5,scn,'maps/source.tif','maps/sink.tif')
    return h5,scn

def mycdist_t(A,B):
    """
    NOTE: This returns the transpose of numpy's cdist!!
    """
    x1=A[:,0]
    y1=A[:,1]
    x2=B[:,0][:,np.newaxis]
    y2=B[:,1][:,np.newaxis]
    r=np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return r

def mycdist(A,B):
    x1=A[:,0][:,np.newaxis]
    y1=A[:,1][:,np.newaxis]
    x2=B[:,0]
    y2=B[:,1]
    r=np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return r

def test_mycdist(name='l_m_1'):
    h5=makeProject("fract4.h5","Fractal Landscapes")
    scn=makeScenario(h5,name)
    addHabTif(h5,scn,'maps/l_m_1.tif')
    addSrcSinkTif2(h5,scn,'source.tiff','sink.tiff')

    x=scn.x.read()
    y=scn.y.read()
    tg_x=scn.tg_x.read()
    tg_y=scn.tg_y.read()

    hab=np.asarray([x,y]).transpose()
    src=np.asarray([tg_x,tg_y]).transpose()
    cd1=distance.cdist(hab,src)
    cd2=mycdist(hab,src)
    
    print "CD1",cd1
    print "CD2",cd2
    print "DIF",cd1-cd2
    print cd1.shape
    print cd2.shape
    return h5,scn
