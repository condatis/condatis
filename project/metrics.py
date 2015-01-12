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
