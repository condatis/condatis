from PyQt4 import QtCore, QtGui
import aboutui
import string
import numpy
import scipy
import matplotlib
import osgeo
import tables

REVISION="$Rev: 18 $"
sp=string.split(REVISION)
VERSION="0.4."+sp[1]

aboutHtml = """
<html>
    <head>
    </head>
    <body>
    <h1>Condatis</h1>
    <p>
    Condatis is Copyright The University of Liverpool (2014), Version %s
    </p>
    <p>
This is a Beta version of software issued only to members of the Condatis project for testing.\nPlease do redistribute this software. If you are interested in obtaining a copy then please contact either:\n\nJenny Hodgson - jenny.hodgson@liverpool.ac.uk\nDavid Wallis - d.wallis@liverpool.ac.uk.
    </p>
    </body>
</html>
""" % VERSION

ackHtml = """
<html>
    <head>
    </head>
    <body>
    <h1>We would like to thank</h1>
    <p>
    Joe Bloggs, Bob Smith,....
    </p>
    </body>
</html>
"""

def buildHtml():
    html="""
    <html>
    <head>
    </head>
    <body>
    <h1>Condatis, Version %s</h1> 
    """ % VERSION
    html+="<h2>Built using</h2>"

    html+="Numpy: %s<br>" % numpy.__version__ 
    html+="Scipy: %s<br>" % scipy.__version__ 
    html+="Matplotlib: %s<br>" % matplotlib.__version__ 
    html+="PyQt4: ??<br>"
    html+="osgeo: %s<br>" % osgeo.__version__
    html+="Pil: ??<br>"
    html+="tables: %s<br>" % tables.__version__
    html+="""
    </body>
    </html>
    """
    return html


class AboutDialog(QtGui.QDialog,aboutui.Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.aboutBrowser.setHtml(aboutHtml)
        self.ackBrowser.setHtml(ackHtml)
        self.buildBrowser.setHtml(buildHtml())
        self.closeButton.clicked.connect(self.close)
