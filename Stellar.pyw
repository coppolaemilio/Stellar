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

import cfg

"""
Stellar %s
""" % cfg.__version__

import sys
import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil
from splashscreen import Start
from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from scriptgui import ScriptGUI
from objectgui import ObjectGUI
from PyQt4 import QtCore, QtGui




class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, main):
        super(TreeWidget, self).__init__(main)
        self.header().setHidden(True)
        self.setWindowTitle('Resources')
        self.main = main
        self.dirname = ''
        self.connect(self, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),self.DoEvent)

        self.PathSprite = ''
        self.PathSound = ''
        self.PathFonts = ''
        self.PathScripts = ''
        self.PathObjects = ''
        self.PathRooms = ''

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        insertAction = menu.addAction("Insert")
        insertAction.triggered.connect(self.AddSprChild)
        
        duplicateAction = menu.addAction("Duplicate")
        duplicateAction.setShortcut('Alt+Ins')
        duplicateAction.setDisabled (True)
        menu.addSeparator()
        insertgroupAction = menu.addAction("Insert Group")
        insertgroupAction.setShortcut('Shift+Ins')
        insertgroupAction.setDisabled (True)
        menu.addSeparator()
        deleteAction = menu.addAction("Delete")
        deleteAction.setShortcut('Shift+Del')
        deleteAction.setDisabled (True)
        menu.addSeparator()
        renameAction = menu.addAction("Rename")
        renameAction.setShortcut('F2')
        renameAction.setDisabled (True)
        menu.addSeparator()
        propertiesAction = menu.addAction("Properties...")
        propertiesAction.setShortcut('Alt+Enter')
        propertiesAction.triggered.connect(self.DoEvent)
        action = menu.exec_(self.mapToGlobal(event.pos()))


    def DoEvent(self):
        item = self.currentItem()
        bln = True
        if not item.parent() == None:
            if item.parent().text(0) == "Sprites":

                for index, sprite in enumerate(self.main.Sprites):
                    if sprite[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_sprites.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(0)
                        break

                if bln==True:
                
                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_sprites.addTab(self.main.tab, item.text(0))

                    self.main.Sprites.append([SpriteGUI(self.main.Frame,item.text(0), self.main.dirname),item.text(0)])
                    self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-3, self.main.tab_widget.height()-42)
                    self.main.Sprites[len(self.main.Sprites)-1][0].scrollArea.setGeometry(350, 0, self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.width()-350, self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.height())
                    
                    self.main.tab_widget_sprites.setCurrentIndex(len(self.main.Sprites)-1)
                    self.main.tab_widget_sprites.setTabIcon(len(self.main.Sprites)-1,(QtGui.QIcon(os.path.join(self.main.dirname, 'Sprites', str(item.text(0))))))
                    self.main.tab_widget.setCurrentIndex(0)
                    
                    
            elif item.parent().text(0) == "Sound":

                for index, sound in enumerate(self.main.Sound):
                    if sound[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_sound.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(1)
                        break

                if bln==True:
                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_sound.addTab(self.main.tab, item.text(0))

                    self.main.Sound.append([SoundGUI(self.main.Frame,item.text(0), self.main.dirname),item.text(0)])
                    self.main.Sound[len(self.main.Sound)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-3, self.main.tab_widget.height()-42)

                    

                    self.main.tab_widget_sound.setCurrentIndex(len(self.main.Sound)-1)
                    self.main.tab_widget.setCurrentIndex(1)

            elif item.parent().text(0) == "Fonts":

                for index, font in enumerate(self.main.Fonts):
                    if font[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_font.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(2)
                        break

                if bln==True:
                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_font.addTab(self.main.tab, item.text(0))

                    self.main.Fonts.append([FontGUI(self.main.Frame, self.main.dirname),item.text(0)])
                    self.main.Fonts[len(self.main.Fonts)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-4, self.main.tab_widget.height()-42)

                    
                    self.main.tab_widget_font.setCurrentIndex(len(self.main.Fonts)-1)
                    self.main.tab_widget.setCurrentIndex(2)

            elif item.parent().text(0) == "Scripts":

                for index, script in enumerate(self.main.Scripts):
                    if script[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_scripts.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(3)
                        break

                if bln==True:
                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_scripts.addTab(self.main.tab, item.text(0))

                    self.main.Scripts.append([ScriptGUI(self.main.Frame,item.text(0), self.main.dirname),item.text(0)])
                    self.main.Scripts[len(self.main.Scripts)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-3, self.main.tab_widget.height()-42)
                    self.main.Scripts[len(self.main.Scripts)-1][0].textEdit.setGeometry(0, 30, self.main.tab_widget.width()-3, self.main.tab_widget.height()-70)
					
                    self.main.tab_widget_scripts.setCurrentIndex(len(self.main.Scripts)-1)
                    self.main.tab_widget.setCurrentIndex(3)
                    
            elif item.parent().text(0) == "Objects":

                for index, object in enumerate(self.main.Objects):
                    if object[1] == item.text(0):
                        bln = False
                        self.main.tab_widget_objects.setCurrentIndex(index)
                        self.main.tab_widget.setCurrentIndex(4)
                        break

                if bln==True:
                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_objects.addTab(self.main.tab, item.text(0))

                    self.main.Objects.append([ObjectGUI(self.main.Frame,item.text(0), self.main.dirname),item.text(0)])
                    self.main.Objects[len(self.main.Objects)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-3, self.main.tab_widget.height()-42)
                    self.main.tab_widget_objects.setCurrentIndex(len(self.main.Objects)-1)
                    self.main.tab_widget.setCurrentIndex(4)

                    

    def InitParent(self):

        #Sprites------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSprite = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sprites'))
        self.ParentSprite.setIcon(0,icon)

        #sound--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSound = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sound'))
        self.ParentSound.setIcon(0,icon)
        
        #Fonts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentFonts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Fonts'))
        self.ParentFonts.setIcon(0,icon)

        #Scripts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentScripts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Scripts'))
        self.ParentScripts.setIcon(0,icon)

        #Objects------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentObjects = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Objects'))
        self.ParentObjects.setIcon(0,icon)

        #Rooms--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentRooms = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Rooms'))
        self.ParentRooms.setIcon(0,icon)

        #Included Files-----------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentIncluded = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Included Files'))
        self.ParentIncluded.setIcon(0,icon)

        #Extensions---------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentExtensions = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Extensions'))
        self.ParentExtensions.setIcon(0,icon)

    def InitChild(self):
        self.dirname = self.main.dirname
        self.PathSprite = os.path.join(self.dirname, "Sprites")
        self.PathSound = os.path.join(self.dirname, "Sound")
        self.PathFonts = os.path.join(self.dirname, "Fonts")
        self.PathScripts = os.path.join(self.dirname, "Scripts")
        self.PathObjects = os.path.join(self.dirname, "Objects")
        self.PathRooms = os.path.join(self.dirname, "Rooms") 

        #Sprites----------------------------------
        for ChildSprite in os.listdir(self.PathSprite):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.PathSprite, ChildSprite)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(ChildSprite[:-4])).setIcon(0,icon)      

        #Sound------------------------------------
        for ChildSound in os.listdir(self.PathSound):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(ChildSound[:-4])).setIcon(0,icon)

        #Fonts------------------------------------
        for ChildFont in os.listdir(self.PathFonts):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(ChildFont[:-4])).setIcon(0,icon)

        #Scripts------------------------------------
        for ChildScript in os.listdir(self.PathScripts):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "addscript.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(ChildScript[:-3])).setIcon(0,icon)

        #Objects----------------------------------
        for ChildObject in os.listdir(self.PathObjects):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentObjects, QtCore.QStringList(ChildObject[:-3])).setIcon(0,icon)

        #Rooms------------------------------------
        for ChildRoom in os.listdir(self.PathRooms):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "game.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentRooms, QtCore.QStringList(ChildRoom[:-4])).setIcon(0,icon)


    def AddSprChild(self,name):
        #Sprites----------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.PathSprite, name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(name[:-4])).setIcon(0,icon)    

    def AddSndChild(self,name):
        #Sound------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(name[:-4])).setIcon(0,icon)

    def AddScriptChild(self,name):
        #Script------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(name)).setIcon(0,icon)
        
    def AddObjectChild(self,name):
        #Object------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentObjects, QtCore.QStringList(name)).setIcon(0,icon)

    def AddFontChild(self,name):
        #Font------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(name[:-4])).setIcon(0,icon)        
   
class Stellar(QtGui.QMainWindow,QtGui.QTextEdit,QtGui.QTreeWidget):
    
    def __init__(self):
        super(Stellar, self).__init__()
        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.Objects=[]
        self.Rooms=[]
        self.initUI()
        
    def initUI(self):
        
        #Saving where you opened the program for opening a new window in the future
        self.stellardir = inspect.getfile(inspect.currentframe())
        dirname, filename = os.path.split(os.path.abspath(self.stellardir))
        self.pref = "preferences.pyw"
        self.stellarnew = "Stellar.pyw"
        
        #ACTIONS -------------------------------
        
        def newAction(name, image, trigger, statusTip, shortcut='', enabled=True):
            action = QtGui.QAction(QtGui.QIcon('Data/'+image), name, self)
            action.setShortcut(shortcut)
            action.setStatusTip(statusTip)
            action.triggered.connect(trigger)
            action.setEnabled(enabled)
            return action
        
        projectAction = newAction('New Project', 'new.png', self.newproject, 'New Project', 'Ctrl+N', False)
        
        loadAction = newAction('Open...', 'folder.png', self.openfile, 'Open Game.', 'Ctrl+O')
        saveAction = newAction('Save Game As...', 'save.png', self.savefile, 'Save Game As...', 'Ctrl+Shift+S')
        fsaveAction = newAction('Save', 'save.png', self.fsavefile, 'Save Game', 'Ctrl+S')
        
        shareAction = newAction('Share', 'publish.png', self.sharegame, 'Share your creations with the community!')
        buildAction = newAction('Build', 'build.png', self.Build, 'Build game.')
        playAction = newAction('Run', 'play.png', self.playgame, 'Test your game.', 'F5')
        playDebugAction = newAction('Run in debug mode', 'playdebug.png', self.playgame, 'Test your game on debug mode.', 'F6')
        
        spriteAction = newAction('Add Sprite', 'sprite.png', self.addsprite, 'Add a sprite to the game.')
        animatedspriteAction = newAction('Add Animated Sprite', 'gif.png', self.addAnimatedSprite, 'Add an animated sprite to the game.')
        soundAction = newAction('Add Sound', 'sound.png', self.addsound, 'Add a sound to the game.')
        fontAction = newAction('Add Font', 'font.png', self.addfont, 'Add a font to the game.')
        objectAction = newAction('Add Object', 'object.png', self.addObject, 'Add an object to the game.')
        roomAction = newAction('Add Room', 'room.png', self.addRoom, 'Add an room to the game.')
        scriptAction = newAction('Add Script', 'addscript.png', self.addScript, 'Add A Script To The Game.')
        
        zoominAction = newAction('Zoom In', 'plus.png', self.onZoomInClicked, 'Zoom in the font of the editor.')
        zoomoutAction = newAction('Zoom Out', 'minus.png', self.onZoomOutClicked, 'Zoom out the font of the editor.')
        sfontAction = newAction('Set Font', 'font.png', self.fontdialog, 'Change the font of the text editor.')

        exitAction = newAction('Exit', 'exit.png', self.close, 'Exit application.', 'Ctrl+Q')
        aboutAction = newAction('About', 'info.png', self.close, 'About Stellar.')
        preferencesAction = newAction('Preferences...', 'preferences.png', self.preferencesopen, 'Change Stellar preferences.')
        

        self.statusBar()

        #MENU BAR --------------------------------------
        menubar = self.menuBar()
        
        def addBar(bar, action):
            if bar == 'menubar':
                self.fileMenu = menubar.addMenu(action[0])
            
            for i in range(1, len(action)):
                if action[i] == '|':
                    self.fileMenu.addSeparator()
                else:
                    if bar == 'menubar':
                        self.fileMenu.addAction(action[i])
                    elif bar == 'toolbar': 
                        self.toolbar.addAction(action[i])
            
                        
                
        addBar('menubar', ['&File', projectAction, loadAction, '|', fsaveAction, saveAction, '|',\
                                buildAction, shareAction, '|', preferencesAction, '|', exitAction])
        
        addBar('menubar', ['&Resources', spriteAction, animatedspriteAction, soundAction, objectAction,\
                                fontAction, roomAction])
        
        addBar('menubar', ['&Scripts', scriptAction])
        addBar('menubar', ['&Run', playAction, playDebugAction])
        addBar('menubar', ['&Text Editor', zoominAction, zoomoutAction, sfontAction])
        addBar('menubar', ['&Help', aboutAction])
        
        

        #TOOL BAR --------------------------------------
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (False)
        
        addBar('toolbar', [ None, projectAction, fsaveAction, loadAction, '|', buildAction, shareAction, '|',\
                                playAction, '|', spriteAction, animatedspriteAction, soundAction, fontAction,\
                                scriptAction, objectAction, roomAction, '|', aboutAction, zoominAction, zoomoutAction ] )
        
        
        

        #Qtree----------------------------------------
        self.tree = TreeWidget(self)
        self.tree.resize(200, self.height()-125)
        self.tree.move(0,self.toolbar.height()+self.fileMenu.height())
        self.tree.show()

        #QLogo-----------------------------------------
        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap("Data/Logo.png"))
        self.logo.resize(200,55)
        self.logo.move(0,self.height()-122+self.toolbar.height()+self.fileMenu.height())
        self.logo.show()

        #QFrame ---------------------------------------
        self.Frame = QtGui.QFrame(self)

        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.setMovable (False) # True will give some errors, could be fixed though with an array when True
        
        def create_tab(names, tab_widget):
            for name in names:
                tab = QtGui.QWidget()
                vertical = QtGui.QVBoxLayout(tab) 
                tab_widget.addTab(tab, name)
        
        
        create_tab( ["Sprites", "Sound", "Fonts", "Scripts", "Objects", "Rooms"] , self.tab_widget)
        

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.tab_widget)
        self.Frame.setLayout(self.vbox)
        self.connect(self.tab_widget, QtCore.SIGNAL("currentChanged(int)"), self.TopTabChanged)


        
        def add_tab_widget(event):
            tab_widget = QtGui.QTabWidget(self.tab_widget)
            tab_widget.setMovable (True)
            tab_widget.setTabsClosable (True)
            tab_widget.setGeometry(0, 22, self.tab_widget.width(), self.tab_widget.height()-22)
            self.connect(tab_widget, QtCore.SIGNAL("currentChanged(int)"), event)
            self.connect(tab_widget, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeTab)
            return tab_widget
        

        self.tab_widget_sprites = add_tab_widget(self.SpriteTabChanged)         #QFrame QTab Sprites
        self.tab_widget_sound = add_tab_widget(self.SoundTabChanged)            #QFrame QTab Sounds
        self.tab_widget_font = add_tab_widget(self.FontsTabChanged)             #QFrame QTab Font
        self.tab_widget_scripts = add_tab_widget(self.ScriptTabChanged)         #QFrame QTab Rooms
        self.tab_widget_objects = add_tab_widget(self.ObjectsTabChanged)        #QFrame QTab Objects
        self.tab_widget_rooms = add_tab_widget(self.RoomsTabChanged)            #QFrame QTab Rooms
        



        #WINDOW----------------------------------------
        self.setGeometry(200, 200, 800, 600)
        self.setWindowIcon(QtGui.QIcon('Data/icon.png'))
        self.fname = "<New game>"
        self.dirname = ''
        self.setWindowTitle('%s - Stellar %s'% (self.fname, cfg.__version__))
        self.setMinimumSize(800,600)
        self.center()
        self.start = Start(self)
        self.tab_widget.setCurrentIndex(0)
        self.TopTabChanged(0)

    def closeTab(self, index):
        self.tab_widget_sprites.removeTab(index)

    def TopTabChanged(self, index):

        #Show Sprite----------------------
        if index == 0:
            self.tab_widget_sprites.show()
            self.SpriteTabChanged(self.tab_widget_sprites.currentIndex())
            
            #Hide Sound
            self.tab_widget_sound.hide()
            for Sound in self.Sound:
                Sound[0].HideMe()

            #Hide Script
            self.tab_widget_scripts.hide()
            for Script in self.Scripts:
                Script[0].HideMe()

            #Hide Font
            self.tab_widget_font.hide()
            for font in self.Fonts:
                font[0].HideMe()

            #Hide Objects
            self.tab_widget_objects.hide()
            for objects in self.Objects:
                objects[0].HideMe()

            #Hide Rooms
            self.tab_widget_rooms.hide()
            for room in self.Rooms:
                room[0].HideMe()

        #Show Sound----------------------
        if index == 1:
            self.tab_widget_sound.show()
            self.SoundTabChanged(self.tab_widget_sound.currentIndex())

            #Hide Sprite
            self.tab_widget_sprites.hide()
            for Sprite in self.Sprites:
                Sprite[0].HideMe()

            #Hide Script
            self.tab_widget_scripts.hide()
            for Script in self.Scripts:
                Script[0].HideMe()

            #Hide Font
            self.tab_widget_font.hide()
            for font in self.Fonts:
                font[0].HideMe()
                
            #Hide Objects
            self.tab_widget_objects.hide()
            for objects in self.Objects:
                objects[0].HideMe()

            #Hide Rooms
            self.tab_widget_rooms.hide()
            for room in self.Rooms:
                room[0].HideMe()

        #Show Fonts----------------------
        if index == 2:
            self.tab_widget_font.show()
            self.FontsTabChanged(self.tab_widget_font.currentIndex())

            #Hide Sprite
            self.tab_widget_sprites.hide()
            for Sprite in self.Sprites:
                Sprite[0].HideMe()

            #Hide Script
            self.tab_widget_scripts.hide()
            for Script in self.Scripts:
                Script[0].HideMe()

            #Hide Sound
            self.tab_widget_sound.hide()
            for Sound in self.Sound:
                Sound[0].HideMe()
                
            #Hide Objects
            self.tab_widget_objects.hide()
            for objects in self.Objects:
                objects[0].HideMe()

            #Hide Rooms
            self.tab_widget_rooms.hide()
            for room in self.Rooms:
                room[0].HideMe()

        #Show Script----------------------
        if index == 3:
            self.tab_widget_scripts.show()
            self.ScriptTabChanged(self.tab_widget_scripts.currentIndex())

            #Hide Sprite
            self.tab_widget_sprites.hide()
            for Sprite in self.Sprites:
                Sprite[0].HideMe()
                
            #Hide Sound
            self.tab_widget_sound.hide()
            for Sound in self.Sound:
                Sound[0].HideMe()

            #Hide Font
            self.tab_widget_font.hide()
            for font in self.Fonts:
                font[0].HideMe()
                
            #Hide Objects
            self.tab_widget_objects.hide()
            for objects in self.Objects:
                objects[0].HideMe()

            #Hide Rooms
            self.tab_widget_rooms.hide()
            for room in self.Rooms:
                room[0].HideMe()

        #Show Objects----------------------
        if index == 4:
            self.tab_widget_objects.show()
            self.ScriptTabChanged(self.tab_widget_objects.currentIndex())

            #Hide Sprite
            self.tab_widget_sprites.hide()
            for Sprite in self.Sprites:
                Sprite[0].HideMe()
                
            #Hide Sound
            self.tab_widget_sound.hide()
            for Sound in self.Sound:
                Sound[0].HideMe()

            #Hide Font
            self.tab_widget_font.hide()
            for font in self.Fonts:
                font[0].HideMe()

            #Hide Script
            self.tab_widget_scripts.hide()
            for Script in self.Scripts:
                Script[0].HideMe()

            #Hide Rooms
            self.tab_widget_rooms.hide()
            for room in self.Rooms:
                room[0].HideMe()

        #Show Rooms----------------------
        if index == 5:
            self.tab_widget_objects.show()
            self.ScriptTabChanged(self.tab_widget_objects.currentIndex())

            #Hide Sprite
            self.tab_widget_sprites.hide()
            for Sprite in self.Sprites:
                Sprite[0].HideMe()
                
            #Hide Sound
            self.tab_widget_sound.hide()
            for Sound in self.Sound:
                Sound[0].HideMe()

            #Hide Font
            self.tab_widget_font.hide()
            for font in self.Fonts:
                font[0].HideMe()

            #Hide Script
            self.tab_widget_scripts.hide()
            for Script in self.Scripts:
                Script[0].HideMe()

            #Hide Objects
            self.tab_widget_objects.hide()
            for objects in self.Objects:
                objects[0].HideMe()

    def SpriteTabChanged(self, index):
        for Zet, Sprite in enumerate(self.Sprites):
            if Zet == index:
                Sprite[0].ShowMe()
            else:
                Sprite[0].HideMe()

    def SoundTabChanged(self, index):
        for Zet, Sound in enumerate(self.Sound):
            if Zet == index:
                Sound[0].ShowMe()
            else:
                Sound[0].HideMe()

    def ScriptTabChanged(self, index):
        for Zet, Script in enumerate(self.Scripts):
            if Zet == index:
                Script[0].ShowMe()
            else:
                Script[0].HideMe()

    def FontsTabChanged(self, index):
        for Zet, Fonts in enumerate(self.Fonts):
            if Zet == index:
                Fonts[0].ShowMe()
            else:
                Fonts[0].HideMe()

    def ObjectsTabChanged(self, index):
        for Zet, Objects in enumerate(self.Objects):
            if Zet == index:
                Objects[0].ShowMe()
            else:
                Objects[0].HideMe()

    def RoomsTabChanged(self, index):
        for Zet, Room in enumerate(self.Rooms):
            if Zet == index:
                Room[0].ShowMe()
            else:
                Room[0].HideMe() 


    def resizeEvent(self, event):
        self.tree.resize(200, self.height()-125)
        self.tree.move(0,self.toolbar.height()+self.fileMenu.height())
        self.logo.move(0,self.height()-122+self.toolbar.height()+self.fileMenu.height())
        self.Frame.setGeometry(QtCore.QRect(200,self.toolbar.height()+self.fileMenu.height()-10,self.width()-200,self.height()-(self.toolbar.height()+self.fileMenu.height())*0.8))        
        self.tab_widget.setGeometry(9, 9, self.Frame.width()-18, self.Frame.height()-18)
        self.tab_widget_sprites.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-18)
        self.tab_widget_sound.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-18)
        self.tab_widget_font.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-18)
        self.tab_widget_scripts.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-18)
        self.tab_widget_objects.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-18)

        for sprite in self.Sprites:
            sprite[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)
            sprite[0].scrollArea.setGeometry(350, 0, sprite[0].ContainerBox.width()-350, sprite[0].ContainerBox.height())

        for sound in self.Sound:
            sound[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)

        for font in self.Fonts:
            font[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)

        for scripts in self.Scripts:
            scripts[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)

        for objects in self.Objects:
            objects[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)

        for room in self.Rooms:
            room[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)
            
    def preferencesopen(self):
        
        print self.pref
        execfile(self.pref, {})

    def newproject(self):
        print "To do"

        
    def Build(self):
        print "To do"
        
    def aboutStellar(self):
        about = QtGui.QMessageBox.information(self, 'About Stellar',
            "<center><b>Stellar</b> is an open-source program inspired in 'Game Maker' for <b>Pygame/Python</b> development.<br/><br/>    The goal is to have a program to design your own games using easy-to-learn drag-and-drop actions and different easy tools for begginers.<br/>    When you become more experienced, you will have the possibilitie of writing and editing your game with the full flexibility given by <b>Python/Pygame</b>.<br/><br/>    This is an uncomplete version, it has almost nothing, but I would love to be helped by anyone interested in the project.<br/><br/>    You are free to distribute the games you create with <b>Stellar</b> in any way you like. You can even sell them.<br/>     This of course assumes that the sprites, images, and sounds you use can be distributed or sold as well.<br/><HR><br/>  You can contribute to the project on our Github:<br/><a href=\'https://github.com/Coppolaemilio/stellar'>Stellar on Git</a></center>", QtGui.QMessageBox.Ok)
            
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, "Exit Stellar", "Save Python File before Exit?",
                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            f = open(os.path.join(self.dirname, os.path.basename(self.fname)), 'w')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, cfg.__version__))

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)
                f.close()
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.accept()
        else:
            event.ignore()
            
    def openfile(self):
        print "To do"

    def sharegame(self):
        webbrowser.open("http://www.pygame.org/news.html")
            
    def savefile(self):
        print "To do"
        
            
    def fsavefile(self):
        print "To do"

    def onZoomInClicked(self):
        self.textEdit.zoomIn(+1)

    def onZoomOutClicked(self):
        self.textEdit.zoomOut(+1)       
        
    def playgame(self):
        print "To do"

    def fontdialog(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def addsprite(self):

        self.asprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
        if self.asprite !='':
            for sprite in self.asprite:
                d = os.path.basename(str(sprite))
                if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                    if d[:4]=='spr_':
                        shutil.copy(sprite, os.path.join('Sprites', d))
                        self.tree.AddSprChild(d)
                    else:
                        shutil.copy(sprite, os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                        self.tree.AddSprChild('spr_' + d)
            

    def addAnimatedSprite(self):

        self.aGIFsprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Animated Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
        if self.aGIFsprite !='':
            for sprite in self.aGIFsprite:
                d = os.path.basename(str(sprite))
                if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                    if d[:4]=='spr_':
                        shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', d))
                        self.tree.AddSprChild(d)
                    else:
                        shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                        self.tree.AddSprChild('spr_' + d)


    def addsound(self):

        self.asound = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sound(s)', 
                '', self.tr("Sound file (*.ogg *.wav)"))
        
        if self.asound !='':
            for sound in self.asound:
                d = os.path.basename(str(sound))
                if not os.path.exists(os.path.join(self.dirname, 'Sound', d)):
                    if d[:4]=='snd_':
                        shutil.copy(sound,os.path.join(self.dirname, 'Sound', d))
                        self.tree.AddSndChild(d)
                    else:
                        shutil.copy(sound,os.path.join(self.dirname, 'Sound', 'snd_{0}'.format(d)))
                        self.tree.AddSndChild('snd_'+d)

    def addfont(self):

        self.afont = QtGui.QFileDialog.getOpenFileNames(self, 'Open Font(s)', 
                '', self.tr("Font file (*.ttf *.ttc *.fon)"))
        
        if self.afont !='':
            for font in self.afont:
                d = os.path.basename(str(font))
                f = os.path.splitext(d)[0]
                if not os.path.exists(os.path.join(self.dirname, 'Fonts', d)):
                    if d[:5]=='font_':
                        shutil.copy(font,os.path.join(self.dirname, 'Fonts', d))
                        self.tree.AddFontChild(d)
                    else:
                        shutil.copy(font,os.path.join(self.dirname, 'Fonts', 'font_{0}'.format(d)))
                        self.tree.AddFontChild('font_'+d)         

    def addScript(self):
        script = "script_"
        scriptnumber = 0
        TmpScript = script + str(scriptnumber)
        while os.path.exists(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript))):
            scriptnumber += 1 
            TmpScript = script + str(scriptnumber)
        f = open(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript)),'w')
        f.close()
        self.tree.AddScriptChild(TmpScript)

    def addObject(self):
        object = "obj_"
        objectnumber = 0
        TmpObject= object + str(objectnumber)
        while os.path.exists(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject))):
            objectnumber += 1 
            TmpObject = object + str(objectnumber)
        f = open(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject)),'w')
        f.close()
        self.tree.AddObjectChild(TmpObject)

    def addRoom(self):
        pass


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


      
def main():
    app = QtGui.QApplication(sys.argv)
    st = Stellar()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
