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

import os, sys, json, subprocess
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabel("Project")
        self.setCentralWidget(self.treeWidget)

        self.createActions()
        self.createMenus()

        self.item = None

        style = self.treeWidget.style()

        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()
        self.contentsIcon = QtGui.QIcon()
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_FileIcon))
        self.contentsIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_FileDialogContentsView))

        self.connect (self.treeWidget, QtCore.SIGNAL ("itemDoubleClicked(QTreeWidgetItem*, int)"), self.editChild)

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("Stellar")
        self.resize(300, 320)

    def open(self):
        self.statusBar().showMessage("Opening project...")
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "Open Project File", QtCore.QDir.currentPath(),
                "Project Files (*.JSON)")
        #fileName=os.path.join("example","example.JSON")

        if not fileName:
            return
        self.treeWidget.clear()
        
        decoded_data=json.loads(open(fileName,'r').read())
        self.format_main_response(decoded_data)

        self.statusBar().showMessage("File loaded", 2000)

    def format_main_response(self, json_string):
        #Start reading the index file
        for key, value in json_string.iteritems():
            if key=='Classes' or key=='Functions':
                self.addChild(key, self.folderIcon, False)
                
                for val in value:
                    self.addChild(val, self.bookmarkIcon, True)

                self.item = self.item.parent() #This line closes the key child

        #Adding shortcuts to settings
        self.addChild("Constants", self.contentsIcon, True)
        self.addChild("Game Information", self.contentsIcon, True)
        self.addChild("Global Game Settings", self.contentsIcon, True)

    def addChild(self, text, icon, closed):
        if self.item:
            childItem = QtGui.QTreeWidgetItem(self.item)
        else:
            childItem = QtGui.QTreeWidgetItem(self.treeWidget)
        childItem.setData(0, QtCore.Qt.UserRole, text)
        self.item = childItem
        #self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
        self.item.setIcon(0, icon)
        self.item.setText(0, text)
        self.treeWidget.setItemExpanded(self.item, False)
        if closed:
            self.item = self.item.parent()


    def editChild(self):
        f=self.treeWidget.currentItem().text(0)
        parent=self.treeWidget.currentItem().parent().text(0)
        if parent=="Functions":
            ftype=".py"
        elif parent=="Classes":
            ftype=".json"
        fileName = os.path.join("example", str(self.treeWidget.currentItem().parent().text(0)) , str(self.treeWidget.currentItem().text(0))+ftype)
        print fileName

    def saveAs(self):
        pass

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveAsAct = QtGui.QAction("&Save As...", self, shortcut="Ctrl+S",
                triggered=self.saveAs)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())