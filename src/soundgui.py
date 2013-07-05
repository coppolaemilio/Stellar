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


import sys, pygame.mixer, shutil, os
from PyQt4 import QtGui, QtCore

if sys.version_info.major == 2:
    str = unicode

class SoundGUI(QtGui.QWidget):
  
    def __init__(self, main, FileName, dirname, tree):
        super(SoundGUI, self).__init__(main)
        
        self.main = main
        self.dirname = dirname
        self.FileName = FileName
        self.tree = tree

        self.extension = self.tree.snd_parser.get(self.FileName, 'extension')

        self.volume = int(self.tree.snd_parser.get(self.FileName, 'volume'))
        self.pan = int(self.tree.snd_parser.get(self.FileName, 'pan'))

        self.edit_pan = self.pan
        self.edit_volume = self.volume
        
        pygame.mixer.init()
        
        self.sound_file = os.path.join(self.dirname, "Sound", "%s.%s"%(self.FileName, self.extension))
        self.sound_handle = None
        self.sound = None
        self.channel = None #active Channel sound may be playing in
        
        #load sound file via handle
        self.LoadSound()
        
        #loading the file this way caused a leak, which led to problems with renaming/deleting the file
        #a handle needs to be created and closed in order for other functions to work properly
        #self.sound = pygame.mixer.music.load(os.path.join(self.dirname, "Sound", "%s.%s"%(self.FileName, self.extension)))
        
        self.initUI()
        
        #close the Sound, only load it when its needed.
        self.CloseSound()
        
    #clean up after self, if window is closed or terminated
    def closeEvent(self, event):
        self.StopSound()
        self.CloseSound()
    
    def initUI(self):
        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        
        self.LblName = QtGui.QLabel('Name:') 
        self.LblName.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 

        self.qleSound = QtGui.QLineEdit(self.FileName)

        self.BtnLoad = QtGui.QPushButton('Load Sound')
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        
        self.BtnPlay = QtGui.QPushButton()
        self.BtnPlay.setIcon(QtGui.QIcon('Data/playsound.png'))
        self.BtnPlay.clicked.connect(self.PlaySound)

        self.BtnStop = QtGui.QPushButton()
        self.BtnStop.setIcon(QtGui.QIcon('Data/stopsound.png'))
        self.BtnStop.setEnabled(False)
        self.BtnStop.clicked.connect(self.StopSound)

        self.BtnSave = QtGui.QPushButton('Save Sound')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.clicked.connect(self.SaveSound)

        self.BtnEdit = QtGui.QPushButton('Edit Sound')
        self.BtnEdit.setEnabled(False)
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))        
        
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setIcon(QtGui.QIcon('Data/accept.png'))
        self.BtnOK.clicked.connect(self.ok)


        #------------------------------------------------------------------------------------
        self.OptionsBox = QtGui.QGroupBox()
        self.OptionsBox.setObjectName("groupBox")
        self.OptionsBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.OptionsBox.setTitle("Options")

        self.RadioSound = QtGui.QRadioButton("Normal Sound")
        self.RadioSound.setEnabled(False)
        self.RadioSound.toggle()
        
        self.RadioMusic = QtGui.QRadioButton("Background Music")
        self.RadioMusic.setEnabled(False)
        
        self.optionslayout = QtGui.QGridLayout()
        self.optionslayout.setMargin(0)
        self.optionslayout.addWidget(self.RadioSound,1,0)
        self.optionslayout.addWidget(self.RadioMusic,2,0)
        self.OptionsBox.setLayout(self.optionslayout)
        #------------------------------------------------------------------------------------
        self.PanBox = QtGui.QGroupBox()
        self.PanBox.setObjectName("groupBox")
        self.PanBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.PanBox.setTitle("Pan")
        self.PanBox.setMinimumWidth(150)

        self.PanSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.PanSlider.setEnabled(True)
        self.PanSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.PanSlider.setRange(-50,50)
        self.PanSlider.setValue(self.pan)
        self.PanSlider.valueChanged[int].connect(self.changeValuePan)
        
        self.LblPan = QtGui.QLabel()
        self.LblPan.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        #set Pan Label Text based on pan value
        self.changeValuePan(self.pan)
        
        self.panlayout = QtGui.QGridLayout()
        self.panlayout.setMargin(0)
        self.panlayout.addWidget(self.PanSlider,1,0)
        self.panlayout.addWidget(self.LblPan,2,0)
        self.PanBox.setLayout(self.panlayout) 

        #------------------------------------------------------------------------------------
        self.MusicBox = QtGui.QGroupBox()
        self.MusicBox.setObjectName("groupBox")
        self.MusicBox.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.MusicBox.setTitle("Volume")

        self.Music = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.Music.setEnabled(True)
        self.Music.setFocusPolicy(QtCore.Qt.NoFocus) 
        self.Music.setRange(0,100)
        self.Music.setValue(self.volume)
        self.Music.valueChanged[int].connect(self.changeValueMusic)

        self.LblMusic = QtGui.QLabel() 
        self.LblMusic.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) 

        #change label text based on actual volume
        self.changeValueMusic(self.volume)
        
        self.musiclayout = QtGui.QGridLayout()
        self.musiclayout.setMargin(0)
        self.musiclayout.addWidget(self.Music,1,0)
        self.musiclayout.addWidget(self.LblMusic,2,0)
        self.MusicBox.setLayout(self.musiclayout) 
        #------------------------------------------------------------------------------------
        

        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.NameFrame = QtGui.QFrame()
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin(0)
        self.namelayout.addWidget(self.LblName,0,0)
        self.namelayout.addWidget(self.qleSound,0,1)
        self.NameFrame.setLayout(self.namelayout)

        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin (6)
        self.showlayout.addWidget(self.NameFrame,1,0)
        self.showlayout.addWidget(self.BtnLoad,2,0)
        self.showlayout.addWidget(self.BtnSave,3,0)
        self.showlayout.addWidget(self.BtnEdit,4,0)
        self.showlayout.addWidget(self.OptionsBox,5,0)
        
        self.showlayout.addItem(spacerItem,6,0)
        self.showlayout.addWidget(self.BtnOK,7,0)
                
        self.ShowFrame.setLayout(self.showlayout)



        self.RightFrame = QtGui.QFrame()
        self.rightlayout = QtGui.QGridLayout()
        self.rightlayout.setMargin(10)     
        self.rightlayout.addWidget(self.BtnPlay,0,0)
        self.rightlayout.addWidget(self.BtnStop,0,1)
        self.rightlayout.addWidget(self.PanBox,1,0,1,2)
        self.rightlayout.addWidget(self.MusicBox,2,0,2,2)
        
        self.RightFrame.setLayout(self.rightlayout)



        self.LastWidget = QtGui.QWidget()
        self.spritesplitter = QtGui.QHBoxLayout()
        self.rightlayout.setMargin(0)
        self.spritesplitter.addWidget(self.ShowFrame)
        self.spritesplitter.addWidget(self.RightFrame)
        
        self.LastWidget.setLayout(self.spritesplitter)
        self.ContainerGrid.addWidget(self.LastWidget)
        
        self.setLayout(self.ContainerGrid)
        
    def changeValuePan(self, value):
        self.edit_pan = value
        
        #convert self.pan into channel volumes using y = -x/100 + 1/2
        left = float(-self.edit_pan)/100.0 + .5
        right = 1 - left
                
        if left != right:
            self.LblPan.setText("%d%s, %d%s" %(left*100, "% Left", right*100, "% Right"))
        else:
            self.LblPan.setText("%s " %("Music is Centered"))

        #save changed value to config
        self.pan = self.edit_pan
        self.tree.snd_parser.set(self.FileName, 'pan', self.pan)
        
        #if sound is playing, update it with new information
        self.SetSoundVolume()

    def changeValueMusic(self, value):
        self.edit_volume = value
        self.LblMusic.setText("%s %d%s " %("Volume is set to", value, "% "))
        
        #save changed value to config
        self.volume = self.edit_volume
        self.tree.snd_parser.set(self.FileName, 'volume', self.volume)
        
        #if sound is playing, update it with new information
        self.SetSoundVolume()

    def LoadSound(self):
        if self.sound is None:
            self.sound_handle = open(self.sound_file, 'rb')
            self.sound = pygame.mixer.Sound(self.sound_handle)
        
    def CloseSound(self):
        if self.sound:
            self.sound_handle.close()
            self.sound = None
    
    def SetSoundVolume(self):
        #calculate volume of sound based on pan, volume
        if self.channel is not None:
            if self.channel.get_busy():
            
                #convert self.pan into channel volumes using y = -x/100 + 1/2
                left = float(-self.pan)/100.0 + .5
                right = 1 - left
                
                #adjust left and right pan by the overall volume
                left = left * (self.volume)/100
                right = right * (self.volume)/100
                
                self.channel.set_volume(left, right)
    
    def PlaySound(self):
        self.LoadSound()
        
        playSound = False
        
        if self.channel is None:
            playSound = True
        else:
            if not self.channel.get_busy():
                playSound = True
        
        if playSound:
            self.channel = self.sound.play(-1)
            
            #update sound's volume/pan
            self.SetSoundVolume()
                            
            #disable play button when sound is playing
            self.BtnPlay.setEnabled(False)
            self.BtnStop.setEnabled(True)
    
    def StopSound(self):
        if self.channel.get_busy():
            self.channel.stop()
            self.sound.stop()
            self.BtnPlay.setEnabled(True)
            self.BtnStop.setEnabled(False)
        
    def SaveSound(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Sound', 
                '', self.tr("Sound (*.ogg *.wav)"))

        if self.fname !='':
            shutil.copy(os.path.join(self.dirname, "Sound", "%s.%s"%(self.FileName, self.extension)), self.fname)

    def ok(self):
        snd = str(self.qleSound.text())
        # if file had a new name, go through renaming process
        if str(self.FileName) != snd:
            #if sound is playing, stop it
            self.StopSound()
            
            #close sound, can't be renamed if in use by another process
            self.CloseSound()
            
            #hyphens result in problems, convert them to underscores           
            snd = snd.replace('-', '_')
            
            #increment name automatically if section already exists            
            new_snd = snd
            i = 0
            while self.tree.snd_parser.has_section(new_snd):
                i += 1
                new_snd = snd + '_' + str(i)
            
            snd = new_snd
            
            #update soundconfig
            self.tree.snd_parser.remove_section(self.FileName)
            self.tree.snd_parser.add_section(snd)

            # get old and new filename for rename
            in_fname = os.path.join(self.dirname, 'Sound', "%s.%s" %
                                    (self.FileName, self.extension))
            out_fname = os.path.join(self.dirname, 'Sound', "%s.%s" % 
                                    (snd, self.extension)) 
            
            #rename the sound file
            try:
                os.rename(in_fname, out_fname)
            except OSError as exc:
                QtGui.QMessageBox.question(self, "File could not be renamed",
                    "File could not be rename: "+exc.strerror,
                    QtGui.QMessageBox.Ok)
           
            #update current object with new sound file
            self.FileName = str(snd)
            
            self.sound_file = os.path.join(self.dirname, "Sound", "%s.%s"%
                (self.FileName, self.extension))
                

        self.tree.snd_parser.set(self.FileName, 'extension', self.extension)

        self.pan = self.edit_pan
        self.volume = self.edit_volume
        self.tree.snd_parser.set(self.FileName, 'pan', self.pan)
        self.tree.snd_parser.set(self.FileName, 'volume', self.volume)

        self.tree.write_sound()

        self.main.updatetree()
        
        #if sound is still open, close it - it's not needed
        self.CloseSound()
        
        self.main.qmdiarea.activeSubWindow().close()
            
    def ShowMe(self):
        self.ContainerBox.show()
        
    def HideMe(self):
        self.ContainerBox.hide()
