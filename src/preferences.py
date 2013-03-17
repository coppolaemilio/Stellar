#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
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
import cfg

from PyQt4 import QtGui

if sys.version_info.major == 2:
    str = unicode

class PreferencesDialog(QtGui.QDialog): 
    def __init__(self, main): 
        super(PreferencesDialog, self).__init__(main) 
         
        self.setGeometry(0,0, 412,470) 
        self.setWindowTitle("Preferences") 
        self.setWindowIcon(QtGui.QIcon("Data/icon.png"))  
        self.setMinimumSize(412,470)
        self.setMaximumSize(412,470) 
        self.center()
         
        #TABS ----------------
         
        tab_widget = QtGui.QTabWidget() 
        tab1 = QtGui.QWidget() 
        tab2 = QtGui.QWidget()
         
        p1_vertical = QtGui.QVBoxLayout(tab1) 
        p2_vertical = QtGui.QVBoxLayout(tab2)
         
        tab_widget.addTab(tab1, "Editors") 
        tab_widget.addTab(tab2, "General")

        self.ContainerBox = QtGui.QGroupBox(self)

        #code editor       
        self.codeeditorbox = QtGui.QGroupBox('Code Editor',self.ContainerBox)
        self.codeeditorbox.setGeometry(16, 16, 330, 100)
        self.usebuilt_code = QtGui.QRadioButton("Use built-in code editor", self.codeeditorbox)
        self.usebuilt_code.move(16, 20)
        self.usebuilt_code.clicked.connect(self.built_codeeditor)
        self.useexternal_code = QtGui.QRadioButton("Use external code editor", self.codeeditorbox)
        self.useexternal_code.move(16, 40)
        self.useexternal_code.clicked.connect(self.codeeditor)
        self.inp_codeeditor = QtGui.QLineEdit('',self.codeeditorbox)
        self.inp_codeeditor.setGeometry(20,65,255,21)
        self.button_code = QtGui.QPushButton("...", self.codeeditorbox)
        self.button_code.setGeometry(280,65,40,21)
        self.button_code.clicked.connect(self.codeeditor)

        #image editor
        self.imageeditorbox = QtGui.QGroupBox('Image Editor',self.ContainerBox)
        self.imageeditorbox.setGeometry(16, 126, 330, 100)
        self.usebuilt_img = QtGui.QRadioButton("Use built-in image editor", self.imageeditorbox)
        self.usebuilt_img.move(16, 20)
        self.usebuilt_img.clicked.connect(self.built_imageeditor)
        self.useexternal_img = QtGui.QRadioButton("Use external image editor", self.imageeditorbox)
        self.useexternal_img.move(16, 40)
        self.useexternal_img.clicked.connect(self.imageeditor)
        self.inp_imageeditor = QtGui.QLineEdit('',self.imageeditorbox)
        self.inp_imageeditor.setGeometry(20,65,255,21)
        self.button_img = QtGui.QPushButton("...", self.imageeditorbox)
        self.button_img.setGeometry(280,65,40,21)
        self.button_img.clicked.connect(self.imageeditor)

        #sound editor
        self.soundeditorbox = QtGui.QGroupBox('Sound Editor',self.ContainerBox)
        self.soundeditorbox.setGeometry(16, 246, 330, 100)
        self.usebuilt_sound = QtGui.QRadioButton("Use built-in sound editor", self.soundeditorbox)
        self.usebuilt_sound.move(16, 20)
        self.usebuilt_code.clicked.connect(self.built_soundeditor)
        self.useexternal_sound = QtGui.QRadioButton("Use external sound editor", self.soundeditorbox)
        self.useexternal_sound.move(16, 40)
        self.useexternal_sound.clicked.connect(self.soundeditor)
        self.inp_soundeditor = QtGui.QLineEdit('',self.soundeditorbox)
        self.inp_soundeditor.setGeometry(20,65,255,21)
        self.button_sound = QtGui.QPushButton("...", self.soundeditorbox)
        self.button_sound.setGeometry(280,65,40,21)
        self.button_sound.clicked.connect(self.soundeditor)

        #--------------------------------------------------
        
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

        self.InitPreferences()

        self.show()

    def InitPreferences(self):
        if cfg.codeeditor is not "":
            self.inp_codeeditor.setText(cfg.codeeditor)
            self.useexternal_code.setChecked(True)
        else:
            self.usebuilt_code.setChecked(True)
            
        if cfg.imageeditor is not "":
            self.inp_imageeditor.setText(cfg.imageeditor)
            self.useexternal_img.setChecked(True)
        else:
            self.usebuilt_img.setChecked(True)
            
        if cfg.soundeditor is not "":
            self.inp_soundeditor.setText(name)
            self.useexternal_sound.setChecked(True)
        else:
            self.usebuilt_sound.setChecked(True)

    def built_codeeditor(self):
        self.inp_codeeditor.clear()

    def built_imageeditor(self):
        self.inp_imageeditor.clear()

    def built_soundeditor(self):
        self.inp_soundeditor.clear()
            
    def codeeditor(self):
        name = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Program',
                '', self.tr("Programs (*.exe)")))
        if name is not "":
            self.useexternal_code.setChecked(True)
            self.inp_codeeditor.setText(name)
        else:
            self.usebuilt_code.setChecked(True)
            
    def imageeditor(self):
        name = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Program',
                '', self.tr("Programs (*.exe)")))
        if name is not "":
            self.useexternal_img.setChecked(True)
            self.inp_imageeditor.setText(name)
        else:
            self.usebuilt_img.setChecked(True)
            
    def soundeditor(self):
        name = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Program',
                '', self.tr("Programs (*.exe)")))
        if name is not "":
            self.useexternal_sound.setChecked(True)
            self.inp_soundeditor.setText(name)
        else:
            self.usebuilt_sound.setChecked(True)
                
    def okbutton(self):
        if self.useexternal_code.isChecked():
            cfg.set('stellar', 'codeeditor', str(self.inp_codeeditor.text()))
            cfg.codeeditor = str(self.inp_codeeditor.text())
        else:
            cfg.set('stellar', 'codeeditor', '')
            cfg.codeeditor = ''
            
        if self.useexternal_sound.isChecked():
            cfg.set('stellar', 'soundeditor', str(self.inp_soundeditor.text()))
            cfg.soundeditor = str(self.inp_soundeditor.text())
        else:
            cfg.set('stellar', 'soundeditor', '')
            cfg.codeeditor = ''
            
        if self.useexternal_img.isChecked():
            cfg.set('stellar', 'imageeditor', str(self.inp_imageeditor.text()))
            cfg.imageeditor = str(self.inp_imageeditor.text())
        else:
            cfg.set('stellar', 'imageeditor', '')
            cfg.codeeditor = ''

        cfg.save()

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
