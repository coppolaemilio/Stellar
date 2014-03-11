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

import sys, os, subprocess
from PyQt4 import QtGui, QtCore
sys.path.append("tools")
import treeview
import toolbar

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.projectdir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'example')
        self.eeldir=os.path.join(os.path.dirname(os.path.realpath(__file__)),'eel','eel')
        if sys.platform=="win32":
            self.eeldir+='.exe'

        self.deleteFileAction = QtGui.QAction('Delete', self)
        self.editFileAction = QtGui.QAction('Edit', self)

        self.treeView = treeview.TreeView(self)

        self.output = QtGui.QTextEdit()
        self.output.setReadOnly(True)
        self.font = QtGui.QFont()
        self.font.setFamily('Monaco')
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setFixedPitch(True)
        self.output.setFont(self.font)

        self.deleteFileAction.triggered.connect(self.treeView.delete_file)
        self.editFileAction.triggered.connect(self.treeView.edit_file)

        self.mdi = QtGui.QMdiArea()
        self.mdi.setViewMode(self.mdi.TabbedView)
        self.mdi.setTabsClosable(True)
        self.mdi.setTabsMovable(True)
        backf = QtGui.QBrush(QtGui.QPixmap(os.path.join('images','background.png')))
        self.mdi.setBackground(backf)

        self.toolBar = self.addToolBar(toolbar.ToolBar(self))

        self.statusBar().showMessage('Ready', 2000)

        self.vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.vsplitter.addWidget(self.mdi)
        self.vsplitter.addWidget(self.output)
        self.output.hide()
        self.c_displayed=False
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.treeView)
        splitter.addWidget(self.vsplitter)

        self.setCentralWidget(splitter)
        self.setWindowTitle("Stellar - "+self.projectdir)
        self.resize(640, 480)

        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join('images','stellar.png')))
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    f = open(os.path.join('themes','default.css'))
    style = f.read()
    f.close()
    app.setStyleSheet(style)
    mw = MainWindow()
    mw.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    