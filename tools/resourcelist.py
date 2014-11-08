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
        self.header().close()
        json_data = open(self.main.projectdir)
        self.data = json.load(json_data)

        self.setIconSize(QtCore.QSize(self.main.treeview_icon_size,
                                      self.main.treeview_icon_size))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.itemDoubleClicked.connect(self.DoubleClicked)
        self.itemClicked.connect(self.Clicked)
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
        self.ReadSection("sounds", "Sounds")
        self.ReadSection("scripts", "Scripts")
        self.ReadSection("objects", "Objects")
        self.ReadSection("rooms", "Rooms")
        self.AddItem("Extensions", self.main.extension_sprite)
        self.AddItem("Settings", self.main.settings_sprite)
    
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

    def Clicked(self, index):
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

    def DoubleClicked(self, index):
        resource_name = str(index.text(0))
        project_folder = os.path.dirname(self.main.projectdir)
        with open(self.main.projectdir) as f:
            data = json.load(f)

        if str(index.parent().text(0)).lower() == "sprites":
            filePath = project_folder+'/sprites/'+resource_name
            window = imageviewer.ImageEditor(self.main, resource_name, filePath)
        elif self.item_index[resource_name] == "objects":
            text = data["objects"][resource_name]
            filePath = project_folder+'/objects/'+ data["objects"][resource_name]
            window = codeeditor.CodeEditor(self.main, filePath)
        elif self.item_index[resource_name] == "scripts":
            filePath = project_folder+'/scripts/'+ data["scripts"][resource_name]
            window = codeeditor.CodeEditor(self.main, filePath)
        elif self.item_index[resource_name] == "rooms":
            filePath = project_folder+'/rooms/'+ data["rooms"][resource_name]
            window = codeeditor.CodeEditor(self.main, filePath)
        elif self.item_index[resource_name] == "project_overview":
            window = self.main.ShowProjectOverview()
            return

        #try:  #checking if the window is already open
        #    self.main.window_index[resource_name]
        #except:
        self.OpenTab(window, resource_name)

    def OpenTab(self, window, resource_name):
        self.main.window_index[resource_name] = window
        self.main.mdi.addSubWindow(window)
        window.setWindowTitle(resource_name)
        window.setVisible(True)

    def AddItem(self, name, icon):
        item = QtGui.QTreeWidgetItem(self)
        if str(icon) == "file":
            item.setIcon(0, QtGui.QIcon(self.main.file_sprite))
        else:
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