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

import sys, pygame.mixer, shutil
from PyQt4 import QtGui, QtCore


class SoundGUI(QtGui.QWidget):
  
    def __init__(self, main, FileName):
        super(SoundGUI, self).__init__(main)
        
        self.main = main
        self.FileName = FileName
        self.initUI()
        pygame.mixer.init()
        self.sound = pygame.mixer.music.load("Sound/%s.ogg"%(self.FileName))
        
        
        

    def initUI(self):

        #Groupbox Container-----------------------------------
        self.ContainerBox = QtGui.QGroupBox(self.main)
        self.ContainerBox.setObjectName("groupBox")
        self.ContainerBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.ContainerBox.setGeometry(QtCore.QRect(0,0,350,400))
        self.ContainerBox.setMinimumSize(350,400)

        self.LblName = QtGui.QLabel('Name:', self.ContainerBox) 
        self.LblName.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
        self.LblName.setGeometry(15, 15, 100, 25)

        self.qleSound = QtGui.QLineEdit(self.FileName, self.ContainerBox)
        self.qleSound.setGeometry(50, 15, 290, 25)

        self.BtnLoad = QtGui.QPushButton('Load Sound', self.ContainerBox)
        self.BtnLoad.setIcon(QtGui.QIcon('../../Data/folder.png'))
        self.BtnLoad.setGeometry(25, 55, 125, 25)
        
        self.BtnPlay = QtGui.QPushButton(self.ContainerBox)
        self.BtnPlay.setIcon(QtGui.QIcon('../../Data/playsound.png'))
        self.BtnPlay.setGeometry(160, 55, 35, 25)
        self.BtnPlay.clicked.connect(self.PlaySound)

        self.BtnStop = QtGui.QPushButton(self.ContainerBox)
        self.BtnStop.setIcon(QtGui.QIcon('../../Data/stopsound.png'))
        self.BtnStop.setGeometry(195, 55, 35, 25)
        self.BtnStop.clicked.connect(self.StopSound)

        self.BtnSave = QtGui.QPushButton('Save Sound', self.ContainerBox)
        self.BtnSave.setIcon(QtGui.QIcon('../../Data/save.png'))
        self.BtnSave.setGeometry(230, 55, 110, 25)
        self.BtnSave.clicked.connect(self.SaveSound)

        self.BtnEdit = QtGui.QPushButton('Edit Sound', self.ContainerBox)
        self.BtnEdit.setIcon(QtGui.QIcon('../../Data/editbutton.png'))        
        self.BtnEdit.setGeometry(25, 170, 125, 25)
        
        self.BtnOK = QtGui.QPushButton('OK', self.ContainerBox)
        self.BtnOK.setIcon(QtGui.QIcon('../../Data/accept.png'))
        self.BtnOK.setGeometry(25, 200, 125, 25)

        #Groupbox Options---------------------------
        self.OptionsBox = QtGui.QGroupBox(self.ContainerBox)
        self.OptionsBox.setGeometry(QtCore.QRect(15,85,135,70))
        self.OptionsBox.setObjectName("groupBox")
        self.OptionsBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.OptionsBox.setTitle("Options")

        self.RadioSound = QtGui.QRadioButton(self.OptionsBox)
        self.RadioSound.setGeometry(QtCore.QRect(15, 15, 150, 25))
        self.RadioSound.setText(" Normal Sound")
        self.RadioSound.toggle()
        
        self.RadioMusic = QtGui.QRadioButton(self.OptionsBox)
        self.RadioMusic.setGeometry(QtCore.QRect(15, 40, 150, 25))
        self.RadioMusic.setText(" Background Music")

        self.radioGroup = QtGui.QButtonGroup(self.OptionsBox)
        self.radioGroup.addButton(self.RadioSound, 1)
        self.radioGroup.addButton(self.RadioMusic, 2)

        #Groupbox Pan---------------------------
        self.PanBox = QtGui.QGroupBox(self.ContainerBox)
        self.PanBox.setGeometry(QtCore.QRect(160,85,175,70))
        self.PanBox.setObjectName("groupBox")
        self.PanBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.PanBox.setTitle("Pan")

        self.pan = QtGui.QSlider(QtCore.Qt.Horizontal, self.PanBox)
        self.pan.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pan.setGeometry(10, 40, 150, 25)
        self.pan.setRange(-50,51)
        self.pan.valueChanged[int].connect(self.changeValuePan)

        self.LblPan = QtGui.QLabel(self.PanBox) 
        self.LblPan.setText('Music is Centered') 
        self.LblPan.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) 
        self.LblPan.setGeometry(10, 10, 150, 25)

        #Groupbox Music---------------------------
        self.MusicBox = QtGui.QGroupBox(self.ContainerBox)
        self.MusicBox.setGeometry(QtCore.QRect(160,165,175,70))
        self.MusicBox.setObjectName("groupBox")
        self.MusicBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.MusicBox.setTitle("Pan")

        self.Music = QtGui.QSlider(QtCore.Qt.Horizontal, self.MusicBox)
        self.Music.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Music.setGeometry(10, 40, 150, 25)
        self.Music.setRange(-100,0)
        self.Music.valueChanged[int].connect(self.changeValueMusic)

        self.LblMusic = QtGui.QLabel(self.MusicBox) 
        self.LblMusic.setText('Volume is 0 percent muted') 
        self.LblMusic.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) 
        self.LblMusic.setGeometry(10, 10, 150, 25)
      

        #Main Window------------------------------------------
        self.ContainerBox.show()
 
    def changeValuePan(self, value):

        if (value)<0:
            NewValue = abs(value)
            self.LblPan.setText("%d %s " %(NewValue*2, " percent to the left"))
        elif (value)>1:
            NewValue = abs(value-1)
            self.LblPan.setText("%d %s " %(NewValue*2, " percent to the right"))
        else:
            self.LblPan.setText("%s " %("Music is Centered"))

    def changeValueMusic(self, value):

        self.LblMusic.setText("%s %d %s " %("Volume is ",abs(value), " percent muted"))

    def PlaySound(self):
        pygame.mixer.music.play()

    def StopSound(self):
        pygame.mixer.music.stop()

    def SaveSound(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Sound', 
                '', self.tr("Sound (*.ogg)"))

        if self.fname !='':
            shutil.copy("Sound/%s.ogg"%(self.FileName), self.fname)
            
    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
