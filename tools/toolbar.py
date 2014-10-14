#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import os, sys, subprocess
import docreader

class ToolBar(QtGui.QToolBar):
    def __init__(self, main):
        super(ToolBar, self).__init__(main)
        self.main = main
        
        # func, img, title, hotkey
        funcs = [
            [self.open, 'stellar_1.png', 'Stellar', False], 
            [self.open, 'open.png', 'Open', False],
            [self.main.resourcelist.add_file, 'addfile.png', 'Add file', False],
            [self.main.resourcelist.add_directory, 'addfolder.png', 'Add folder', False],
            #[self.open_documentation, 'documentation.png', 'Documentation', 'F1'],
            [self.toggle_console, 'output.png', 'Show output', False],
            [self.run_project, 'run.png', 'Run', 'Ctrl+B'],
            [QtGui.qApp.quit, 'close.png', 'Exit', 'Ctrl+Q']
        ]

        for i,x in enumerate(funcs):
            action = QtGui.QAction(QtGui.QIcon(os.path.join('images', x[1])), x[2], self)
            action.triggered.connect(x[0])
            if x[3]!=False:
                action.setShortcut(x[3])
            self.addAction(action)
            if i == 5:
                spacer = QtGui.QWidget() 
                spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 
                self.addWidget(spacer)
                #self.separator = self.addSeparator()

        self.setMovable(True) 


    def toggle_console(self):
        self.main.output_display = not self.main.output_display
        self.main.output.setVisible(self.main.output_display)

    def open(self):
        if self.main.mode == "eel-game":
            target = str(QtGui.QFileDialog.getOpenFileName(self, "Open project", "/projects/", "*project.json"))
            if target:
                self.root = self.main.resourcelist.fileSystemModel.setRootPath(target)
                self.main.resourcelist.setRootIndex(self.root)
                self.main.projectdir = target
        else:
            target = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
            if target:
                self.root = self.main.resourcelist.fileSystemModel.setRootPath(target)
                self.main.resourcelist.setRootIndex(self.root)
                self.main.projectdir = target

    def open_documentation(self):
        self.w = docreader.DocReader(self.main)
        self.w.setWindowTitle("Documentation")
        self.w.setGeometry(QtCore.QRect(100, 100, 400, 200))
        self.w.show()

    def run_project(self):
        self.main.statusBar().showMessage('Running project...', 2000)
        #current_dir = os.path.dirname(os.path.realpath(__file__))
        if self.main.mode == "python":
            os.chdir(os.path.dirname(self.main.projectdir))
            print os.path.dirname(self.main.projectdir)
        if sys.platform=="win32":
            if self.main.mode == "python":
                python = subprocess.Popen(["python", "build.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out = python.stdout.read()

            self.main.output.setText(out)
            self.main.output.moveCursor(QtGui.QTextCursor.End)
            self.main.statusBar().showMessage('Done!', 2000)
        else:
            if self.main.mode == "python":
                python = os.system("python build.py")
            self.main.statusBar().showMessage('Done!', 2000)


        os.chdir(os.pardir)
