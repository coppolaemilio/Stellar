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
import ConfigParser

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

        buttonnew = QtGui.QPushButton("New Project", self.welcomwidget)
        buttonnew.setIcon(QtGui.QIcon(os.path.join('Data', 'new.png')))
        buttonnew.move(180,6)
        buttonnew.clicked.connect(self.newbutton)
        
        buttonrec = QtGui.QPushButton("Open last project", self.welcomwidget)
        buttonrec.setIcon(QtGui.QIcon(os.path.join('Data', 'folder.png')))
        buttonrec.move(170,46)

        if self.recentp == "":
            buttonrec.setDisabled(True)
        buttonrec.clicked.connect(self.openlastproject)

        buttonwebsite = QtGui.QPushButton("Stellar Website", self.welcomwidget)
        buttonwebsite.setIcon(QtGui.QIcon(os.path.join('Data', 'home.png')))
        buttonwebsite.move(175,86)
        buttonwebsite.clicked.connect(self.openwebsite)
        
        p4_vertical.addWidget(self.welcomwidget)

        

        #-----------------
        self.name = QtGui.QLabel('Project Name: ')
        self.nameEdit = QtGui.QLineEdit()

        #Projects Folder-------------------------
        dirname = 'Projects'

        self.btn_New = QtGui.QPushButton('Create \nNew File', self)
        self.btn_New.setGeometry(25, 75, 100, 50)
        QtCore.QObject.connect(self.btn_New, QtCore.SIGNAL('clicked()'), self.CreateProject)

        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(15)
        self.grid.addWidget(self.name, 2, 0)
        self.grid.addWidget(self.nameEdit, 2, 1)
        self.grid.addWidget(self.btn_New, 3, 1)
        
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
        self.te.setReadOnly (True)
        self.te.setMaximumSize(475,120)
        p3_vertical.addWidget(self.te)


        #Project Path-----------
        
        if not os.path.exists(dirname):
            os.mkdir('Projects')
        os.chdir('Projects')

        #Window-----------------
 
        self.setWindowTitle('Stellar - %s' % cfg.__version__)
        self.setWindowIcon(QtGui.QIcon(os.path.join('data', 'icon.png')))
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

    def CreateProject(self):

        self.tmp = self.main.fname
        self.main.fname =  os.path.join(str(self.nameEdit.text()),
                                        "{0}.py".format(self.nameEdit.text()))
        
        if self.main.fname == "":
            self.main.fname = self.main.tmp
        else:
            #Main Folder for Windows
            if self.nameEdit.text() != "":
                if not os.path.exists(self.nameEdit.text()):
                    os.mkdir(self.nameEdit.text())

                    #Project Sub-Folders for Windows
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Sprites')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Sprites'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Sound')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Sound'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Fonts')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Fonts'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Scripts')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Scripts'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Objects')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Objects'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Rooms')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Rooms'))
                    if not os.path.exists(os.path.join(str(self.nameEdit.text()), 'Build')):
                        os.mkdir(os.path.join(str(self.nameEdit.text()), 'Build'))

                    #f = open(self.main.fname, 'w')
                    #f.close()      
                    cfg.config.set('stellar', 'recentproject', self.main.fname)
                    with open('../config.ini', 'wb') as configfile:
                        cfg.config.write(configfile)
                    p = self.main.fname
                    d = os.path.basename(str(p))
                    self.main.setWindowTitle('%s - Stellar %s'% (d, cfg.__version__))

                    dirname, filename = os.path.split(os.path.abspath(self.main.fname))
                    os.chdir(dirname)
                    self.close()
                    self.main.tree.InitParent()
                    self.main.tree.InitChild()
                    self.main.show()
                else:
                    reply = QtGui.QMessageBox.question(self, "Already Exists",
                                                            "That Project already exists, Do you want to open it?",
                                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        print("#Program Anchor#")

    def openwebsite(self):
        webbrowser.open("http://stellarpygame.blogspot.com")
        
    def newbutton(self):
        self.tab_widget.setCurrentIndex(1)
                    
    def openlastproject(self):
        self.main.tmp = self.main.fname
        #RECENT FILE--
        self.recentp = cfg.recentproject
        #-------------
        self.main.fname = self.recentp

        if self.main.fname == "":
            self.main.fname = self.main.tmp
        else:
            #f = open(self.main.fname, 'r')
            p = self.main.fname
            d = os.path.basename(str(p))
            self.main.setWindowTitle('%s - Stellar %s'% (d, cfg.__version__))
            
            '''with f:        
                data = f.read()
                self.main.textEdit.setText(data)'''
                
            dirname, filename = os.path.split(os.path.abspath(self.main.fname))
            os.chdir(dirname)
            self.close()
            self.main.tree.InitParent()
            self.main.tree.InitChild()
            self.main.show()
        
    def OpenFile(self):
        self.main.tmp = self.main.fname
        self.main.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Game', 
                '', self.tr("Python files (*.py *.pyw)"))
        #RECENT FILE--
        data = self.main.fname
        self.recentp = data

        cfg.config.set('stellar', 'recentproject', data)
        with open('../config.ini', 'wb') as configfile:
            cfg.config.write(configfile)
        #-------------

        if self.main.fname == "":
            self.main.fname = self.main.tmp
        else:
            #f = open(self.main.fname, 'r')
            p = self.main.fname
            d = os.path.basename(str(p))
            self.main.setWindowTitle('%s - Stellar %s'% (d, cfg.__version__))
            
            '''with f:        
                data = f.read()
                self.main.textEdit.setText(data)'''
                
            dirname, filename = os.path.split(os.path.abspath(str(self.main.fname)))
            os.chdir(dirname)
            self.close()
            self.main.tree.InitParent()
            self.main.tree.InitChild()
            self.main.show()
