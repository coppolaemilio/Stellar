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
import listview
import toolbar
import ConfigParser

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.read_settings()
        
        if self.mode=="eel-game":
            self.folder_sprite = "images/open.png"
            self.file_sprite = "images/new.png"
            self.extension_sprite = "images/extensions.png"
            self.settings_sprite = "images/settings.png"
            self.filesView = listview.ListView(self)
        else:
            self.filesView = treeview.TreeView(self)
        self.font = QtGui.QFont()
        self.font.setFamily(self.font_name)
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setFixedPitch(True)
        self.output = QtGui.QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(self.font)

        self.mdi = QtGui.QMdiArea()

        if self.tabbed_view:
            self.mdi.setViewMode(self.mdi.TabbedView)
        self.mdi.setTabsClosable(True)
        self.mdi.setTabsMovable(True)
        self.mdi.setBackground(QtGui.QBrush(QtGui.QPixmap(os.path.join('images','background.png'))))

        self.toolBar = self.addToolBar(toolbar.ToolBar(self))

        self.vsplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.vsplitter.addWidget(self.mdi)
        self.vsplitter.addWidget(self.output)
        
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.filesView)
        splitter.addWidget(self.vsplitter)

        self.setCentralWidget(splitter)
        self.setWindowTitle("Stellar - " + os.path.basename(self.projectdir))
        self.resize(int(self.size.split("x")[0]), int(self.size.split("x")[1]))
        self.statusBar().showMessage('Ready', 2000)
        self.show()

    def read_settings(self):
        config = ConfigParser.ConfigParser()
        config.read('settings.ini')
        try:
            self.projectdir = os.path.join(config.get('project', 'last_project'))
        except:
            self.projectdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'example')
        self.eeldir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'eel','eel')
        if sys.platform == "win32":
            self.eeldir += '.exe'

        self.mode = config.get('settings', 'mode')
        self.size = config.get('settings', 'start_size')
        self.output_display = bool(int(config.get('settings', 'compile_form')))
        self.theme_dir = config.get('settings', 'theme_folder')
        self.theme_name = config.get('settings', 'theme_name')
        self.qt_style = config.get('settings', 'qt_style')
        self.tabbed_view = int(config.get('settings', 'tabbed_view'))
        self.font_name = config.get('settings', 'font')

def main():
    app = QtGui.QApplication(sys.argv)
    Stellar = MainWindow()
    Stellar.setStyle(QtGui.QStyleFactory.create(Stellar.qt_style))
    Stellar.setWindowIcon(QtGui.QIcon(os.path.join('images','icon.png')))
    with open(os.path.join(Stellar.theme_dir, Stellar.theme_name + '.css')) as file:
        Stellar.setStyleSheet(file.read())
    Stellar.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()