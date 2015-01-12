# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import aboutui
import string
import numpy
import scipy
import matplotlib
import osgeo
import tables
from PIL import Image
import version

VERSION=version.version

aboutHtml = """
<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=windows-1252" http-equiv="content-type">
    <title>Condatis about box</title>
  </head>
  <body>
    <h3> Condatis; software to assist with the planning of habitat restoration</h3>
    <h4><a target="_blank" href="http://www.condatis.org.uk">www.condatis.org.uk</a></h4>

<p>
Version %s
</p>

    Copyright &#169; 2015 D.W. Wallis and J.A. Hodgson<br>
    <br>
    The latest information about Condatis can be found at www.condatis.org.uk,
    including links to the source distribution, preferred citations, and contact
    details for the copyright holders.<br>
    <br>
    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License (GPL) as published by the
    Free Software Foundation, <a target="_blank" href="http://www.gnu.org/licenses/gpl-3.0.html">version
      3 of the license</a>, and the additional term below. <br>
    <br>
    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.<br>
    <br>
    The full text of the license is included with the program, in the file
    'Condatis_License.html'<br>
    <h3>Additional term under GNU GPL version 3 section 7. </h3>
    A1) If you convey a modified version of this work:<br>
    <ul>
      <li>(i) you should delete the text that appears in the Acknowledgements
        tab of the About box in the Condatis user interface.</li>
      <li>(ii) a comment at the head of any file containing the source code
        derived from this covered work should read: Part of this work is a
        modified version of the work Condatis v.[version number] Copyright &#169;
        [year]&nbsp; D.W. Wallis and J.A. Hodgson.&nbsp; Our modification was
        permitted by the GNU General Public License v.3. Instructions for
        obtaining the original version of Condatis can be found at
        www.condatis.org.uk. Any modified or verbatim copies of our work must
        preserve this notice. Where text in square brackets should be replaced
        by the appropriate numbers.</li>
      <li>(iii) if your modified work has a user interface, the user interface
        should prominently display the notice: Part of this work is a modified
        version of the work Condatis v.[version number] Copyright &#169; [year]&nbsp;
        D.W. Wallis and J.A. Hodgson.&nbsp; See www.condatis.org.uk. Where text
        in square brackets should be replaced by the appropriate numbers.</li>
    </ul>
  </body>
</html>
""" % version.version

ackHtml = """
<html>
    <head>
    </head>
    <body>
    <h3>Acknowledgements</h3> 
<p>
The authors would like to acknowledge a large number of people who made suggestions for the software specification of Condatis, or recommendations to improve user-friendliness, specifically Aidan Lonergan, Andrew Suggitt, Atte Moilanen, Chloe Bellamy, Duncan Blake, Geoffrey Heard, James Latham, Jamie Robins, Jonathan Rothwell, Jonathan Winn, Kevin Watts, Nicholas Macgregor, Nik Bruce, Paul Evans, Phil Baarda, Sarah Scriven, Sarah Taylor, Sheila George, Steve Palmer, Tim Graham, Tom Squires, and Vicky Kindemba. The authors also acknowledge funding from the UK Natural Environment Research Council grant number NE/L002787/1.
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
    <h3>Condatis, Version %s</h3> 
    """ % VERSION
    html+="<h4>Built using</h4>"

    html+="Numpy: %s<br>" % numpy.__version__ 
    html+="Scipy: %s<br>" % scipy.__version__ 
    html+="Matplotlib: %s<br>" % matplotlib.__version__ 
    html+="PyQt4: %s<br>" % QtCore.QT_VERSION_STR
    html+="osgeo: %s<br>" % osgeo.__version__
    html+="Pil: %s<br>" % Image.VERSION
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
