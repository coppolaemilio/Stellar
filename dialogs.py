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


from PyQt4 import QtCore, QtGui
import os, sys
import cfg

class NewProjectDialog(QtGui.QDialog):
    def __init__(self, main):
        super(NewProjectDialog, self).__init__(main)
        self.main = main
        self.initUI()

    def initUI(self):
        self.ContainerGrid = QtGui.QGridLayout(self)

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

        

        self.ContainerGrid.addWidget(self.name, 2, 0)
        self.ContainerGrid.addWidget(self.nameEdit, 2, 1)
        self.ContainerGrid.addWidget(self.pathname, 3, 0)
        self.ContainerGrid.addWidget(self.pathEdit, 3, 1)
        self.ContainerGrid.addWidget(self.browsebtn, 3, 2)
        self.ContainerGrid.addWidget(self.btn_New, 4, 1)

        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.setWindowTitle("New project")
        self.resize(500,100)
        #self.setMinimumSize(300,200)
        #self.setMaximumSize(300,200) 
        self.show()

    def CreateProject(self):
        if str(self.nameEdit.text()) == '':
            QtGui.QMessageBox.information(self, "Name not specified",
                                                "You must specify name before creating.",
                                                QtGui.QMessageBox.Ok)
            return
        elif str(self.pathEdit.text()) == '':
            QtGui.QMessageBox.information(self, "Project directory not specified",
                                                "You must specify project directory before creating.",
                                                QtGui.QMessageBox.Ok)
            return
        
        self.name = str(self.nameEdit.text()).replace(".py", "") + '.py'
        self.path = str(self.pathEdit.text())


        self.dirname = os.path.join(self.path, str(self.nameEdit.text()))
        

        #Main Folder for Windows
        if self.name is not "" and self.path is not "":
            if not os.path.exists(self.dirname) and not os.path.isfile(os.path.join(self.dirname, self.name)):
                self.main.fname = "{0}.py".format(self.nameEdit.text())
                os.mkdir(self.dirname)

                #Project Sub-Folders for Windows
                subfolders = ['Sprites', 'Sound', 'Fonts', 'Scripts', 'Objects', 'Rooms', 'Build']
                
                for subfolder in subfolders:
                    if not os.path.exists(os.path.join(self.dirname, subfolder)):
                        os.mkdir(os.path.join(self.dirname, subfolder))


                f = open(os.path.join(self.dirname, self.name), 'w+')
                f.write('# This file was created with Stellar')
                f.close() 

                cfg.config.set('stellar', 'recentproject', os.path.join(self.dirname, self.name))
                with open('config.ini', 'wb') as configfile:
                    cfg.config.write(configfile)

                d = os.path.basename(str(self.main.fname))
                self.main.setWindowTitle('%s - Stellar %s'% (d, cfg.__version__))

                self.close()
                self.main.Sprites = []
                self.main.Sound = []
                self.main.Fonts = []
                self.main.Scripts = []
                self.main.Objects = []
                self.main.Rooms = []
                
                self.main.dirname = self.dirname
                self.main.tree.clear()
                self.main.tree.InitParent()
                self.main.tree.InitChild()
                self.main.show()
            else:
                reply = QtGui.QMessageBox.question(self, "Already Exists",
                                                        "That Project already exists. Do you want to open it?",
                                                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.OpenFile(self.dirname, self.name)

    def OpenFile(self, dirname = None, name = None):        
        # check if we opens existing file from CreateProject function
        if dirname != None and name != None:
            self.dirname = dirname
            self.main.dirname = self.dirname
            self.main.fname = name
            data = os.path.join(dirname, name)
        else:
            self.project = str(QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Game', 
                '', self.tr("Python files (*.py *.pyw)")))

            if self.project == '':
                return
            if not os.path.isfile(self.project):
                QtGui.QMessageBox.information(self, "Project doesn't exist",
                    "This project doesn't exist or has been removed",
                    QtGui.QMessageBox.Ok)
                return


            subfolders = ['Sprites', 'Sound', 'Fonts', 'Scripts', 'Objects', 'Rooms', 'Build']
                
            for subfolder in subfolders:
                if not os.path.exists(os.path.join(os.path.dirname(self.project), subfolder)):
                    QtGui.QMessageBox.information(self, "Project is broken",
                        "Project is broken or doesn't contain important folders",
                        QtGui.QMessageBox.Ok)
                    return

            self.dirname = os.path.dirname(self.project)
            self.main.dirname = self.dirname
            self.main.fname = os.path.basename(self.project)

        
        cfg.config.set('stellar', 'recentproject', self.project)
        with open('config.ini', 'wb') as configfile:
            cfg.config.write(configfile)
        #-------------

        #f = open(self.main.fname, 'r')
        self.main.setWindowTitle('%s - Stellar %s'% (self.main.fname, cfg.__version__))
            
        self.close()
        self.main.Sprites = []
        self.main.Sound = []
        self.main.Fonts = []
        self.main.Scripts = []
        self.main.Objects = []
        self.main.Rooms = []

        self.main.tree.clear()
        self.main.tree.InitParent()
        self.main.tree.InitChild(fillarrays = True)
        self.main.show()

    def ChooseFolder(self):
        dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory of project"))
        self.dirname = dir
        self.pathEdit.setText(dir)
        self.pathEdit.setCursorPosition(0)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    name= NewProjectDialog(None)
    sys.exit(app.exec_())
