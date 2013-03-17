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


from PyQt4 import QtCore, QtGui
import os, sys
import cfg

if sys.version_info.major == 2:
    str = unicode


class NewProjectDialog(QtGui.QDialog):
    def __init__(self, main):
        super(NewProjectDialog, self).__init__(main)
        self.main = main
        self.subfolders = self.main.subfolders
                
                
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
        
        self.name = str(self.nameEdit.text())
        self.path = str(self.pathEdit.text())

        self.dirname = os.path.join(self.path, self.name)
        
        
        #Main Folder for Windows
        if self.name != "" and self.path != "":
            
            if not os.path.exists(self.dirname) and not os.path.isfile(os.path.join(self.dirname, self.name)):
                self.main.dirname = self.dirname
                self.main.fname = self.name
                self.main.createProject(self.dirname, self.name)
                self.main.clearSources()
                self.close()
                
            else:
                reply = QtGui.QMessageBox.question(self, "Already Exists",
                                                        "That Project already exists. Do you want to open it?",
                                                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    self.OpenFile(self.dirname, self.name)
                    

    def OpenFile(self, dirname = None, name = None):        
        # check if we opens existing file from CreateProject function
        if dirname != None and name != None:
            path = os.path.join(dirname, name)
            self.main.openProject(path)
        else:
            self.main.openProject()
            
        self.close()
        

    def ChooseFolder(self):
        dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory of project"))
        self.dirname = dir
        self.pathEdit.setText(dir)
        self.pathEdit.setCursorPosition(0)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    name= NewProjectDialog(None)
    sys.exit(app.exec_())
