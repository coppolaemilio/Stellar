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
import os, sys, subprocess

class ToolBar(QtGui.QToolBar):
    def __init__(self, main):
        super(ToolBar, self).__init__(main)
        self.main = main

        stellarAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','stellar_1.png')), 'Stellar', self)
        stellarAction.triggered.connect(self.open_folder)
        openAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','open.png')), 'Open', self)
        openAction.triggered.connect(self.open_folder)
        runAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','run.png')), 'Run', self)
        runAction.triggered.connect(self.run_project)
        runAction.setShortcut('Ctrl+B')
        addFileAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','addfile.png')), 'Add file', self)
        addFileAction.triggered.connect(self.main.treeView.add_file)
        addFolderAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','addfolder.png')), 'Add Folder', self)
        addFolderAction.triggered.connect(self.main.treeView.add_directory)

        exitAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','close.png')), 'Exit', self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        consoleAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','output.png')), 'Show output', self)
        consoleAction.triggered.connect(self.toggle_console)
        spacer = QtGui.QWidget() 
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 
        docsAction = QtGui.QAction(QtGui.QIcon(os.path.join('images','documentation.png')), 'Documentation', self)
        docsAction.triggered.connect(self.open_folder)

        #toolbar = self.addToolBar('Toolbar')
        self.setMovable(False)
        self.addAction(stellarAction)
        self.addAction(runAction)
        self.addAction(addFileAction)
        self.addAction(addFolderAction)
        self.addWidget(spacer) 
        self.addAction(docsAction)
        self.addAction(consoleAction)

    def toggle_console(self):
        self.main.c_displayed = not self.main.c_displayed
        self.main.output.setVisible(self.main.c_displayed)

    def open_folder(self):
        target = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if target:
            self.root = self.treeView.fileSystemModel.setRootPath(target)
            self.treeView.setRootIndex(self.root)

    def run_project(self):
        self.main.statusBar().showMessage('Running project...', 2000)
        eel = self.main.eeldir
        f = 'main'
        os.chdir(self.main.projectdir)
        args = [eel, f]
        if sys.platform=="win32":
            eelbox = subprocess.Popen([eel, f], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = eelbox.stdout.read()
            self.main.output.setText(out)
            self.main.output.moveCursor(QtGui.QTextCursor.End)
            self.main.statusBar().showMessage('Done!', 2000)