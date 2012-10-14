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
from PyQt4 import QtGui, QtCore
from PIL import Image



class SpriteGUI(QtGui.QWidget):
  
    def __init__(self, main,icon):
        super(SpriteGUI, self).__init__()

        self.main = main
        self.dirname = self.main.dirname
        self.icon = icon
        self.initUI()

    def initUI(self):

        self.image_file = os.path.join(self.dirname, "Sprites/%s.png"%(self.icon))
        img = Image.open(self.image_file)
        width, height = img.size
        extension = os.path.splitext(self.image_file)[1][1:]
        Format  = str(extension)

        #Groupbox Container-----------------------------------
        self.ContainerBox = QtGui.QGroupBox(self.main)
        self.ContainerBox.setGeometry(QtCore.QRect(25,25,self.width()-100,550))
        self.ContainerBox.setObjectName("groupBox")
        self.ContainerBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.ContainerBox.setGeometry(200, 150, 600, 330)
        self.ContainerBox.setMinimumSize(480,330)
                
        self.BtnOK = QtGui.QPushButton('OK', self.ContainerBox)
        self.BtnOK.setIcon(QtGui.QIcon('Data/accept.png'))
        self.BtnOK.setGeometry(32, 240, 60, 25)
        self.BtnOK.clicked.connect(self.HideMe)

        #Scroll Area------------------------------------------
        self.sprite = QtGui.QPixmap(os.path.join(self.dirname, "Sprites/%s.png"%(self.icon)))
                                    
        self.spriteLbl = QtGui.QLabel(self.main)
        self.spriteLbl.setPixmap(self.sprite)
                                    
        self.scrollArea = QtGui.QScrollArea(self.ContainerBox)
        self.scrollArea.setWidget(self.spriteLbl)
        
        #Groupbox General-------------------------------------
        self.GeneralBox = QtGui.QGroupBox(self.ContainerBox)
        self.GeneralBox.setGeometry(QtCore.QRect(16,16,180,160))
        self.GeneralBox.setObjectName("groupBox")
        self.GeneralBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.GeneralBox.setTitle("General")
 
        self.BtnLoad = QtGui.QPushButton('Load Sprite', self.GeneralBox)
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        self.BtnLoad.setGeometry(50, 55, 115, 25)
        self.BtnLoad.clicked.connect(self.LoadSprite)

        self.BtnSave = QtGui.QPushButton('Save Sprite', self.GeneralBox)
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.setGeometry(50, 85, 115, 25)
        self.BtnSave.clicked.connect(self.SaveSprite)
 
        self.BtnEdit = QtGui.QPushButton('Edit Sprite', self.GeneralBox)
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))
        self.BtnEdit.setGeometry(50, 114, 115, 25)
        self.BtnEdit.clicked.connect(self.EditSprite)

        self.LblName = QtGui.QLabel(self.GeneralBox) 
        self.LblName.setText('Name:') 
        self.LblName.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
        self.LblName.setGeometry(15, 25, 100, 25)

        self.qleSprite = QtGui.QLineEdit("%s"%(self.icon), self.GeneralBox)
        self.qleSprite.setGeometry(50, 25, 115, 25)

        #Groupbox Image Information---------------------------
        self.InformationBox = QtGui.QGroupBox(self.ContainerBox)
        self.InformationBox.setGeometry(QtCore.QRect(210,16,125,130))
        self.InformationBox.setObjectName("groupBox")
        self.InformationBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.InformationBox.setTitle("Image Information")

        self.LblWidth = QtGui.QLabel(self.InformationBox) 
        self.LblWidth.setText('Width:   %d Pixels'%(width)) 
        self.LblWidth.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
        self.LblWidth.setGeometry(15, 25, 125, 25) 
 
        self.LblHeight = QtGui.QLabel(self.InformationBox) 
        self.LblHeight.setText('Height:  %d Pixels'%(height)) 
        self.LblHeight.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
        self.LblHeight.setGeometry(15, 55, 125, 25) 

        self.LblFormat = QtGui.QLabel(self.InformationBox) 
        self.LblFormat.setText('File Format:  %s'%(Format)) 
        self.LblFormat.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
        self.LblFormat.setGeometry(15, 85, 125, 25) 

        #Groupbox Collision Checking---------------------------
        self.CollisionBox = QtGui.QGroupBox(self.ContainerBox)
        self.CollisionBox.setGeometry(QtCore.QRect(210,155,125,55))
        self.CollisionBox.setObjectName("groupBox")
        self.CollisionBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.CollisionBox.setTitle("Collision Checking")

        self.BtnLoad = QtGui.QPushButton('Modify Mask', self.CollisionBox)
        self.BtnLoad.setGeometry(15, 20, 100, 25) 
      

        #Main Window------------------------------------------
        self.ContainerBox.show()

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
        

