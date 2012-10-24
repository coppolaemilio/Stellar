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
		
        self.BtnSave = QtGui.QPushButton('')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
		
        self.BtnOpen = QtGui.QPushButton('')
        self.BtnOpen.setIcon(QtGui.QIcon('Data/folder.png'))
		
        editor= self.textEdit = CompletionTextEdit()
        highlight = syntax.PythonHighlighter(editor.document())
        self.textEdit.zoomIn(+4)
        self.texEdit=CompletionTextEdit()
        self.ContainerGrid.addWidget(editor, 1, 0,1,15)
        self.ContainerGrid.addWidget(self.LblName, 0, 0)
        self.ContainerGrid.addWidget(self.nameEdit, 0, 1)
        self.ContainerGrid.addWidget(self.BtnSave, 0, 2)
        self.ContainerGrid.addWidget(self.BtnOpen, 0, 3)

            
    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
