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
# Python Qt4 bindings for GUI objects
#from PyQt4 import QtGui
from PyQt4 import QtCore, QtGui

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg \
import FigureCanvasQTAgg as FigureCanvas
# Matplotlib Figure object
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
        QtGui.QSizePolicy.Expanding,
        QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)

class MplSubCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""

    def onclick(self,event):
            print "Matplotlib canvas mouse click"

    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
        QtGui.QSizePolicy.Expanding,
        QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)
#        self.mpl_connect('button_press_event', self.onclick)
        

    
class MplWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()

        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus )
        self.canvas.setFocus()
        
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
        # add mpl widget to vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to th vertical box
        self.setLayout(self.vbl)

class MplSubWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplSubCanvas()
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
        # add mpl widget to vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to th vertical box
        self.setLayout(self.vbl)

    def mousePressEvent(self,event):
        print "Matplotlib widget mouse click"
#        super(Widget, self).mousePressEvent(event)
