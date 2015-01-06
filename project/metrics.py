import scipy.linalg
import contable8 as con
import dwwspatial as dwwsp
import numpy as np
import logging

def kern(d, R=1.0, alpha=1.0):
#    print "I SHOULDN'T REALLY BE CALLED: Kernel params: R=%e, alpha=%e" % (R, alpha)
    return R*alpha**2.0/(2.0*np.pi) * np.exp(-alpha*d)

def eigenMatrix(scn):
    x=scn.x.read()
    y=scn.y.read()
    ap=scn.ap.read()
    R=scn._v_attrs.R
    dispersal=scn._v_attrs.dispersal
    dm=dwwsp.dist(x,y)
    phi=kern(dm,R,2.0/dispersal)
    ap2=ap**2
    aa=np.outer(ap,ap2)
    return phi*aa

def ViL(M):
    w,vl,vr=scipy.linalg.eig(M,left=True,right=True)
#    "Eigenvalues: ",w
    Lm=w[0]
    x,y=vr,vl
    return Lm*x*y

def ViS(M,scn):
    ap=scn.ap.read()
    return 3*ViL(M)/ap

def VLS(M,scn):
    ap=scn.ap.read()
    w,vl,vr=scipy.linalg.eig(M,left=True,right=True)
#    print "Eigenvalues: ",w
    i=0
    Lm=np.real(w[i])
    x,y=np.real(vr[:,i]),np.real(vl[:,i])
    VL=Lm*x*y
    VS=3*VL/ap
    return VL,VS,Lm

def calcMetrics(h5,scn):
    logging.info("Generating eigen matrix")
    M=eigenMatrix(scn)
    logging.info("Getting eigenvalues and eigenvectors")
    VL,VS,met=VLS(M,scn)
    if scn.metrics.__contains__('ViL'):
        scn.metrics.ViL.remove()
    if scn.metrics.__contains__('ViS'):
        scn.metrics.ViS.remove()
    h5.createArray(scn.metrics,'ViL',VL)
    h5.createArray(scn.metrics,'ViS',VS)
    scn._v_attrs.metapopCapacity=met
    logging.info("Eigenvalues and eigenvectors calculated")

def clearMetrics(scn):
    logging.info("Clearing metrics")
    if scn.metrics.__contains__('ViL'):
        scn.metrics.ViL.remove()
    if scn.metrics.__contains__('ViS'):
        scn.metrics.ViS.remove()
