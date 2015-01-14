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
from PyQt4 import QtCore, QtGui
import calculatingui


class CalculatingDialog(QtGui.QDialog,calculatingui.Ui_CalculatingDialog):
    def __init__(self,parent=None,pcnt=[10,20,50,75,100]):
        QtGui.QDialog.__init__(self,parent),
        self.setupUi(self)
        self.stop=False
        self.percentages=pcnt

        # QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), 
        #                        self.cancel)

        self.strings=["Generating input vector","Generating output vector", "Generating free matrix", "Solving equations"]

        # for i in range(len(self.strings)):
        #     self.listWidget.addItem(self.strings[i])

    def setState(self,st):
        self.progressBar.setValue(self.percentages[st])
        QtGui.QApplication.processEvents()

    # def setStateFull(self,st):
    #     self.progressBar.setValue(st)
    #     self.listWidget.clear()
    #     print "Setting state: %d" % st
    #     for i in range(len(self.strings)):
    #         str=self.strings[i]
    #         if i <= st:
    #             str+=" - Completed"
    #         self.listWidget.addItem(str)
    #     QtGui.QApplication.processEvents()
    
    def cancel(self):
        self.stop=True
