#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import os, sys

class Inspector(QtGui.QDialog):
    def __init__(self, main):
        super(Inspector, self).__init__(main)
        self.main = main

        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setPlaceholderText("Name")
        self.nameEdit.setMinimumWidth(150)
        self.title = QtGui.QLabel("<h2>Inspector</h2>")

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (10)
        self.ContainerGrid.setSpacing(10)
        
        
        self.ContainerGrid.addWidget(self.title)
        self.ContainerGrid.addWidget(self.nameEdit, 1, 0)
        self.spacer = QtGui.QWidget() 
        self.spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 
        self.ContainerGrid.addWidget(self.spacer)

        self.setLayout(self.ContainerGrid)
