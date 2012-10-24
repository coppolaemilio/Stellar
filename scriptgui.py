#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Emilio Coppola
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


import sys
import pygame.mixer
import shutil
import os
import syntax
from PyQt4 import QtGui, QtCore
from autocomplete import CompletionTextEdit

class ScriptGUI(QtGui.QWidget):
  
    def __init__(self, main, FileName, dirname):
        super(ScriptGUI, self).__init__(main)
        
        self.main = main
        self.dirname = dirname
        self.FileName = FileName
        self.initUI()
        

    def initUI(self):
        
        #Groupbox Container-----------------------------------
        self.ContainerBox = QtGui.QGroupBox(self.main)
        self.ContainerBox.setObjectName("groupBox")
        self.ContainerBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.ContainerBox.setGeometry(QtCore.QRect(0,0,350,400))
        self.ContainerBox.setMinimumSize(350,400)
		
        self.ContainerGrid = QtGui.QGridLayout(self.ContainerBox)
		
        self.LblName = QtGui.QLabel('Name:')
        self.nameEdit = QtGui.QLineEdit(self.FileName)
		
        saveAction = QtGui.QAction(QtGui.QIcon('Data/tick.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveScript)
		
        exportAction = QtGui.QAction(QtGui.QIcon('Data/save.png'), 'Export', self)
        exportAction.triggered.connect(self.exportScript)
		
        importAction = QtGui.QAction(QtGui.QIcon('Data/folder.png'), 'Open', self)
        importAction.triggered.connect(self.openScript)

        undoAction = QtGui.QAction(QtGui.QIcon('Data/undo.png'), 'Undo', self)
        redoAction = QtGui.QAction(QtGui.QIcon('Data/redo.png'), 'Redo', self)
		
        self.toolbar = QtGui.QToolBar('Script Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(exportAction)		
        self.toolbar.addAction(importAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.LblName)
        self.toolbar.addWidget(self.nameEdit)
		
		
		
        editor= self.textEdit = CompletionTextEdit()
        highlight = syntax.PythonHighlighter(editor.document())
        self.textEdit.zoomIn(+4)
        self.texEdit=CompletionTextEdit()
		
        self.ContainerGrid.setSpacing(0)
        self.ContainerGrid.addWidget(editor, 1, 0,1,15)
        self.ContainerGrid.addWidget(self.toolbar, 0, 0)
		
        self.startopen()

	
    def exportScript(self):
        print str(self.dirname)+ ("/Scripts/") + str(self.FileName)+".py"
        fname = self.dirname + "/Scripts/" + self.FileName + ".py"
        f = open(fname, 'w')
        with f:    
            data = self.textEdit.toPlainText()
            f.write(data)
            f.close()

    def saveScript(self):
        print str(self.dirname)+ ("/Scripts/") + str(self.FileName)+".py"
        fname = self.dirname + "/Scripts/" + self.FileName + ".py"
        f = open(fname, 'w')
        with f:    
            data = self.textEdit.toPlainText()
            f.write(data)
            f.close()
			
    def startopen(self):

        fname = self.dirname + "/Scripts/" + self.FileName + ".py"
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data)
			
    def openScript(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data)

    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
