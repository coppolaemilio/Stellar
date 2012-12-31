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



import pygame.mixer

from PyQt4 import QtGui, QtCore





class ObjectGUI(QtGui.QWidget):

  

    def __init__(self, main, FileName, dirname):

        super(ObjectGUI, self).__init__(main)

        

        self.main = main

        self.dirname = dirname

        self.FileName = FileName

        self.initUI()



    def initUI(self):

        

        #Groupbox Container-----------------------------------



        self.ContainerGrid = QtGui.QGridLayout(self.main)
        self.ContainerGrid.setMargin (0)

		

        self.LblName = QtGui.QLabel('Name:')

        self.nameEdit = QtGui.QLineEdit(self.FileName)




                

        self.BnewSprite = QtGui.QPushButton("New")
        self.BeditSprite = QtGui.QPushButton("Edit")
        self.SpriteCombo = QtGui.QComboBox()
        
        self.SpriteFrame = QtGui.QGroupBox("Sprite")

        self.spritelayout = QtGui.QGridLayout()

        self.spritelayout.setMargin (8)

        self.spritelayout.addWidget(self.SpriteCombo,0,0,1,2)

        self.spritelayout.addWidget(self.BnewSprite,1,0)
        self.spritelayout.addWidget(self.BeditSprite,1,1)

        self.SpriteFrame.setLayout(self.spritelayout)





        self.NameFrame = QtGui.QFrame()

        self.namelayout = QtGui.QGridLayout()

        self.namelayout.setMargin (0)

        self.namelayout.addWidget(self.LblName,0,0)

        self.namelayout.addWidget(self.nameEdit,0,1)

        self.namelayout.addWidget(self.SpriteFrame,1,0,1,2)



        

        self.NameFrame.setLayout(self.namelayout)





        

        

        self.cbvisible = QtGui.QCheckBox('Visible', self)

        self.cbsolid = QtGui.QCheckBox('Solid', self)

        self.cbpersis = QtGui.QCheckBox('Persistent', self)

        self.LblDepth = QtGui.QLabel('Depth:')

        self.depthEdit = QtGui.QLineEdit("0")

        self.LblParent = QtGui.QPushButton("Parent:")

        self.ParentEdit = QtGui.QComboBox()

        self.LblMask = QtGui.QPushButton("Mask:")

        self.MaskEdit = QtGui.QComboBox()

        self.Btninfo = QtGui.QPushButton("Show Information")

        self.Btninfo.setIcon(QtGui.QIcon(os.path.join('Data', 'info.png')))

        self.Btnok = QtGui.QPushButton("OK")

        self.Btnok.setIcon(QtGui.QIcon('Data/accept.png'))

        self.eventstree = QtGui.QTreeWidget()
        self.eventstree.setHeaderLabel("Events")

        self.actionstree = QtGui.QTreeWidget()
        self.actionstree.setHeaderLabel("Actions")

        self.Btnaddevent = QtGui.QPushButton("Add Event")

        self.Btndelete = QtGui.QPushButton("Delete")

        self.Btnchange = QtGui.QPushButton("Change")

        

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)


        self.FirstWidget = QtGui.QWidget()
        self.FirstGrid = QtGui.QGridLayout()

        self.FirstGrid.addWidget(self.NameFrame, 0, 0, 1, 2)

        self.FirstGrid.addWidget(self.SpriteFrame, 1, 0, 1, 2)

        self.FirstGrid.addWidget(self.cbvisible, 2, 0)

        self.FirstGrid.addWidget(self.cbsolid, 2, 1)

        self.FirstGrid.addWidget(self.cbpersis, 3, 0)

        self.FirstGrid.addWidget(self.LblDepth, 4, 0)

        self.FirstGrid.addWidget(self.depthEdit, 4, 1)

        self.FirstGrid.addWidget(self.LblParent, 5, 0)

        self.FirstGrid.addWidget(self.ParentEdit, 5, 1)

        self.FirstGrid.addWidget(self.LblMask, 6, 0)

        self.FirstGrid.addWidget(self.MaskEdit, 6, 1)

        self.FirstGrid.addItem(spacerItem)

        self.FirstGrid.addWidget(self.Btninfo, 7, 0, 1, 2)

        self.FirstGrid.addWidget(self.Btnok, 8, 0,1,2)
        self.FirstWidget.setLayout(self.FirstGrid)
        

        #---

        self.SecondWidget = QtGui.QWidget()
        self.SecondGrid = QtGui.QGridLayout()

        self.SecondGrid.addWidget(self.eventstree, 0, 0, 7, 2)

        self.SecondGrid.addWidget(self.Btnaddevent,    7, 0, 1, 2)

        self.SecondGrid.addWidget(self.Btndelete,      8, 0)

        self.SecondGrid.addWidget(self.Btnchange,      8, 1)
        self.SecondWidget.setLayout(self.SecondGrid)

        #---
        self.ThirdWidget = QtGui.QWidget()
        self.ThirdGrid = QtGui.QGridLayout()

        self.ThirdGrid.addWidget(self.actionstree, 0, 0, 9, 2)
        self.ThirdWidget.setLayout(self.ThirdGrid)







        self.objectsplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)

        self.objectsplitter.addWidget(self.FirstWidget)

        self.objectsplitter.addWidget(self.SecondWidget)
        self.objectsplitter.addWidget(self.ThirdWidget)
        self.objectsplitter.setStretchFactor(1, 1)
        

        self.ContainerGrid.addWidget(self.objectsplitter)
        



        #self.startopen()
