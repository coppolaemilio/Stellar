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

from PyQt4 import QtGui, QtCore


class FontGUI(QtGui.QWidget):
  
    def __init__(self, main, dirname):
        super(FontGUI, self).__init__(main)

        self.main = main
        self.dirname = dirname
        self.initUI()

    def initUI(self):

        #Groupbox Container-----------------------------------
        self.ContainerBox = QtGui.QGroupBox(self.main)
        self.ContainerBox.setObjectName("groupBox")
        self.ContainerBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.ContainerBox.setGeometry(QtCore.QRect(0,0,450,400))
        self.ContainerBox.setMinimumSize(450,400)

        self.basicwidg = QtGui.QWidget(self.ContainerBox)

        self.name = QtGui.QLabel('Name:',self.basicwidg)
        self.name.move(6,13)
        self.nameEdit = QtGui.QLineEdit('',self.basicwidg)
        self.nameEdit.setGeometry(45,10,145,21)

        self.font = QtGui.QLabel('Font:',self.basicwidg)
        self.font.move(6,40)
        self.fontBox = QtGui.QFontComboBox(self.basicwidg)
        self.fontBox.setGeometry(45,37,145,21)
        
        self.fontBox.activated.connect(self.onFontChanged)
        
        self.size = QtGui.QLabel('Size:',self.basicwidg)
        self.size.move(6,67)
        self.sizeEdit = QtGui.QLineEdit('12',self.basicwidg)
        self.sizeEdit.setGeometry(45,64,145,21)
        self.sizeEdit.textChanged.connect(self.onFontChanged)
    
        self.bold = QtGui.QCheckBox('Bold', self.ContainerBox)
        self.bold.move(46, 94)
        self.Italic = QtGui.QCheckBox('Italic', self.ContainerBox)
        self.Italic.move(106, 94)
        self.antiAli = QtGui.QCheckBox('Anti-Aliasing', self.ContainerBox)
        self.antiAli.move(46, 124)

        #self.CharacterBox = QtGui.QGroupBox('Character Range',self)
        #self.CharacterBox.setGeometry(16,120,170,100)
        
        #self.fromc = QtGui.QLineEdit('32')
        #self.till = QtGui.QLabel('till')
        #self.toc = QtGui.QLineEdit('127')
        #self.normalb = QtGui.QPushButton('Normal')
        #self.digitsb = QtGui.QPushButton('Digits')
        #self.allb = QtGui.QPushButton('All')
        #self.lettersb = QtGui.QPushButton('Letters')

        self.testtext = QtGui.QTextEdit('A text. 1234567890',self.ContainerBox)
        self.testtext.setGeometry(200,9,240,100)

        self.previewtext = QtGui.QTextEdit('A text. 1234567890',self.ContainerBox)
        self.previewtext.setGeometry(200,119,240,100)
        self.previewtext.setCurrentFont( QtGui.QFont(self.fontBox.currentText(), 10, True) )

        self.BtnOK = QtGui.QPushButton('OK', self.ContainerBox)
        self.BtnOK.setIcon(QtGui.QIcon(os.path.join('Data', 'accept.png')))
        self.BtnOK.setGeometry(32, 240, 60, 25)

        #Main Window------------------------------------------
        self.ContainerBox.show()
        self.setMinimumSize(350,400)
 
    def resizeEvent(self, event):
        pass

    def onFontChanged(self):
        self.previewtext.setFont(QtGui.QFont(self.fontBox.currentText(),float(self.sizeEdit.text())) )
        
    def onChanged(self, text):
        self.previewtext.setText(text)

    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
