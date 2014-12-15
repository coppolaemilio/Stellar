#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFont
import os, sys, shutil
import json
import imageviewer
import codeeditor

class ResourceList(QtGui.QTreeWidget):
    def __init__(self, main):
        super(ResourceList, self).__init__(main)
        self.main = main
        self.item_index = {}
        self.main.window_index = {}
        
        self.header().close()
        self.load_project_data()
        self.folders = ("sprites", "sounds", "objects", "scripts", "rooms")
        
        icon_size = self.main.treeview_icon_size
        self.setIconSize(QtCore.QSize(icon_size,icon_size))
        
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.itemDoubleClicked.connect(self.double_clicked)
        self.itemClicked.connect(self.clicked)
        
        self.show_project_name()
        self.create_tree()

    def load_project_data(self):
        json_data = open(self.main.projectdir)
        self.data = json.load(json_data)
        json_data.close()

    def create_tree(self):
        self.read_section("sprites", "Sprites")
        self.read_section("sounds", "Sounds")
        self.read_section("scripts", "Scripts")
        self.read_section("objects", "Objects")
        self.read_section("rooms", "Rooms")
        self.AddItem("Extensions", self.main.extension_sprite)
        self.AddItem("Settings", self.main.settings_sprite)
    
    def show_project_name(self):
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
    
    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        item = self.currentItem().text(0)
        newscraction = QtGui.QAction(QtGui.QIcon('images/new.png'), "New script", self)
        newscraction.triggered.connect(self.NewScript)
        deleteaction = QtGui.QAction(QtGui.QIcon('images/close.png'), "Delete " + item, self)
        deleteaction.triggered.connect(self.DeleteResource)
        try:
            if self.currentItem().parent().text(0) == "Scripts": 
                menu.addAction(newscraction)
        except:
            if self.currentItem().text(0) == "Scripts": 
                menu.addAction(newscraction)
        
        try: #checking if it's a main group
            if self.currentItem().parent().text(0):
                menu.addAction(deleteaction)
        except:
            print "No delete here"
        menu.popup(event.globalPos())
        event.accept()

    def NewScript(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Create Script', 
            'Script name:')
        text = str(text)
        if ok:
            item = QtGui.QTreeWidgetItem(self)
            item.setIcon(0, QtGui.QIcon(self.main.file_sprite))
            item.setText(0, text)
            self.CreateResource(text, "scripts", text+".py")

    def CreateResource(self, text, section, value):
        #self.AddItem(text, "file")
        self.item_index[text] = section
        with open(self.main.projectdir) as f:
            data = json.load(f)
        d = {}
        for i in data[section]:
            d[i] = data[section][i]
        d[text] = value
        data[section].update(d)
        with open(self.main.projectdir, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)
        project_folder = self.main.projectdir

        open(project_folder+'/'+ section +'/'+ value, 'a').close()

    def DeleteResource(self):
        index = self.currentItem()

        dl_msg = "Are you sure you want to delete \"" + index.text(0) + "\"?"
        reply = QtGui.QMessageBox.question(self, 'Delete Resource', 
                         dl_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            print index.text(0)
            print index.parent().text(0)
        else:
            return

    def clicked(self, index):
        resource_name = str(index.text(0))
        try: #checking if it has a parent
            index.parent().text(0)
        except:
            return 0
        
        self.main.inspector.information.setText("")
        self.main.inspector.nameEdit.setText(resource_name)
        if str(index.parent().text(0)).lower() == "sprites":
            self.main.inspector.scrollArea.show()
            self.main.inspector.open_image(resource_name)
        else:
            self.main.inspector.scrollArea.hide()

    def double_clicked(self, index):
        resource_name = str(index.text(0))
        project_folder = os.path.dirname(self.main.projectdir)
        
        for folder in self.folders:
            if self.item_index[resource_name] == folder:
                path = os.path.join(project_folder, folder, resource_name)
                self.open_tab(path, resource_name, folder)
       
    def open_tab(self, path, name, type):
        if type == "sprites":
            window = imageviewer.ImageEditor(self.main, name, path)
        else:
            window = codeeditor.CodeEditor(self.main, path)
        self.main.window_index[name] = window
        self.main.mdi_area.addSubWindow(window)
        window.setWindowTitle(name)
        window.setVisible(True)

    def AddItem(self, name, icon):
        item = QtGui.QTreeWidgetItem(self)
        if str(icon) == "file":
            item.setIcon(0, QtGui.QIcon(self.main.file_sprite))
        else:
            item.setIcon(0, QtGui.QIcon(icon))
        item.setText(0, name)

    def read_section(self, section, name):
        item = QtGui.QTreeWidgetItem(self)
        item.setExpanded(True)
        item.setIcon(0, QtGui.QIcon(self.main.folder_sprite))
        item.setText(0, name)
        for i in self.data[section]:
            subitem = QtGui.QTreeWidgetItem()
            subitem.setText(0, str(i))
            icon_path = os.path.dirname(self.main.projectdir) + '/sprites/' +  str(self.data[section][i])
            if os.path.isfile(icon_path):
                subitem.setIcon(0, QtGui.QIcon(icon_path))
            else:
                subitem.setIcon(0, QtGui.QIcon(self.main.file_sprite))
            #print os.path.dirname(self.main.projectdir) + '/' +  str(self.data[section][i])
            item.addChild(subitem)
            self.item_index[str(i)]=section

    def doMenu(self, point):
        print("TO DO")

    def edit_file(self):
        print("TO DO")

    def delete_file(self):
        print("TO DO")
                
    def delete_folder(self, f):
        print("TO DO")

    def add_file(self):
        print("TO DO")

    def add_directory(self):
        print("TO DO")

    def rename_file(self):
        print("TO DO")
