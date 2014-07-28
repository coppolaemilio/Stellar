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
import os, sys, shutil
import json
import imageviewer

class ListView(QtGui.QTreeWidget):
    def __init__(self, main):
        super(ListView, self).__init__(main)
        self.main = main
        self.setHeaderLabel("Resources")
        json_data=open(self.main.projectdir)
        self.data = json.load(json_data)

        self.itemDoubleClicked.connect(self.DoubleClicked)
        self.item_number = 0
        self.item_index = {}

        self.ReadSection("sprites", "Sprites")
        self.ReadSection("objects", "Objects")
        self.ReadSection("rooms", "Rooms")
        self.AddItem("Extensions", self.main.extension_sprite)
        self.AddItem("Settings", self.main.settings_sprite)
        

        json_data.close()


    def DoubleClicked(self, index):
        resource_name = str(index.text(0))
        if self.item_index[resource_name] == "sprites":
            target = resource_name
            filePath = 'projects/images/'+resource_name
            self.main.window = imageviewer.ImageEditor(self.main, target, filePath)
            self.main.window.setWindowTitle(target)
            self.main.mdi.addSubWindow(self.main.window)
            self.main.window.setVisible(True)
        #print index.text(0) + self.item_index[str(index.text(0))]

    def AddItem(self, name, icon):
        self.part = QtGui.QTreeWidgetItem(self)
        self.part.setIcon(0, QtGui.QIcon(icon))
        self.part.setText(0, name)

    def ReadSection(self, section, name):
        self.part = QtGui.QTreeWidgetItem(self)
        self.part.setExpanded(True)
        self.part.setIcon(0, QtGui.QIcon(self.main.folder_sprite))
        self.part.setText(0, name)
        for i in self.data[section]:
            item = QtGui.QTreeWidgetItem()
            item.setText(0, str(i))
            icon_path = os.path.dirname(self.main.projectdir) + '/' +  str(self.data[section][i])
            if os.path.isfile(icon_path):
                item.setIcon(0, QtGui.QIcon(icon_path))
            else:
                item.setIcon(0, QtGui.QIcon(self.main.file_sprite))
            #print os.path.dirname(self.main.projectdir) + '/' +  str(self.data[section][i])
            self.part.addChild(item)
            self.item_index[str(i)]=section

    def doMenu(self, point):
        print "TO DO"

    #def edit(self, index, trigger, event):
    #    print "TO DO"

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