#!/usr/bin/python
# -= coding: utf-8 =-

import sys, os, subprocess
from PyQt4 import QtGui, QtCore
sys.path.append("tools")
import resourcelist
import inspector
import toolbar
import projectinfo
import ConfigParser

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()#parent=None, flags=QtCore.Qt.FramelessWindowHint)
        self.read_settings()
        self.icon = QtGui.QIcon(os.path.join('images','icon.png'))
        if self.mode=="python":
            self.folder_sprite = "images/open.png"
            self.file_sprite = "images/new.png"
            self.extension_sprite = "images/extensions.png"
            self.settings_sprite = "images/settings.png"
            self.resourcelist = resourcelist.ResourceList(self)
            
        def set_font():
            font = QtGui.QFont()
            font.setFamily(self.font_name)
            font.setStyleHint(QtGui.QFont.Monospace)
            font.setFixedPitch(True)
            return font
        
        def set_output():
            output = QtGui.QTextEdit()
            output.setReadOnly(True)
            output.setFont(self.font)
            return output

        
        self.font = set_font()
        self.output = set_output()
        
        self.mdi_area = self.create_mdi_area()
        
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.resourcelist)
        self.splitter.addWidget(self.mdi_area)
        
        self.setCentralWidget(self.splitter)
        self.create_toolbar("top")
        self.create_toolbar("right")
        
        self.setWindowTitle("Stellar - " + os.path.basename(self.projectdir))
        self.resize(int(self.size.split("x")[0]), int(self.size.split("x")[1]))
        self.statusBar().showMessage('Ready', 2000)

        self.app_path = os.getcwd()

        #self.show_project_overview()
        self.show()
        
    def create_toolbar(self, type):
        if type == "right":
            self.inspector = inspector.Inspector(self)
            inspectorToolbar = QtGui.QToolBar()
            inspectorToolbar.addWidget(self.inspector)
            self.addToolBar(QtCore.Qt.RightToolBarArea, inspectorToolbar)
            
        elif type == "top":
            self.addToolBar(toolbar.ToolBar(self))
        
    def create_mdi_area(self):
        mdi = QtGui.QMdiArea()

        if self.tabbed_view:
            mdi.setViewMode(mdi.TabbedView)
        mdi.setTabsClosable(True)
        mdi.setTabsMovable(True)
        mdi.setBackground(QtGui.QBrush(QtGui.QPixmap(os.path.join('images','background.png'))))
        return mdi
        
    def show_project_overview(self):
        #Load startup info
        resource_name = "Project Overview"
        window = projectinfo.ProjectInfo(self)
        self.window_index[resource_name] = window
        self.mdi.addSubWindow(window)
        window.setWindowTitle(resource_name)
        window.setVisible(True)
        window.setWindowState(QtCore.Qt.WindowMaximized)
        return window

    def read_settings(self):
        config = ConfigParser.ConfigParser()
        config.read('settings.ini')
        try:
            self.projectdir = os.path.join(config.get('project', 'last_project'))
        except:
            self.projectdir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'example')

        self.mode = config.get('settings', 'mode')
        self.size = config.get('settings', 'start_size')
        self.output_display = bool(int(config.get('settings', 'compile_form')))
        self.theme_dir = config.get('settings', 'theme_folder')
        self.theme_name = config.get('settings', 'theme_name')
        self.qt_style = config.get('settings', 'qt_style')
        self.tabbed_view = int(config.get('settings', 'tabbed_view'))
        self.font_name = config.get('settings', 'font')
        self.treeview_icon_size = int(config.get('treeview', 'icon_size'))

def main():
    app = QtGui.QApplication(sys.argv)
    Stellar = MainWindow()
    Stellar.setStyle(QtGui.QStyleFactory.create(Stellar.qt_style))
    Stellar.setWindowIcon(Stellar.icon)
    with open(os.path.join(Stellar.theme_dir, Stellar.theme_name + '.css')) as file:
        Stellar.setStyleSheet(file.read())
    Stellar.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
