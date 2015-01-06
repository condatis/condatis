import gdal
import exportgisui
from PyQt4 import QtCore, QtGui
import numpy as np
from gdalconst import *
from osgeo import osr

NODATA_FLOAT=3.4e38
NODATA_INT=-9999
NODATA_BYTE=255

class ExportGisDialog(QtGui.QDialog,exportgisui.Ui_ExportGisDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

        # self.opTexts["GeoTiff","Arc ASCII Grid","Arc Binary Grid"]
        # self.opTypes=[gdal.GetDriverByName('GTiff'),
        #               gdal.GetDriverByName('AAIGrid'),
        #               gdal.GetDriverByName('AIG')]
        # self.opExts=['.tif','.txt','.adf']

        # NOTE: AAIGrid and AIG don't support create
        self.opTexts=["GeoTiff"]
        self.opTypes=[gdal.GetDriverByName('GTiff')]
        self.opExts=['.tif']

        self.comboBox.addItems(self.opTexts)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), 
                               self.outButClicked)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), 
                               self.copyButClicked)

    def setValues(self,op,cp):
        self.lineEdit.setText(op)
        self.lineEdit_2.setText(cp)

    def getValues(self):
        copyname=str(self.lineEdit_2.text())
        optype_n=self.comboBox.currentIndex()
        opname=str(self.lineEdit.text()+self.opExts[optype_n])
        driver=self.opTypes[optype_n]
        return (opname,copyname,driver,1.0)

    def outButClicked(self):
        dr=self.lineEdit.text()
        file = QtGui.QFileDialog.getSaveFileName(self, 
            "Save GIS layer", dr, "[GDAL] Raster (*)")
        if file:
            self.lineEdit.setText(file)

    def copyButClicked(self):
        dr=self.lineEdit_2.text()
        file = QtGui.QFileDialog.getOpenFileName(self, 
            "Open GIS layer to copy [GDAL]", dr, "[GDAL] Raster (*)")
        if file:
            self.lineEdit_2.setText(file)


# Function to read the original file's projection:
def getGeoInfo(fileName):
    SourceDS = gdal.Open(fileName, GA_ReadOnly)
    NDV = SourceDS.GetRasterBand(1).GetNoDataValue()
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    DataType = SourceDS.GetRasterBand(1).DataType
    DataType = gdal.GetDataTypeName(DataType)
    return NDV, xsize, ysize, GeoT, Projection, DataType


def createGeoFile(name,driver,a,projinfo,dtype=gdal.GDT_Float64):
    NDV,xsize,ysize,GeoT,Projection,DataType=projinfo
#    if NDV==None:
#        NDV=-9999

    if dtype==gdal.GDT_Float64:
        NDV=NODATA_FLOAT
    else:
        NDV=NODATA_INT

    NewFileName = name
    # Set nans to the original No Data Value
    a[np.isnan(a)] = NDV
    # Set up the dataset
    DataSet = driver.Create( NewFileName, xsize, ysize, 1, dtype )
#    DataSet = driver.Create( NewFileName, xsize, ysize, 1, gdal.GDT_Float32 )
            # the '1' is for band 1.
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection( Projection.ExportToWkt() )
    # Write the array
#    z=np.max(a)/1e32
#    a[np.where(a<z)]=NDV
#    a[np.where(a!=z)]=10.0
#    a[np.where(a==z)]=NDV
    DataSet.GetRasterBand(1).WriteArray(np.transpose(a).astype(np.float64))
    DataSet.GetRasterBand(1).SetNoDataValue(NDV)
    return NewFileName



def createGeoFile_old2(name,driver,a,projinfo):
    NDV,xsize,ysize,GeoT,Projection,DataType=projinfo
    if DataType == 'Float32':
        DataType = gdal.GDT_Float32
        NDV=NODATA_FLOAT
    if DataType == 'Float64':
        DataType = gdal.GDT_Float64
        NDV=NODATA_FLOAT
    if DataType == 'Int32':
        DataType = gdal.GDT_Int32
        a=a.astype(int)
        NDV=NODATA_INT
    if DataType == 'Byte':
        DataType = gdal.GDT_Byte
        NDV=NODATA_BYTE

    NewFileName = name
    # Set nans to the original No Data Value
    a[np.isnan(a)] = NDV
    # Set up the dataset
    DataSet = driver.Create( NewFileName, xsize, ysize, 1, DataType )
#    DataSet = driver.Create( NewFileName, xsize, ysize, 1, gdal.GDT_Float32 )
            # the '1' is for band 1.
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection( Projection.ExportToWkt() )
    # Write the array
#    z=np.max(a)/1e32
#    a[np.where(a<z)]=NDV
#    a[np.where(a!=z)]=10.0
#    a[np.where(a==z)]=NDV
    DataSet.GetRasterBand(1).WriteArray(np.transpose(a).astype(np.float64))
    DataSet.GetRasterBand(1).SetNoDataValue(NDV)
    return NewFileName



def createGeoFile_old(name,driver,a,projinfo):
    NDV,xsize,ysize,GeoT,Projection,DataType=projinfo
                                                            
    if DataType == 'Float32':
        DataType = gdal.GDT_Float32
    if DataType == 'Int32':
        DataType = gdal.GDT_Int32
        a=a.astype(int)
    if DataType == 'Byte':
        DataType = gdal.GDT_Byte
    print "Data type",DataType
    print "Array:",a
    print "Min/Max of exported array: %f, %f" % (np.min(a)*1.0, np.max(a)*1.0)
#    if NDV==None:
#        NDV=-9999

    DataType=gdal.GDT_Float64
    NDV=NODATA


    NewFileName = name
    # Set nans to the original No Data Value
    a[np.isnan(a)] = NDV
    # Set up the dataset
    DataSet = driver.Create( NewFileName, xsize, ysize, 1, DataType )
#    DataSet = driver.Create( NewFileName, xsize, ysize, 1, gdal.GDT_Float32 )
            # the '1' is for band 1.
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection( Projection.ExportToWkt() )
    # Write the array
#    z=np.max(a)/1e32
#    a[np.where(a<z)]=NDV
#    a[np.where(a!=z)]=10.0
#    a[np.where(a==z)]=NDV


    DataSet.GetRasterBand(1).WriteArray(np.transpose(a).astype(np.float64))

    print "NDV:",NDV
    DataSet.GetRasterBand(1).SetNoDataValue(NDV)
    return NewFileName

