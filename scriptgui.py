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
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
import os
import shutil
import syntax

import pygame.mixer
from PyQt4 import QtGui, QtCore

from autocomplete import CompletionTextEdit


class ScriptGUI(QtGui.QWidget):
  
    def __init__(self, main, FileName, dirname, parent):
        super(ScriptGUI, self).__init__(main)
        
        self.main = main
        self.parent = parent
        self.dirname = dirname
        self.FileName = FileName
        self.initUI()

    def initUI(self):
        self.ContainerGrid = QtGui.QGridLayout(self.main)
		
        self.LblName = QtGui.QLabel('Name:')
        self.nameEdit = QtGui.QLineEdit(self.FileName)
        self.nameEdit.textChanged[str].connect(self.onChanged)
		
        saveAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'tick.png')), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveScript)
		
        exportAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'save.png')), 'Export', self)
        exportAction.triggered.connect(self.exportScript)
		
        importAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'folder.png')), 'Open', self)
        importAction.triggered.connect(self.openScript)

        undoAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'undo.png')), 'Undo', self)
        redoAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'redo.png')), 'Redo', self)
		
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
        self.textEdit.setFont(QtGui.QFont("Courier"))
        self.textEdit.zoomIn(+2)
        self.textEdit.setLineWrapMode(0)
        self.texEdit=CompletionTextEdit()

        self.ContainerGrid.setSpacing(0)
        self.ContainerGrid.addWidget(editor, 1, 0,1,15)
        self.ContainerGrid.addWidget(self.toolbar, 0, 0)
		
        self.startopen()
        
        self.main.setWindowTitle("Script Properties: "+ self.FileName)
        
        self.show()

    def onChanged(self, text):
        self.main.setWindowTitle("Script Properties: "+ text)
        self.main.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'addscript.png')))
        fname = self.FileName + ".py"
        finalname = str(text) + ".py"

        #rename file in folder
        os.rename(os.path.join(self.dirname, "Scripts", str(self.FileName)) + ".py",
                  os.path.join(self.dirname, "Scripts", finalname))
        
        #rename file in tree widget
        self.parent.updatetree()

        self.FileName = text
	
    def exportScript(self):
        #print str(self.dirname)+ ("/Scripts/") + str(self.FileName)+".py"
        fname = os.path.join(self.dirname, "Scripts", str(self.FileName))+ ".py"
        with open(fname, 'w') as f:    
            data = self.textEdit.toPlainText()
            f.write(data)
            f.close()

    def saveScript(self):
        #print str(self.dirname)+ ("/Scripts/") + str(self.FileName)+".py"
        fname = os.path.join(self.dirname, "Scripts", str(self.FileName)) + ".py"
        with open(fname, 'w') as f:    
            data = self.textEdit.toPlainText()
            f.write(data)
            f.close()
        self.main.close()
			
    def startopen(self):
        fname = os.path.join(self.dirname, "Scripts", str(self.FileName)) + ".py"

        with open(fname, 'r') as f:
            data = f.read()
            self.textEdit.setText(data)
            f.close()
			
    def openScript(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                str(os.getcwd()))

        if fname == '':
            return

        with open(fname, 'r') as f:
            data = f.read()
            self.textEdit.setText(data)
