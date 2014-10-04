#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import os, sys

class Inspector(QtGui.QDialog):
    def __init__(self, main):
        super(Inspector, self).__init__(main)
        self.main = main

        self.nameEdit = QtGui.QLineEdit()

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)
        
        self.ContainerGrid.addWidget(self.nameEdit)

        self.setLayout(self.ContainerGrid)
