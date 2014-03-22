#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2014 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui, QtWebKit
import os, sys
from PyQt4.QtGui import QFont

if sys.version_info.major == 2:
    str = unicode    

class DocReader(QtGui.QDialog):
    def __init__(self, main):
        super(DocReader, self).__init__(main)
        self.main = main

        if os.path.exists(os.path.join('..','images')):
        	img_path=os.path.join('..','images')
        else:
        	img_path=os.path.join('images')

        self.toolbar = QtGui.QToolBar('Documentation Toolbar')


        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)

        self.webkit = QtWebKit.QWebView()

        self.ContainerGrid.addWidget(self.toolbar)
        self.ContainerGrid.addWidget(self.webkit)

        self.setLayout(self.ContainerGrid)

        url = "docs/index.html"
        self.webkit.load(QtCore.QUrl(url))
        self.webkit.show()

class Editor(QtGui.QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        target="none"
        pathtofile="stellar.png"

        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin(0)

        self.docreader = DocReader(self, target, pathtofile)

        self.showlayout.addWidget(self.docreader)
        self.ShowFrame.setLayout(self.showlayout)

        self.setCentralWidget(self.ShowFrame)
        self.setWindowTitle("Stellar - DocReader")
        self.resize(640, 480)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = Editor()
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())