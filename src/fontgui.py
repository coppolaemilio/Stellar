#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
#
# This file is part of Stellar.
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
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFont

class FontGUI(QtGui.QWidget):
    def __init__(self, main, name, dirname, tree):
        super(FontGUI, self).__init__()
        self.main = main
        self.name = name
        self.dirname = dirname
        self.tree = tree

        self.font = self.tree.fnt_parser.get(self.name, 'font')
        self.fontindex = self.tree.fnt_parser.get(self.name, 'fontindex')
        self.size = self.tree.fnt_parser.get(self.name, 'size')
        self.bold = self.tree.fnt_parser.get(self.name, 'bold') == 'True'
        self.italic = self.tree.fnt_parser.get(self.name, 'italic') == 'True' 
        self.antialiasing = self.tree.fnt_parser.get(self.name, 'antialiasing') == 'True'

        #if self.font == '': self.font = 'Arial'
        if self.size == '': self.size = 11

        self.initUI()

    def initUI(self):
        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        
        self.ContainerBox = QtGui.QFrame(self.main)
        self.nameLabel = QtGui.QLabel('Name:')
        self.nameEdit = QtGui.QLineEdit(self.name)
        self.fontLabel = QtGui.QLabel('Font:')
        self.fontBox = QtGui.QFontComboBox()
        try:
            self.fontBox.setCurrentIndex(int(self.fontindex))
        except:
            print("Error: No font index found.")

        self.fontBox.setCurrentFont(QtGui.QFont(str(self.fontBox.currentText())))
        #self.fontBox.currentFontChanged.connect(self.onChanged)
        
        self.sizeLabel = QtGui.QLabel('Size:')
        self.sizeEdit = QtGui.QSpinBox()
        self.sizeEdit.setValue(int(self.size))
        self.sizeEdit.valueChanged.connect(self.onChanged)
        self.boldLabel = QtGui.QCheckBox('Bold')
        self.boldLabel.clicked.connect(self.onChanged)
        self.ItalicLabel = QtGui.QCheckBox('Italic')
        self.ItalicLabel.clicked.connect(self.onChanged)
        self.antiAliLabel = QtGui.QCheckBox('Anti-Aliasing')
        self.antiAliLabel.clicked.connect(self.onChanged)
        
        self.boldLabel.setChecked(self.bold)
        self.ItalicLabel.setChecked(self.italic)
        self.antiAliLabel.setChecked(self.antialiasing)

        self.testtext = QtGui.QTextEdit('!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
        #self.testtext.textChanged.connect(self.onChanged)
        
        self.previewtext = QtGui.QTextEdit('!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
        self.previewtext.setReadOnly(True)
        self.previewtext.setCurrentFont( QtGui.QFont(self.fontBox.currentText(), int(self.size), True) )
        
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setIcon(QtGui.QIcon(os.path.join('Data', 'accept.png')))
        self.BtnOK.clicked.connect(self.ok)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)


        self.OptionsBox = QtGui.QGroupBox("Options")
        self.optionslayout = QtGui.QGridLayout()
        self.optionslayout.setMargin(0)
        self.optionslayout.addWidget(self.boldLabel,0,0)
        self.optionslayout.addWidget(self.ItalicLabel,0,1)
        self.optionslayout.addWidget(self.antiAliLabel,1,0)
        self.OptionsBox.setLayout(self.optionslayout)
        
        self.NameFrame = QtGui.QFrame()
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin(0)
        self.namelayout.addWidget(self.nameLabel,0,0)
        self.namelayout.addWidget(self.nameEdit,0,1)
        self.namelayout.addWidget(self.fontLabel,1,0)
        self.namelayout.addWidget(self.fontBox,1,1)
        self.namelayout.addWidget(self.sizeLabel,2,0)
        self.namelayout.addWidget(self.sizeEdit,2,1)
        self.NameFrame.setLayout(self.namelayout)
  
        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin (6)
        self.showlayout.addWidget(self.NameFrame,1,0)
        self.showlayout.addWidget(self.OptionsBox,5,0)
        self.showlayout.addItem(spacerItem,6,0)
        self.showlayout.addWidget(self.BtnOK,7,0)
        self.ShowFrame.setLayout(self.showlayout)
        
        self.RightFrame = QtGui.QFrame()
        self.rightlayout = QtGui.QGridLayout()
        self.rightlayout.setMargin(0)     
        self.rightlayout.addWidget(self.testtext,0,0)
        self.rightlayout.addWidget(self.previewtext,1,0)
        self.RightFrame.setLayout(self.rightlayout)        
        
        self.LastWidget = QtGui.QWidget()
        self.spritesplitter = QtGui.QHBoxLayout()
        self.spritesplitter.addWidget(self.ShowFrame)
        self.spritesplitter.addWidget(self.RightFrame)
        
        self.LastWidget.setLayout(self.spritesplitter)
        self.ContainerGrid.addWidget(self.LastWidget)
        self.setLayout(self.ContainerGrid)

        #self.connect(self.testtext,QtCore.SIGNAL("textChanged()"),self.onChanged)
        QtCore.QObject.connect(self.testtext, QtCore.SIGNAL("textChanged()"), self.onChanged)
        QtCore.QObject.connect(self.fontBox, QtCore.SIGNAL("currentFontChanged(QFont)"), self.previewtext.setCurrentFont)
        self.onChanged()
        
    def onChanged(self):
        self.bold = bool(self.boldLabel.checkState())
        self.italic = bool(self.ItalicLabel.checkState())
        self.antialiasing = bool(self.antiAliLabel.checkState())

        if self.bold:
            self.previewtext.setFontWeight(QFont.Bold)
        else:
            self.previewtext.setFontWeight(QFont.Normal)
        
        self.previewtext.setFontItalic(self.italic) 

        self.previewtext.setPlainText(self.testtext.toPlainText())
        self.previewtext.setFontPointSize(self.sizeEdit.value())
        self.previewtext.setFontFamily(self.fontBox.currentText())

        self.tree.fnt_parser.set(self.name, 'bold', self.bold)
        self.tree.fnt_parser.set(self.name, 'italic', self.italic)
        self.tree.fnt_parser.set(self.name, 'antialiasing', self.antialiasing)

    def ok(self):
        self.close()
        name = str(self.nameEdit.text())
        if self.name is not name:
            self.tree.fnt_parser.remove_section(self.name)
            self.tree.fnt_parser.add_section(name)

            self.name = str(self.nameEdit.text())


        self.tree.fnt_parser.set(name, 'font', self.fontBox.currentText())
        self.tree.fnt_parser.set(name, 'fontindex', self.fontBox.currentIndex())
        
        self.tree.fnt_parser.set(name, 'size', self.sizeEdit.value())
        self.tree.fnt_parser.set(name, 'bold', bool(self.boldLabel.checkState()))
        self.tree.fnt_parser.set(name, 'italic', bool(self.ItalicLabel.checkState()))
        self.tree.fnt_parser.set(name, 'antialiasing', bool(self.antiAliLabel.checkState()))

        self.tree.write_fonts()

        self.main.updatetree()
        self.main.qmdiarea.activeSubWindow().close()
