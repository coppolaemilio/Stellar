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
import xml.etree.ElementTree as ET
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui

sys.path.append("tools")
import fonteditor
import constantspanel
import stj

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fname = ""
        self.dirname = ""

        self.qmdiarea = QtGui.QMdiArea()
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabel("Project")

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter.addWidget(self.treeWidget)
        self.splitter.addWidget(self.qmdiarea)
        self.setCentralWidget(self.splitter)

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
        self.resize(640, 480)

    def open(self):
        self.statusBar().showMessage("Opening project...")
<<<<<<< HEAD
        #self.fname = QtGui.QFileDialog.getOpenFileName(self,
        #        "Open Project File", QtCore.QDir.currentPath(),
        #        "Project Files (*.JSON)")
        self.fname = os.path.join("Example","Example.json")
=======
        self.fname = QtGui.QFileDialog.getOpenFileName(self,
                "Open Project File", QtCore.QDir.currentPath(),
                "Project Files (*.JSON *.gmx)")
        #self.fname = os.path.join("Example","Example.JSON")
>>>>>>> Added GM:Studio import

        if not self.fname:
            return
        self.treeWidget.clear()

        if ".gmx" in self.fname:
            self.importgmxproject(self.fname)
        else:
            decoded_data = json.loads(open(self.fname,'r').read())
            self.format_main_response(decoded_data)

        self.statusBar().showMessage("File loaded", 2000)

    def format_main_response(self, json_string):
        #Start reading the index file
        for key, value in json_string.iteritems():
            if key=='Classes' or key=='Functions' or key =='Fonts':
                self.addChild(key, self.folderIcon, False)
                
                for val in value:
                    self.addChild(val, self.bookmarkIcon, True)

                self.item = self.item.parent() #This line closes the key child

        #Adding shortcuts to settings
        self.addChild("Constants", self.contentsIcon, True)
        self.addChild("Game Information", self.contentsIcon, True)
        self.addChild("Global Game Settings", self.contentsIcon, True)

    def importgmxproject(self, file):
        root = ET.parse(file).getroot()
        for child in root:
            for dr in ["scripts", "objects", "rooms"]:
                if child.tag==dr:
                    self.addChild(child.tag, self.folderIcon, False)
                    self.scan_sub_xml(child,child.tag)
                    self.item = self.item.parent() #This line closes the key child
        self.addChild("Constants", self.contentsIcon, True)
        self.addChild("Game Information", self.contentsIcon, True)
        self.addChild("Global Game Settings", self.contentsIcon, True)

    def scan_sub_xml(self, key, name):
        child = key
        for key in key.findall(name[:-1]):
            self.addChild(key.text.replace(name+"\\", ""), self.bookmarkIcon, True)
        for key in child.findall(name):
            val = key.get('name')
            self.addChild(val, self.folderIcon, False)
            self.scan_sub_xml(key,name)
            self.item = self.item.parent() #This line closes the key child

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
        if f=="Constants":
            constantsdialog = constantspanel.ConstantsPanel(self, self)
            return
        parent=self.treeWidget.currentItem().parent().text(0)
        target=str(self.treeWidget.currentItem().text(0))
        if parent=="Functions":
            ftype=".py"
        elif parent=="Classes":
            ftype=".json"
        elif parent=="Sprites":
            ftype=".png"
        elif parent=="Sound":
            ftype=".ogg"
        elif parent=="Fonts":
            fontdialog = fonteditor.FontEditor(self, self, target)
            fontdialog.show()
            return

        fileName = os.path.join("example", str(self.treeWidget.currentItem().parent().text(0)) , target + ftype)
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
