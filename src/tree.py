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
sys.path.append("src")

import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil

from PyQt4 import QtCore, QtGui

import cfg
from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from scriptgui import ScriptGUI
from objectgui import ObjectGUI

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
        
        self.Names = self.main.Names
        self.ImageNames = (None, 'sound.png', 'font.png', 'script.png', 'object.png', 'game.png')
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
       
        def openWindow(directory):
            if item.parent().text(0) == directory:
                self.main.window = QtGui.QWidget()
                
                if directory == "Sprites":
                    self.main.sprite = SpriteGUI(self.main.window,item.text(0), self.main.dirname)
                elif directory == "Sound":
                    self.main.sound = SoundGUI(self.main.window,item.text(0), self.main.dirname)
                elif directory == "Fonts":
                    self.main.font = FontGUI(self.main.window,item.text(0))
                elif directory == "Scripts":
                    self.main.script = ScriptGUI(self.main.window,item.text(0), self.main.dirname, self.main)
                elif directory == "Objects":
                    self.main.object = ObjectGUI(self.main.window,item.text(0), self.main.dirname)
                
                if directory[-1:] == "s":
                    directory = directory[:-1]
                
                self.main.qmdiarea.addSubWindow(self.main.window)
                
                self.main.window.setVisible(True)
                self.main.window.setWindowTitle( directory + " properties: " + item.text(0) )
                if directory == "Sprite":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sprite.png')))
                elif directory == "Sound":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sound.png')))
                else:
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', self.ImageName[unicode(directory + 's')])))

        
        
        item = self.currentItem()
        if not item.parent() == None:
            for name in self.Names:
                openWindow(name)
    
    def InitParent(self):
        
        for name in self.Names:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Parent[name] = QtGui.QTreeWidgetItem(self, QtCore.QStringList(name))
            self.Parent[name].setIcon(0,icon)
            
    def InitChild(self, fillarrays=False):
        dirname = self.main.dirname
        
        for name in self.Names:
            self.Path[name] = os.path.join(dirname, name)
            for ChildSource in sorted(os.listdir(self.Path[name])):                
                icon = QtGui.QIcon()
                if name == "Sprites":
                    icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[name], ChildSource)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[name])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    
                if name == "Sprites" or name == "Sound" or name == "Fonts" or name == "Rooms":
                    QtGui.QTreeWidgetItem(self.Parent[name], QtCore.QStringList(ChildSource[:-4])).setIcon(0,icon) 
                elif name == "Objects" or name == "Scripts":
                    QtGui.QTreeWidgetItem(self.Parent[name], QtCore.QStringList(ChildSource[:-3])).setIcon(0,icon)

                if fillarrays:
                    self.main.Sources[name].append(ChildSource)
        

    def addChild(self, directory, name):
        icon = QtGui.QIcon()
        
        if directory == 'Sprites':
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[directory], name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[directory])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                
               
        if directory == 'Scripts' or directory == 'Objects':
            QtGui.QTreeWidgetItem(self.Parent[directory], QtCore.QStringList(name)).setIcon(0,icon)
        else:
            QtGui.QTreeWidgetItem(self.Parent[directory], QtCore.QStringList(name[:-4])).setIcon(0,icon) 
