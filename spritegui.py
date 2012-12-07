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
import os
import os.path
import shutil
from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore
from PIL import Image



class SpriteGUI(QtGui.QWidget):
  
    def __init__(self, main, icon, dirname):
        super(SpriteGUI, self).__init__()
        self.main = main
        self.dirname = dirname
        self.icon = icon
        self.initUI()
        
        
    def initUI(self):
        self.image_file = os.path.join(self.dirname, "Sprites/%s.png"%(self.icon))
        img = Image.open(self.image_file)
        width, height = img.size
        extension = os.path.splitext(self.image_file)[1][1:]
        Format  = str(extension)

        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self.main)
        self.ContainerGrid.setMargin (0)
        
                
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setGeometry (32,32,32,32)
        self.BtnOK.setIcon(QtGui.QIcon('Data/accept.png'))
        self.BtnOK.clicked.connect(self.HideMe)

        #Scroll Area------------------------------------------
        self.sprite = QtGui.QPixmap(os.path.join(self.dirname, "Sprites/%s.png"%(self.icon)))
                                    
        self.spriteLbl = QtGui.QLabel(self.main)
        self.spriteLbl.setPixmap(self.sprite)
        self.spriteLbl.setAlignment(QtCore.Qt.AlignTop)
                                    
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.spriteLbl)
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        
        self.scrollArea.setWidgetResizable(True)
        
        
        #Groupbox General-------------------------------------
        self.GeneralBox = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()		
        self.NameAndThingsBox = QtGui.QFrame() 
        self.nameandlayout = QtGui.QGridLayout()
		
        self.BtnLoad = QtGui.QPushButton('Load Sprite')
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        self.BtnLoad.clicked.connect(self.LoadSprite)

        self.BtnSave = QtGui.QPushButton('Save Sprite')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.clicked.connect(self.SaveSprite)
 
        self.BtnEdit = QtGui.QPushButton('Edit Sprite')
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))
        self.BtnEdit.clicked.connect(self.EditSprite)

        self.LblName = QtGui.QLabel() 
        self.LblName.setText('Name:') 
        self.LblName.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.Lblspacer = QtGui.QLabel(" ")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.qleSprite = QtGui.QLineEdit("%s"%(self.icon))

        self.LblWidth = QtGui.QLabel('Width:   %d Pixels'%(width)) 
 
        self.LblHeight = QtGui.QLabel('Height:  %d Pixels'%(height))
        
        self.LblSubimages = QtGui.QLabel('Number of subimages: %d'%(frames))

        self.LblFormat = QtGui.QLabel('File Format:  %s'%(Format)) 

	
        self.nameandlayout.addWidget(self.LblName,0,0)	
        self.nameandlayout.addWidget(self.qleSprite,0,1)
        
        self.nameandlayout.addWidget(self.Lblspacer,1,0)
        
        self.nameandlayout.addWidget(self.BtnLoad,1,0,1,2)
        self.nameandlayout.addWidget(self.BtnSave,2,0,2,2)
        self.nameandlayout.addWidget(self.BtnEdit,4,0,4,2)
        
        self.nameandlayout.addWidget(self.LblWidth,8,0,8,0)
        self.nameandlayout.addWidget(self.LblHeight,12,0,12,0)
        self.nameandlayout.addWidget(self.LblSubimages,18,0,18,0)
        
        self.NameAndThingsBox.setLayout(self.nameandlayout)

		
        self.layout.addWidget(self.NameAndThingsBox,0,0)
        self.layout.addItem(spacerItem)
        self.layout.addWidget(self.BtnOK)
		

        self.GeneralBox.setLayout(self.layout)		
		
        #Groupbox Image Information---------------------------
        #self.InformationBox = QtGui.QGroupBox()
        #self.layout1 = QtGui.QGridLayout()	 
		
        #self.layout1.addWidget(self.LblWidth,0,0)	
        #self.layout1.addWidget(self.LblHeight,1,0)
        #self.layout1.addWidget(self.LblFormat,3,0)
        #self.InformationBox.setLayout(self.layout1)	
		
        #Groupbox Collision Checking---------------------------
        #self.CollisionBox = QtGui.QGroupBox()
        #self.CollisionBox.setObjectName("groupBox")
        #self.CollisionBox.setTitle("Collision Checking")

        #self.BtnLoad = QtGui.QPushButton('Modify Mask', self.CollisionBox)
      

        #Main Window------------------------------------------
		
        self.ContainerGrid.setSpacing(0)



		
        self.spritesplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.spritesplitter.addWidget(self.GeneralBox)
        self.spritesplitter.setCollapsible ( 0, False)
        
        #self.spritesplitter.addWidget(self.InformationBox)
        self.spritesplitter.addWidget(self.scrollArea)
        self.spritesplitter.setMinimumSize(350,200)
        self.spritesplitter.setStretchFactor(1, 2)
        self.ContainerGrid.addWidget(self.spritesplitter, 0, 0)

		
		
		

    def LoadSprite(self):
        self.asprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
        if self.asprite !='':
            for sprite in self.asprite:
                shutil.copy(sprite, self.image_file)
                self.sprite = QtGui.QPixmap(sprite)
                self.spriteLbl.setPixmap(self.sprite)
                self.image_file = os.path.join(self.dirname, "Sprites/%s.png"%(self.icon))
                img = Image.open(self.image_file)
                width, height = img.size
                extension = os.path.splitext(self.image_file)[1][1:]
                Format  = str(extension)
                self.LblWidth.setText('Width:   %d Pixels'%(width))
                self.LblHeight.setText('Height:  %d Pixels'%(height))
                self.LblFormat.setText('File Format:  %s'%(Format))
                

    def SaveSprite(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Sprite(s)', 
                '', self.tr("Image file (*.png)"))

        if self.fname !='':
            shutil.copy(self.image_file, self.fname)


    def EditSprite(self):
        os.startfile(self.image_file)#TO BE DONE :)
    
    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
        

