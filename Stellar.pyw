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

__version__ = "0.3.0"

"""
Stellar %s
""" % __version__

import sys
import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil
from autocomplete import CompletionTextEdit
from splashscreen import Start
from scriptlist import ScriptList
from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from PyQt4 import QtCore, QtGui




class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, main):
        super(TreeWidget, self).__init__(main)
        self.header().setHidden(True)
        self.setWindowTitle('Resources')
        self.main = main
        self.connect(self, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),self.DoEvent)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        insertAction = menu.addAction("Insert")
        insertAction.setDisabled (True)
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

                    self.main.Sprites.append([SpriteGUI(self.main.Frame,item.text(0)),item.text(0)])
                    self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.setGeometry(10, 50, self.main.tab_widget.width()-3, self.main.tab_widget.height()-42)
                    self.main.Sprites[len(self.main.Sprites)-1][0].scrollArea.setGeometry(350, 0, self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.width()-350, self.main.Sprites[len(self.main.Sprites)-1][0].ContainerBox.height())
                    
                    self.main.tab_widget_sprites.setCurrentIndex(len(self.main.Sprites)-1)
                    self.main.tab_widget_sprites.setTabIcon(len(self.main.Sprites)-1,(QtGui.QIcon(os.path.join('Sprites', str(item.text(0))))))
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

                    self.main.Sound.append([SoundGUI(self.main.Frame,item.text(0)),item.text(0)])
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

                    self.main.Fonts.append([FontGUI(self.main.Frame),item.text(0)])
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
                    #editor = self.main.textEdit = CompletionTextEdit(self.main.Frame)
                    editor = self.main.textEdit = CompletionTextEdit()
                    highlight = syntax.PythonHighlighter(editor.document())
                    self.main.textEdit.zoomIn(+4)
                    self.main.textEdit.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

                    self.main.tab = QtGui.QWidget()
                    self.main.tab_widget_scripts.addTab(self.main.tab, item.text(0))

                    self.main.Scripts.append([self.main.textEdit,item.text(0)])
                    self.main.Scripts[len(self.main.Scripts)-1][0].setGeometry(0, 0, 800, 600)
                    self.main.Scripts[len(self.main.Scripts)-1][0].center()

                    self.main.tab_widget_scripts.setCurrentIndex(len(self.main.Scripts)-1)
                    self.main.tab_widget.setCurrentIndex(3)

                    

    def InitParent(self):

        #Sprites------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSprite = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sprites'))
        self.ParentSprite.setIcon(0,icon)

        #sound--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentSound = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Sound'))
        self.ParentSound.setIcon(0,icon)
        
        #Fonts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentFonts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Fonts'))
        self.ParentFonts.setIcon(0,icon)

        #Scripts--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentScripts = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Scripts'))
        self.ParentScripts.setIcon(0,icon)

        #Objects------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentObjects = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Objects'))
        self.ParentObjects.setIcon(0,icon)

        #Rooms--------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentRooms = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Rooms'))
        self.ParentRooms.setIcon(0,icon)

        #Included Files-----------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentIncluded = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Included Files'))
        self.ParentIncluded.setIcon(0,icon)

        #Extensions---------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParentExtensions = QtGui.QTreeWidgetItem(self, QtCore.QStringList('Extensions'))
        self.ParentExtensions.setIcon(0,icon)

    def InitChild(self):
        PathSprite = "Sprites"
        PathSound = "Sound"
        PathFonts = "Fonts"
        PathScripts = "Scripts"
        PathObjects = "Objects"
        PathRooms = "Rooms"
        

        #Sprites----------------------------------
        for ChildSprite in os.listdir(PathSprite):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Sprites", ChildSprite)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(ChildSprite[:-4])).setIcon(0,icon)      

        #Sound------------------------------------
        for ChildSound in os.listdir(PathSound):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(ChildSound[:-4])).setIcon(0,icon)

        #Fonts------------------------------------
        for ChildFont in os.listdir(PathFonts):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(ChildFont[:-4])).setIcon(0,icon)

        #Scripts------------------------------------
        for ChildScript in os.listdir(PathScripts):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(ChildScript[:-3])).setIcon(0,icon)

        #Objects----------------------------------
        for ChildObject in os.listdir(PathObjects):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentObjects, QtCore.QStringList(ChildObject[:-3])).setIcon(0,icon)

        #Rooms------------------------------------
        for ChildRoom in os.listdir(PathRooms):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "game.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            QtGui.QTreeWidgetItem(self.ParentRooms, QtCore.QStringList(ChildRoom[:-4])).setIcon(0,icon)


    def AddSprChild(self,name):
        PathSprite = "Sprites"

        #Sprites----------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("Sprites", name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSprite, QtCore.QStringList(name[:-4])).setIcon(0,icon)    

    def AddSndChild(self,name):
        PathSprite = "Sound"

        #Sound------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "sound.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentSound, QtCore.QStringList(name[:-4])).setIcon(0,icon)

    def AddScriptChild(self,name):

        #Script------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "object.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentScripts, QtCore.QStringList(name)).setIcon(0,icon)

    def AddFontChild(self,name):
        PathSprite = "Fonts"

        #Font------------------------------------
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("..", "..", "Data", "font.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtGui.QTreeWidgetItem(self.ParentFonts, QtCore.QStringList(name[:-4])).setIcon(0,icon)        
   
class Stellar(QtGui.QMainWindow,QtGui.QTextEdit,QtGui.QTreeWidget):
    
    def __init__(self):
        super(Stellar, self).__init__()
        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.initUI()
        
    def initUI(self):
        
        #Saving where you opened the program for opening a new window in the future
        self.stellardir = inspect.getfile(inspect.currentframe())
        dirname, filename = os.path.split(os.path.abspath(self.stellardir))
        os.chdir(dirname)
        self.pref = os.path.join(dirname, "preferences.pyw")
        self.stellarnew = os.path.join(dirname, "Stellar.pyw")
              
        '''editor= self.textEdit = CompletionTextEdit()
        highlight = syntax.PythonHighlighter(editor.document())
        self.textEdit.zoomIn(+4)
        self.setCentralWidget(self.textEdit)
        self.texEdit=CompletionTextEdit()'''
        
        #ACTIONS -------------------------------
        newAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'new.png')), 'New Project', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Project.')
        newAction.triggered.connect(self.newproject)
        
        exitAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'exit.png')), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application.')
        exitAction.triggered.connect(self.close)

        aboutAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'info.png')),'About', self)
        aboutAction.setStatusTip('About Stellar.')
        aboutAction.triggered.connect(self.aboutStellar)

        scriptAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'clock.png')),'Add Script', self)
        scriptAction.setStatusTip('Add A Script To The Game.')
        scriptAction.triggered.connect(self.addScript)

        buildAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'build.png')),'Build', self)
        buildAction.setStatusTip('Build game.')
        buildAction.triggered.connect(self.Build)

        playAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'play.png')),'Run', self)
        playAction.setStatusTip('Test your game.')
        playAction.setShortcut('F5')
        playAction.triggered.connect(self.playgame)

        playDebugAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'playdebug.png')),'Run in debug mode', self)
        playDebugAction.setStatusTip('Test your game on debug mode.')
        playDebugAction.setShortcut('F6')
        playDebugAction.triggered.connect(self.playgame)

        spriteAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'sprite.png')),'Add Sprite', self)
        spriteAction.setStatusTip('Add a sprite to the game.')
        spriteAction.triggered.connect(self.addsprite)

        animatedspriteAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'gif.png')),'Add Animated Sprite', self)
        animatedspriteAction.setStatusTip('Add an animated sprite to the game.')
        animatedspriteAction.triggered.connect(self.addAnimatedSprite)

        soundAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'sound.png')),'Add Sound', self)
        soundAction.setStatusTip('Add a sound to the game.')
        soundAction.triggered.connect(self.addsound)

        shareAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'publish.png')),'Share', self)
        shareAction.setStatusTip('Share your creations with the community!')
        shareAction.triggered.connect(self.sharegame)

        fontAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'font.png')),'Add Font', self)
        fontAction.setStatusTip('Add a font to the game.')
        fontAction.triggered.connect(self.addfont)

        zoominAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'plus.png')),'Zoom In', self)
        zoominAction.setStatusTip('Zoom in the font of the editor.')
        zoominAction.triggered.connect(self.onZoomInClicked)

        zoomoutAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'minus.png')),'Zoom Out', self)
        zoomoutAction.setStatusTip('Zoom out the font of the editor.')
        zoomoutAction.triggered.connect(self.onZoomOutClicked)

        sfontAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'font.png')),'Set Font', self)
        sfontAction.setStatusTip('Change the font of the text editor.')
        sfontAction.triggered.connect(self.fontdialog)

        loadAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'folder.png')),'Open...', self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.setStatusTip('Open Game.')
        loadAction.triggered.connect(self.openfile)

        saveAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'save.png')),'Save Game As...', self)
        saveAction.setShortcut('Ctrl+Shift+S')
        saveAction.setStatusTip('Save Game As...')
        saveAction.triggered.connect(self.savefile)

        fsaveAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'save.png')),'Save', self)
        fsaveAction.setShortcut('Ctrl+S')
        fsaveAction.setStatusTip('Save Game.')
        fsaveAction.triggered.connect(self.fsavefile)

        preferencesAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'preferences.png')),'Preferences...', self)
        preferencesAction.setStatusTip('Change Stellar preferences.')
        preferencesAction.triggered.connect(self.preferencesopen)

        self.statusBar()

        #MENU BAR --------------------------------------
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(newAction)
        self.fileMenu.addAction(loadAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(fsaveAction)
        self.fileMenu.addAction(saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(buildAction)
        self.fileMenu.addAction(shareAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(preferencesAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(exitAction)
        self.fileMenu = menubar.addMenu('&Resources')
        self.fileMenu.addAction(spriteAction)
        self.fileMenu.addAction(animatedspriteAction)
        self.fileMenu.addAction(soundAction)
        self.fileMenu.addAction(fontAction)
        self.fileMenu.addSeparator()
        self.fileMenu = menubar.addMenu('&Scripts')
        self.fileMenu.addAction(scriptAction)
        self.fileMenu = menubar.addMenu('&Run')
        self.fileMenu.addAction(playAction)
        self.fileMenu.addAction(playDebugAction)
        self.fileMenu = menubar.addMenu('&Text Editor')
        self.fileMenu.addAction(zoominAction)
        self.fileMenu.addAction(zoomoutAction)
        self.fileMenu.addAction(sfontAction)
        self.fileMenu = menubar.addMenu('&Help')
        self.fileMenu.addAction(aboutAction)

        #TOOL BAR --------------------------------------
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (False)
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(fsaveAction)
        self.toolbar.addAction(loadAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(buildAction)
        self.toolbar.addAction(shareAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(playAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(spriteAction)
        self.toolbar.addAction(animatedspriteAction)
        self.toolbar.addAction(soundAction)
        self.toolbar.addAction(fontAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(scriptAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(aboutAction)
        self.toolbar.addAction(zoominAction)
        self.toolbar.addAction(zoomoutAction)

        #Qtree----------------------------------------
        self.tree = TreeWidget(self)
        self.tree.resize(200, self.height()-125)
        self.tree.move(0,self.toolbar.height()+self.fileMenu.height())
        self.tree.show()

        #QLogo-----------------------------------------
        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap(os.path.join("data", "Logo.png")))
        self.logo.resize(200,55)
        self.logo.move(0,self.height()-122+self.toolbar.height()+self.fileMenu.height())
        self.logo.show()

        #QFrame ---------------------------------------
        self.Frame = QtGui.QFrame(self)

        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.setMovable (False) # True will give some errors, could be fixed though with an array when True
        self.tab1 = QtGui.QWidget() 
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tab4 = QtGui.QWidget()
        self.tab5 = QtGui.QWidget()
        self.tab6 = QtGui.QWidget() 
         
        self.p1_vertical = QtGui.QVBoxLayout(self.tab1) 
        self.p2_vertical = QtGui.QVBoxLayout(self.tab2)
        self.p3_vertical = QtGui.QVBoxLayout(self.tab3)
        self.p4_vertical = QtGui.QVBoxLayout(self.tab4)
        self.p5_vertical = QtGui.QVBoxLayout(self.tab5)
        self.p6_vertical = QtGui.QVBoxLayout(self.tab6) 
         
        self.tab_widget.addTab(self.tab1, "Sprites") 
        self.tab_widget.addTab(self.tab2, "Sound")
        self.tab_widget.addTab(self.tab3, "Fonts") 
        self.tab_widget.addTab(self.tab4, "Scripts")
        self.tab_widget.addTab(self.tab5, "Objects")
        self.tab_widget.addTab(self.tab6, "Rooms")

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.tab_widget)
        self.Frame.setLayout(self.vbox)
        self.connect(self.tab_widget, QtCore.SIGNAL("currentChanged(int)"), self.TopTabChanged)

        #QFrame QTab Sprites
        self.tab_widget_sprites = QtGui.QTabWidget(self.tab_widget)
        self.tab_widget_sprites.setMovable (True)
        self.tab_widget_sprites.setTabsClosable (True)
        self.tab_widget_sprites.setGeometry(0, 22, self.tab_widget.width(), self.tab_widget.height()-22)
        self.connect(self.tab_widget_sprites, QtCore.SIGNAL("currentChanged(int)"), self.SpriteTabChanged)

        #QFrame QTab Sound
        self.tab_widget_sound = QtGui.QTabWidget(self.tab_widget)
        self.tab_widget_sound.setMovable (True)
        self.tab_widget_sound.setTabsClosable (True)
        self.tab_widget_sound.setGeometry(0, 22, self.tab_widget.width(), self.tab_widget.height()-22)
        self.connect(self.tab_widget_sound, QtCore.SIGNAL("currentChanged(int)"), self.SoundTabChanged)

        #QFrame QTab Fonts
        self.tab_widget_font = QtGui.QTabWidget(self.tab_widget)
        self.tab_widget_font.setMovable (True)
        self.tab_widget_font.setTabsClosable (True)
        self.tab_widget_font.setGeometry(0, 18, self.tab_widget.width(), self.tab_widget.height()-22)
        self.connect(self.tab_widget_font, QtCore.SIGNAL("currentChanged(int)"), self.FontsTabChanged)

        #QFrame QTab Scripts
        self.tab_widget_scripts = QtGui.QTabWidget(self.tab_widget) 
        self.tab_widget_scripts.setGeometry(0, 22, self.tab_widget.width(), self.tab_widget.height()-22)
        self.connect(self.tab_widget_scripts, QtCore.SIGNAL("currentChanged(int)"), self.ScriptTabChanged)

        #WINDOW----------------------------------------
        self.setGeometry(200, 200, 800, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.fname = "<New game>"
        self.setWindowTitle('%s - Stellar 0.1.2'% self.fname)
        self.setMinimumSize(800,600)
        self.center()
        self.start = Start(self)
        self.tab_widget.setCurrentIndex(0)
        self.TopTabChanged(0)

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

        for sprite in self.Sprites:
            sprite[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)
            sprite[0].scrollArea.setGeometry(350, 0, sprite[0].ContainerBox.width()-350, sprite[0].ContainerBox.height())
        for sound in self.Sound:
            sound[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)
        for font in self.Fonts:
            font[0].ContainerBox.setGeometry(10, 50, self.tab_widget.width()-3, self.tab_widget.height()-42)

    def preferencesopen(self):
        
        print self.pref
        execfile(self.pref, {})

    def newproject(self):

        execfile(self.stellarnew, {})

    def Build(self):
        if self.fname != "<New game>":
            print("win")
        else:
            self.savefile()
        
    def aboutStellar(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(self.tr("About Stellar"))
        about.setText(self.tr("<b>Stellar 0.3.0</b><br/>Programmed by <a href=\"https://twitter.com/#!/Coppola_Emilio\">Emilio Coppola</a>.<br/>Program main icon by <a href=\"http://dakirby309.deviantart.com\">dAKirby309</a><br/>Co-Programmer <a href='#'>Hans Gillis</a><br/>Animated Gif by <a href='http://pyedpypers.org/index.php'>Roebros</a><br/><br/>License  <a href=\"http://creativecommons.org/licenses/by-nc-sa/3.0\">(CC BY-NC-SA 3.0)</a>.<br/><br/>For more information visit the website:<br/><a href=\"http://www.pygame.org/project-Stellar+-+Pygame+GUI-2293-.html\">www.pygame.org/project-Stellar...</a>"))
        about.exec_()
            
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, "Exit Stellar", "Save Python File before Exit?",
                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            f = open(self.fname, 'w')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, __version__))

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
        self.tmp = self.fname
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Game', 
                '', self.tr("Python files (*.py *.pyw)"))

        if self.fname == "":
            self.fname = self.tmp
        else:
            f = open(self.fname, 'r')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, __version__))
            
            with f:        
                data = f.read()
                self.textEdit.setText(data)
                
            dirname, filename = os.path.split(os.path.abspath(self.fname))
            os.chdir(dirname)

    def sharegame(self):
        webbrowser.open("http://www.pygame.org/news.html")
            
    def savefile(self):
        self.tmp = self.fname
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Game', 
                '', self.tr("Python files (*.py)"))

        if self.fname == "":
            self.fname = self.tmp
        else:
            f = open(self.fname, 'w')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, __version__))

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)
                f.close()
            dirname, filename = os.path.split(os.path.abspath(self.fname))
            os.chdir(dirname)
        
            
    def fsavefile(self):
        if self.fname=="<New game>":
            self.savefile()
        else:
            f = open(self.fname, 'w')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, __version__))

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)
                f.close()

    def onZoomInClicked(self):
        self.textEdit.zoomIn(+1)

    def onZoomOutClicked(self):
        self.textEdit.zoomOut(+1)       
        
    def playgame(self):
        if self.fname=="<New game>":
            self.savefile()
        else:
            f = open(self.fname, 'w')
            p = self.fname
            d = os.path.basename(str(p))
            self.setWindowTitle('%s - Stellar %s'% (d, __version__))

            with f:
                data = self.textEdit.toPlainText()
                f.write(data)
                f.close()
        dirname, filename = os.path.split(os.path.abspath(self.fname))
        os.chdir(dirname)

        execfile(filename, {})

        # This possibility is also worth looking at:
        # http://stackoverflow.com/questions/4230725/how-to-execute-a-python-script-file-with-an-argument-from-inside-another-python

##        major, minor, patchlevel = platform.python_version_tuple()
##        if platform.system() == "Windows":
##            subprocess.Popen(["C:\Python{0}{1}\python.exe".format(major, minor),
##                              filename]).communicate() # Going to add settings menu for the path
##        elif platform.system() == "Darwin":
##            subprocess.Popen([
##                "System/Library/Frameworks/Python.framework/Versions/{0}.{1}/Library/Python/python.app".format(major, minor),
##                filename]).communicate() # Going to add settings menu for the path
##        elif platform.system() == "Linux":
##            subprocess.Popen(["python{0}.{1}".format(major, minor),
##                              filename]).communicate() # Not sure though

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
                if not os.path.exists(os.path.join('Sprites', d)):
                    if d[:4]=='spr_':
                        shutil.copy(sprite, os.path.join('Sprites', d))
                        self.tree.AddSprChild(d)
                    else:
                        shutil.copy(sprite, os.path.join('Sprites', 'spr_{0}'.format(d)))
                        self.tree.AddSprChild('spr_' + d)
            

    def addAnimatedSprite(self):

        self.aGIFsprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Animated Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
        if self.aGIFsprite !='':
            for sprite in self.aGIFsprite:
                d = os.path.basename(str(sprite))
                if not os.path.exists(os.path.join('Sprites', d)):
                    if d[:4]=='spr_':
                        shutil.copy(sprite,os.path.join('Sprites', d))
                        self.tree.AddSprChild(d)
                    else:
                        shutil.copy(sprite,os.path.join('Sprites', 'spr_{0}'.format(d)))
                        self.tree.AddSprChild('spr_' + d)


    def addsound(self):

        self.asound = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sound(s)', 
                '', self.tr("Sound file (*.ogg *.wav)"))
        
        if self.asound !='':
            for sound in self.asound:
                d = os.path.basename(str(sound))
                if not os.path.exists(os.getcwd()+'Sound'+d):
                    if d[:4]=='snd_':
                        shutil.copy(sound,os.path.join('Sound', d))
                        self.tree.AddSndChild(d)
                    else:
                        shutil.copy(sound,os.path.join('Sound', 'snd_{0}'.format(d)))
                        self.tree.AddSndChild('snd_'+d)

    def addfont(self):

        self.afont = QtGui.QFileDialog.getOpenFileNames(self, 'Open Font(s)', 
                '', self.tr("Font file (*.ttf *.ttc *.fon)"))
        
        if self.afont !='':
            for font in self.afont:
                d = os.path.basename(str(font))
                f = os.path.splitext(d)[0]
                if not os.path.exists(os.path.join('Fonts', d)):
                    if d[:5]=='font_':
                        shutil.copy(font,os.path.join('Fonts', d))
                        self.tree.AddFontChild(d)
                    else:
                        shutil.copy(font,os.path.join('Fonts', 'font_{0}'.format(d)))
                        self.tree.AddFontChild('font_'+d)         

    def addScript(self):
        script = "script_"
        scriptnumber = 0
        TmpScript = script + str(scriptnumber)
        while os.path.exists(os.path.join('Scripts', "{0}.py".format(TmpScript))):
            scriptnumber += 1 
            TmpScript = script + str(scriptnumber)
        f = open(os.path.join('Scripts', "{0}.py".format(TmpScript)),'w')
        f.close()
        self.tree.AddScriptChild(TmpScript)


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
