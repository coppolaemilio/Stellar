#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
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

from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore

import os


class RoomGUI(QtGui.QWidget):
    def __init__(self, main, dirname):
        super(RoomGUI, self).__init__()
        self.main = main
        self.dirname = dirname
        self.initUI()
        

    def initUI(self):
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)

        #TOOLBAR
        self.LblName = QtGui.QLabel('Name:')
        self.nameEdit = QtGui.QLineEdit()
        #self.nameEdit.textChanged[str].connect(self.onChanged)
		
        saveAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'tick.png')), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        #saveAction.triggered.connect(self.saveScript)
		
        exportAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'save.png')), 'Export', self)
        #exportAction.triggered.connect(self.exportScript)
		
        importAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'folder.png')), 'Open', self)
        #importAction.triggered.connect(self.openScript)

        self.undoAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'undo.png')), 'Undo', self)
        #self.undoAction.triggered.connect(self.undo)
        
        self.redoAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'redo.png')), 'Redo', self)
        #self.redoAction.triggered.connect(self.redo)
        
        self.whitespacevisAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'font.png')), 'White Space', self)
        #self.whitespacevisAction.triggered.connect(self.whitespace)
        self.visible= False
		
        self.toolbar = QtGui.QToolBar('Script Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(exportAction)
        self.toolbar.addAction(importAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.whitespacevisAction)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.LblName)
        self.toolbar.addWidget(self.nameEdit)
        #/TOOLBAR

        
        self.FirstWidget = QtGui.QTextEdit()
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)

        self.splitterwidg = QtGui.QWidget()
        self.objectsplitter = QtGui.QHBoxLayout()
        self.objectsplitter.setMargin (0)
        self.objectsplitter.addWidget(self.FirstWidget)
        self.objectsplitter.addWidget(self.scrollArea)
        self.splitterwidg.setLayout(self.objectsplitter)

        
        self.ContainerGrid.addWidget(self.toolbar)
        self.ContainerGrid.addWidget(self.splitterwidg)
        self.setLayout(self.ContainerGrid)
