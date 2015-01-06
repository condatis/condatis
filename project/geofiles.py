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

    
    
