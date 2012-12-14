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

from PyQt4 import QtCore, QtGui
import os, webbrowser
import cfg
from dialogs import NewProjectDialog

class Start(QtGui.QWidget):
  
    def __init__(self, main,parent=None):
        super(Start, self).__init__(parent)
        self.main = main
        self.initUI()

    def initUI(self):

        pic = QtGui.QLabel(self)
        pic.setGeometry(12, 10, 500, 145)
        pic.setPixmap(QtGui.QPixmap(os.path.join("Data", "stellarsplash.png")))

        #TABS ----------------
         
        self.tab_widget = QtGui.QTabWidget() 
        tab1 = QtGui.QWidget() 
        tab2 = QtGui.QWidget()
        tab3 = QtGui.QWidget()
        tab4 = QtGui.QWidget() 
         
        p1_vertical = QtGui.QVBoxLayout(tab1)
        p2_vertical = QtGui.QVBoxLayout(tab2)
        p3_vertical = QtGui.QVBoxLayout(tab3)
        p4_vertical = QtGui.QVBoxLayout(tab4)

        self.tab_widget.addTab(tab4, "Welcome")
        self.tab_widget.addTab(tab1, "New Project") 
        self.tab_widget.addTab(tab2, "Open Project")
        self.tab_widget.addTab(tab3, "Release Notes") 

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.tab_widget)
         
        self.setLayout(vbox)

        self.welcomwidget = QtGui.QWidget(self)
        #RECENT FILE for disable/enable open recent button --
        self.recentp = cfg.recentproject
        #-------------

        self.buttonnew = QtGui.QPushButton("New Project")
        self.buttonnew.setIcon(QtGui.QIcon(os.path.join('Data', 'new.png')))
        self.buttonnew.clicked.connect(self.newbutton)
        
        self.buttonrec = QtGui.QPushButton("Open last project (%s)" % os.path.basename(cfg.recentproject))
        self.buttonrec.setIcon(QtGui.QIcon(os.path.join('Data', 'folder.png')))

        if self.recentp == "" or not os.path.isfile(self.recentp):
            self.buttonrec.setDisabled(True)
        self.buttonrec.clicked.connect(self.openlastproject)

        self.buttonwebsite = QtGui.QPushButton("Stellar Website")
        self.buttonwebsite.setIcon(QtGui.QIcon(os.path.join('Data', 'home.png')))
        self.buttonwebsite.clicked.connect(self.openwebsite)
		
        self.Spacer = QtGui.QLabel(' ')
        self.Spacer1 = QtGui.QLabel(' ')
		
        self.grid1 = QtGui.QGridLayout()
        self.grid1.setSpacing(15)
        self.grid1.addWidget(self.Spacer, 1, 0)
        self.grid1.addWidget(self.buttonnew, 1, 1)
        self.grid1.addWidget(self.buttonwebsite, 3, 1)
        self.grid1.addWidget(self.buttonrec, 2, 1)
        self.grid1.addWidget(self.Spacer1, 3, 3)
		
        p4_vertical.addLayout(self.grid1)

        

        #-----------------
        self.name = QtGui.QLabel('Project Name: ')
        self.nameEdit = QtGui.QLineEdit()

        self.pathname = QtGui.QLabel('Project Folder: ')
        self.pathEdit = QtGui.QLineEdit()

        self.browsebtn = QtGui.QPushButton("...")
        QtCore.QObject.connect(self.browsebtn, QtCore.SIGNAL('clicked()'), self.ChooseFolder)

        #Projects Folder-------------------------
        self.dirname = ''

        self.btn_New = QtGui.QPushButton('Create \nNew File', self)
        self.btn_New.setGeometry(25, 75, 100, 50)
        QtCore.QObject.connect(self.btn_New, QtCore.SIGNAL('clicked()'), self.CreateProject)

        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(15)
        self.grid.addWidget(self.name, 2, 0)
        self.grid.addWidget(self.nameEdit, 2, 1)
        self.grid.addWidget(self.pathname, 3, 0)
        self.grid.addWidget(self.pathEdit, 3, 1)
        self.grid.addWidget(self.browsebtn, 3, 2)
        self.grid.addWidget(self.btn_New, 4, 1)
        
        p1_vertical.addLayout(self.grid)

 
        self.btn_Open = QtGui.QPushButton('Open \nExisting File', self)
        self.btn_Open.setGeometry(150, 75, 100, 50)
        QtCore.QObject.connect(self.btn_Open, QtCore.SIGNAL('clicked()'), self.OpenFile)
        p2_vertical.addWidget(self.btn_Open)
        

        self.te = QtGui.QTextEdit()
        f = open(os.path.join("Data", "releasenotes.txt"), 'r')
        with f:        
            data = f.read()
            self.te.setText(data)
            f.close()
        self.te.setReadOnly (True)
        self.te.setMaximumSize(475,120)
        p3_vertical.addWidget(self.te)


        #Project Path-----------
        
        #if not os.path.exists(self.dirname):
        #    os.mkdir('Projects')
        #os.chdir('Projects')

        #Window-----------------
 
        self.setWindowTitle('Stellar - %s' % cfg.__version__)
        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.resize(500,350)
        self.setMinimumSize(500,350)
        self.setMaximumSize(500,350) 
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ChooseFolder(self):
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory of project"))
        self.dirname = dir
        self.pathEdit.setText(dir)
        self.pathEdit.setCursorPosition(0)

    def CreateProject(self):
        name = unicode(self.nameEdit.text())
        path = unicode(self.pathEdit.text())

        dirname = os.path.join(path, name)

        if self.name != "" or path != "":
            if not os.path.exists(dirname) and not os.path.isfile(os.path.join(dirname, name)):
                os.mkdir(dirname)
                
                self.main.dirname = dirname
                self.main.createProject(dirname, name)
                self.main.clearSources()
                self.close()
            else:
                reply = QtGui.QMessageBox.question(self, "Already Exists",
                                                        "That Project already exists. Do you want to open it?",
                                                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.OpenFile(dirname, name)

    def openwebsite(self):
        webbrowser.open("http://stellarpygame.blogspot.com")
        
    def newbutton(self):
        self.tab_widget.setCurrentIndex(1)
                    
    def openlastproject(self):
        if not os.path.exists(os.path.dirname(cfg.recentproject)):
            QtGui.QMessageBox.information(self, "Project doesn't exist",
                                            "This project doesn't exist or has been removed",
                                            QtGui.QMessageBox.Ok)
            return
            
        #RECENT FILE--
        self.recentp = cfg.recentproject
        self.dirname = os.path.dirname(self.recentp)
        self.main.fname = os.path.basename(self.recentp)
        self.main.dirname = self.dirname
        
        
        name = os.path.basename(self.main.fname)
        self.main.setTitle(name)

        self.main.clearSources()
        
    def OpenFile(self, dirname = None, name = None):
        # check if we opens existing file from CreateProject function
        if dirname != None and name != None:
            path = os.path.join(dirname, name)
            self.main.openProject(path)
        else:
            self.main.openProject()
            
        self.close()
