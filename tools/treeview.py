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
import os, sys
import scripteditor
import imageviewer

class TreeView(QtGui.QTreeView):
    def __init__(self, main):
        super(TreeView, self).__init__(main)
        self.main = main
        self.fileSystemModel = QtGui.QFileSystemModel(self)
        self.fileSystemModel.setReadOnly(False)
        self.clicked.connect(self.on_treeView_clicked)
        self.abstractitem = QtGui.QAbstractItemView
        self.setDragDropMode(self.abstractitem.InternalMove)
        self.connect (self,
                QtCore.SIGNAL ("currentTextChanged(const QString&)"),
                QtGui.qApp.quit)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.root = self.fileSystemModel.setRootPath(self.main.projectdir)
        self.setModel(self.fileSystemModel)
        self.setRootIndex(self.root)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.header().close()  
        self.indexItem=""
        self.connect(self,QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.doMenu)

        renameAction = QtGui.QAction('Rename', self)
        renameAction.triggered.connect(self.rename_file)

        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(self.main.editFileAction)
        self.popMenu.addAction(renameAction)
        self.popMenu.addAction(self.main.deleteFileAction)
        self.popMenu.addSeparator()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        self.indexItem = self.fileSystemModel.index(index.row(), 0, index.parent())
        filePath = self.fileSystemModel.filePath(self.indexItem)
        fileName = self.fileSystemModel.fileName(self.indexItem)

    def doMenu(self, point):
        self.popMenu.exec_( self.mapToGlobal(point) )

    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            self.edit_file()
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)

    def edit_file(self):
        target=str(self.abstractitem.currentIndex(self.main.treeView).data().toString())
        filePath = self.fileSystemModel.filePath(self.indexItem)
        sufix = filePath[-4:]

        if sufix == ".exe":
            reply = QtGui.QMessageBox.question(self, "Not assigned", 
                         "Stellar does not have a progam to edit this kind of file, would you like to choose one?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)            
        if sufix in [".png", ".jpg", ".bmp"]:
            self.main.window = imageviewer.ImageEditor(self.main, target, filePath)
            self.main.window.setWindowTitle(target)
            self.main.mdi.addSubWindow(self.main.window)
            self.main.window.setVisible(True)
        else:
            self.main.window = scripteditor.ScriptEditor(self.main, target, filePath)
            self.main.window.setWindowTitle(target)
            self.main.mdi.addSubWindow(self.main.window)
            self.main.window.setVisible(True)

    def delete_file(self):
        f= filePath = self.fileSystemModel.filePath(self.indexItem)
        delete_msg = "You are about to delete "+f+" Continue?"
        reply = QtGui.QMessageBox.question(self, 'Confirm', 
                         delete_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            os.remove(str(f))

    def rename_file(self):
        index = self.abstractitem.currentIndex(self.main.treeView)
        return QtGui.QTreeView.edit(self, index)
