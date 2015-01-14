#!/usr/bin/env python
"""
Condatis; software to assist with the planning of habitat restoration

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
(ii) a comment at the head of any file containing the source code derived from this covered work should read: "Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  Our modification was permitted by the GNU General Public License v.3. Instructions for obtaining the original version of Condatis can be found at www.condatis.org.uk. Any modified or verbatim copies of our work must preserve this notice." Where text in square brackets should be replaced by the appropriate numbers.
(iii) if your modified work has a user interface, the user interface should prominently display the notice: "Part of this work is a modified version of the work Condatis v.[version number] Copyright (c)[year]  D.W. Wallis and J.A. Hodgson.  See www.condatis.org.uk." Where text in square brackets should be replaced by the appropriate numbers.
"""
import copy
import cPickle as pickle
from mplwidget import MplWidget
from PyQt4 import QtCore, QtGui
import econetui
import numpy as np
import matplotlib.pyplot as plt
import ecoplot
import os
import project.contable8 as con
import project.project as project
import sourcesinkui
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QTAgg as NavigationToolbar
import project.metrics as metrics
import calculatingui
from PIL import Image
import gc
import cProfile
import re
import manualui
import string
import exportgis
import calcdialog
import logging
import droppinggui
import dropfiltergui
import ntpath
import gdal
import openhabitat
import settingsgui
import addcellgui
import sys
import time
import cStringIO
import traceback
import patterns
import sourcesinkgui
import addinggui
import registergui
import aboutgui
import manualgui
import version

__author__ = "David Wallis"
__copyright__ = "Copyright 2015, D.W Wallis and J.A Hodgson"
__credits__ = ["Aidan Lonergan", "Andrew Suggitt", "Atte Moilanen", "Chloe Bellamy", "Duncan Blake", "Geoffrey Heard", "James Latham", "Jamie Robins", "Jonathan Rothwell", "Jonathan Winn", "Kevin Watts", "Nicholas Macgregor", "Nik Bruce", "Paul Evans", "Phil Baarda", "Sarah Scriven", "Sarah Taylor", "Sheila George", "Steve Palmer", "Tim Graham", "Tom Squires", "Vicky Kindemba", "The authors also acknowledge funding from the UK Natural Environment Research Council grant number NE/L002787/1."]
__license__ = "GPL"
__version__ = version.version
__maintainer__ = "D.W. Wallis"
__email__ = "d.wallis@liv.ac.uk"
__status__ = "Development"


#REVISION="$Rev: 18 $"
#REVISION="$Rev: 18 $"
#sp=string.split(REVISION)

VERSION=__version__

def makeIfNot(dir):
    if not os.path.exists(dir):
        os.makedirs(str(dir))

def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """

    separator = '-' * 80
    logFile = "condatiserror.log"

    notice="An unhandled exception occured. Please help to improve this software by telling us about this problem. Please copy the error report below and send it an in an email to: econets@liverpool.ac.uk\n"
    versionInfo=VERSION
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    
    
    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    errorbox = QtGui.QMessageBox()
    errorbox.setText(str(notice)+str(msg)+"Version:"+str(versionInfo))
    errorbox.exec_()

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))



class MyMain(QtGui.QMainWindow, econetui.Ui_MainWindow):
    def __init__(self,projectfile=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        # Settings
        self.settingsDlg=settingsgui.SettingsDialog(self)
        if os.path.isfile("condatis.save"):
            settingsgui.appsettings=settingsgui.loadSettings()
        else:
            settingsgui.appsettings=settingsgui.Settings()
        self.settingsDlg.setFromSettings(settingsgui.appsettings)
        self.checkMakeDirectories()
        
        # Add matplotlib's navigation toolbar.
        self.mpl_toolbar = NavigationToolbar(self.mainfig.canvas, self.centralwidget)
        self.verticalLayout_3.addWidget(self.mpl_toolbar)

        # Set up figures and bind button click to open figure in main window.
        self.fig=[self.subfig1,self.subfig2,self.subfig3,self.subfig4]
        self.fig[0].canvas.mpl_connect('button_press_event', self.subFig0Clicked)
        self.fig[1].canvas.mpl_connect('button_press_event', self.subFig1Clicked)
        self.fig[2].canvas.mpl_connect('button_press_event', self.subFig2Clicked)
        self.fig[3].canvas.mpl_connect('button_press_event', self.subFig3Clicked)

        # Set up views for subplots
        self.fNullView=[ecoplot.showNull,
                        ecoplot.showNull,
                        ecoplot.showNull,
                        ecoplot.showNull]
        self.nullTips=['','','','']
        self.fHabView=[ecoplot.showHabitat,
                       ecoplot.showHabSourceSink,
                       ecoplot.showSource,
                       ecoplot.showSink,
                       ecoplot.showNull]
        self.habTips=['Habitat','Habitat, Source and Target','Source','Target', '']
        self.fVoltView=[ecoplot.showFlow,
                        ecoplot.showVoltage,
                        ecoplot.showVoltageLayers,
                        ecoplot.showSortedVoltage]
        self.voltTips=['Flow','Progress', 'Isolated Areas','Layers','Habitat']
        self.fPowerView=[ecoplot.showSigEdgePower,
                         ecoplot.showVoltageContour,
                         ecoplot.showCumSum,
                         ecoplot.showCumSumPC]
        self.powerTips=['Bottlenecks','Progress Contours','Cumulative Power','Percentage Cumulative Power',]
        self.fDroppingView=[ecoplot.showDroppingDropped,
                            ecoplot.showDroppingNewHab,
                            ecoplot.showDroppingFlow,
                            ecoplot.showDroppingPCFlow]
        self.droppingTips=['Dropped Habitat','New Habitat','Dropped Node Flow',''] 
        self.fPopulationView=[ecoplot.showPatchLoss,
                       ecoplot.showPatchPArea,
                       ecoplot.showNull,
                       ecoplot.showNull,
                        ecoplot.showNull]
        self.populationTips=['Patch Loss','Area Loss','','',''] 
        self.fComparisonView=[ecoplot.showFlowComparison,
                       ecoplot.showAreaComparison,
                       ecoplot.showMetapopComparison,
                       ecoplot.showTLSComparison,
                       ecoplot.showNull]
        self.comparisonTips=['Speed','Areas','Metapopulation capacity','Total link strength',''] 
       
        self.fCurrentView=self.fHabView
        self.currentTip=self.habTips

        # Bind menu actions to functions
        self.actionSettings.triggered.connect(self.settings)

        self.actionNew.triggered.connect(self.guiNewProject)
        self.actionSave.triggered.connect(self.saveProject)
        self.actionOpen.triggered.connect(self.guiOpenProject)
        self.actionClose.triggered.connect(self.closeProject)
        self.actionOpen_Habitat.triggered.connect(self.guiOpenHabitat)
        self.actionAbout.triggered.connect(self.about)
        self.actionView_Map.triggered.connect(self.habitatView)
        self.actionView_Voltage.triggered.connect(self.voltageView)
        self.actionView_Power.triggered.connect(self.powerView)
        self.actionView_Population.triggered.connect(self.populationView)
        self.actionComparison_View.triggered.connect(self.comparisonView)
        self.actionDropping_View.triggered.connect(self.droppingView)
        self.actionConductance.triggered.connect(self.calc)
        self.actionCalc_Power.triggered.connect(self.calcPower)
        self.actionDropping_Filter.toggled.connect(self.dropFilter)
        self.actionCalculate_All.triggered.connect(self.calcAll)
        self.actionShow_subplots.triggered.connect(self.showSubplots)
        self.actionShow_history_and_controls.triggered.connect(self.showHistory)
        self.actionShow_Plot_navigation_bar.triggered.connect(self.showNavbar)
        self.actionHide_plot_navigation_bar.triggered.connect(self.hideNavbar)
        self.actionDuplicate_Scenario.triggered.connect(self.duplicateScenario)
        self.actionRename_Scenario.triggered.connect(self.renameScenario)
        self.actionDelete_From_Scenarios.triggered.connect(self.deleteScenario)
        self.actionAdd_Source_Sink.triggered.connect(self.assignSourceSink)
        self.actionCalculate_Metrics.triggered.connect(self.calculateMetrics)
        self.actionToggle_Navbar.toggled.connect(self.toggleNavbar)
        self.actionToggle_Subplots.toggled.connect(self.toggleSubplots)
        self.actionToggle_Sidebar.toggled.connect(self.toggleSidebar)
        self.actionSmoothing.toggled.connect(self.toggleSmoothing)
        self.actionScenario_Data.triggered.connect(self.exportScenarioData)
        self.actionProject_Data.triggered.connect(self.exportProjectData)
        self.actionCurrent_Map.triggered.connect(self.exportCurrentMap)
        self.listWidget.itemClicked.connect(self.selectHistory)
        self.actionBackwards_Improvement.toggled.connect(self.openDroppingDialog)
        self.actionForward_Optimise.toggled.connect(self.adding)
        self.cumPowerSpinBox.valueChanged.connect(self.cumPowerChanged)
        self.cumGoButton.clicked.connect(self.goButtonPressed)
        self.actionManual.toggled.connect(self.openManual)
        self.actionWhats_This.triggered.connect(self.whatsThis)
        self.actionVoltage_Map.triggered.connect(self.exportVoltageMap)
        self.actionDropped_Habitat_2.triggered.connect(self.exportDroppedHabitat)
        self.actionDropping_Map.triggered.connect(self.exportDroppedRankMap)
        self.actionVoltage_Layers_Map.triggered.connect(self.exportVoltageLayersMap)
        self.actionHabitat_Map.triggered.connect(self.exportHabitatMap)
        self.actionSource_Map.triggered.connect(self.exportSourceMap)
        self.actionSink_Map.triggered.connect(self.exportSinkMap)
        self.actionFlow_Map.triggered.connect(self.exportFlowMap)
        self.actionDropping_Data.triggered.connect(self.exportDroppingData)
        self.mainCanvas().mpl_connect('button_press_event', self.onclick)
        self.actionPoint.toggled.connect(self.onpoint)
        self.actionClose_App.triggered.connect(self.closeApp)

        self.registerCondatis()
        
        # Other stuff to initialise
        self.mainAxes().set_aspect('auto')
        self.hideNavbar()
        self.show()
        self.project=[]
        if projectfile:
            self.openProject(projectfile)
        else:
            self.startup()
        self.setButtonStates()
        self.subFig=0
        self.addingDialog=None
        self.droppingDialog=None
        self.manualDialog=None
        self.dropFilterDlg=None
        self.clickstate=None
        self.navbarflag=False
        self.addingdlg=None


    def adding(self,state):
        if state:
            if self.addingdlg is None:
                self.addingdlg=addinggui.addingDlg(self,self.project)
            else:
                self.addingdlg.init2()
            self.addingdlg.show()
        else:
            self.addingdlg.hide()

        
    def projFile(self):
        return self.project.h5file.filename

    def projFileName(self):
        return os.path.basename(self.projFile())

    def projName(self):
        base=self.projFileName()
        return os.path.splitext(base)[0]
        
    def projPath(self):
        return os.path.dirname(self.projFile())
        
    def whatsThis(self):
         QtGui.QWhatsThis.enterWhatsThisMode()

    def openManual(self,stat):
        if stat:
            if self.manualDialog is None:
                self.manualDialog = manualgui.ManualDialog(self)
            self.manualDialog.show()
        else:
            self.manualDialog.hide()

    def doRegister(self):
        print "Registering Condatis"
        
    def registerCondatis(self):
        if not settingsgui.appsettings.registered == True:
            dlg=registergui.registerDlg(self)
            ret=dlg.exec_()
            
    def about(self):
        dlg=aboutgui.AboutDialog(self)
        ret=dlg.exec_()

    def about_old(self):
        QtGui.QMessageBox.about(self, "About", "Condatis. \n\nCopyright The University of Liverpool (2014).\nVersion %s\n\nThis is a Beta version of software issued only to members of the Condatis project for testing.\nPlease do redistribute this software. If you are interested in obtaining a copy then please contact either:\n\nJenny Hodgson - jenny.hodgson@liverpool.ac.uk\nDavid Wallis - d.wallis@liverpool.ac.uk. " % VERSION)


    def checkMakeDirectories(self):
        # Make all the directories if they don't exist.
        base=settingsgui.appsettings.path
        makeIfNot(base)
        for i in ['maps','projects','exports', 'manual']:
            filename=base+'/'+i
            makeIfNot(filename)
        manpage=base+'/manual/index.html'
        if not os.path.exists(manpage):
            with open(manpage,'w+') as f:
                f.write(""" 
<html>
<h1>Condatis Manual</h1>
<p>
You don't have the manual installed. You can get it <a href="http://download.condatis.org.uk">here</a>.
</p>

<p>
When you have downloaded the manual, save it in your condatis home folder. A folder has been created for you called 'manual'. The manual must be saved here or Candatis will not be able to find it.
</p>

<p>
You may also want to download the example maps from the same site. These need to be saved in your condatis home folder under 'maps'
</p>

</html>
""")
            

    def settings(self):
        if self.settingsDlg.exec_():
            # Have to save the registered status to stop
            # overwriting it
            reg=settingsgui.appsettings.registered
            st=self.settingsDlg.getRawData()
            # Put the registered status back to what it was
            st.registered=reg
            settingsgui.appsettings=st
            settingsgui.saveSettings(st)
            self.checkMakeDirectories()

    def onpoint(self,stat):
        if stat:
            self.clickstate='point'
        else:
            self.clickstate=None

    def clearSource(self):
        self.project.clearSource()
        self.infoBox()
        self.setButtonStates()
        
    def clearTarget(self):
        self.project.clearTarget()
        self.infoBox()
        self.setButtonStates()

    def clearSourceTarget(self):
        self.project.clearSourceTarget()
        self.infoBox()
        self.setButtonStates()
            
    def add2layer(self,x,y,v,layer):
        if layer==0: # Habitat
            self.project.add2hab(x,y,val)
        if layer == 1: # Source
            self.project.add2source(x,y)
        if layer == 2: # Targt
            self.project.add2target(x,y)
        self.infoBox()

    def addPoints(self,x,y,val,r,N,layer,pattern):
        if pattern == -2: # Point
            xx,yy=x,y
        if pattern == -3: # Circle
            xx,yy=patterns.circle(x,y,r)
        if pattern == -4: # Star
            xx,yy=patterns.star(x,y,r,N)
        if pattern == -5: # Random uniform
            xx,yy=patterns.uniform(x,y,r,N)
        if pattern == -6: # Random normal
            xx,yy=patterns.normal(x,y,r,N)

        if pattern == -2:
            xxx=xx
            yyy=yy
        else:
            xxyy=np.array(list(set(zip(list(xx),list(yy)))))
            xxx=xxyy[:,0]
            yyy=xxyy[:,1]
        vvv=xxx*0+val

        if layer==0:
            ms=self.project.scenario._v_attrs.map_x_scale
            self.project.add2hab(xxx,yyy,vvv)
            if self.project.scenario._v_attrs.map_x_scale == 1.0:
                self.project.scenario._v_attrs.map_x_scale = ms
        if layer==1:
            self.project.add2source(xx,yy)
        if layer==2:
            self.project.add2target(xx,yy)

    def onclick(self,event):
        if event.inaxes:
            if self.clickstate=='point' and not self.navbarflag:
                x=int(event.xdata+.5)
                y=int(event.ydata+.5)
                dlg=addcellgui.AddCellDialog(self,self.project)
                dlg.setxy(x,y)
                if dlg.exec_():
                    xnew,ynew,val,r,N=dlg.getValues()
                    layer=dlg.getLayer()
                    pattern=dlg.getPattern()

                    reply = QtGui.QMessageBox.question(self, 'Message',
                            "Are you sure? This Cannot be undone!", QtGui.QMessageBox.Yes | 
                            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                
                    if reply == QtGui.QMessageBox.Yes:
                        self.addPoints(x,y,val,r,N,layer,pattern)
                        self.infoBox()
                        self.setButtonStates()
                        if dlg.checkBox.isChecked():
                            self.refreshMainMap()

    def dropFilter(self):
        if self.dropFilterDlg is None:
            self.dropFilterDlg=dropfiltergui.DropFilterDialog(self,project=self.project)
        self.dropFilterDlg.show()

    def openDroppingDialog(self,stat):
        if stat:
            if self.droppingDialog is None:
                self.droppingDialog = droppinggui.DroppingDialog(self,self.project)
            self.droppingDialog.show()
            self.droppingDialog.init()
        else:
            if self.droppingDialog:
                self.droppingDialog.hide()
        

    def goButtonPressed(self):
        val=self.cumPowerSpinBox.value()
        self.project.cumPowerThreshold=val
        if not self.fCurrentView == self.fPowerView:
            self.powerView()
        ecoplot.showSigEdgePower(self.mainCanvas(),self.project)
                
    def cumPowerChanged(self):
        val=self.cumPowerSpinBox.value()
        self.project.cumPowerThreshold=val
        ecoplot.showCumSum(self.mainCanvas(),self.project)
        

    def layersChanged(self):
        val=self.layersSpinBox.value()
        self.project.powerThreshold=val
        logging.debug("Layers threshold = ", val)
        self.project.scVLPclear()
        if not self.fCurrentView == self.fPowerView:
            self.powerView()
        else:
            ecoplot.showPowerConnects(self.mainCanvas(),self.project)

    def openAddingDialog(self,stat):
        if stat:
            if self.addingDialog is None:
                self.addingDialog = ForwardOptDialog(self)
            self.addingDialog.show()
#            self.powerView()
        else:
            self.addingDialog.hide()


    def refreshMaps(self):
        self.selectView(self.fCurrentView, self.currentTip)
        self.fCurrentView[self.subFig](self.mainCanvas(),self.project)


    def refreshMainMap(self):
        self.fCurrentView[self.subFig](self.mainCanvas(),self.project)

    def mapScaleChanged(self,val):
        self.project.scenario._v_attrs.mapscale=val

    def areaScaleChanged(self,val):
        self.project.scenario._v_attrs.areascale=val
        self.project.calcap()
        self.infoBox()
        self.refreshMaps()

    def toggleSmoothing(self,stat):
        if stat:
            ecoplot.interp='gaussian'
        else:
            ecoplot.interp='nearest'
        self.fCurrentView[self.subFig](self.mainCanvas(),self.project)

    def toggleNavbar(self,stat):
        if stat:
            self.showNavbar()
            self.navbarflag=True
        else:
            self.hideNavbar()
            self.navbarflag=False

    def toggleSubplots(self,stat):
        if stat:
            self.showSubplots()
        else:
            self.hideSubplots()

    def toggleSidebar(self,stat):
        if stat:
            self.showHistory()
        else:
            self.hideHistory()

    def scenarioName(self):
        if self.project.scenario==[]:
            return "None"
        else:
            return self.project.scenario._v_name

    def fileName(self):
        if self.project.h5file==[]:
            return "None"
        else:
            return self.project.h5file.filename        

    def showMessage(self,text):
        msg="PROJECT: %s SCENARIO: %s | %s" % \
            (self.fileName(),self.scenarioName(),text)
        self.statusbar.showMessage(msg)           

    def guiNewProject(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Start Project', 
                                              'Project Name:')
        filepath=settingsgui.appsettings.path+'/projects/'
        filename=filepath+text+'.h5'
        if ok:
            if QtCore.QFile.exists(filename):
                existerr='A project already exists with that name. Do you want to overwrite it?'
                reply = QtGui.QMessageBox.question(self, \
                    'Start Project',existerr, QtGui.QMessageBox.Yes, \
                                                   QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    os.remove(str(filename))
                    self.closeProject()
                    self.newProject(filename)
                else:
                    self.guiNewProject()
            else:
                self.closeProject()
                self.newProject(filename)
            self.setButtonStates()
            self.nullView()
            self.infoBoxClr()
            self.clearList()
        return ok


    def startup(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText('How do you want to start?')
        msgBox.addButton(QtGui.QPushButton('Start a new project'), QtGui.QMessageBox.YesRole)
        msgBox.addButton(QtGui.QPushButton('Open an existing project'), QtGui.QMessageBox.NoRole)
        ret = msgBox.exec_();
        if ret==0:
            if not self.guiNewProject():
                self.startup()
        else:
            self.guiOpenProject()


    def updateUi(self):
        self.infoBox()
        self.updateList()

    # Project functions
    def newProject(self,projname):
        logging.info("Creating new project")
        self.project=project.Project(str(projname))
        self.setWindowTitle(self.project.h5file.filename)
        self.setButtonStates()
        self.showMessage("New project created.")

    def openProject_(self,fname):
        logging.info("Opening existing project")
        self.project=project.Project(projname)
        self.setWindowTitle(self.project.h5file.filename)
        self.setButtonStates()
    
    def openProject(self,fname):
        self.closeProject()
        self.project=project.Project(fname)
        if self.project.h5file.root.scenarios._v_nchildren > 0:
            key=self.project.h5file.root.scenarios._v_children.keys()[0]
            self.project.scenario=self.project.h5file.root.scenarios._v_children[key]
            self.habitatView()
            self.updateList()
            self.infoBox()
        else:
            self.nullView()
            self.clearList()
            self.clearList()
        self.setButtonStates()
        self.setWindowTitle(self.project.h5file.filename)

    def guiOpenProject(self):
        projpath=settingsgui.appsettings.path+'/projects'
        file = QtGui.QFileDialog.getOpenFileName(self, 
            "Open Project", projpath, "*.h5")
        if file:
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            self.openProject(fname)

    def openProject_old(self,fname):
        self.lslist=pickle.load(open(fname,"rb"))
        self.projectName=fname
        self.setWindowTitle(self.projectName)
        self.ls=self.lslist[0]
        self.habitatView()


    def closeProject(self):
        if self.project:
            logging.info("Closing the project.")
            self.project.h5file.flush()
            self.project.h5file.close()
            if self.droppingDialog:
                self.droppingDialog.close()
                self.droppingDialog=None
            if self.dropFilterDlg:
                self.dropFilterDlg.close()
                self.dropFilterDlg=None
            self.project.scenario=[]
            self.project.h5file=[]
            self.nullView()
            self.listWidget.clear()
            self.infoBoxClr()
            self.project=[]
            self.setButtonStates()
            self.setWindowTitle('Condatis')

    def guiSaveProject(self):
        file = QtGui.QFileDialog.getSaveFileName(self, 
            "Save Project As..", ".", "*.eho")
        if file:
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            self.projectName=fname
            self.doSaveProject

    def saveProject(self):
        logging.info("Saving project")
        self.project.saveProject()

    def saveProjectAs(self,fname):
        pass

    def mapll(self,x,y):
        fpath=self.project.scenario._v_attrs.habfilename
        ds = gdal.Open(fpath)
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        
        dx=gt[4]
        dy=gt[5]



        minx = gt[0]
        miny = gt[3] + width*gt[4] + height*gt[5] 

        lat=minx+x*dx
        lon=miny-y*dy
        return lat,lon
        
    def doExportDroppingData(self,filename):
#        logging.info("Creating export file: %s",filename)
        f=open(filename,'w')
        scenarioName=self.project.scenario._v_name
        fname=self.project.h5file.filename

        scn=self.project.scenario
        indlist=scn.indlist.read()
        xnew,ynew=scn.xnew.read(),scn.ynew.read()
        lat,lon=mapll(xnew,ynew)

        for i in range(xnew.size):
            f.write("%d,%d,%d,%f,%f\n" % i,xnew[i],ynew[i],lat[i],lon[i])
            
        f.close()

    def exportDroppingData(self):
        txttype="TXT (*.txt)"
        scenarioName=self.project.scenario._v_name
        fname=self.project.h5file.filename
        suggested=settingsgui.appsettings.path+"/%s.%s.dropping" % (fname,scenarioName)
        filename,fil = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save File',suggested, txttype)
        logging.debug("Exporting to" + filename)
        if filename:
            self.doExportDroppingData(filename)



    def doExportScenarioData(self,filename):
        logging.info("Creating export file: %s",filename)
        f=open(filename,'w')
        scenarioName=self.project.scenario._v_name
        fname=self.project.h5file.filename
        f.write("Scenario data for scenario '%s' in project '%s'.\n" % (scenarioName,fname))
        f.write('Number of cells: %f\n' % self.project.habitatN())
        f.write('Horisontal grid size: %f\n' % self.project.rasterSize()[0])
        f.write('Vertical grid size: %f\n' % self.project.rasterSize()[1])
        f.write('Habitat area: %f\n' % self.project.totalArea())
        f.write('Origin x: %f\n' % self.project.originX())
        f.write('Origin y: %f\n' % self.project.originY())
        f.write('Cell size x: %f\n' % self.project.cellSizeX())
        f.write('Cell size y: %f\n' % self.project.cellSizeY())
        # f.write('Map scale: %f\n' % self.project.mapscale())
        # f.write('Cell Area: %f\n' % self.project.areascale())
        if self.project.hasBeenCalculated():
            f.write('R: %f\n' % self.project.R())
            f.write('Dispersal: %f\n' % self.project.dispersal())
            f.write('Flow: %f\n' % self.project.networkFlow())
            f.write('Total Power: %f\n' % self.project.totalPower())
            f.write('Metapopulation Capacity: %f\n' % self.project.metapopCapacity())
            f.write('Total Link Strength: %f\n' % self.project.totalLinkStrength())
        f.close()

    def exportScenarioData(self):
        txttype="TXT (*.txt)"
        scenarioName=self.project.scenario._v_name
        fname=self.project.h5file.filename
        suggested=settingsgui.appsettings.path+"/%s.%s" % (fname,scenarioName)
        filename,fil = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save File',suggested, txttype)
        logging.debug("Exporting to" + filename)
        if filename:
            self.doExportScenarioData(filename)

    def doExportProjectData_old(self,filename):
        logging.info("Creating export file: %s", filename)
        f=open(filename,'w')
        scenarioName=self.project.scenario._v_name
        for i in range(self.project.numberOfScenarios()):
            fstring="%d,%s,%d,%d,%d,%f,%f,%d,%f,%f,%f,%f,%f,%f\n" \
                % (i,scenarioName,self.project.habitatN(),\
                   self.project.rasterSize()[0],self.project.rasterSize()[1],\
                   self.project.totalArea(),self.project.mapscale(),self.project.areascale(),\
                   self.project.R(),self.project.dispersal(),self.project.flow(),\
                   self.project.totalPower(),self.project.metapopCapacity(),\
                   self.project.totalLinkStrength())
            f.write(fstring)
        f.close()

    def doExportProjectData(self,filename):
        logging.info("Creating export file: %s", filename)
        f=open(filename,'w')
        scenarioName=self.project.scenario._v_name
        f.write("N,Scenario,N Cells,EW Raster Size,NS Raster Size,Area,EW Origin,NS Origin,EW Cell Size,NS Cell Size,Dispersal,R,Speed,Time,Resistance to Ext.,Link Strength\n")
        for i in range(self.project.numberOfScenarios()):
            scn=con.getNth(self.project.h5file,i)
            scenarioName=scn._v_name
            fstring="%d,%s,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" \
                % (i,\
                   scn._v_name,\
                   scn.x.shape[0],\
                   scn._v_attrs.map_x_size,\
                   scn._v_attrs.map_y_size,\
                   self.project.totalArea(scn),\
                   scn._v_attrs.map_x_origin,\
                   scn._v_attrs.map_y_origin,\
                   scn._v_attrs.map_x_scale,\
                   scn._v_attrs.map_x_scale,\
                   scn._v_attrs.R,\
                   scn._v_attrs.dispersal,\
                   scn._v_attrs.I0,\
                   1.0/scn._v_attrs.I0,\
                   0.0,\
                   scn._v_attrs.totalLinkStrength)
            f.write(fstring)
        f.close()

    def exportProjectData(self):
        logging.info("export project data")
        txttype="TXT (*.txt)"
        dr=settingsgui.appsettings.path+'/exports/'
        filename=QtGui.QFileDialog.getSaveFileName(self,'Export Project Data',dr,txttype)
        if filename:
            self.doExportProjectData(filename)

    def exportMap(self,a,txt,dtype=gdal.GDT_Float64):
        d=exportgis.ExportGisDialog(self)
        oppath=settingsgui.appsettings.path+'/exports/'
        opfname=oppath+self.project.scenario._v_name+'_'+txt
        d.setValues(opfname,self.project.scenario._v_attrs.habfilename)
        ret=d.exec_()
        if ret:
            logging.info("Exporting map")
            op,cp,driver,mult=d.getValues()
            proj=exportgis.getGeoInfo(cp)
            if np.issubdtype(a.dtype,int):
                mult=int(mult)
            
            if dtype==gdal.GDT_Float64:    
                NODATA=exportgis.NODATA_FLOAT
            else:
                NODATA=exportgis.NODATA_INT

            a=a*mult
            wa=np.where(a)
            b=np.zeros(a.shape).astype(a.dtype)+NODATA
            b[wa]=a[wa]
            a=b
            f=exportgis.createGeoFile(op,driver,a,proj,dtype=dtype)

    def exportVoltageMap(self):
        a=self.project.nodeVoltageA()
        self.exportMap(a,"progress")

    def exportHabitatMap(self):
        a=self.project.habitatMaskUnexpanded()
        self.exportMap(a,"habitat")
        
    def exportSourceMap(self):
        a=self.project.sourceMaskUnexpanded()
        self.exportMap(a,"source")

    def exportSinkMap(self):
        a=self.project.sinkMaskUnexpanded()
        self.exportMap(a,"target")

    def exportDroppedHabitat(self):
        dhab=np.zeros(self.project.rasterSize(),dtype=np.int)
        fil=self.dropFilterDlg
        if not fil:
            box=QtGui.QMessageBox.information(None,'Information','You need to have filtered your dropping results to export this map.',QtGui.QMessageBox.Ok)
            return
        x=self.project.scenario.xnew.read()
        y=self.project.scenario.ynew.read()
        indlist=self.project.scenario.indlist.read()
        N=fil.horizontalSlider.value()
        for i in range(N):
            i1=indlist.size-i-1
            ii=indlist[i1]
            dhab[x[ii],y[ii]]=255
        self.exportMap(dhab,"dropped_habitat",dtype=gdal.GDT_Int32)

    def exportVoltageLayersMap(self):
        a=ecoplot.calcVoltageLayers(self.project)
        b=a*0+exportgis.NODATA_INT
        b[np.where(a)]=a[np.where(a)]
        self.exportMap(b,"isolated_areas",dtype=gdal.GDT_Int32)

    def exportFlowMap(self):
        a=self.project.nodeFlowA()
        self.exportMap(a,"flow")

    def exportDroppedRankMap(self):
        scn=self.project.scenario
        indlist=scn.indlist.read()
        xnew,ynew=scn.xnew.read(),scn.ynew.read()
        xs,ys=scn.x.read(),scn.y.read()
        SZX=np.max(np.array((np.max(xs),np.max(xnew))))
        SZY=np.max(np.array((np.max(ys),np.max(ynew))))
        sh=self.project.nodeVoltageA().shape
        SZX=sh[0]
        SZY=sh[1]
        da=np.zeros((SZX+0,SZY+0)).astype(int)
        da+=exportgis.NODATA_INT
        for i in range(len(indlist)):
            ii=indlist[i]
            da[xnew[ii],ynew[ii]]=i
        self.exportMap(da,"rank",dtype=gdal.GDT_Int32)

    def exportCurrentMap(self):
        logging.info("Export current Map")
        txttype="GDAL (*)"
        scenarioName=self.project.scenario._v_name
        fname=self.project.h5file.filename
        suggested="./%s.%s" % (fname,scenarioName)
        filename,fil = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save File',suggested, txttype)
        if filename:
            im.save(filename+'.tif')

    def clearList(self):
        self.listWidget.clear()

    def updateList(self):
        self.listWidget.clear()
        for i in con.getOrdered(self.project.h5file):
            txt="%d:   %s" % (i._v_attrs.ind,i._v_name)
            self.listWidget.addItem(txt)
        scN=self.project.scenario._v_attrs.ind
        oinds=con.getOrderedInds(self.project.h5file)
        N=oinds.index(scN)
        self.listWidget.setCurrentRow(N)
        
    def selectScenario(self,N):
        ns=con.getOrderedInds(self.project.h5file)
        self.project.scenario=con.getNth(self.project.h5file,N)
        msg="Scenario %s selected" % self.project.scenario._v_name
        self.infoBox()
        self.updateList()
        self.setButtonStates()
        self.showMessage(msg)
        self.showMessage(msg)

    def _guiRMisMatch(self):
        return not self.project.scenario._v_attrs.R==self.rSpinBox.value()
        
    def _guiDispMisMatch(self):
        return not self.project.scenario._v_attrs.dispersal==self.dispersalSpinBox.value()

    def guiMisMatch(self):
        return (self._guiRMisMatch() or self._guiDispMisMatch())
        
    def selectHistory(self):
        if self.guiMisMatch():
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You have changed the kernel parameters without recalculating the conductance!')
            msgBox.addButton(QtGui.QPushButton('Abandon change'), QtGui.QMessageBox.YesRole)
            msgBox.addButton(QtGui.QPushButton('Commit by re-calculating the conductance'), QtGui.QMessageBox.NoRole)
            ret = msgBox.exec_();
            if not ret==0:
                self.calc()
        self.showMessage('Loading scenario.')           
        selected=self.listWidget.currentRow()
        ns=con.getOrderedInds(self.project.h5file)
        N=ns[selected]
        self.selectScenario(N)
#        self.habitatView()
        self.selectView(self.fCurrentView, self.currentTip)
        self.fCurrentView[self.subFig](self.mainCanvas(),self.project)
        msg="Scenario %s selected" % self.project.scenario._v_name
        self.showMessage(msg)
        self.infoBox()
        if not self.droppingDialog is None:
           self.droppingDialog.sync() 
        if not self.dropFilterDlg is None:
            self.dropFilterDlg.sync()

    def deleteScenario(self):
        logging.info("Delete Scenario")
        self.project.deleteScenario()
        self.habitatView()
        self.infoBox()
        self.updateList()
        self.setButtonStates()         

    def duplicateScenario(self):
        text, ok = QtGui.QInputDialog.getText(self, 'New Scenario', 
                                              'Scenario Name')
        if ok:
            scn2=self.project.duplicateScenario(self.project.scenario,str(text))
            self.habitatView()
            self.infoBox()
            self.updateList()

    def renameScenario(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Rename Scenario', 
                                              'Scenario Name')
        if ok:
            self.project.renameScenario(str(text))
            self.infoBox()
            self.updateList()


    def openHabitat(self,fname,mincut=0):
        rasterName=ntpath.basename(fname)
        scn=os.path.splitext(rasterName)[0]
        root,ext=ntpath.splitext(fname)        
        if self.project.h5file.root.scenarios.__contains__(scn):
            text, ok = QtGui.QInputDialog.getText(self, 'Duplicate scenario', 'Enter scenario name:')
            if ok:
                rasterName=ntpath.basename(str(text))
                scn=os.path.splitext(rasterName)[0]
            else:
                return

        self.project.loadInputGeo(name=fname,scn_name=scn,mincut=mincut)
        if self.project.scenario._v_attrs.map_x_scale == 1.0:
            text, ok = QtGui.QInputDialog.getText(self, 'Map Scale', 
                                                  'Enter map cell size',text='1000.0')
            sc=float(text)
            if ok:
                self.project.scenario._v_attrs.map_x_scale=sc
                self.project.scenario._v_attrs.map_y_scale=sc


    def guiOpenHabitat1(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 
            "Open Habitat Layer [GDAL]", ".", "[GDAL] Raster (*)")
        if file:
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            if os.path.isfile(fname):
                self.openHabitat(fname)
                self.setButtonStates()
                self.infoBox()

    def guiOpenHabitat_orig(self):
        dlg=QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.AnyFile);
        e=dlg.exec_()
        if e:
            file=dlg.selectedFiles()[0]
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            if os.path.isfile(fname):
                self.openHabitat(fname)
        self.setButtonStates()
        self.infoBox()

    # Note case -3 requires no alteration (proportion)
    def normaliseHabitat_(self,id):
        if id==-2:
            logging.info("Percentage. Divide by 100")
            a=self.project.scenario.ap.read()
            logging.info("Max area",np.max(a))
            self.project.scenario.ap[:]=a/100.0
        if id==-4:
            logging.info("Area. Divide by cell area (km)")
            ca=self.project.cellArea()
            logging.info("Cell area:",ca)
            a=self.project.scenario.ap.read()
            logging.info("Max area",np.max(a))
            newa=a/ca
            self.project.scenario.ap[:]=newa

        if id==-5:
            logging.info("Area. Divide by cell area (km^2)")
            ca=self.project.cellArea()/1e6
            logging.info("Cell area:",ca)
            a=self.project.scenario.ap.read()
            logging.info("Max area",np.max(a))
            newa=a/ca
            self.project.scenario.ap[:]=newa

        if id==-6:
            logging.info("Load as mask")
            self.project.scenario.ap[:]=1.0

    def guiOpenHabitat(self):
        dlg=openhabitat.OpenHabitatDialog()
        e=dlg.exec_()
        if e:
            file,id,mincut=dlg.getValues()
            logging.info("Filename is:",file)
            logging.info("ID:",id)
            fileinfo = QtCore.QFileInfo(file)
            fname = str(fileinfo.canonicalFilePath())
            if os.path.isfile(fname):
                self.openHabitat(fname,mincut)
                self.normaliseHabitat_(id)
                self.habitatView()
                self.updateList()
                self.setButtonStates()
                self.infoBox()
            
    def guiOpenHabitat_fiddle(self):
        dlg=openhabitat.OpenHabitatDialog()
        e=dlg.exec_()
        if e:
            x,y,a,gt=dlg.getValues()


    def genSourceSink(self,ssdConf):
        ditch,sstype,width,ch=ssdConf
        rsx,rsy=self.project.habitatSize()
        rsx-=0
        rsy-=0
        if sstype==-3:
            sx=(np.arange(rsx*width)%rsx).astype(np.int_)
            sy=(np.arange(rsx*width)/rsx).astype(np.int_)
            tx=(np.arange(rsx*width)%rsx).astype(np.int_)
            ty=((np.arange(rsx*width)/rsx)+rsy-width).astype(np.int_)
        if sstype==-2:
            sx=(np.arange(rsx*width)%rsx).astype(np.int_)
            ty=(np.arange(rsx*width)/rsx).astype(np.int_)
            tx=(np.arange(rsx*width)%rsx).astype(np.int_)
            sy=((np.arange(rsx*width)/rsx)+rsy-width).astype(np.int_)
        if sstype==-4:
            sy=(np.arange(rsy*width)%rsy).astype(np.int_)
            sx=(np.arange(rsy*width)/rsy).astype(np.int_)
            ty=(np.arange(rsy*width)%rsy).astype(np.int_)
            tx=((np.arange(rsy*width)/rsy)+rsx-width).astype(np.int_)
        if sstype==-5:
            sy=(np.arange(rsy*width)%rsy).astype(np.int_)
            tx=(np.arange(rsy*width)/rsy).astype(np.int_)
            ty=(np.arange(rsy*width)%rsy).astype(np.int_)
            sx=((np.arange(rsy*width)/rsy)+rsx-width).astype(np.int_)
        # Checkbox ticked for expand area.
        if ch:
            if sstype==-3: 
                sy-=width
                ty+=width
            if sstype==-2: 
                sy+=width
                ty-=width
            if sstype==-4: 
                sx-=width
                tx+=width
            if sstype==-5: 
                sx+=width
                tx-=width
        self.project.addSrcSink(sx,sy,tx,ty)
        self.project.calcCombinedHabitat()

    def loadSourceSink(self,ssdConf):
        ditch,sourceName,srcval,snkval=ssdConf
        self.project.loadSourceSink(str(sourceName),srcval,snkval)

    def clearST(self,w):
        if w==-2:
            logging.info("clearing source")
            self.clearSource()
        if w==-3:
            self.clearTarget()
            logging.info("cleaqring target")
        if w==-4:
            self.clearSourceTarget()
            logging.info("clearing both")
            
    def assignSourceSink(self):
        logging.info("Assigning source and target.")
        ssd=sourcesinkgui.SourceSinkDialog(self)
        rtn=ssd.exec_()
        if rtn==1:
            self.showMessage("I might take a few moments to check for duplicates between the source / target and habitat.")
            ssdConf=ssd.getValues()
            if ssdConf[0]==0: # Using files
                self.loadSourceSink(ssdConf)
                self.habitatView()
                self.showMessage("Source and target loaded from files.")
            if ssdConf[0]==1: # Using Edges
                self.genSourceSink(ssdConf)
                self.habitatView()
                self.showMessage("Source and target generated.")
            if ssdConf[0]==2:
                self.clearST(ssdConf[1])
                self.habitatView()
                self.showMessage("Source and target cleared.")
                
            self.setButtonStates()


    def readKParams(self):
        self.project.scenario._v_attrs.R=self.rSpinBox.value()
        self.project.scenario._v_attrs.dispersal=self.dispersalSpinBox.value()

    def docalc(self):
        self.project.calcDists()
        self.readKParams()           
        self.project.calcIpvIn()
        logging.info("ipv_in calculated.")
        gc.collect()
        self.dlg.setState(1)
        self.project.calcIpvOut()
        logging.info("ipv_out calculated.")
        gc.collect()
        self.dlg.setState(2)
        self.project.calcIpvFree()
        logging.info("ipv_free calculated.")
        gc.collect()
        self.dlg.setState(3)
        self.project.calcCond()
        logging.info("Voltages calculated.")
        gc.collect()
        logging.info("Garbage collected")
        self.dlg.setState(4)
        self.voltageView()
        self.infoBox()
        self.setButtonStates()
        self.showMessage('Finished Calculating Ready.')
        self.dlg.hide()
        logging.info("End of calc")

    def calc(self):
        # The next line never shows. use thread?
        # Only on OS X
        if self.project.canCalculateScenario():
            self.dlg=calcdialog.CalculatingDialog(self)
            self.dlg.show()
            self.dlg.setState(0)
            self.showMessage('Please wait. Calculating...')
            self.docalc()
            metrics.clearMetrics(self.project.scenario)
            self.setButtonStates()
            self.project.scVLPclear()

    def calcPower(self):
        self.project.calcPower()
        self.powerView()

    def calcAll(self):
        N=self.project.numberOfScenarios()
        for i in range(N):
            self.selectScenario(i)
            if self.project.canCalculateScenario():
                self.calc()
            else:
                reply = QtGui.QMessageBox.question(self, 'Calculate All',\
                    "Cannot calculate scenario. Do you want to continue?",\
                    QtGui.QMessageBox.Yes | \
                    QtGui.QMessageBox.No, \
                    QtGui.QMessageBox.No)
                if reply==QtGui.QMessageBox.No:
                    break

    def calculateMetrics(self):
        logging.info("Calculate Metrics")
        self.showMessage('Please wait. Calculating eigenfunctions...')
        metrics.calcMetrics(self.project.h5file,self.project.scenario)
        self.setButtonStates()
        self.populationView()
        self.showMessage('Finished Calculating. Ready.')
        self.infoBox()


    def subFig0Clicked(self,event):
        self.fCurrentView[0](self.mainCanvas(),self.project)
        self.subFig=0

    def subFig1Clicked(self,event):
        self.fCurrentView[1](self.mainCanvas(),self.project)
        self.subFig=1

    def subFig2Clicked(self,event):
        self.fCurrentView[2](self.mainCanvas(),self.project)
        self.subFig=2

    def subFig3Clicked(self,event):
        self.fCurrentView[3](self.mainCanvas(),self.project)
        self.subFig=3

    def subFig4Clicked(self,event):
        self.fCurrentView[4](self.mainCanvas(),self.project)

        
    def mainCanvas(self):
        return self.mainfig.canvas

    def mainAxes(self):
        return self.mainfig.canvas.ax

    def showSubplots(self):
        self.dockWidget_2.show()
    
    def hideSubplots(self):
        self.dockWidget_2.hide()
    
    def showHistory(self):
        self.dockWidget.show()

    def hideHistory(self):
        self.dockWidget.hide()

    def showNavbar(self):
        self.mpl_toolbar.show()

    def hideNavbar(self):
        self.mpl_toolbar.hide()
    
    def selectView(self,view,tips):
        self.fCurrentView=view
        self.currentTip=tips
        for i in range(4):
            self.fCurrentView[i](self.fig[i].canvas,self.project)
            self.fig[i].setToolTip(self.currentTip[i])
        self.fCurrentView[0](self.mainCanvas(),self.project)

    def nullView(self):
        self.selectView(self.fNullView,self.nullTips)
#        self.showMessage('No habitat loaded.')
        self.subFig=0
        
    def habitatView(self):
        self.selectView(self.fHabView,self.habTips)
        self.showMessage('Habitat view.')
        self.subFig=0

    def voltageView(self):
        self.selectView(self.fVoltView,self.voltTips)
        self.showMessage('Voltage view.')           
        self.subFig=0
        
    def comparisonView(self):
        self.selectView(self.fComparisonView,self.comparisonTips)
        self.showMessage('Comparison view.')           
        self.subFig=0
        
    def powerView(self):
#        if not self.project.powerMap Calculated():
#            self.project.calcPowerMap()
#        if not self.project.scenario.__contains__("edgePower"):
#            con.calcPower(self.project.h5file, self.project.scenario)
        self.selectView(self.fPowerView,self.powerTips)
        self.showMessage('Power view.')           
        self.subFig=0

    def droppingView(self):
        self.selectView(self.fDroppingView,self.droppingTips)
        self.showMessage('View backwards optimisation plots.')           
        self.subFig=0

    def populationView(self):
        logging.info("Population View")
        self.selectView(self.fPopulationView,self.populationTips)
        self.showMessage('Population view.')           
        self.subFig=0        
        
    def clearInfoBox(self):
        self.lineEdit_1.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')

    def infoBoxClr(self):
        self.dispersalSpinBox.setValue(0)
        self.rSpinBox.setValue(0)
        self.nCellsSpinBox.setValue(0)
        self.habitatAreaSpinBox.setValue(0)
        self.hGridSizeSpinBox.setValue(0)
        self.vGridSizeSpinBox.setValue(0)
        self.originXSpinBox.setValue(0)
        self.originYSpinBox.setValue(0)
        self.cellSizeXSpinBox.setValue(0)
        self.cellSizeYSpinBox.setValue(0)
        self.lineEdit_1.setText(QtCore.QString().setNum(0))
        self.lineEdit_2.setText(QtCore.QString().setNum(0))
        self.lineEdit_3.setText(QtCore.QString().setNum(0))
        self.lineEdit_4.setText(QtCore.QString().setNum(0))

    def infoBox(self):
        self.dispersalSpinBox.setValue(self.project.dispersal())
        self.rSpinBox.setValue(self.project.R())
        self.nCellsSpinBox.setValue(self.project.habitatN())
        self.habitatAreaSpinBox.setValue(self.project.totalArea())
        self.hGridSizeSpinBox.setValue(self.project.rasterSize()[0])
        self.vGridSizeSpinBox.setValue(self.project.rasterSize()[1])
        self.originXSpinBox.setValue(self.project.originX())
        self.originYSpinBox.setValue(self.project.originY())
        self.cellSizeXSpinBox.setValue(self.project.cellSizeX())
        self.cellSizeYSpinBox.setValue(self.project.cellSizeY())
        self.lineEdit_1.setText(QtCore.QString().setNum(self.project.networkFlow()))
        self.lineEdit_2.setText(QtCore.QString().setNum(1.0/self.project.networkFlow()))
        self.lineEdit_3.setText(QtCore.QString().setNum(self.project.metapopCapacity()))
        self.lineEdit_4.setText(QtCore.QString().setNum(self.project.totalLinkStrength()))

    def switchAllOff(self,state=False):
        self.actionView_Voltage.setEnabled(state)
        self.actionView_Power.setEnabled(state)
        self.actionView_Map.setEnabled(state)
        self.actionDelete_From_Scenarios.setEnabled(state)
        self.actionDuplicate_Scenario.setEnabled(state)
        self.actionAdd_Source_Sink.setEnabled(state)
        self.actionSave_Image.setEnabled(state)
        self.actionPrint.setEnabled(state)
        self.actionCalculate_All.setEnabled(state)
        self.actionConductance.setEnabled(state)
        self.actionComparison_View.setEnabled(state)
        self.actionView_Population.setEnabled(state)
        self.actionCalculate_Metrics.setEnabled(state)
        self.actionForward_Optimise.setEnabled(state)
        self.actionBackwards_Improvement.setEnabled(state)
        self.actionRename_Scenario.setEnabled(state)
        self.actionOpen_Habitat.setEnabled(state)
        self.actionClose.setEnabled(state)
        self.actionNew.setEnabled(state)
        self.actionOpen.setEnabled(state)
        self.actionDropping_Filter.setEnabled(state)
        self.actionDropping_View.setEnabled(state)
        self.actionCalc_Power.setEnabled(state)

    def setButtonStates(self):
        self.switchAllOff()

        if self.project==[]:
            logging.info("No project")
            self.actionNew.setEnabled(True)
            self.actionOpen.setEnabled(True)
        else:
            logging.info("Has project")
            self.actionClose.setEnabled(True)
            self.actionOpen_Habitat.setEnabled(True)

            if self.project.hasScenario():
                logging.info("Has Scenario")
                self.actionView_Map.setEnabled(True)
                self.actionAdd_Source_Sink.setEnabled(True)
                self.actionDuplicate_Scenario.setEnabled(True)        
                self.actionRename_Scenario.setEnabled(True)
                self.actionDelete_From_Scenarios.setEnabled(True)
#                self.actionForward_Optimise.setEnabled(True)

                if self.project.canCalculateScenario():
                    logging.info("Can Calculate")
                    self.actionConductance.setEnabled(True)
                    logging.info("actionConductance Enabled")
                    
                    if self.project.hasBeenCalculated():
                        logging.info("Has been calculated")
                        self.actionView_Voltage.setEnabled(True)
                        self.actionView_Power.setEnabled(True)
                        self.actionComparison_View.setEnabled(True)
                        self.actionCalculate_Metrics.setEnabled(True)
                        self.actionBackwards_Improvement.setEnabled(True)
                        self.actionView_Population.setEnabled(True)
                        self.actionCalc_Power.setEnabled(True)
#                        self.actionForward_Optimise.setEnabled(True)
                        if self.project.scenario.__contains__("indlist"):
                            logging.info("Has Dropping")
                            self.actionDropping_Filter.setEnabled(True)
                            self.actionDropping_View.setEnabled(True)



    def setButtonStates_old(self):
        self.switchAllOff()
        if not self.project==[]:
            if not self.project.h5file==[]:
                self.setButtonsCalc(False)
                if self.project.hasScenario():
                    logging.debug("Has scenario")
                    self.setButtonsWithScenario()
                    if self.project.canCalculateScenario():
                        logging.debug("Can Calculate")
                        self.setButtonsCalc()

        self.actionDropping_Filter.setEnabled(False)
        if self.project.scenario.__contains__("indlist"):
            self.actionDropping_Filter.setEnabled(True)

    def closeApp(self):
        self.close()


        
def initDirectories():
    hd=os.path.expanduser('~')
    cond=hd+'/condatis'
    maps=cond+'/maps'
    projects=cond+'/projects'
    exports=cond+'/exports'

    # Make all the directories if they don't exist.
    for i in [cond,maps,projects,exports]:
        makeIfNot(i)    
    
if __name__ == "__main__":
    import sys
    logging.root.setLevel(logging.DEBUG)
#    logging.basicConfig(filename='condatis.log')

    initDirectories()
    
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)==2:
        MainWindow = MyMain(projectfile=sys.argv[1])
    else:
        MainWindow = MyMain()

    sys.exit(app.exec_())

