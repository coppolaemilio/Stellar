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
import inspect
import cfg

from PyQt4 import QtGui, QtCore

#direc = inspect.getfile(inspect.currentframe())
#dirname, filename = os.path.split(os.path.abspath(direc))


class PreferencesDialog(QtGui.QDialog): 
    def __init__(self, main): 
        super(PreferencesDialog, self).__init__(main) 
         
        self.setGeometry(0,0, 412,470) 
        self.setWindowTitle("Preferences") 
        self.setWindowIcon(QtGui.QIcon("Data/icon.png"))  
        self.setMinimumSize(412,470)
        self.setMaximumSize(412,470) 
        self.center()

        self.soundeditor = ''
        self.codeeditor = ''
        self.imageeditor = ''
         
        #TABS ----------------
         
        tab_widget = QtGui.QTabWidget() 
        tab1 = QtGui.QWidget() 
        tab2 = QtGui.QWidget()
         
        p1_vertical = QtGui.QVBoxLayout(tab1) 
        p2_vertical = QtGui.QVBoxLayout(tab2)
         
        tab_widget.addTab(tab1, "Editors") 
        tab_widget.addTab(tab2, "General")

        self.ContainerBox = QtGui.QGroupBox(self)
        
        self.codeeditorbox = QtGui.QGroupBox('Code Editor',self.ContainerBox)
        self.codeeditorbox.setGeometry(16, 16, 330, 100)
        self.usebuilt = QtGui.QRadioButton("Use built-in code editor", self.codeeditorbox)
        self.usebuilt.move(16, 20)
        self.usebuilt.toggle()
        self.useexternal = QtGui.QRadioButton("Use external code editor", self.codeeditorbox)
        self.useexternal.move(16, 40)
        self.useexternal.clicked.connect(self.codeeditor)
        self.editor = QtGui.QLineEdit('',self.codeeditorbox)
        self.editor.setGeometry(20,65,255,21)
        self.button = QtGui.QPushButton("...", self.codeeditorbox)
        self.button.setGeometry(280,65,40,21)
        self.button.clicked.connect(self.codeeditor)
        
        self.imageeditorbox = QtGui.QGroupBox('Image Editor',self.ContainerBox)
        self.imageeditorbox.setGeometry(16, 126, 330, 100)
        self.usebuilt1 = QtGui.QRadioButton("Use built-in code editor", self.imageeditorbox)
        self.usebuilt1.move(16, 20)
        self.usebuilt1.toggle()
        self.useexternal1 = QtGui.QRadioButton("Use external code editor", self.imageeditorbox)
        self.useexternal1.move(16, 40)
        self.useexternal1.clicked.connect(self.imageeditor)
        self.editor1 = QtGui.QLineEdit('',self.imageeditorbox)
        self.editor1.setGeometry(20,65,255,21)
        self.button1 = QtGui.QPushButton("...", self.imageeditorbox)
        self.button1.setGeometry(280,65,40,21)
        self.button1.clicked.connect(self.imageeditor)

        self.soundeditorbox = QtGui.QGroupBox('Sound Editor',self.ContainerBox)
        self.soundeditorbox.setGeometry(16, 246, 330, 100)
        self.usebuilt2 = QtGui.QRadioButton("Use built-in code editor", self.soundeditorbox)
        self.usebuilt2.move(16, 20)
        self.usebuilt2.toggle()
        self.useexternal2 = QtGui.QRadioButton("Use external code editor", self.soundeditorbox)
        self.useexternal2.move(16, 40)
        self.useexternal2.clicked.connect(self.soundeditor)
        self.editor2 = QtGui.QLineEdit('',self.soundeditorbox)
        self.editor2.setGeometry(20,65,255,21)
        self.button2 = QtGui.QPushButton("...", self.soundeditorbox)
        self.button2.setGeometry(280,65,40,21)
        self.button2.clicked.connect(self.soundeditor)
        
        p1_vertical.addWidget(self.ContainerBox)

        okButton = QtGui.QPushButton("OK")
        okButton.setIcon(QtGui.QIcon(os.path.join('Data', 'accept.png')))
        okButton.clicked.connect(self.okbutton)
        
        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.setIcon(QtGui.QIcon(os.path.join('Data', 'cancel.png')))
        cancelButton.clicked.connect(self.close)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        self.ResolutionBox = QtGui.QGroupBox(self)
        self.full = QtGui.QCheckBox('Set the resolution of the screen', self.ResolutionBox)
        self.full.move(16, 16)
        p2_vertical.addWidget(self.ResolutionBox)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tab_widget) 
        vbox.addLayout(hbox)
        self.setLayout(vbox) 

        #Load Preferences-----------------------------

        #-----------------------------------------

        self.show()

    
    # editor -> codeeditor
    # editor1 -> soundeditor
    # editor2 -> imageeditor
    
    def codeeditor(self):
        if not self.editor.text():
            name = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Select Program', 
                    '', self.tr("Programs (*.exe)")))
            if name is not "":
                self.useexternal.toggle()
                self.editor.setText(name)
            
    def imageeditor(self):
        if not self.editor1.text():
            name = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Select Program', 
                    '', self.tr("Programs (*.exe)")))
            if name is not "":
                self.useexternal1.toggle()
                self.editor1.setText(name)
            
    def soundeditor(self):
        if not self.editor2.text():
            name = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Select Program', 
                    '', self.tr("Programs (*.exe)")))
            if name is not "":
                self.useexternal2.toggle()
                self.editor2.setText(name)
                
    def okbutton(self):
        if self.useexternal.isChecked():
            cfg.config.set('stellar', 'codeeditor', unicode(self.editor.text()).encode('utf-8'))
            cfg.codeeditor = unicode(self.editor.text())
        if self.useexternal2.isChecked():
            cfg.config.set('stellar', 'soundeditor', unicode(self.editor1.text()).encode('utf-8'))
            cfg.soundeditor = unicode(self.editor1.text())
        if self.useexternal3.isChecked():
            cfg.config.set('stellar', 'imageeditor', unicode(self.editor2.text()).encode('utf-8'))
            cfg.imageeditor = unicode(self.editor2.text())

        with open('config.ini', 'w') as configfile:
            cfg.config.write(configfile)

        self.close()

    def center(self): 
        screen = QtGui.QDesktopWidget().screenGeometry() 
        size = self.geometry() 
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2) 


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv) 
    frame = PreferencesDialog(None) 
    sys.exit(app.exec_())
