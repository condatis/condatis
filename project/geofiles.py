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
#!/usr/bin/env python

# FILE: geofiles.py
# PURPOSE: Conversion between numpy, GDAL and QGIS
# AUTHOR: David Wallis
# CREATED: 11/2/14

import gdal
import numpy as np
#import osr

#from PyQt4.QtCore import *
#from PyQt4 import QtGui
#from qgis.core import *
#from qgis.gui import *
#import sys
#import os

def compose2(f,g):
    """Function composition: returns function g(f(x)) """
    return lambda x: f(g(x))



def file2GDAL(fname):
    """Return a GDAL object from fname."""
    return gdal.Open(fname)

def GDAL2np(gd):
    """Return a numpy array from GDAL object."""
    return np.array(gd.GetRasterBand(1).ReadAsArray())

#Return a numpy array from a filename.
#file2np=compose2(GDAL2np,file2GDAL)

def file2np(fname):
    gd=gdal.Open(fname)
#    gn=np.array(gd.GetRasterBand(1).ReadAsArray().astype(np.int32))
    gn=np.array(gd.GetRasterBand(1).ReadAsArray().astype(np.int32))
    return gn

def file2layer(fname):
    """Return QGIS raster layer from fname."""
    return qgis.core.QgsRasterLayer(fname)

def layer2GDAL(layer):
    return gdal.Open(str(layer.source()))

#Return a numpy array from a QGIS layer
layer2np=compose2(layer2GDAL,GDAL2np)

#NOTE: This is specifically a geotiff
def np2tiff(arr, fname="gdaltmp1234.tiff"):
    xsize,ysize=arr.shape
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(fname,xsize,ysize, 1, gdal.GDT_Byte )
    DriverGTiff = gdal.GetDriverByName('GTiff')
    dst_ds.GetRasterBand(1).WriteArray(arr)
    dst_ds = None

    
    
