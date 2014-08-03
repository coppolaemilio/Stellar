#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2014 Emilio Coppola
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFont
import os, sys, shutil
import json
import imageviewer
import scripteditor

class ListView(QtGui.QTreeWidget):
    def __init__(self, main):
        super(ListView, self).__init__(main)
        self.main = main
        self.header().close()
        json_data=open(self.main.projectdir)
        self.data = json.load(json_data)

        self.setIconSize(QtCore.QSize(self.main.treeview_icon_size,
                                      self.main.treeview_icon_size))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.itemDoubleClicked.connect(self.DoubleClicked)
        self.item_index = {}
        self.main.window_index = {}

        
        item = QtGui.QTreeWidgetItem(self)
        item.setIcon(0, self.main.icon)
        project_name = "Example"
        item.setText(0, project_name)
        self.item_index[str(project_name)]="project_overview"
        self.font = QtGui.QFont()
        #self.font.setFamily('ClearSans')
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setFixedPitch(True)
        self.font.setPointSize(int(20))
        item.setFont(0, self.font)


        self.ReadSection("sprites", "Sprites")
        self.ReadSection("objects", "Objects")
        self.ReadSection("rooms", "Rooms")
        self.AddItem("Extensions", self.main.extension_sprite)
        self.AddItem("Settings", self.main.settings_sprite)
        

        json_data.close()

    def DoubleClicked(self, index):
        resource_name = str(index.text(0))

        if self.item_index[resource_name] == "sprites":
            filePath = 'projects/images/'+resource_name
            window = imageviewer.ImageEditor(self.main, resource_name, filePath)
        elif self.item_index[resource_name] == "objects":
            text = self.data["objects"][resource_name]
            window = scripteditor.ScriptEditor(self.main, resource_name, text)
        elif self.item_index[resource_name] == "project_overview":
            window = self.main.ShowProjectOverview()
            return

        try:  #checking if the window is already open
            self.main.window_index[resource_name]
        except:
            self.OpenTab(window, resource_name)

    def OpenTab(self, window, resource_name):
        self.main.window_index[resource_name] = window
        self.main.mdi.addSubWindow(window)
        window.setWindowTitle(resource_name)
        window.setVisible(True)

    def AddItem(self, name, icon):
        item = QtGui.QTreeWidgetItem(self)
        item.setIcon(0, QtGui.QIcon(icon))
        item.setText(0, name)

    def ReadSection(self, section, name):
        item = QtGui.QTreeWidgetItem(self)
        item.setExpanded(True)
        item.setIcon(0, QtGui.QIcon(self.main.folder_sprite))
        item.setText(0, name)
        for i in self.data[section]:
            subitem = QtGui.QTreeWidgetItem()
            subitem.setText(0, str(i))
            icon_path = os.path.dirname(self.main.projectdir) + '/' +  str(self.data[section][i])
            if os.path.isfile(icon_path):
                subitem.setIcon(0, QtGui.QIcon(icon_path))
            else:
                subitem.setIcon(0, QtGui.QIcon(self.main.file_sprite))
            #print os.path.dirname(self.main.projectdir) + '/' +  str(self.data[section][i])
            item.addChild(subitem)
            self.item_index[str(i)]=section

    def doMenu(self, point):
        print "TO DO"

    def edit_file(self):
        print "TO DO"

    def delete_file(self):
        print "TO DO"
                
    def delete_folder(self, f):
        print "TO DO"

    def add_file(self):
        print "TO DO"

    def add_directory(self):
        print "TO DO"

    def rename_file(self):
        print "TO DO"