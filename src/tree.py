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
from PyQt4 import QtCore, QtGui

if sys.version_info.major > 2:
    import configparser
    StringList = type([])
else:
    str = unicode
    import ConfigParser as configparser
    StringList = QtCore.QStringList

from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from scriptgui import ScriptGUI
from objectgui import ObjectGUI
from roomgui import RoomGUI
from backgroundgui import BackgroundGUI


class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, main):
        super(TreeWidget, self).__init__(main)
        self.header().setHidden(True)
        self.setWindowTitle('Resources')
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.main = main
        self.connect(self, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),self.DoEvent)
        self.connect(self, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem *)"), self.itemCollapsed)
        self.connect(self, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem *)"), self.itemExpanded)
        self.Path = {}

        lastposition= QtCore.QPoint(-32,-32)
        self.nwindows = 0
        
        
        self.Names = self.main.Names
        self.ImageNames = (None, 'sound.png', 'backgrounds.png', 'font.png', 'script.png', 'object.png', 'game.png')
        self.Parent = {}
        self.ImageName = {}
        j=0
        for i in self.Names:
            self.ImageName[i] = self.ImageNames[j]
            j+=1
        
    def itemCollapsed(self, obj):
        self.main.expanded[str(obj.text(0))] = False

    def itemExpanded(self, obj):
        self.main.expanded[str(obj.text(0))] = True

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        insertAction = menu.addAction("Insert")
        insertAction.triggered.connect(self.InsertItem)
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
        deleteAction.triggered.connect(self.DeleteEvent)
        deleteAction.setDisabled (False)
        menu.addSeparator()
        renameAction = menu.addAction("Rename")
        renameAction.setShortcut('F2')
        renameAction.setDisabled (True)
        menu.addSeparator()
        propertiesAction = menu.addAction("Properties...")
        propertiesAction.setShortcut('Alt+Enter')
        propertiesAction.triggered.connect(self.DoEvent)
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
    def DeleteEvent(self):
        def openWindow(directory):
            if item.parent().text(0) == directory:
                itemtext = str(item.text(0))

                if directory == "Sprites":
                    print ("TODO")
                elif directory == "Backgrounds":
                    reply = QtGui.QMessageBox.question(self, "Confirm", 'You are about to delete "'+itemtext+'". This will be permanent. Continue?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        os.remove(os.path.join(self.main.dirname, directory, itemtext+".png"))
                elif directory == "Sound":
                    print ("TODO")
                elif directory == "Fonts":
                    print ("TODO")
                elif directory == "Scripts":
                    reply = QtGui.QMessageBox.question(self, "Confirm", 'You are about to delete "'+itemtext+'". This will be permanent. Continue?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        os.remove(os.path.join(self.main.dirname, directory, itemtext+".py"))
                elif directory == "Objects":
                    reply = QtGui.QMessageBox.question(self, "Confirm", 'You are about to delete "'+itemtext+'". This will be permanent. Continue?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        os.remove(os.path.join(self.main.dirname, directory, itemtext+".ini"))
                elif directory == "Rooms":
                    reply = QtGui.QMessageBox.question(self, "Confirm", 'You are about to delete "'+itemtext+'". This will be permanent. Continue?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        os.remove(os.path.join(self.main.dirname, directory, itemtext+".py"))

                if directory[-1:] == "s":
                    directory = directory[:-1]

                self.main.updatetree()

            def GameSettings():
                print ("hola")
        
        item = self.currentItem()
        if not item.parent() == None:
            for name in self.Names:
                openWindow(name)
                
    def DoEvent(self, itemtext=False):
        def openWindow(directory, itemtext=None):
            if itemtext == None:
                itemtext = str(item.text(0))
                if item.parent().text(0) != directory:
                    return

            try:
                lastposition = self.main.qmdiarea.activeSubWindow().pos()
            except:
                lastposition = QtCore.QPoint(-25,-25)

            if directory == "Sprites":
                self.window = SpriteGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Backgrounds":
                self.window = BackgroundGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Sound":
                self.window = SoundGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Fonts":
                self.window = FontGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Scripts":
                self.window = ScriptGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Objects":
                self.window = ObjectGUI(self.main, itemtext, self.main.dirname, self)
            elif directory == "Rooms":
                self.window = RoomGUI(self.main, itemtext, self.main.dirname, self)

            #Check for existing window to focus on, if not create one
            windowTitle = directory[:-1] + " properties: " + itemtext
            
            windowList = self.main.qmdiarea.subWindowList()
            
            existingWindowFound = False
            
            #TODO: loops through windows checking for matching title, 
            #gotta be a better way to find existing window
            for existingWindow in windowList: 
                if (existingWindow.windowTitle() == windowTitle):
                    self.window = existingWindow
                    self.main.qmdiarea.setActiveSubWindow(self.window)
                    existingWindowFound = True
                    break
            
            #create a new window, if one doesn't exist
            if not existingWindowFound:
                self.window.setWindowTitle( windowTitle )
                self.main.qmdiarea.addSubWindow(self.window)
                self.nwindows += 1 #creating a new window, increment window count
            
            #new or old, make the window visible
            self.window.setVisible(True)
            
            #if window is new, set icon/geometry
            if not existingWindowFound:
                if directory == "Sprites":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sprite.png')))
                elif directory == "Sound":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sound.png')))
                elif directory == "Scripts":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'script.png')))
                elif directory == "Rooms":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'room.png')))
                elif directory == "Objects":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', self.ImageName[directory[:-1] + 's'])))
                    self.main.qmdiarea.activeSubWindow().setGeometry(0, 0, 520, 380)
                else:
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', self.ImageName[directory[:-1] + 's'])))

            #move window to proper location on screen
            if self.nwindows == 1: #first window
                self.main.qmdiarea.activeSubWindow().move(0,0) #show in top left corner
            elif (not existingWindowFound): #new window, but not first window
                self.main.qmdiarea.activeSubWindow().move(lastposition+QtCore.QPoint(25,25))
            else: #old window
                pass #keep in last known position 
                
            def GameSettings():
                print ("hola")

        

        if "QtGui" in str(itemtext):
            item = self.currentItem()
            if not item.parent() == None:
                for name in self.Names:
                    openWindow(name)
                        
        else:
            openWindow('Sprites', itemtext)

                    

    def InsertItem(self):
        item = self.currentItem()    
        itemtext = str(item.text(0))
        if itemtext == "Sprites":
            self.main.addSprite()
        elif itemtext == "Sound":
            self.main.addSound()
        elif itemtext == "Backgrounds":
            self.main.addBackground()
        elif itemtext == "Fonts":
            self.main.addFont()
        elif itemtext == "Scripts":
            self.main.addScript()
        elif itemtext == "Objects":
            self.main.addObject()
        elif itemtext == "Rooms":
            self.main.addRoom()
        
    def InitParent(self):
        
        for name in self.Names:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Parent[name] = QtGui.QTreeWidgetItem(self, StringList([name]))
            self.Parent[name].setIcon(0,icon)
            
        iconpref = QtGui.QIcon()
        iconpref.addPixmap(QtGui.QPixmap(os.path.join("Data", "treepreferences.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ggs = QtGui.QTreeWidgetItem(self, StringList(["Global Game Settings"]))
        self.ggs.setIcon(0,iconpref)
        
    def InitChild(self, fillarrays=False):
        dirname = self.main.dirname
        self.InitParsers()
        
        for name in self.Names:
            self.Path[name] = os.path.join(dirname, name)
            
            if name == "Fonts":
                for section in self.fnt_parser.sections():
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[name])), QtGui.QIcon.Normal, QtGui.QIcon.Off)               
                    QtGui.QTreeWidgetItem(self.Parent[name], StringList(section)).setIcon(0,icon)
            else:
                for ChildSource in sorted(os.listdir(self.Path[name])):
                    ChildSource = str(ChildSource)
                    icon = QtGui.QIcon()
                    if name == "Sprites" or name == "Backgrounds":
                        icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[name], ChildSource)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    elif name =="Objects":
                        self.config = configparser.ConfigParser()
                        self.config.read(os.path.join(self.Path[name], ChildSource))
                        currentsprite = self.config.get('data', 'sprite', 0)
                        currentsprite = str(currentsprite)+".png"
                        icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path["Sprites"], currentsprite)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    else:
                        icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[name])), QtGui.QIcon.Normal, QtGui.QIcon.Off)               

                    if name == "Sprites" or name == "Sound" or name == "Backgrounds":
                        if ChildSource.endswith(".ini"):#skips the .ini of sprite information
                            continue

                        
                        if "-0" in ChildSource[:-4]: #now checking if it's an animated sprite
                            QtGui.QTreeWidgetItem(self.Parent[name], StringList([ChildSource[:-6]])).setIcon(0,icon)
                        elif "-" in ChildSource[:-4]:
                            continue
                        else:
                            QtGui.QTreeWidgetItem(self.Parent[name], StringList([ChildSource[:-4]])).setIcon(0,icon)
                        
                    elif name == "Scripts" or name == "Rooms":
                        QtGui.QTreeWidgetItem(self.Parent[name], StringList([ChildSource[:-3]])).setIcon(0,icon)
                    elif name == "Objects":
                        if ChildSource.endswith(".ini"):
                            QtGui.QTreeWidgetItem(self.Parent[name], StringList([ChildSource[:-4]])).setIcon(0,icon)
                        else:
                            continue                    
                    
                    if fillarrays:
                        self.main.Sources[name].append(ChildSource)

    def InitParsers(self):
        self.spr_parser = configparser.RawConfigParser()
        self.spr_parser.read(os.path.join(self.main.dirname, 'Sprites', 'spriteconfig.ini'))

        self.snd_parser = configparser.RawConfigParser()
        self.snd_parser.read(os.path.join(self.main.dirname, 'Sound', 'soundconfig.ini'))

        self.fnt_parser = configparser.RawConfigParser()
        self.fnt_parser.read(os.path.join(self.main.dirname, 'Fonts', 'fontconfig.ini'))

        #TODO: soundparser...etc

    def write_sprites(self):
        with open(os.path.join(self.main.dirname, 'Sprites', 'spriteconfig.ini'), 'w') as configfile:
            self.spr_parser.write(configfile)

    def write_sound(self):
        with open(os.path.join(self.main.dirname, 'Sound', 'soundconfig.ini'), 'w') as configfile:
            self.snd_parser.write(configfile)

    def write_fonts(self):
        with open(os.path.join(self.main.dirname, 'Fonts', 'fontconfig.ini'), 'w') as configfile:
            self.fnt_parser.write(configfile)

    def add_sprite_section(self, name):
        self.spr_parser.add_section(name[:-4])
        if name[-3:]=="gif":
            self.spr_parser.set(name[:-4], 'extension', 'png')
        else:
            self.spr_parser.set(name[:-4], 'extension', name[-3:])
        self.spr_parser.set(name[:-4], 'xorig', 0)
        self.spr_parser.set(name[:-4], 'yorig', 0)

        self.write_sprites()

    def add_sound_section(self, name):
        self.snd_parser.add_section(name[:-4])
        self.snd_parser.set(name[:-4], 'extension', name[-3:])
        self.snd_parser.set(name[:-4], 'volume', '0')
        self.snd_parser.set(name[:-4], 'pan', '0')

        self.write_sound()

    def add_font_section(self, name):
        self.fnt_parser.add_section(name)
        self.fnt_parser.set(name, 'font', '')
        self.fnt_parser.set(name, 'fontindex', '')
        self.fnt_parser.set(name, 'size', '')
        self.fnt_parser.set(name, 'bold', 'False')
        self.fnt_parser.set(name, 'italic', 'False')
        self.fnt_parser.set(name, 'antialiasing', 'False')

        self.write_fonts()
        
    def addChild(self, directory, name):
        icon = QtGui.QIcon()
        
        if directory == 'Sprites':
            if "gif" in name:
                icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[directory], name[:-4]+"-0.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            else:
                icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[directory], name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.add_sprite_section(name)
        else:
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[directory])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            if directory == 'Sound':
                self.add_sound_section(name)
            elif directory == 'Fonts':
                self.add_font_section(name)
                
               
        if directory == 'Scripts' or directory =='Rooms' or directory =='Objects' or directory == 'Fonts':
            QtGui.QTreeWidgetItem(self.Parent[directory], StringList([name])).setIcon(0,icon)
        else:
            QtGui.QTreeWidgetItem(self.Parent[directory], StringList([name[:-4]])).setIcon(0,icon)
